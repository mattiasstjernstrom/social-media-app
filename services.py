from datetime import datetime
from flask import request, url_for, redirect, session
from flask_login import current_user
from random import randint

from models.notifications import UserNotifications


# check if user is logged in and redirect to the correct page
def is_logged_in():

    # TODO; GDPR compliance
    if not current_user.is_authenticated and not "session_id" in session:
        timestamp = datetime.now().timestamp()

        session["session_id"] = int(
            timestamp + randint(111, 999)
        )  # If high load on site, change to higher number
    if (
        request.path == url_for("unauthenticated.sign_in")
        and current_user.is_authenticated
    ):
        return redirect(url_for("site.index"))
    elif request.path == url_for("site.index") and not current_user.is_authenticated:
        return redirect(url_for("unauthenticated.welcome"))


# Global config
def inject_config():
    if not current_user.is_authenticated:
        return {"title": "StjernSocial"}
    new_notifications = UserNotifications.query.filter_by(
        to_user_id=current_user.id, date_read=None, date_deleted=None
    ).count()

    return {
        "title": "StjernSocial",
        "check_notifications": new_notifications,
    }


# Global injection for Jinja2 templates to see if the current page is active
def is_active(page_name):
    if not current_user.is_authenticated:
        if request.path == url_for(page_name):
            return "active"
        else:
            return ""
