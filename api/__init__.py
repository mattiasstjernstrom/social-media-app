from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from api.comments import Comments
from api.posts import Posts
from api.trending import TrendingPosts
from api.notifications import Notifications

api = Blueprint("api", __name__)


@api.route("/")
def index():
    return jsonify({"message": "Welcome to the API!"}), 200


@api.get("/post/<int:post_id>/comments/")
def get_comments(post_id):
    limit = request.args.get("limit", 3, type=int)
    offset = request.args.get("offset", 0, type=int)
    return Comments().load_toJSON(post_id, limit, offset), 200


@api.get("/post/<int:post_id>/get_last_posted_comment")
@login_required
def get_last_posted_comment(post_id):
    return Comments().loadPostedComment(current_user.id, post_id).to_dict(), 200


@api.get("/feed_posts")
@api.get("/feed_posts/")
@login_required
def get_feed_posts():
    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    return Posts().get_feed_post(limit, offset), 201


@api.get("/trending_posts")
@api.get("/trending_posts/")
def get_trending_posts():
    limit = request.args.get("limit", 10, type=int)
    offset = request.args.get("offset", 0, type=int)
    return TrendingPosts().load_toJSON(limit, offset), 201


@api.get("/notifications")
@api.get("/notifications/")
@login_required
def get_notifications():
    return Notifications().load_toJSON(current_user), 200
