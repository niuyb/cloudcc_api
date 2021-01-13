from flask import Flask

from cloudcc_api.account.views import init_account_views
from cloudcc_api.general.views import init_general_views
from cloudcc_api.opportunity.views import init_opportunity_views
from cloudcc_api.order.views import init_order_views
from cloudcc_api.user.views import init_user_views


def create_app():
    app = Flask(__name__)

#     加载配置

#     加载三方文件

#     加载路由
    init_general_views(app)
    init_account_views(app)
    init_opportunity_views(app)
    init_order_views(app)
    init_user_views(app)

    return app
