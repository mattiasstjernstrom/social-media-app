from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from forms.post import PostForm
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

    context = {
        "page_title": "Profile",
    }
    return (
        render_template("user/profile.html", **context, user=get_user),
        200,
    )


@site.route("/post/", methods=["GET", "POST"])
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
        return redirect(url_for("site.post"))

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
