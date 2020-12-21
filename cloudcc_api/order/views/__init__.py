from cloudcc_api.order.views.api import blue_order


def init_order_views(app):

    app.register_blueprint(blue_order)

