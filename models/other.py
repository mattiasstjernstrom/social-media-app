from models.db import db


class AlembicVersion(db.Model):
    __tablename__ = "alembic_version"
    version_num = db.Column(db.String(32), primary_key=True)
