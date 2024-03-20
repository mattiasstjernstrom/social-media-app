from flask import jsonify
from modules.user_logics import NotificationLogics


class Notifications:
    #! TODO: Fix
    def load_toJSON(self, current_user):
        return jsonify(NotificationLogics().get_notifications(current_user))
