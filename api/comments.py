from flask import jsonify
from models.posts import UserPostComments
from models.users import User


class Api:
    def __init__(self): ...

    def load(self, id, limit=10, offset=0):
        return (
            UserPostComments.query.filter_by(post_id=id)
            .order_by(UserPostComments.id.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def loadPostedComment(self, user_id, post_id):
        return (
            UserPostComments.query.filter_by(user_id=user_id, post_id=post_id)
            .order_by(UserPostComments.id.desc())
            .first()
        )

    def load_toJSON(self, id, limit, offset):
        comments = (
            UserPostComments.query.filter_by(post_id=id)
            .order_by(UserPostComments.id.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        comments_list = [comment.to_dict() for comment in comments]
        return jsonify(comments_list)
