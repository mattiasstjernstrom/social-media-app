"""
Logics for the follower module
"""

from flask_login import current_user
from models.users import Followers
from models.db import db
from models.posts import UserPost, UserPostComments
from models.notifications import UserNotifications
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
            .filter(UserPost.draft == False)
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


class NotificationLogics:

    def get_notifications(self, current_user):
        notification_list = []
        notifications = (
            db.session.query(UserNotifications)
            .filter(UserNotifications.to_user_id == current_user.id)
            .order_by(UserNotifications.date_created.desc())
            .limit(20)
            .all()
        )

        for notification in notifications:
            to_post = None
            if notification.notification_for_type == "post":
                for_type = (
                    db.session.query(UserPost)
                    .filter(UserPost.id == notification.notification_for_id)
                    .first()
                )

                notification_text = for_type.title
                for_post = str(notification.notification_rel.id)

            if notification.notification_for_type == "comment":
                for_type = (
                    db.session.query(UserPostComments)
                    .filter(UserPostComments.id == notification.notification_for_id)
                    .first()
                )

                get_post: UserPostComments = (
                    db.session.query(UserPostComments)
                    .filter(UserPostComments.id == notification.notification_for_id)
                    .first()
                )
                notification_text = get_post.content
                for_post = get_post.post_id
                to_post = f"comment-{get_post.id}"

            notification_dict = {
                "id": notification.id,
                "to_user_id": notification.to_user_id,
                "from_user_id": notification.from_user_id,
                "from_username": notification.from_user_rel.username,
                "notification_type_id": notification.notification_type_id,
                "notification_for_id": notification.notification_for_id,
                "notification_for_type": notification.notification_for_type,
                "notification_types": notification.notification_rel,
                "notification_rel": for_type,
                "to_post": to_post,
                "for_post": for_post,
                "text": notification_text,
                "date_created": notification.date_created,
                "date_created_humanized": humanize_time(notification.date_created),
                "date_read": notification.date_read,
                "date_deleted": notification.date_deleted,
                "new": notification.date_read is None,
            }
            notification_list.append(notification_dict)

            # Mark as read
            if notification.date_read is None:
                notification.date_read = db.func.now()
                db.session.add(notification)
                db.session.commit()

        return notification_list

    def make_notification(
        self,
        to_user_id,
        from_user_id,
        notification_type_id,
        notification_for_id,
        notification_for_type,
    ):
        notification = UserNotifications(
            to_user_id=to_user_id,
            from_user_id=from_user_id,
            notification_type_id=notification_type_id,
            notification_for_id=notification_for_id,
            notification_for_type=notification_for_type,
            date_read=None,
        )
        db.session.add(notification)
        db.session.commit()
