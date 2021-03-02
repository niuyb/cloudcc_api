#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/13 11:58
# 工具：PyCharm
# Python版本：3.7.0
import json
import pandas as pd
from flask import request, Blueprint
from public.utils import Result, engine
from script.data_config import OPPORTUNITY_SQL_TABLE, USER_SQL_TABLE
from settings import settings
from settings.config import OPPORTUNITY_APPEND_ITEMS, APPEND_PAGE_NUMS, USER_APPEND_ITEMS

blue_user = Blueprint("blue_user",__name__)

@blue_user.route("/user/append",methods=["GET"])
def user_update_append():
    """
    获取date指定日期之前所有 更新的opportunity
    date : timestamp ms
    # 最多返回500条数据
    :param request: date,token,page
    :return: data [{},{}]
    """
    result = Result()
    token = request.args.get("token", None)
    page = request.args.get("page",None)
    try:
        page = int(page) - 1
        if page < 0:
            page = 0
    except:
        result.msg = "page 无效"
        return json.dumps(result.dict(), ensure_ascii=False)
    if token:
        try:
            new_data = engine(settings.db_91)
            select_items = ",".join(USER_APPEND_ITEMS)
            print(select_items)
            count_sql = """ select count(crm_id) as nums from {}  """.format(USER_SQL_TABLE)
            count_nums = pd.read_sql_query(count_sql,new_data)["nums"].tolist()[0]
            sql = """ select {} from {}  limit {},{}""".format(str(select_items),USER_SQL_TABLE,page*APPEND_PAGE_NUMS,APPEND_PAGE_NUMS)
            df = pd.read_sql_query(sql, new_data)
            data_dict = df.to_dict(orient='records')
            result.code = 1
            result.total = count_nums
            result.data = data_dict
        except Exception as e:
            print(e)
            result.msg = "获取user增量更新失败"
            return json.dumps(result.dict(),ensure_ascii=False)
    else:
        result.msg = "token无效"
    return json.dumps(result.dict(),ensure_ascii=False)
