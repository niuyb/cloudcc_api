#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json

from flask import Blueprint, request

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql, modify_by_api
from public.permission_utils import CHECK_PERMISSION_QUERY
from public.utils import Result
from settings.config import ACCOUNT_QUERY_ALLOW, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ClOUDCC_OBJECT, \
    ACCOUNT_MODIFY_ALLOW, ACCOUNT_MAPPING, QY_token, ZW_token, ACCOUNT_FUZZY_QUERY

blue_account = Blueprint("blue_account",__name__)

@blue_account.route("/account/api",methods=["GET"])
def account_query():
    """
    :param request: field_name,field_value,token
    :return: data [{},{}]
    """
    result = Result()
    field_name = request.args.get("field_name",None)
    field_value = request.args.get("field_value",None)
    token = request.args.get("token", None)
    if token:
        if field_name in ACCOUNT_QUERY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)
            try:
                sql_str=CHECK_PERMISSION_QUERY(token,"account")
                if sql_str:
                    if field_name in ACCOUNT_FUZZY_QUERY :
                        sql_string = """ select {} from `{}` where `{}` like '%{}%' limit 15"""
                    else:
                        # 暂未添加多值处理
                        sql_string = """ select {} from `{}` where `{}` in ('{}') """
                    sql_name = ACCOUNT_MAPPING.get(field_name,None)
                    if sql_name:
                        cloudcc_object = ClOUDCC_OBJECT.get("account")
                        sql = sql_string.format(sql_str,cloudcc_object, field_name,field_value)
                        print(sql)
                        data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
                        for data_dict in data:
                            del data_dict["CCObjectAPI"]
                        result.data = data
                        result.code = 1
                    else:
                        result.msg = "field_name传参有误"
                else:
                    result.msg = "暂无权限查询"
            except:
                result.msg = "获取data失败,请检查参数"
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "field_name传参有误,请使用id或name"
    else:
        result.msg = "token无效"
    return json.dumps(result.dict(),ensure_ascii=False)



@blue_account.route("/account/api",methods=["PUT"])
def account_modify():
    """
    :param request:  account_id,modify_field,modify_value,token
    :return:  True or False
    """
    result = Result()
    account_id = request.args.get("account_id", None)
    modify_field = request.args.get("modify_field", None)
    modify_value = request.args.get("modify_value", None)
    token = request.args.get("token", None)
    if token:
        if modify_field in ACCOUNT_MODIFY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)
            try:
                # --------------------后续修改暂时写死----------------------
                if token == QY_token and modify_field == "back_url":
                    cloudcc_field = ACCOUNT_MAPPING.get("qy_"+modify_field)
                elif token == ZW_token and modify_field == "back_url":
                    cloudcc_field = ACCOUNT_MAPPING.get("zw_"+modify_field)
                elif token == ZW_token or token == QY_token:
                    cloudcc_field = ACCOUNT_MAPPING.get(modify_field)
                else:
                    result.msg = "暂无权限"
                    return json.dumps(result.dict(), ensure_ascii=False)
                # --------------------------------------------------------
                # cloudcc_field = ACCOUNT_MAPPING.get(modify_field)
                cloudcc_object = ClOUDCC_OBJECT.get("account")
                data = [{"id": account_id, cloudcc_field: modify_value}]
                res_data = modify_by_api(access_url, "update", cloudcc_object, data, binding)
                result.data = res_data
                result.code = 1
            except Exception as e:
                print(e)
                result.msg = "获取data失败,请检查参数"
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "put modify_field传参有误"
    else:
        result.msg = "token无效"
    return json.dumps(result.dict(),ensure_ascii=False)
