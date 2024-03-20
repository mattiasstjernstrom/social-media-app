from datetime import datetime
from models.db import db


class UserNotifications(db.Model):
    __tablename__ = "user_notifications"
    id = db.Column(db.Integer, primary_key=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    from_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    notification_type_id = db.Column(db.Integer, db.ForeignKey("notification_types.id"))
    notification_for_id = db.Column(
        db.Integer,
    )
    notification_for_type = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_read = db.Column(db.DateTime, nullable=True)
    date_deleted = db.Column(db.DateTime, nullable=True)

    notification_rel = db.relationship("NotificationTypes", backref="notification_rel")
    to_user_rel = db.relationship(
        "User", foreign_keys=[to_user_id], backref="to_user_rel"
    )
    from_user_rel = db.relationship(
        "User", foreign_keys=[from_user_id], backref="from_user_rel"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "to_user_id": self.to_user_id,
            "from_user_id": self.from_user_id,
            "notification_type_id": self.notification_type_id,
            "notification_for_id": self.notification_for_id,
            "notification_for_type": self.notification_for_type,
            "date_created": self.date_created,
            "date_read": self.date_read,
            "date_deleted": self.date_deleted,
        }

    def __repr__(self):
        return f"UserNotifications('{self.id}', '{self.to_user_id}', '{self.from_user_id}', '{self.notification_type_id}', '{self.notification_for_id}', '{self.notification_for_type}', '{self.date_created}', '{self.date_read}', '{self.date_deleted}')"


class NotificationTypes(db.Model):
    __tablename__ = "notification_types"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
        }

    def __repr__(self):
        return f"NotificationTypes('{self.id}', '{self.type}', '{self.description}')"
