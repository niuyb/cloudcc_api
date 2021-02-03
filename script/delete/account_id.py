#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/30 19:27
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

import  pandas as pd
import pymysql

from public.utils import engine, time_ms
from script.data_config import ACCOUNT_TABLE_STRING
from script.data_utils import create_id
from settings import settings
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)

def get_conn():
    host = "192.168.185.129"
    user = "nyb"
    passwd = "nyb123"
    db = "yydw"
    port = 3306
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=db,
        port=port,
        charset='utf8')
    # 获得游标
    cur = conn.cursor()


    return cur, conn


def test():
    new_data = engine(settings.db_new_data)

    old_sql = """ select id,crm_id from account_back """
    old_df = pd.read_sql_query(old_sql,new_data)

    sql = """ select * from account_back_copy1 """
    df = pd.read_sql_query(sql,new_data)
    df = df.drop(['id'], axis=1)
    df = pd.merge(df, old_df, how='left', on="crm_id")

    sql_index = 0
    for row in df.itertuples():
        id = getattr(row, 'id')
        if not id:
            index = getattr(row, 'Index')
            account_name = getattr(row, 'account_name')
            created_at = getattr(row, 'created_at')
            timestamp  =time_ms(created_at)
            id= create_id(account_name, timestamp, sql_index)
            sql_index +=1
            df.at[index, 'id'] = id

    sql_table = "account_back_copy1"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = ACCOUNT_TABLE_STRING.format( sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()


def change():
    new_data = engine(settings.db_new_data)
    sql = """ select * from account_back_copy1"""
    cc_df = pd.read_sql_query(sql,new_data)

    for row in cc_df.itertuples():

        df_index = getattr(row, 'Index')
        close_date = getattr(row, 'recent_activity_time')
        try:
            cc_df.at[df_index, 'recent_activity_time'] = time_ms(close_date)
        except:
            pass
        close_date = getattr(row, 'push_sea_date')
        try:
            cc_df.at[df_index, 'push_sea_date'] = time_ms(close_date)
        except:
            pass
        created_at = getattr(row, 'created_at')
        try:
            cc_df.at[df_index, 'created_at'] = time_ms(created_at)
        except:
            pass
        updated_at = getattr(row, 'updated_at')
        try:
            cc_df.at[df_index, 'updated_at'] = time_ms(updated_at)
        except:
            pass
        xsy_id = getattr(row, 'xsy_id')
        try:
            xsy_id = str(xsy_id).strip()
        except:
            pass
        cc_df.at[df_index, 'xsy_id'] = xsy_id

    # print(cc_df)

    # owner_id
    local_user_sql = """select `id` as local_owner_id ,crm_id as owner_id from {}""".format("user_back")
    local_user_df = pd.read_sql_query(local_user_sql, new_data)
    cc_df = pd.merge(cc_df, local_user_df, how='left', on="owner_id")
    cc_df = cc_df.drop(["owner_id"], axis=1)
    cc_df = cc_df.rename(columns={"local_owner_id": "owner_id"})
    # created_by
    local_user_df = local_user_df.rename(columns={"owner_id": "created_by"})
    cc_df = pd.merge(cc_df, local_user_df, how='left', on="created_by")
    cc_df = cc_df.drop(["created_by"], axis=1)
    cc_df = cc_df.rename(columns={"local_owner_id": "created_by"})
    # updated_by
    local_user_df = local_user_df.rename(columns={"created_by": "updated_by"})
    cc_df = pd.merge(cc_df, local_user_df, how='left', on="updated_by")
    cc_df = cc_df.drop(["updated_by"], axis=1)
    cc_df = cc_df.rename(columns={"local_owner_id": "updated_by"})
    # sea_id
    local_user_df = local_user_df.rename(columns={"updated_by": "sea_id"})
    cc_df = pd.merge(cc_df, local_user_df, how='left', on="sea_id")
    cc_df = cc_df.drop(["sea_id"], axis=1)
    cc_df = cc_df.rename(columns={"local_owner_id": "sea_id"})
    #recent_activity_by
    local_user_df = local_user_df.rename(columns={"sea_id": "recent_activity_by"})
    cc_df = pd.merge(cc_df, local_user_df, how='left', on="recent_activity_by")
    cc_df = cc_df.drop(["recent_activity_by"], axis=1)
    cc_df = cc_df.rename(columns={"local_owner_id": "recent_activity_by"})


    print(cc_df)
    sql_table = "account_back_copy1"
    cc_df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = ACCOUNT_TABLE_STRING.format(sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()
    new_data.close()

if __name__ == "__main__":

    # test()
    change()




