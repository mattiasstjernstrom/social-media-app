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
    content = TextAreaField(
        "Content",
        [validators.Length(min=10, max=1000), validators.DataRequired()],
        render_kw={"placeholder": "Your thoughts..."},
    )
    draft = SwitchField("Draft")
    friends_only = BooleanField("Friends Only")
    followers_only = BooleanField("Followers Only")
