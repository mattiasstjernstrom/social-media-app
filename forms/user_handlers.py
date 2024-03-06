from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    PasswordField,
    validators,
    BooleanField,
)


class SignInForm(FlaskForm):
    email = EmailField(
        "Email",
        [validators.Length(min=4, max=25)],
        render_kw={"placeholder": "email@example.com"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=6, max=35)],
        render_kw={"placeholder": "•••••••••••••••"},
    )
    remember = BooleanField("Keep me signed in")


class SignUpForm(FlaskForm):
    email = EmailField(
        "Email",
        [validators.Length(min=4, max=25)],
        render_kw={"placeholder": "email@example.com"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=6, max=35)],
        render_kw={"placeholder": "•••••••••••••••"},
    )
    confirm = PasswordField(
        "Confirm Password",
        [validators.EqualTo("password", message="Passwords must match")],
        render_kw={"placeholder": "•••••••••••••••"},
    )
