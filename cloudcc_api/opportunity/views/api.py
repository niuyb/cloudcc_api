#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json
from flask import Blueprint, request
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.permission_utils import CHECK_PERMISSION_QUERY
from public.utils import Result, engine, list_to_sql_string
from script.data_config import OPPORTUNITY_SQL_TABLE, OPPORTUNITY_DICT
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
                sql_str=CHECK_PERMISSION_QUERY(token,"opportunity")
                if sql_str:
                    sql_name = OPPORTUNITY_MAPPING.get(field_name,None)
                    if field_name in OPPORTUNITY_FUZZY_QUERY :
                        sql_string = """ select {} from `{}` where `{}` like '%{}%' and is_deleted="0" limit 15"""
                    elif field_name == "id":
                        # 暂未添加多值处理
                        sql_string = """ select {} from `{}` where `{}` in ('{}') and is_deleted="0" """
                        query_sql = """ select crm_id from {} where id in ("{}") """.format(OPPORTUNITY_SQL_TABLE, field_value)
                        query_df = pd.read_sql_query(query_sql, database)
                        if query_df.shape[0] > 0:
                            field_value = query_df.iloc[0].tolist()[0]
                        else:
                            result.msg = "暂无数据"
                            return json.dumps(result.dict(), ensure_ascii=False)
                    elif field_name == "account_id":
                        # 暂未添加多值处理
                        sql_string = """ select {} from `{}` where `{}` in ('{}') and is_deleted="0" """
                        query_sql = """ select crm_id from {} where account_id in ("{}") """.format(OPPORTUNITY_SQL_TABLE, field_value)
                        query_df = pd.read_sql_query(query_sql, database)
                        if query_df.shape[0] > 0:
                            field_value = query_df.iloc[0].tolist()[0]
                            sql_name = "id"
                        else:
                            result.msg = "暂无数据"
                            return json.dumps(result.dict(), ensure_ascii=False)
                    else:
                        sql_string = """ select {} from `{}` where `{}` in ('{}') and is_deleted="0" """
                    if sql_name:
                        cloudcc_object = ClOUDCC_OBJECT.get("opportunity")
                        sql = sql_string.format(sql_str,cloudcc_object,sql_name,field_value)
                        print(sql)
                        data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
                        print(data)
                        # 取出所有id
                        id_list = []
                        for data_dict in data:
                            id_list.append(data_dict.get("id"))
                        df_sql = """ select id,crm_id,account_id from {} where crm_id in ({})""".format(OPPORTUNITY_SQL_TABLE,list_to_sql_string(id_list))
                        df = pd.read_sql_query(df_sql, database)
                        new_data=[]
                        for data_dict in data:
                            del data_dict["CCObjectAPI"]
                            # 修改输出的key值,不暴露原有api的key
                            new_data_dict={}
                            for key,value in data_dict.items():
                                if OPPORTUNITY_DICT.get(key) == "crm_id":
                                    id = df.loc[df["crm_id"] == value, "id"].tolist()
                                    if id:
                                        new_data_dict["id"]= id[0]
                                    else:
                                        new_data_dict["id"] =""
                                elif OPPORTUNITY_DICT.get(key) == "account_id":
                                    account_id = df.loc[df["crm_id"] == data_dict.get("id"), "account_id"].tolist()
                                    if account_id:
                                        new_data_dict["account_id"]= account_id[0]
                                    else:
                                        new_data_dict["account_id"] =""
                                elif OPPORTUNITY_DICT.get(key) == "xsy_id":
                                    # 去除 \t
                                    new_data_dict[OPPORTUNITY_DICT.get(key, "null")] = str(value).strip()
                                else:
                                    new_data_dict[OPPORTUNITY_DICT.get(key,"null")] = value
                            try:
                                del new_data_dict["null"]
                            except:
                                pass
                            new_data.append(new_data_dict)

                        result.data = new_data
                        result.code = 1
                    else:
                        result.msg = "field_name传参有误,请使用id或name"
                else:
                    result.msg = "暂无权限查询"
            except:
                result.msg = "获取data失败,请检查参数"
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "field_name传参有误,请使用id或name"
    else:
        result.msg = "token无效"
    return json.dumps(result.dict(), ensure_ascii=False)


