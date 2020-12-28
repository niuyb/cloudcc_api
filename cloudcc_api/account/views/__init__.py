# from cloudcc_api.account.test import blue, init_route
from cloudcc_api.account.views.api import blue_account


from cloudcc_api.account.views.api import (account_query,account_modify)
from cloudcc_api.account.views.update_append import (account_update_append)


def init_account_views(app):
    # 原生
    # init_route(app)
    # blueprint
    # app.register_blueprint(blue)
    app.register_blueprint(blue_account)

