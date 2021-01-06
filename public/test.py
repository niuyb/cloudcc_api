#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/5 9:54
# 工具：PyCharm
# Python版本：3.7.0

# python 2
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# python 3
# import sys
# import importlib
# importlib.reload(sys)
from public.utils import engine
from settings import settings
import pandas as pd



database = engine(settings.db_new_data)
query_sql  =""" select id from account_back """
account_df = pd.read_sql_query(query_sql, database)

query_sql  =""" select id from account_back_copy """
account_copy_df = pd.read_sql_query(query_sql, database)

account_add_df = account_df.append(account_copy_df, sort=False)
account_add_df = account_add_df.drop_duplicates(subset=['id'], keep=False)


print(account_add_df.shape)
print(account_add_df)