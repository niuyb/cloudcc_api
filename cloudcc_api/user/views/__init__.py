from cloudcc_api.user.views.append import blue_user


def init_user_views(app):
    # blueprint
    app.register_blueprint(blue_user)

