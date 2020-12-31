#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json
from flask import Blueprint, request
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import Result, engine
from script.data_config import OPPORTUNITY_SQL_TABLE
from settings import settings
from settings.config import OPPORTUNITY_QUERY_ALLOW, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, ClOUDCC_OBJECT, \
    OPPORTUNITY_MAPPING, OPPORTUNITY_FUZZY_QUERY
import pandas as pd

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
    token = request.args.get("token", None)
    database = engine(settings.db_new_data)
    if token:
        if field_name in OPPORTUNITY_QUERY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)
            try:
                if field_name in OPPORTUNITY_FUZZY_QUERY :
                    sql_string = """ select id as opportunity_id,`name`,`zzkh` as account_id,is_deleted from `{}` where `{}` like '%{}%' limit 15"""
                else:
                    # 暂未添加多值处理
                    sql_string = """ select id as opportunity_id,`name`,`zzkh` as account_id,is_deleted from `{}` where `{}` in ('{}') """
                    query_sql = """ select crm_id from {} where id in ("{}") """.format(OPPORTUNITY_SQL_TABLE, field_value)
                    query_df = pd.read_sql_query(query_sql, database)
                    if query_df.shape[0] > 0:
                        field_value = query_df.iloc[0].tolist()[0]
                    else:
                        result.msg = "暂无数据"
                        return json.dumps(result.dict(), ensure_ascii=False)
                sql_name = OPPORTUNITY_MAPPING.get(field_name,None)
                if sql_name:
                    cloudcc_object = ClOUDCC_OBJECT.get("opportunity")
                    sql = sql_string.format(cloudcc_object,sql_name,field_value)
                    print(sql)
                    all_data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
                    data = []
                    for dict in all_data:
                        if int(dict["is_deleted"]) == 0:
                            data.append(dict)
                        else:
                            pass
                    for data_dict in data:
                        del data_dict["CCObjectAPI"]
                        del data_dict["accountId"]
                        del data_dict["opportunityId"]
                        del data_dict["is_deleted"]
                        del data_dict["isDeleted"]
                    result.data = data
                    result.code = 1
                else:
                    result.msg = "field_name传参有误,请使用id或name"
            except:
                result.msg = "获取data失败,请检查参数"
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "field_name传参有误,请使用id或name"
    else:
        result.msg = "token无效"
    return json.dumps(result.dict(), ensure_ascii=False)


