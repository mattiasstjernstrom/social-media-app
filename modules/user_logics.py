"""
Logics for the follower module
"""

from flask_login import current_user
from sqlalchemy.orm import joinedload
from models.users import Followers
from models.db import db
from models.posts import UserPost
from sqlalchemy import or_, select
from modules.date_logics import humanize_time
from modules.check_likes import check_liked


class FollowerLogics:
    def check_following(self, user_id, target_id):
        results = (
            db.session.query(Followers)
            .filter(
                Followers.follower_id == user_id, Followers.followed_id == target_id
            )
            .first()
        )
        return results is not None

    def get_followers(self, user_id):
        return (
            select(Followers.followed_id)
            .where(Followers.follower_id == user_id)
            .scalar_subquery()
        )

    def view_followers(self, user_id):
        return (
            db.session.query(Followers)
            .filter(Followers.followed_id == user_id)
            .order_by(Followers.id.desc())
            .all()
        )

    def view_following(self, user_id):
        return (
            db.session.query(Followers)
            .filter(Followers.follower_id == user_id)
            .order_by(Followers.id.desc())
            .all()
        )

    def get_followers_posts(self, limit=10, offset=0):
        followers_subquery = self.get_followers(current_user.id)
        posts = (
            db.session.query(UserPost)
            .join(UserPost.owner_user)
            .filter(
                or_(
                    UserPost.user_id == current_user.id,
                    UserPost.user_id.in_(followers_subquery),
                )
            )
            .order_by(UserPost.date_posted.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        for post in posts:
            post.humanized_time = humanize_time(post.date_posted)
            post.liked = check_liked(post.id)

        return posts


class ProfileLogics:
    def get_user_posts(self, user_id, limit=10, offset=0):
        posts = (
            db.session.query(UserPost)
            .filter(UserPost.user_id == user_id)
            .order_by(UserPost.date_posted.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        for post in posts:
            post.humanized_time = humanize_time(post.date_posted)
            post.liked = check_liked(post.id)

        return posts