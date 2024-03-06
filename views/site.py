from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from forms.post import PostForm
from modules.date_logics import humanize_time
from models.db import db
from models.posts import UserPost
from models.users import User

site = Blueprint("site", __name__)


@site.route("/")
@login_required
def index():
    context = {
        "page_title": "Welcome back!",
    }
    return render_template("index.html", **context), 200


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
        humanized_date = humanize_time(post.date_posted)
        post_dict = {
            "id": post.id,
            "date_posted": humanized_date,
            "title": post.title,
            "splash_url": post.splash_url,
            "content_truncated": post.content_truncated,
        }
        get_posts.append(post_dict)

    context = {
        "page_title": "Profile",
    }
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
    if not get_post:
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))
    elif get_post.draft and get_post.owner_user.id != current_user.id:
        flash("Post not found", "danger")
        return redirect(url_for("site.index"))

    context = {
        "page_title": get_post.title,
    }
    return (
        render_template("posts/view_post.html", **context, post=get_post),
        200,
    )


@site.get("/post/<int:id>/delete/")
@login_required
def delete_post(id):
    get_post = UserPost.query.get(id)
    if not get_post:
        flash("Post not found", "danger")
        return redirect(url_for("site.profile", id=current_user.id))
    elif get_post.owner_user.id != current_user.id:
        flash("Post not found", "danger")
        return redirect(url_for("site.profile", id=current_user.id))

    db.session.delete(get_post)
    db.session.commit()

    flash("Post deleted", "success")
    return redirect(url_for("site.profile", id=current_user.id))
