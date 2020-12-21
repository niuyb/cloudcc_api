from cloudcc_api.opportunity.views.api import blue_opportunity


def init_opportunity_views(app):
    # blueprint
    app.register_blueprint(blue_opportunity)

