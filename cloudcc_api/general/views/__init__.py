from cloudcc_api.general.views.general_api import blue_general
from cloudcc_api.general.views.delete_infos import get_deleted_infos

def init_general_views(app):
    # blueprint
    app.register_blueprint(blue_general)

