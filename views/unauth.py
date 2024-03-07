from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user

from models.db import db
from models.users import User
from forms.user import SignInForm, SignUpForm, CreateUsernameForm

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


@unauthenticated.route("/create-username", methods=["GET", "POST"])
def create_username():
    if current_user.is_authenticated and current_user.username == None:
        form = CreateUsernameForm()
        if request.method == "POST":
            username = request.form["username"]
            if db.session.query(User).filter_by(username=username).first():
                flash("Username already exists, try another one!", "danger")
                return render_template("unauth/username.html", form=form), 200
            current_user.username = username
            try:
                db.session.add(current_user)
                db.session.commit()
                db.session.refresh(current_user)
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred! Please try again later.", "danger")
                return render_template("unauth/username.html", form=form), 200
            flash("Username created successfully!", "success")
            return redirect(url_for("site.index"))
        else:
            return render_template("unauth/username.html", form=form), 200


@unauthenticated.route("/sign-up")
def sign_up():
    context = {
        "page_title": "Sign Up",
    }
    form = SignUpForm()
    return render_template("unauth/sign-up.html", **context, form=form), 200
