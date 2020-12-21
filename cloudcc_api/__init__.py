from flask import Flask

from cloudcc_api.account.views import init_account_views
from cloudcc_api.opportunity.views import init_opportunity_views
from cloudcc_api.order.views import init_order_views


def create_app():
    app = Flask(__name__)

#     加载配置

#     加载三方文件

#     加载路由
    init_account_views(app)
    init_opportunity_views(app)
    init_order_views(app)

    return app
