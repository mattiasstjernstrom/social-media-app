from datetime import datetime, timedelta
from flask import jsonify
from models.posts import UserPost, UserPostComments, UserPostLikes, PostViews
from models.users import User


class TrendingPosts:
    def __init__(self): ...

    def load(self, limit=10, offset=0):
        post_views = PostViews.query.all()
        post_views_dict = {}
        for post_view in post_views:
            if post_view.post_id in post_views_dict:
                post_views_dict[post_view.post_id] += 1
            else:
                post_views_dict[post_view.post_id] = 1

        post_likes = UserPostLikes.query.all()
        post_likes_dict = {}
        for post_like in post_likes:
            if post_like.post_id in post_likes_dict:
                post_likes_dict[post_like.post_id] += 1
            else:
                post_likes_dict[post_like.post_id] = 1

        total_comments = UserPostComments.query.all()
        total_comments_dict = {}
        for comment in total_comments:
            if comment.post_id in total_comments_dict:
                total_comments_dict[comment.post_id] += 1
            else:
                total_comments_dict[comment.post_id] = 1

        trending_posts = []
        for post in UserPost.query.filter(
            UserPost.date_posted > (datetime.now() - timedelta(days=7))
        ).all():
            post_owner = User.query.get(post.user_id)
            post_dict = {
                "id": post.id,
                "title": post.title,
                "date_posted": post.date_posted,
                "total_views": post_views_dict.get(post.id, 0),
                "total_likes": post_likes_dict.get(post.id, 0),
                "total_comments": total_comments_dict.get(post.id, 0),
            }
            for key, value in post_owner.to_dict().items():
                if key in ["username", "active"]:
                    post_dict[key] = value
            trending_posts.append(post_dict)

        for post in trending_posts:
            post["score"] = (
                post["total_views"]
                + 1000 * 0.5
                + post["total_likes"]
                + 1000 * 0.3
                + post["total_comments"]
                + 1000 * 0.2
            )

        trending_posts.sort(key=lambda x: x["score"], reverse=True)
        return trending_posts[offset : offset + limit]

    def load_toJSON(self, limit, offset):
        return jsonify(self.load(limit, offset))
