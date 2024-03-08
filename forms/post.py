from collections.abc import Sequence
from typing import Mapping
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    TextAreaField,
    validators,
)
from wtforms.validators import Optional, URL
from flask_bootstrap import SwitchField


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        [validators.Length(min=4, max=25), validators.DataRequired()],
        render_kw={"placeholder": "Write a selling title..."},
    )
    splash_url = StringField(
        "Splash",
        validators=[Optional(), URL()],
        render_kw={"placeholder": "https://example.com/splash.png"},
    )
    splash_caption = StringField(
        "Caption",
        validators=[Optional(), validators.Length(min=4, max=100)],
        render_kw={"placeholder": "A caption for the splash..."},
    )
    splash_credit = StringField(
        "Credit",
        validators=[Optional(), validators.Length(min=4, max=100)],
        render_kw={"placeholder": "Credit the splash..."},
    )
    content = TextAreaField(
        "Content",
        [validators.Length(min=10, max=10000), validators.DataRequired()],
        render_kw={"placeholder": "Your thoughts..."},
    )
    draft = SwitchField("Draft")
    friends_only = SwitchField("Friends Only")
    followers_only = SwitchField("Followers Only")
    comments_disabled = SwitchField("Disable comments on this post")
