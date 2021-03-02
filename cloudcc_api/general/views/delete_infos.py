#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/22 17:19
# 工具：PyCharm
# Python版本：3.7.0
import json
from urllib import parse

from flask import request

from cloudcc_api.general.views import blue_general
from public.cloudcc_utils import cloudcc_query_sql, cloudcc_get_request_url, cloudcc_get_binding
from public.utils import Result, engine, ms_date, list_to_sql_string
from script.data_config import ACCOUNT_SQL_TABLE, OPPORTUNITY_SQL_TABLE, OPPORTUNITY_API_NAME, ACCOUNT_API_NAME
from settings import settings
from settings.config import GENERAL_DELETED_TYPE_ALLOW, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ACCESS_URL

@blue_general.route("/general/deleted_infos",methods=["GET"])
def get_deleted_infos():

    type = request.args.get("type",None)
    date_stamp = parse.unquote(request.args.get("date", None))
    date = ms_date(int(date_stamp))
    token = request.args.get("token", None)

    result = Result()
    database = engine(settings.db_91)

    if token:
        if type in GENERAL_DELETED_TYPE_ALLOW:

            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                database.close()
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)

            if type == "account":
                object_table = ACCOUNT_SQL_TABLE
                object_api = ACCOUNT_API_NAME
            elif type == "opportunity":
                object_table = OPPORTUNITY_SQL_TABLE
                object_api = OPPORTUNITY_API_NAME
            else:
                result.msg = "type暂不支持"
                database.close()
                return json.dumps(result.dict(), ensure_ascii=False)

            cc_query_sql = """ select `name` from {} where is_deleted != "0" and lastmodifydate like "%{}%" """
            # cc_query_sql = """ select id from {} where is_deleted != "0" limit 10  """

            cc_query_sql = cc_query_sql.format(object_api,date)
            # cc_query_sql = cc_query_sql.format(object_api)
            data = cloudcc_query_sql(access_url, "cqlQuery", object_api, cc_query_sql, binding)

            new_data=[]
            for data_dict in data:
                temp_dict={}
                temp_dict["name"] = data_dict.get("name","")
                new_data.append(temp_dict)
            result.data=new_data
            result.code = 1

        else:
            result.msg = "type错误,请检查参数"
    else:
        result.msg = "token无效"

    database.close()
    return json.dumps(result.dict(), ensure_ascii=False)