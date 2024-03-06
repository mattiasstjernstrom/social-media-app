from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from flask_security import Security

from forms.user_handlers import SignInForm, SignUpForm

unauthenticated = Blueprint("unauthenticated", __name__)


@unauthenticated.route("/welcome")
def welcome():
    context = {
        "page_title": "Yet another social media site!",
        "content": "Hello, World!",
    }
    return render_template("unauth/index.html", **context), 200


@unauthenticated.route("/sign-in")
def sign_in():
    context = {
        "page_title": "Sign In",
    }
    form = SignInForm(request.form)
    return render_template("unauth/sign-in.html", **context, form=form), 200


@unauthenticated.route("/sign-up")
def sign_up():
    context = {
        "page_title": "Sign Up",
    }
    form = SignUpForm()
    return render_template("unauth/sign-up.html", **context, form=form), 200
