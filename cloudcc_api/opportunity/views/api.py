#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json
from urllib import parse

from flask import Blueprint, request

from public.api_update import opportunity_into_mysql
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.permission_utils import CHECK_PERMISSION_QUERY
from public.utils import Result, engine, list_to_sql_string, time_ms
from script.data_config import OPPORTUNITY_SQL_TABLE, OPPORTUNITY_DICT, ACCOUNT_SQL_TABLE, USER_SQL_TABLE
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
    field_name = request.args.get("field_name",None)
    field_value = parse.unquote(request.args.get("field_value",None))
    token = request.args.get("token", None)
    database = engine(settings.db_new_data)

    if token:
        if field_name in OPPORTUNITY_QUERY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                database.close()
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)
            try:
                sql_list=CHECK_PERMISSION_QUERY(token,"opportunity")
                if sql_list:
                    sql_string = """ select * from `{}` where `{}` in ('{}')  and is_deleted="0" """
                    if field_name == "id":
                        query_sql = """ select crm_id from {} where id in ("{}") """.format(OPPORTUNITY_SQL_TABLE,field_value)
                        query_df = pd.read_sql_query(query_sql, database)
                        crm_value = query_df["crm_id"].tolist()
                        if crm_value:
                            field_value = crm_value[0]
                        else:
                            database.close()
                            result.msg = "网络错误,请稍后重试"
                            return json.dumps(result.dict(), ensure_ascii=False)
                    elif field_name in OPPORTUNITY_FUZZY_QUERY :
                        sql_string = """ select * from `{}` where `{}` like '%%{}%%' and is_deleted="0"  order by lastmodifydate DESC limit 15 """
                    elif field_name == "account_id":
                        query_sql = """ select crm_id from {} where id in ("{}") """.format(ACCOUNT_SQL_TABLE,field_value)
                        query_df = pd.read_sql_query(query_sql, database)
                        crm_value = query_df["crm_id"].tolist()
                        if crm_value:
                            field_value = crm_value[0]
                        else:
                            database.close()
                            result.msg = "网络错误,请稍后重试"
                            return json.dumps(result.dict(), ensure_ascii=False)
                    else:
                        database.close()
                        result.msg = "field_name传参有误"
                        return json.dumps(result.dict(), ensure_ascii=False)
                    # 请求cloudcc_api
                    sql_name = OPPORTUNITY_MAPPING.get(field_name,None)
                    if sql_name:
                        cloudcc_object = ClOUDCC_OBJECT.get("opportunity")
                        sql = sql_string.format(cloudcc_object, sql_name,field_value)
                        data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
                        if data:
                            local_data = []
                            for per_data in data:
                                temp_dict = {}
                                for key in sql_list:
                                    temp_dict[key] = per_data.get(key)
                                local_data.append(temp_dict)
                            new_data = []
                            # 入库信息
                            id = opportunity_into_mysql(data)
                            change_df_sql = """ select id from {} where crm_id ="{}" """
                            if id:
                                for data_dict in local_data:
                                    # 修改输出的key值,不暴露原有api的key
                                    new_data_dict = {}
                                    for key, value in data_dict.items():
                                        dict_key = OPPORTUNITY_DICT.get(key, "null")
                                        if dict_key == "crm_id":
                                            new_data_dict[dict_key] = id.get(value,"")
                                        elif dict_key == "account_id":
                                            account_df_list = pd.read_sql_query(change_df_sql.format(ACCOUNT_SQL_TABLE,value),database)["id"].tolist()
                                            if account_df_list:
                                                new_data_dict[dict_key] = account_df_list[0]
                                            else:
                                                new_data_dict[dict_key] = ""
                                        elif dict_key in ["owner_id","updated_by","created_by"]:
                                            user_df_list = pd.read_sql_query(change_df_sql.format(USER_SQL_TABLE,value),database)["id"].tolist()
                                            if user_df_list:
                                                new_data_dict[dict_key] = user_df_list[0]
                                            else:
                                                new_data_dict[dict_key] = ""
                                        elif dict_key == "xsy_id":
                                            # 去除 \t
                                            new_data_dict[dict_key] = str(value).strip()
                                        elif dict_key in ["close_date", "updated_at", "created_at"]:
                                            new_data_dict[dict_key] = time_ms(value)
                                        else:
                                            new_data_dict[dict_key] = value
                                    try:
                                        del new_data_dict["null"]
                                    except:
                                        pass
                                    new_data.append(new_data_dict)
                                result.data = new_data
                                result.code = 1
                            else:
                                result.msg = "更新失败"
                        else:
                            # 空数据
                            pass
                    else:
                        result.msg = "暂无数据"
                else:
                    result.msg = "暂无权限查询"
            except Exception as e:
                print(e)
                database.close()
                result.msg = "获取data失败,请检查参数"
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "field_name传参有误,请使用id或name"
    else:
        result.msg = "token无效"
    database.close()
    return json.dumps(result.dict(),ensure_ascii=False)


