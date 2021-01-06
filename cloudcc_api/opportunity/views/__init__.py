from cloudcc_api.opportunity.views.api import blue_opportunity
from cloudcc_api.opportunity.views.append import opportunity_update_append

def init_opportunity_views(app):
    # blueprint
    app.register_blueprint(blue_opportunity)

