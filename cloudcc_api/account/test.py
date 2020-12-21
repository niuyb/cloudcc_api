#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 13:39
# 工具：PyCharm
# Python版本：3.7.0

from flask import Blueprint


# 原生自建
def init_route(app):
    @app.route("/hello")
    def hello():
        return "hello"


# blueprint
blue = Blueprint("blue",__name__)



@blue.route("/index")
def index():
    return "index"









