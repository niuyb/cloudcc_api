from cloudcc_api.user.views.append import blue_user
from cloudcc_api.user.views.team_members import get_team_member

def init_user_views(app):
    # blueprint
    app.register_blueprint(blue_user)

