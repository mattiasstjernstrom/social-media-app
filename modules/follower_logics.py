"""
Logics for the follower module
"""

from models.db import db
from models.users import User
from models.users import Followers


def check_following(user_id, target_id):
    results = (
        db.session.query(Followers)
        .filter(Followers.follower_id == user_id, Followers.followed_id == target_id)
        .first()
    )
    return results is not None
