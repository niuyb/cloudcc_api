#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/25 9:16
# 工具：PyCharm
# Python版本：3.7.0
import hashlib
import json

from flask import Blueprint, request

from public.utils import Result

blue_general = Blueprint("blue_general",__name__)

@blue_general.route("/token/api",methods=["GET"])
def get_token():
    """
    :param request: username,password
    :return: token
    """
    result = Result()
    username = request.args.get("username",None)
    password = request.args.get("password",None)
    # 验证账号
    if username == "QY_001":
        result.data = {"token":hashlib.md5(username.encode(encoding='UTF-8')).hexdigest()}
        result.code = 1
    elif username == "ZW_001":
        result.data = {"token":hashlib.md5(username.encode(encoding='UTF-8')).hexdigest()}
        result.code = 1
    elif username == "SJ_001":
        result.data = {"token": hashlib.md5(username.encode(encoding='UTF-8')).hexdigest()}
        result.code = 1
    else:
        result.msg = "获取token失败,请检查账号密码"
        return json.dumps(result.dict(), ensure_ascii=False)

    return json.dumps(result.dict(),ensure_ascii=False)