#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/14 15:41
# 工具：PyCharm
# Python版本：3.7.0
import json
from copy import deepcopy
from urllib import parse

from flask import request

from cloudcc_api.user.views import blue_user
from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import Result, engine
from script.data_config import USER_SQL_TABLE, ACCOUNT_SQL_TABLE, OPPORTUNITY_SQL_TABLE
from settings import settings
from settings.config import USER_MEMBER_QUERY_ALLOW, ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD, USER_MEMBER_MAPPING
import pandas as pd


@blue_user.route("/user/team_member",methods=["GET"])
def get_team_member():

    type = request.args.get("type",None)
    value = parse.unquote(request.args.get("value",None))
    token = request.args.get("token", None)
    result = Result()
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
                cc_query_sql = """ select t0.userorgroupid,t0.rowcause,t1.type,t1.related_id from  {} t0 left outer join tp_sys_group t1 on t0.userorgroupid=t1.id  where parentId='{}'  """
                user_sql = """ select id,`username`,email,crm_role,crm_id from {}""".format(USER_SQL_TABLE)
                user_df = pd.read_sql_query(user_sql, database)
                # 个人user
                crm_user_list = []
                # 输出data
                new_data = []
                # 各个角色个人对应的rowcause
                rowcause_dict = {}
                #角色对应的user
                role_list = []
                if type == "account":
                    account_sql = """ select crm_id from {} where id = "{}" """.format(ACCOUNT_SQL_TABLE,value)
                    account_list = pd.read_sql_query(account_sql, database)["crm_id"].tolist()
                    if account_list:
                        value = account_list[0]
                    else:
                        result.msg = "暂无数据"
                        database.close()
                        return json.dumps(result.dict(), ensure_ascii=False)
                    share_table = USER_MEMBER_MAPPING.get(type, "tp_std_datatable1share")
                elif type == "opportunity":
                    opportunity_sql = """ select crm_id from {} where id = "{}" """.format(OPPORTUNITY_SQL_TABLE,value)
                    opportunity_list = pd.read_sql_query(opportunity_sql, database)["crm_id"].tolist()
                    if opportunity_list:
                        value = opportunity_list[0]
                    else:
                        result.msg = "暂无数据"
                        database.close()
                        return json.dumps(result.dict(), ensure_ascii=False)
                    share_table = USER_MEMBER_MAPPING.get(type,"tp_std_datatable2share")
                else:
                    result.msg = "type暂不支持"
                    database.close()
                    return json.dumps(result.dict(), ensure_ascii=False)
                cc_query_sql = cc_query_sql.format(share_table,value)
                data = cloudcc_query_sql(access_url, "cqlQuery",share_table, cc_query_sql, binding)
                # dedl data
                for data_dict in data:
                    rowcause = data_dict["rowcause"]
                    if data_dict["type"] is None:
                        userorgroupid = data_dict["userorgroupid"]
                        rowcause_dict[userorgroupid] = rowcause
                        crm_user_list.append(userorgroupid)
                    elif str(data_dict["type"]) == "1":
                        related_id = data_dict["related_id"]
                        rowcause_dict[related_id] = rowcause
                        role_list.append(related_id)
                    else:
                        pass
                # 复制rowcause_dict
                temp_rowcause_dict = deepcopy(rowcause_dict)
                role_user_list = user_df[user_df["crm_role"].isin(role_list)]["crm_id"].tolist()
                crm_user_list +=role_user_list
                for key in temp_rowcause_dict.keys():
                    temp_list = user_df[user_df["crm_role"]== key]["crm_id"].tolist()
                    for uid in temp_list:
                        rowcause_dict[uid] = rowcause_dict.get(key,None)
                for crm_user in crm_user_list:
                    temp_df =user_df.loc[user_df["crm_id"]==crm_user,["id","username","email"]].to_dict("records")
                    if temp_df:
                        temp_df = temp_df[0]
                        temp_df["rowcause"] = rowcause_dict.get(crm_user,"")
                        new_data.append(temp_df)
                result.data = new_data
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
