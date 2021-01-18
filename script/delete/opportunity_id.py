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

from public.cloudcc_utils import cloudcc_query_sql
from public.utils import engine, time_ms, list_to_sql_string
from script.data_config import OPPORTUNITY_TABLE_STRING
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

    old_sql = """ select id,crm_id from opportunity_back """
    old_df = pd.read_sql_query(old_sql,new_data)

    sql = """ select * from opportunity_back_copy1 """
    df = pd.read_sql_query(sql,new_data)

    df = df.drop(['id'], axis=1)
    df = pd.merge(df, old_df, how='left', on="crm_id")

    sql_index = 0
    for row in df.itertuples():
        id = getattr(row, 'id')
        if not id:
            index = getattr(row, 'Index')
            account_name = getattr(row, 'opportunity_name')
            created_at = getattr(row, 'created_at')
            timestamp  =time_ms(created_at)
            id= create_id(account_name, timestamp, sql_index)
            sql_index +=1
            df.at[index, 'id'] = id
        else:
            pass

    # print(df)
    sql_table = "opportunity_back_copy1"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = OPPORTUNITY_TABLE_STRING .format( sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()






def change_account_id():
    new_data = engine(settings.db_new_data)

    sql = """ select * from opportunity_back_copy1 """
    df = pd.read_sql_query(sql,new_data)
    account_sql = """ select id as new_account_id, crm_id as account_id from account_back """
    account_df = pd.read_sql_query(account_sql,new_data)

    # print(account_df)
    df = pd.merge(df, account_df, how='left', on="account_id")
    df = df.drop(["account_id"],axis=1)
    df = df.rename(columns = {"new_account_id":"account_id"})
    print(df)

    sql_table = "opportunity_back_copy1"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = OPPORTUNITY_TABLE_STRING.format(sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()


def change():
    new_data = engine(settings.db_new_data)
    sql = """ select * from opportunity_back_copy1 """
    cc_df = pd.read_sql_query(sql,new_data)

    for row in cc_df.itertuples():

        df_index = getattr(row, 'Index')
        close_date = getattr(row, 'close_date')
        try:
            cc_df.at[df_index, 'close_date'] = time_ms(close_date)
        except:
            pass
        created_at = getattr(row, 'created_at')
        cc_df.at[df_index, 'created_at'] = time_ms(created_at)
        updated_at = getattr(row, 'updated_at')
        cc_df.at[df_index, 'updated_at'] = time_ms(updated_at)
        xsy_id = getattr(row, 'xsy_id')
        try:
            xsy_id = str(xsy_id).strip()
        except:
            pass
        cc_df.at[df_index, 'xsy_id'] = xsy_id
        phone = getattr(row, 'phone')
        try:
            phone = str(phone).strip()
        except:
            pass
        cc_df.at[df_index, 'phone'] = phone

    # # owner_id
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


    print(cc_df)


    sql_table = "opportunity_back_copy1"
    cc_df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks =OPPORTUNITY_TABLE_STRING.format(sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()
    new_data.close()


def add_url():
    new_data = engine(settings.db_new_data)
    url_str = "https://k8mm3cmt3235c7ed72cede6e.cloudcc.com/queryframe.action?id={}&m=query"

    sql = """ select * from opportunity_back_copy1 """
    df = pd.read_sql_query(sql, new_data)
    for row in df.itertuples():
        df_index = getattr(row, 'Index')
        crm_id = getattr(row, 'crm_id')
        df.at[df_index, 'url'] = url_str.format(crm_id)

    sql_table = "opportunity_back_copy1"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = OPPORTUNITY_TABLE_STRING.format(sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()

    new_data.close()




if __name__ == "__main__":
    # test()
    # change_account_id()
    # change()
    add_url()



