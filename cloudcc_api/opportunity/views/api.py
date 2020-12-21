#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json
from flask import Blueprint, request
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import Result
from settings.config import OPPORTUNITY_QUERY_ALLOW, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ClOUDCC_OBJECT


blue_opportunity = Blueprint("blue_opportunity",__name__)

@blue_opportunity.route("/opportunity/api",methods=["GET"])
def opportunity_query():
    """
    :param request: field_name,field_value,token
    :return: data [{},{}]
    """
    result = Result()
    field_name = request.args.get("field_name", None)
    field_value = request.args.get("field_value", None)
    if field_name in OPPORTUNITY_QUERY_ALLOW:
        try:
            access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            result.msg = "获取binding失败,请检查配置"
            return json.dumps(result.dict(), ensure_ascii=False)
        try:
            cloudcc_object = ClOUDCC_OBJECT.get("opportunity")
            sql = """ select id,`name`,`khmc` as accountId from `{}` where `{}` like '%{}%' """.format(cloudcc_object,
                                                                                                       field_name,
                                                                                                       field_value)
            data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
            result.data = data
            result.code = 1
        except:
            result.msg = "获取data失败,请检查参数"
            return json.dumps(result.dict(), ensure_ascii=False)
    else:
        result.msg = "field_name传参有误,请使用id或name"
    return json.dumps(result.dict(), ensure_ascii=False)


