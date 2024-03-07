class DevConfig:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://root:password@localhost:3306/socialmediaapp"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "randomsecurekey"

    SECURITY_PASSWORD_SALT = "randomsecurepasswordsalt"
    SECURITY_REGISTERABLE = True
    # SECURITY_REGISTER_URL = "/register"
    SECURITY_POST_REGISTER_VIEW = "/create-username"
    SECURITY_LOGIN_URL = "/login"
    SECURITY_LOGOUT_URL = "/logout"
    SECURITY_POST_LOGIN_VIEW = "/"
    USERNAMES_CASE_INSENSITIVE = False

    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
    SECURITY_SEND_PASSWORD_RESET_EMAIL = False
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True

    MAIL_SERVER = "127.0.0.1"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False

    BOOTSTRAP_SERVE_LOCAL = True
