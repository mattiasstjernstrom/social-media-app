from flask import Blueprint, flash, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from sqlalchemy import func

from api.comments import Comments
from forms.post import PostForm
from forms.comments import CommentOnPostForm
from models.db import db
from models.posts import UserPost, UserPostLikes, UserPostComments
from models.users import User, Followers
from models.check_likes import check_liked
from modules.date_logics import humanize_time
from modules.follower_logics import FollowerLogics

site = Blueprint("site", __name__)


@site.route("/")
@login_required
def index():
    context = {
        "page_title": "Welcome back!",
    }
    followers_posts = FollowerLogics().get_followers_posts()

    return (
        render_template("index.html", **context, followers_posts=followers_posts),
        200,
    )


@site.route("/profile/<int:id>/")
@login_required
def profile(id):
    get_user = User.query.get(id)
    raw_posts = (
        UserPost.query.with_entities(
            UserPost.id,
            UserPost.date_posted,
            UserPost.title,
            UserPost.splash_url,
            func.left(UserPost.content, 150).label("content_truncated"),
        )
        .filter_by(user_id=id)
        .order_by(UserPost.date_posted.desc())
    ).all()

    get_posts = []
    for post in raw_posts:
        post_dict = {
            "id": post.id,
            "date_posted": post.date_posted,
            "humanized_date": humanize_time(post.date_posted),
            "title": post.title,
            "splash_url": post.splash_url,
            "content_truncated": post.content_truncated,
        }
        get_posts.append(post_dict)

    is_following = FollowerLogics().check_following(current_user.id, id)

    context = {"page_title": "Profile", "is_following": is_following}
    return (
        render_template("user/profile.html", **context, user=get_user, posts=get_posts),
        200,
    )


