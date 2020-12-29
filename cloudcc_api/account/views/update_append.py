#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/25 15:56
# 工具：PyCharm
# Python版本：3.7.0
import json
import pandas as pd
from flask import request
from cloudcc_api.account.views import blue_account
from public.utils import Result, engine, time_ms
from settings import settings
from settings.config import UPDATE_APPEND_ITEMS


@blue_account.route("/account/append",methods=["GET"])
def account_update_append():
    """
    获取date指定日期之前所有的account
    date : 2020-12-25 17:51
    :param request: date,token
    :return: data [{},{}]
    """
    result = Result()
    date = request.args.get("date",None)
    token = request.args.get("token", None)
    if token:
        try:
            date_stamp = time_ms(date)
            new_data = engine(settings.db_new_data)
            select_items = ",".join(UPDATE_APPEND_ITEMS)
            sql = """ select {} from account where created_at >= {}""".format(str(select_items),date_stamp)
            account_df = pd.read_sql_query(sql, new_data)
            account_dict = account_df.to_dict(orient='records')
            result.code = 1
            result.data = account_dict
        except:
            result.msg = "获取Account增量更新失败"
            return json.dumps(result.dict(),ensure_ascii=False)
    else:
        result.msg = "token无效"
    return json.dumps(result.dict(),ensure_ascii=False)
