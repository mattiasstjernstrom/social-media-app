from flask_wtf import FlaskForm
from wtforms import validators, TextAreaField


class CommentOnPostForm(FlaskForm):
    content = TextAreaField(
        "Comment",
        [validators.Length(min=1, max=1000), validators.DataRequired()],
        render_kw={"placeholder": "Your thoughts..."},
    )
