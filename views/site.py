from datetime import datetime
from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
)
from flask_login import current_user, login_required
from flask_security import roles_accepted

from api.comments import Comments
from api.trending import TrendingPosts
from forms.post import PostForm
from forms.comments import CommentOnPostForm
from models.db import db
from models.posts import (
    UserPost,
    UserPostLikes,
    UserPostComments,
    PostTags,
    Tags,
    PostViews,
)
from models.users import User, Followers
from modules.check_likes import check_liked
from modules.user_logics import FollowerLogics, ProfileLogics

site = Blueprint("site", __name__)


@site.route("/")
@login_required
def index():
    context = {
        "page_title": "Welcome back!",
    }

    top_tags = (
        db.session.query(Tags.tag, db.func.count(PostTags.tag_id).label("total"))
        .join(PostTags)
        .group_by(Tags.tag)
        .order_by(db.func.count(PostTags.tag_id).desc())
        .limit(5)
        .all()
    )

    # Add k to the total if it's over 999
    top_tags = [
        (tag, f"{total // 1000}k+" if total > 999 else total) for tag, total in top_tags
    ]

    top_views = (
        db.session.query(UserPost).order_by(UserPost.post_views.desc()).limit(5).all()
    )

    trending_posts = TrendingPosts().load(5)

    stats = {
        "trending_posts": trending_posts,
        "top_views": top_views,
        "top_tags": top_tags,
    }

    followers_posts = FollowerLogics().get_followers_posts()

    return (
        render_template(
            "index.html", **context, followers_posts=followers_posts, **stats
        ),
        200,
    )


@site.route("/profile/<int:id>/")
@login_required
def profile(id):
    get_user = User.query.get(id)
    get_posts = ProfileLogics().get_user_posts(get_user.id)
    is_following = FollowerLogics().check_following(current_user.id, id)
    context = {"page_title": "Profile", "is_following": is_following}
    return (
        render_template(
            "user/profile.html",
            **context,
            user=get_user,
            posts=get_posts,
        ),
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
            splash_caption=form.splash_caption.data,
            splash_credit=form.splash_credit.data,
            content=form.content.data,
            draft=form.draft.data,
            friends_only=form.friends_only.data,
            users_only=form.users_only.data,
            user_id=current_user.id,
            comments_disabled=form.comments_disabled.data,
            date_posted=datetime.now(),
        )

        db.session.add(save_post)
        db.session.commit()

        split_post_tags = form.tags.data.split(",")
        formatted_tag = [
            tag.strip().lower().replace(" ", "-").replace("#", "")
            for tag in split_post_tags
        ]
        formatted_tag = [tag for tag in formatted_tag if tag]

        for tag in formatted_tag:
            get_tag = Tags.query.filter_by(tag=tag).first()
            if not get_tag:
                save_tag = Tags(tag=tag)
                db.session.add(save_tag)
                db.session.commit()

        for tag in formatted_tag:
            get_tag = Tags.query.filter_by(tag=tag).first()
            save_post_tag = PostTags(post_id=save_post.id, tag_id=get_tag.id)
            db.session.add(save_post_tag)
            db.session.commit()

        flash("Post created", "success")
        return redirect(url_for("site.profile", id=current_user.id))

    return render_template("posts/post.html", **context, form=form), 200


@site.route("/post/<int:id>/edit/", methods=["GET", "POST"])
@login_required
def edit_post(id):
    get_post = UserPost.query.get(id)
    if not get_post or get_post.owner_user.id != current_user.id:
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    if request.method == "GET":
        form = PostForm(obj=get_post)
    else:
        form = PostForm(request.form)

    context = {
        "page_title": "Edit post",
        "edit": True,
    }

    if form.validate_on_submit():
        form.populate_obj(get_post)
        get_post.date_posted = get_post.date_posted
        get_post.date_edited = datetime.now()
        db.session.commit()
        flash("Post updated", "success")
        return redirect(url_for("site.view_post", id=id))

    return render_template("posts/post.html", **context, form=form, post=get_post), 200


@site.route("/post/<int:id>/")
def view_post(id):
    get_post = UserPost.query.get(id)
    if not get_post or (get_post.draft and get_post.owner_user.id != current_user.id):
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    if current_user.is_authenticated:
        check_view = PostViews.query.filter_by(
            post_id=id, user_id=current_user.id
        ).first()
        if not check_view:
            save_view = PostViews(post_id=id, user_id=current_user.id)
            db.session.add(save_view)
            db.session.commit()
    else:
        unauth_id = session.get("session_id")
        check_view = PostViews.query.filter_by(
            post_id=id, unauthorized_id=unauth_id
        ).first()
        if not check_view:
            save_view = PostViews(post_id=id, unauthorized_id=unauth_id)
            db.session.add(save_view)
            db.session.commit()

    if get_post.post_views is None:
        get_post.post_views = 0
    get_post.post_views += 1
    db.session.commit()
    get_comments = Comments().load(id)

    post_tags = (
        db.session.query(Tags)
        .join(PostTags)
        .filter(PostTags.post_id == id)
        .order_by(Tags.tag.asc())
        .all()
    )
    get_post.tags = [tag.tag for tag in post_tags]

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
            form=PostForm(),
        ),
        200,
    )


@site.get("/post/<int:id>/delete/")
@login_required
def delete_post(id):
    # get post and delete whit tags
    get_tags = PostTags.query.filter_by(post_id=id).all()
    for tag in get_tags:
        db.session.delete(tag)

    get_post = UserPost.query.get(id)
    if not get_post or get_post.owner_user.id != current_user.id:
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

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
    get_post = UserPost.query.get(post_id)
    if not get_post or (get_post.draft):
        return jsonify("Post not found"), 404

    get_comment = UserPostComments.query.get(comment_id)
    if not get_comment:
        flash("Comment not found", "danger")
        return redirect(url_for("site.view_post", id=post_id))

    if get_comment.user_id != current_user.id:
        flash("You cannot delete this comment", "danger")

    db.session.delete(get_comment)
    get_post.comments -= 1
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

    get_followings = FollowerLogics().view_following(user_id)
    get_followers = FollowerLogics().view_followers(user_id)

    followers_list = []
    for follower in get_followers:
        follower_user = User.query.get(follower.follower_id)
        followers_list.append(follower_user)

    following_list = []
    for following in get_followings:
        following_user = User.query.get(following.followed_id)
        following_list.append(following_user)

    context = {
        "page_title": "Followers",
    }
    return (
        render_template(
            "user/followers.html",
            **context,
            user=get_user,
            followers=followers_list,
            followings=following_list,
        ),
        200,
    )


@site.route("/view-tag/<string:tag_name>")
def view_tag(tag_name):
    tag = Tags.query.filter_by(tag=tag_name).first()
    if not tag:
        flash("Tag not found", "danger")
        return redirect(url_for("site.index"))

    get_posts_with_tag = (
        db.session.query(UserPost)
        .join(PostTags)
        .filter(PostTags.tag_id == tag.id)
        .order_by(UserPost.date_posted.desc())
        .all()
    )

    context = {
        "page_title": f"Tag: {tag_name}",
    }

    return (
        render_template("posts/view_tags.html", **context, posts=get_posts_with_tag),
        200,
    )


@site.route("/verify/<int:id>")
@site.route("/verify/<int:id>/")
@roles_accepted("Admin")
def verify_user(id):
    get_user = User.query.get(id)
    if not get_user:
        flash("User not found", "danger")
        return redirect(url_for("site.index"))
    get_user.verified = True
    db.session.commit()
    flash("User verified", "success")
    return redirect(url_for("site.index"))
