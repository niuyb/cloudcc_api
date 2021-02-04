#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/28 14:27
# 工具：PyCharm
# Python版本：3.7.0
from copy import deepcopy

from public.utils import list_to_sql_string
from settings.config import QY_token, ZW_token, QY_ACCOUNT_QUERY, ZW_ACCOUNT_QUERY, QY_OPPORTUNITY_QUERY, \
    ZW_OPPORTUNITY_QUERY, ZW_ORDER_QUERY, QY_ORDER_QUERY


def CHECK_PERMISSION_QUERY(token,sql_table):
    # 暂时if 后续分配token后修改方法
    # return 可查询的sql字段 ,无权限则False
    if sql_table == "account":
        if token == QY_token:
            sql_list =QY_ACCOUNT_QUERY
            # sql_str = ",".join(sql_list)
            sql_str = sql_list

            # sql_str = list_to_sql_string(sql_list)
            return sql_str
        elif token == ZW_token:
            sql_list =ZW_ACCOUNT_QUERY
            # sql_str = ",".join(sql_list)
            sql_str = sql_list
            return sql_str
        else:
            return False
    elif sql_table == "opportunity":
        if token == QY_token:
            sql_list =QY_OPPORTUNITY_QUERY
            # sql_str = ",".join(sql_list)
            sql_str = sql_list
            return sql_str
        elif token == ZW_token:
            sql_list =ZW_OPPORTUNITY_QUERY
            # sql_str = ",".join(sql_list)
            sql_str = sql_list
            return sql_str
        else:
            return False
    elif sql_table == "post_order":
        if token == QY_token:
            sql_list =deepcopy(QY_ORDER_QUERY)
            sql_str = sql_list

            # sql_str = ",".join(sql_list)
            # sql_str = list_to_sql_string(sql_list)
            return sql_str
        elif token == ZW_token:
            sql_list =deepcopy(ZW_ORDER_QUERY)
            sql_str = sql_list

            # sql_str = ",".join(sql_list)
            return sql_str
        else:
            return False

def check_permission_modify():
    pass