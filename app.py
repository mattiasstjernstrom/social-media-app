from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_mail import Mail
from flask_migrate import Migrate, upgrade
from flask_security import Security, SQLAlchemyUserDatastore
from flask_wtf.csrf import CSRFProtect

from api import api
from models.db import db
from models.users import User, Role
from models.posts import UserPost
from models.notifications import UserNotifications
from views.unauth import unauthenticated
from views.site import site
from services import *


app = Flask(__name__)
app.config.from_object("config.DevConfig")

db.init_app(app)
app.mail = Mail(app)

app.context_processor(inject_config)
app.before_request(is_logged_in)
app.jinja_env.globals.update(is_active=is_active)
csfr = CSRFProtect(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role, UserPost)
app.security = Security(app, user_datastore)
migrate = Migrate(app, db)

bootstrap = Bootstrap5(app)


# Blueprint registration
app.register_blueprint(unauthenticated, url_prefix="/")
app.register_blueprint(site, url_prefix="/")
app.register_blueprint(api, url_prefix="/api")


if __name__ == "__main__":
    with app.app_context():
        upgrade()
        from modules.data_seeder import DataSeeder

        DataSeeder().seed_all()
    app.run(debug=True, port=5000)
