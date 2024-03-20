from flask import jsonify
from modules.user_logics import FollowerLogics


class Posts:
    def get_feed_post(self, limit, offset):
        post_list = []
        followers_posts = FollowerLogics().get_followers_posts(limit, offset)
        for post in followers_posts:
            post_dict = {
                "id": post.id,
                "user_id": post.user_id,
                "splash_url": post.splash_url,
                "splash_caption": post.splash_caption,
                "splash_credit": post.splash_credit,
                "title": post.title,
                "content": post.content,
                "date_posted": post.date_posted,
                "date_edited": post.date_edited,
                "draft": post.draft,
                "friends_only": post.friends_only,
                "followers_only": post.followers_only,
                "likes": post.likes,
                "shares": post.shares,
                "comments": post.comments,
                "comments_disabled": post.comments_disabled,
            }
        post_list.append(post_dict)

        return post_list
