from cloudcc_api.general.views.general_api import blue_general


def init_general_views(app):
    # blueprint
    app.register_blueprint(blue_general)

