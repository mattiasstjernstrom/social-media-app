from datetime import datetime
from models.db import db


class UserPost(db.Model):
    __tablename__ = "user_posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    splash_url = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
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

    def __repr__(self):
        return f"UserPostComments('{self.user_id}', '{self.post_id}', '{self.date_commented}')"
