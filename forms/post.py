from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    TextAreaField,
    validators,
)
from wtforms.validators import Optional, URL
from flask_bootstrap import SwitchField
from wtforms.validators import Regexp
import regex


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
        validators=[Optional(), validators.Length(min=3, max=100)],
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
    tags = StringField(
        "Add Tags",
        validators=[
            Optional(),
            validators.Length(min=2, max=100),
            Regexp(
                regex.compile(r"^[\p{L}\p{N}\-#-, ]+$", regex.UNICODE),
                message="Only letters, numbers, and hyphens are allowed",
            ),
        ],
        render_kw={"placeholder": "Music, Cats, Programming..."},
    )
    draft = SwitchField("Draft")
    friends_only = SwitchField("Friends Only")
    followers_only = SwitchField("Followers Only")
    comments_disabled = SwitchField("Disable comments on this post")
