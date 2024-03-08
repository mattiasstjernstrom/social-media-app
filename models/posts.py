from datetime import datetime
from models.db import db


class UserPost(db.Model):
    __tablename__ = "user_posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    splash_url = db.Column(db.String(200), nullable=True)
    splash_caption = db.Column(db.String(100), nullable=True)
    splash_credit = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable=True)
    draft = db.Column(db.Boolean, default=False)
    friends_only = db.Column(db.Boolean, default=False)
    followers_only = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    comments_disabled = db.Column(db.Boolean, default=False)

    owner_user = db.relationship("User", backref="user_posts", lazy=True)

    user_post_likes = db.relationship(
        "UserPostLikes", backref="user_post_likes", lazy=True
    )
    user_post_shares = db.relationship(
        "UserPostShares", backref="user_post_shares", lazy=True
    )
    user_post_comments = db.relationship(
        "UserPostComments", backref="user_post_comments", lazy=True
    )

    def __repr__(self):
        return f"UserPost('{self.title}', '{self.date_posted}')"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "splash_url": self.splash_url,
            "splash_caption": self.splash_caption,
            "splash_credit": self.splash_credit,
            "title": self.title,
            "content": self.content,
            "date_posted": self.date_posted,
            "date_edited": self.date_edited,
            "draft": self.draft,
            "friends_only": self.friends_only,
            "followers_only": self.followers_only,
            "likes": self.likes,
            "shares": self.shares,
            "comments": self.comments,
            "comments_disabled": self.comments_disabled,
        }


class UserPostLikes(db.Model):
    __tablename__ = "user_post_likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("user_posts.id"))
    date_liked = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"UserPostLikes('{self.user_id}', '{self.post_id}', '{self.date_liked}')"


class UserPostShares(db.Model):
    __tablename__ = "user_post_shares"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("user_posts.id"))
    date_shared = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"UserPostShares('{self.user_id}', '{self.post_id}', '{self.date_shared}')"
        )


class UserPostComments(db.Model):
    __tablename__ = "user_post_comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("user_posts.id"))
    content = db.Column(db.Text, nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable=True)

    comment_owner = db.relationship("User", backref="user_post_comments", lazy=True)

    def __repr__(self):
        return f"UserPostComments('{self.user_id}', '{self.post_id}', '{self.date_commented}')"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "content": self.content,
            "date_commented": self.date_commented,
            "date_edited": self.date_edited,
        }


class PostTags(db.Model):
    __tablename__ = "post_tags"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("user_posts.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))

    def __repr__(self):
        return f"PostTags('{self.post_id}', '{self.tag_id}')"


class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Tags('{self.tag}')"

    def to_dict(self):
        return {
            "id": self.id,
            "tag": self.tag,
        }
