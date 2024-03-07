from flask import jsonify
from models.posts import UserPostComments
from models.users import User
from modules.date_logics import humanize_time


class Api:
    def __init__(self): ...

    def load(self, id, limit=10, offset=0):
        comments = (
            UserPostComments.query.filter_by(post_id=id)
            .order_by(UserPostComments.id.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        comments_list = []
        for comment in comments:
            comment_owner = User.query.get(comment.user_id)
            comment_dict = {
                "id": comment.id,
                "user_id": comment.user_id,
                "post_id": comment.post_id,
                "content": comment.content,
                "date_commented": comment.date_commented,
                "date_humanized": humanize_time(comment.date_commented),
                "date_edited": comment.date_edited,
            }

            for key, value in comment_owner.to_dict().items():
                if key in ["username", "active"]:
                    comment_dict[key] = value
            comments_list.append(comment_dict)

        return comments_list

    def loadPostedComment(self, user_id, post_id):
        return (
            UserPostComments.query.filter_by(user_id=user_id, post_id=post_id)
            .order_by(UserPostComments.id.desc())
            .first()
        )

    def load_toJSON(self, id, limit, offset):
        return jsonify(self.load(id, limit, offset))
