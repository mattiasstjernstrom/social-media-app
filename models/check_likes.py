from flask_login import current_user
from models.posts import UserPostLikes


def check_liked(post_id):
    if current_user.is_authenticated:
        existing_like = UserPostLikes.query.filter_by(
            user_id=current_user.id, post_id=post_id
        ).first()
        if existing_like:
            return True
        else:
            return False
