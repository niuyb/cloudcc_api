#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 14:16
# 工具：PyCharm
# Python版本：3.7.0
import json

from flask import Blueprint, request
import pandas as pd

from public.api_update import  account_insert_mysql
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql, modify_by_api
from public.permission_utils import CHECK_PERMISSION_QUERY
from public.utils import Result, list_to_sql_string, engine, time_ms
from script.data_config import ACCOUNT_DICT, ACCOUNT_SQL_TABLE
from settings import settings
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
    database = engine(settings.db_new_data)

    if token:
        if field_name in ACCOUNT_QUERY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                database.close()
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)
            try:
                sql_list=CHECK_PERMISSION_QUERY(token,"account")
                if sql_list:
                    str_list=[]
                    for sql_str in sql_list:
                        sql_str = ACCOUNT_DICT.get(sql_str)
                        str_list.append(sql_str)
                    str_list.remove("crm_id")
                    sql_str = ','.join(str_list)
                    if field_name in ACCOUNT_FUZZY_QUERY :
                        query_sql = """ select id,{} from {} where {} like '%%{}%%' limit 15 """.format(sql_str,ACCOUNT_SQL_TABLE, ACCOUNT_DICT.get(field_name),field_value)
                        sql_string = """ select * from `{}` where `{}` like '%%{}%%' and is_deleted="0" limit 15"""
                    else:
                        # 暂未添加多值处理
                        sql_string = """ select * from `{}` where `{}` in ('{}')  and is_deleted="0" """
                        query_sql = """ select id,{} from {} where {} in ("{}") """.format(sql_str,ACCOUNT_SQL_TABLE,field_name,field_value)
                    query_df = pd.read_sql_query(query_sql, database)
                    if query_df.shape[0] >0:
                    # if False:
                        query_dict = query_df.to_dict("records")
                        result.data = query_dict
                        result.code = 1
                    else:
                        sql_name = ACCOUNT_MAPPING.get(field_name,None)
                        if sql_name:
                            # sql_str = ",".join(sql_list)
                            cloudcc_object = ClOUDCC_OBJECT.get("account")
                            sql = sql_string.format(cloudcc_object, field_name,field_value)
                            data = cloudcc_query_sql(access_url, "cqlQuery", cloudcc_object, sql, binding)
                            if data:
                                local_data=[{}]
                                for key in sql_list:
                                    local_data[0][key] = data[0].get(key)
                                new_data=[]
                                # 入库信息
                                id = account_insert_mysql(data)
                                # id = ""
                                for data_dict in local_data:
                                    # 修改输出的key值,不暴露原有api的key
                                    new_data_dict={}
                                    for key,value in data_dict.items():
                                        account_dict_key = ACCOUNT_DICT.get(key,"null")
                                        if account_dict_key == "crm_id":
                                            if id:
                                                new_data_dict["id"]= id
                                            else:
                                                new_data_dict["id"] =""
                                        elif account_dict_key == "xsy_id":
                                            # 去除 \t
                                            new_data_dict[account_dict_key] = str(value).strip()
                                        elif account_dict_key in ["push_sea_date","updated_at","created_at","recent_activity_time"]:
                                            new_data_dict[account_dict_key] = time_ms(value)
                                        else:
                                            new_data_dict[account_dict_key] = value
                                    try:
                                        del new_data_dict["null"]
                                    except:
                                        pass
                                    new_data.append(new_data_dict)
                                result.data = new_data
                                result.code = 1
                            else:
                                # 空数据
                                pass
                        else:
                            result.msg = "field_name传参有误"
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
    database = engine(settings.db_new_data)

    if token:
        if modify_field in ACCOUNT_MODIFY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                result.msg = "获取binding失败,请检查配置"
                database.close()
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
                account_sql = """ select crm_id from {} where id="{}" """.format(ACCOUNT_SQL_TABLE,account_id)
                df = pd.read_sql_query(account_sql, database)
                if df.shape[0] > 0:
                    account_id=df["crm_id"].tolist()[0]
                else:
                    result.msg = "暂无数据"
                    database.close()
                    return json.dumps(result.dict(), ensure_ascii=False)
                data = [{"id": account_id, cloudcc_field: modify_value}]
                res_data = modify_by_api(access_url, "update", cloudcc_object, data, binding)
                result.data = res_data
                result.code = 1
            except Exception as e:
                print(e)
                result.msg = "获取data失败,请检查参数"
                database.close()
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "put modify_field传参有误"
    else:
        result.msg = "token无效"
    database.close()
    return json.dumps(result.dict(),ensure_ascii=False)
