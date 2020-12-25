#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0


from flask import Blueprint

blue_order = Blueprint("blue_order",__name__)

@blue_order.route("/order/api",methods=["GET"])
def order_query():
    return "blue_order_index"



