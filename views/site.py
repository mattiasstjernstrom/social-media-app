from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from forms.user_handlers import SignInForm, SignUpForm
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
    form = SignInForm(request.form)
    get_user = User.query.get(id)

    context = {
        "page_title": "Profile",
    }
    return (
        render_template("user/profile.html", **context, user=get_user, form=form),
        200,
    )
