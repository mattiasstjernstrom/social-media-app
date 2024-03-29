from datetime import datetime
from flask_security import UserMixin, RoleMixin, AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey

from models.db import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    verified = Column(Boolean(), default=False)
    roles = relationship(
        "Role", secondary="roles_users", backref=backref("users", lazy="dynamic")
    )

    def to_dict(self):
        return {
            "user_id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "last_login_at": self.last_login_at,
            "current_login_at": self.current_login_at,
            "last_login_ip": self.last_login_ip,
            "current_login_ip": self.current_login_ip,
            "login_count": self.login_count,
            "active": self.active,
            "fs_uniquifier": self.fs_uniquifier,
            "confirmed_at": self.confirmed_at,
            "verified": self.verified,
        }


class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = Column(Integer(), primary_key=True)
    user_id = Column("user_id", Integer(), ForeignKey("user.id"))
    role_id = Column("role_id", Integer(), ForeignKey("role.id"))


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)


class Followers(db.Model):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey("user.id"))
    followed_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    follower = relationship(
        "User", foreign_keys=[follower_id], backref=backref("followed", lazy="dynamic")
    )
    followed = relationship(
        "User", foreign_keys=[followed_id], backref=backref("followers", lazy="dynamic")
    )
