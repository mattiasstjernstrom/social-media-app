from flask import request, url_for, render_template, redirect
from flask_login import current_user


# check if user is logged in and redirect to the correct page
def is_logged_in():
    if (
        request.path == url_for("unauthenticated.sign_in")
        and current_user.is_authenticated
    ):
        return redirect(url_for("site.index"))
    elif request.path == url_for("site.index") and not current_user.is_authenticated:
        return redirect(url_for("unauthenticated.welcome"))


# Global site name
def inject_title():
    return {"title": "StjernSocial"}  # Change to logic for name


# Global injection for Jinja2 templates to see if the current page is active
def is_active(page_name):
    if not current_user.is_authenticated:
        if request.path == url_for(page_name):
            return "active"
        else:
            return ""