@site.route("/post/", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm(request.form)
    context = {
        "page_title": "Make a post",
    }

    if form.validate_on_submit():
        save_post = UserPost(
            title=form.title.data,
            splash_url=form.splash_url.data,
            content=form.content.data,
            draft=form.draft.data,
            friends_only=form.friends_only.data,
            followers_only=form.followers_only.data,
            user_id=current_user.id,
            comments_disabled=form.comments_disabled.data,
        )

        db.session.add(save_post)
        db.session.commit()

        flash("Post created", "success")
        return redirect(url_for("site.profile", id=current_user.id))

    return render_template("posts/post.html", **context, form=form), 200


@site.route("/post/<int:id>/")
def view_post(id):
    get_post = UserPost.query.get(id)
    get_comments = Comments().load(id)

    if not get_post or (get_post.draft and get_post.owner_user.id != current_user.id):
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    liked = check_liked(id)

    context = {
        "page_title": get_post.title,
    }
    return (
        render_template(
            "posts/view_post.html",
            **context,
            post=get_post,
            all_comments=get_comments,
            liked=liked,
            form=PostForm()
        ),
        200,
    )


@site.get("/post/<int:id>/delete/")
@login_required
def delete_post(id):
    get_post = UserPost.query.get(id)

    db.session.delete(get_post)
    db.session.commit()

    flash("Post deleted", "success")
    return redirect(url_for("site.profile", id=current_user.id))


@site.get("/post/<int:post_id>/like/")
@login_required
def like_post(post_id):
    get_post = UserPost.query.get(post_id)
    if not get_post or (get_post.draft and get_post.owner_user.id != current_user.id):
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    existing_like = UserPostLikes.query.filter_by(
        user_id=current_user.id, post_id=post_id
    ).first()
    if existing_like:
        flash("You have already liked this post", "info")
        return redirect(url_for("site.view_post", id=post_id))

    like_post = UserPostLikes(user_id=current_user.id, post_id=post_id)
    db.session.add(like_post)

    get_post.likes += 1
    db.session.commit()

    flash("Post liked", "success")
    return redirect(url_for("site.view_post", id=post_id, _anchor="callout"))


@site.get("/post/<int:post_id>/unlike/")
@login_required
def unlike_post(post_id):
    get_post = UserPost.query.get(post_id)
    if not get_post or (get_post.draft and get_post.owner_user.id != current_user.id):
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    existing_like = UserPostLikes.query.filter_by(
        user_id=current_user.id, post_id=post_id
    ).first()
    if not existing_like:
        flash("You have not liked this post", "info")
        return redirect(url_for("site.view_post", id=post_id))

    db.session.delete(existing_like)

    get_post.likes -= 1
    db.session.commit()

    flash("Post unliked", "success")
    return redirect(url_for("site.view_post", id=post_id, _anchor="callout"))


#! not tested
@site.get("/post/<int:post_id>/share/")
@login_required
def share_post(post_id):
    get_post = UserPost.query.get(post_id)
    if not get_post or (get_post.draft and get_post.owner_user.id != current_user.id):
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    get_post.shares += 1
    db.session.commit()

    flash("Post shared", "success")
    return redirect(url_for("site.view_post", id=post_id, _anchor="callout"))


@site.post("/post/<int:post_id>/comment/")
@login_required
def comment_post(post_id):
    get_post = UserPost.query.get(post_id)
    if not get_post or (get_post.draft):
        return jsonify("Post not found"), 404

    get_comment = CommentOnPostForm(request.form)
    if not get_comment.validate():
        return jsonify("Invalid comment"), 400

    save_comment = UserPostComments(
        content=get_comment.content.data,
        user_id=current_user.id,
        post_id=post_id,
    )
    db.session.add(save_comment)
    get_post.comments += 1
    db.session.commit()

    return jsonify("Post commented"), 201


@site.get("/post/<int:post_id>/comment/<int:comment_id>/delete/")
@login_required
def delete_comment(post_id, comment_id):
    get_comment = UserPostComments.query.get(comment_id)
    if not get_comment:
        flash("Comment not found", "danger")
        return redirect(url_for("site.view_post", id=post_id))

    if get_comment.user_id != current_user.id:
        flash("You cannot delete this comment", "danger")

    db.session.delete(get_comment)
    db.session.commit()

    flash("Comment deleted", "success")
    return redirect(url_for("site.view_post", id=post_id))


@site.get("/follow/<int:user_id>/")
@login_required
def follow_user(user_id):
    is_following = FollowerLogics().check_following(current_user.id, user_id)
    if is_following:
        flash("You are already following this user", "info")
        return redirect(url_for("site.profile", id=user_id))

    new_follow = Followers(follower_id=current_user.id, followed_id=user_id)
    db.session.add(new_follow)
    db.session.commit()

    flash("You are now following this user", "success")
    return redirect(url_for("site.profile", id=user_id))


@site.get("/unfollow/<int:user_id>/")
@login_required
def unfollow_user(user_id):
    is_following = FollowerLogics().check_following(current_user.id, user_id)
    if not is_following:
        flash("You are not following this user", "info")
        return redirect(url_for("site.profile", id=user_id))

    get_follow = (
        db.session.query(Followers)
        .filter(
            Followers.follower_id == current_user.id, Followers.followed_id == user_id
        )
        .first()
    )
    db.session.delete(get_follow)
    db.session.commit()

    flash("You are no longer following this user", "success")
    return redirect(url_for("site.profile", id=user_id))


@site.get("/followers/<int:user_id>/")
@login_required
def followers(user_id):
    get_user = User.query.get(user_id)
    get_followers = (
        db.session.query(Followers)
        .filter(Followers.followed_id == user_id)
        .order_by(Followers.id.desc())
        .all()
    )

    followers_list = []
    for follower in get_followers:
        follower_user = User.query.get(follower.follower_id)
        followers_list.append(follower_user)

    context = {
        "page_title": "Followers",
    }
    return (
        render_template(
            "user/followers.html", **context, user=get_user, followers=followers_list
        ),
        200,
    )
