from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from api.comments import Api

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return jsonify({"message": "Welcome to the API!"}), 200


@api.get("/post/<int:post_id>/comments/")
def get_comments(post_id):
    limit = request.args.get("limit", 3, type=int)
    offset = request.args.get("offset", 0, type=int)
    return Api().load_toJSON(post_id, limit, offset), 200


@api.get("/post/<int:post_id>/get_last_posted_comment")
@login_required
def get_last_posted_comment(post_id):
    return Api().loadPostedComment(current_user.id, post_id).to_dict(), 200
