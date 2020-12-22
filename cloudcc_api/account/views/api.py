#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json

from flask import Blueprint, request

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql, modify_by_api
from public.utils import Result
from settings.config import ACCOUNT_QUERY_ALLOW, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ClOUDCC_OBJECT, \
    ACCOUNT_MODIFY_ALLOW, ACCOUNT_MAPPING

blue_account = Blueprint("blue_account",__name__)

@blue_account.route("/account/api",methods=["GET"])
def account_query():
    """
    :param request: field_name,field_value
    :return: data [{},{}]
    """
    result = Result()
    field_name = request.args.get("field_name",None)
    field_value = request.args.get("field_value",None)
    if field_name in ACCOUNT_QUERY_ALLOW:
        try:
            access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            result.msg = "获取binding失败,请检查配置"
            return json.dumps(result.dict(), ensure_ascii=False)
        try:
            cloudcc_object = ClOUDCC_OBJECT.get("account")
            sql = """ select id,`name` from `{}` where `{}` like '%{}%' """.format(cloudcc_object, field_name,
                                                                                   field_value)
            data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
            result.data = data
            result.code = 1
        except:
            result.msg = "获取data失败,请检查参数"
            return json.dumps(result.dict(), ensure_ascii=False)
    else:
        result.msg = "field_name传参有误,请使用id或name"
    return json.dumps(result.dict(),ensure_ascii=False)



@blue_account.route("/account/api",methods=["PUT"])
def account_modify():
    """
    :param request:  account_id,modify_field,mofidy_value
    :return:  True or False
    """
    result = Result()
    account_id = request.args.get("account_id", None)
    modify_field = request.args.get("modify_field", None)
    mofidy_value = request.args.get("mofidy_value", None)
    print(modify_field)
    if modify_field in ACCOUNT_MODIFY_ALLOW:
        try:
            access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            result.msg = "获取binding失败,请检查配置"
            return json.dumps(result.dict(), ensure_ascii=False)

        try:
            cloudcc_field = ACCOUNT_MAPPING.get(modify_field)
            cloudcc_object = ClOUDCC_OBJECT.get("account")
            data = [{"id": account_id, cloudcc_field: mofidy_value}]
            res_data = modify_by_api(access_url, "update", cloudcc_object, data, binding)
            result.data = res_data
            result.code = 1
        except:
            result.msg = "获取data失败,请检查参数"
            return json.dumps(result.dict(), ensure_ascii=False)

    else:
        result.msg = "put modify_field传参有误"

    return json.dumps(result.dict(),ensure_ascii=False)
