"""
Logics for the follower module
"""

from flask_login import current_user
from sqlalchemy.orm import joinedload
from models.users import Followers
from models.db import db
from models.posts import UserPost
from sqlalchemy import or_, select


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
        return posts
