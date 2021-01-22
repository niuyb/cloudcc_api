#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/22 9:25
# 工具：PyCharm
# Python版本：3.7.0
import json
from urllib import parse

from flask import request

from cloudcc_api.user.views import blue_user
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import Result, engine, ms_date, list_to_sql_string
from script.data_config import USER_SQL_TABLE, ACCOUNT_SQL_TABLE, OPPORTUNITY_SQL_TABLE
from settings import settings
from settings.config import USER_MEMBER_QUERY_ALLOW, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, \
    USER_MEMBER_MAPPING, APPEND_PAGE_NUMS
import pandas as pd

@blue_user.route("/user/deleted_team",methods=["GET"])
def get_delete_team_member():
    result = Result()
    try:
        type = parse.unquote(request.args.get("type",None))
        date_stamp = parse.unquote(request.args.get("date",None))
        date = ms_date(int(date_stamp))
        page = request.args.get("page",None)
        page = int(page) - 1
        if page < 0:
            page = 0
        token = request.args.get("token", None)
    except:
        result.msg = "获取信息失败"
        return json.dumps(result.dict(), ensure_ascii=False)
    database = engine(settings.db_new_data)

    if token:
        if type in USER_MEMBER_QUERY_ALLOW:
            try:
                access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
                binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
            except:
                database.close()
                result.msg = "获取binding失败,请检查配置"
                return json.dumps(result.dict(), ensure_ascii=False)
            try:
                cc_query_sql = """ select t0.userorgroupid,t0.rowcause,t1.type,t1.related_id,t0.parentid from  {} t0 left outer join tp_sys_group t1 on t0.userorgroupid=t1.id  where isdeleted ="0" and t0.lastmodifydate like "%{}%" limit {},{} """
                total_sql = """ select count(t0.id) as total_num from  {} t0 left outer join tp_sys_group t1 on t0.userorgroupid=t1.id  where isdeleted ="0" and t0.lastmodifydate like "%{}%" """
                user_sql = """ select id as user_id,`username`,email,crm_role,crm_id from {}""".format(USER_SQL_TABLE)
                user_df = pd.read_sql_query(user_sql, database)
                # 输出data
                new_data = []
                # account_crm_id or opportnity_crm_id
                object_crm_id=[]

                if type == "account":
                    object_table=ACCOUNT_SQL_TABLE
                    share_table = USER_MEMBER_MAPPING.get(type, "tp_std_datatable1share")
                elif type == "opportunity":
                    object_table = OPPORTUNITY_SQL_TABLE
                    share_table = USER_MEMBER_MAPPING.get(type,"tp_std_datatable2share")
                else:
                    result.msg = "type暂不支持"
                    database.close()
                    return json.dumps(result.dict(), ensure_ascii=False)

                cc_query_sql = cc_query_sql.format(share_table,date,page*APPEND_PAGE_NUMS,APPEND_PAGE_NUMS)
                data = cloudcc_query_sql(access_url, "cqlQuery",share_table, cc_query_sql, binding)
                cc_total_sql = total_sql.format(share_table,date)
                print(cc_total_sql)
                total_data = cloudcc_query_sql(access_url, "cqlQuery",share_table, cc_total_sql, binding)
                if total_data:
                    total_num = total_data[0]["total_num"]
                else:
                    total_num = ""

                print("total_num",total_num)
                for data_dict in data:
                    object_crm_id.append(data_dict.get("parentid",""))
                object_crm_id_str = list_to_sql_string(object_crm_id)
                object_sql = """ select id,crm_id from {} where crm_id in ({}) """
                object_df = pd.read_sql_query(object_sql.format(object_table,object_crm_id_str), database)

                # # dedl data
                for data_dict in data:
                    temp_dict={}
                    temp_id_list = object_df.loc[object_df["crm_id"]==data_dict.get("parentid",""),"id"].tolist()
                    if temp_id_list:
                        temp_dict["id"] = temp_id_list[0]
                    else:
                        temp_dict["id"] = ""
                    temp_dict["rowcause"] = data_dict["rowcause"]
                    if data_dict["type"] is None:
                        # person 单人
                        userorgroupid = data_dict["userorgroupid"]
                        person_dict =user_df.loc[user_df["crm_id"]==userorgroupid,["user_id","username","email"]].to_dict("records")
                        temp_dict["member"] = person_dict
                        new_data.append(temp_dict)
                    elif str(data_dict["type"]) == "1":
                        # crm_role 角色
                        related_id = data_dict["related_id"]
                        person_dict = user_df.loc[user_df["crm_role"] == related_id, ["user_id", "username", "email"]].to_dict("records")
                        temp_dict["member"] = person_dict
                        new_data.append(temp_dict)
                    else:
                        pass

                result.data = new_data
                result.total = total_num
                result.code = 1

            except Exception as e:
                print(e)
                result.msg="获取信息失败"
                database.close()
                return json.dumps(result.dict(), ensure_ascii=False)
        else:
            result.msg = "type错误,请检查参数"
    else:
        result.msg = "token无效"

    database.close()
    return json.dumps(result.dict(), ensure_ascii=False)