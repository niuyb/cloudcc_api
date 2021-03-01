#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/2/18 16:00
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
from script.data_config import ORDER_TABLE_STRING, ORDER_DETAIL_TABLE_STRING, PRODUCT_SQL_TABLE, \
    PAYMENT_RECORD_TABLE_STRING, PAYMENT_PLAN_TABLE_STRING
from script.data_utils import create_id
from settings import settings
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列

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


# def test():
#     new_data = engine(settings.db_new_data)
#
#     sql = """ select * from order_back """
#     df = pd.read_sql_query(sql,new_data)
#     sql_index = 0
#     for row in df.itertuples():
#         index = getattr(row, 'Index')
#         account_name = getattr(row, 'po')
#         created_at = getattr(row, 'created_at')
#         timestamp  =time_ms(created_at)
#         id= create_id(account_name, timestamp, sql_index)
#         sql_index +=1
#         df.at[index, 'id'] = id
#
#     print(df)
#     sql_table = "order_back"
#     df.to_sql(sql_table, new_data, index=False, if_exists="replace")
#     cur, conn = get_conn()
#
#     sql_remarks = ORDER_TABLE_STRING.format( sql_table)
#     cur.execute(sql_remarks)
#
#     cur.close()
#     conn.close()
#
#
#     new_data.close()


def test():
    new_data = engine(settings.db_new_data)

    old_sql = """ select id,crm_id from payment_plan """
    old_df = pd.read_sql_query(old_sql,new_data)

    sql = """ select * from payment_plan_copy1 """
    df = pd.read_sql_query(sql,new_data)
    df = df.drop(['id'], axis=1)
    df = pd.merge(df, old_df, how='left', on="crm_id")

    sql_index = 0
    for row in df.itertuples():
        id = getattr(row, 'id')
        if not id:
            index = getattr(row, 'Index')
            account_name = getattr(row, 'name')
            created_at = getattr(row, 'created_at')
            timestamp  =time_ms(created_at)
            id= create_id(account_name, timestamp, sql_index)
            sql_index +=1
            df.at[index, 'id'] = id

    print(df)
    sql_table = "payment_plan_copy1"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = PAYMENT_PLAN_TABLE_STRING .format( sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()






def change_account_id():
    new_data = engine(settings.db_new_data)

    sql = """ select * from payment_plan_copy1 """
    df = pd.read_sql_query(sql,new_data)

    # account_sql = """ select id as new_account_id, crm_id as account_id from account_back """
    # account_df = pd.read_sql_query(account_sql,new_data)

    # cc_opportunity_str = list_to_sql_string(cc_df["opportunity_id"].dropna().tolist())
    local_opp_sql = """ select id as local_order_id,crm_id as order_id  from `{}`""".format("order_back")
    local_opp_df = pd.read_sql_query(local_opp_sql, new_data)


    df = pd.merge(df, local_opp_df, how='left', on="order_id")
    df = df.drop(["order_id"], axis=1)
    df = df.rename(columns={"local_order_id": "order_id"})

    print(df)

    sql_table = "payment_plan_copy1"

    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()
    sql_remarks = PAYMENT_PLAN_TABLE_STRING.format(sql_table)
    cur.execute(sql_remarks)
    cur.close()
    conn.close()

    print(df.shape)

    new_data.close()


def change():
    new_data = engine(settings.db_new_data)
    sql = """ select * from payment_plan_copy1 """
    cc_df = pd.read_sql_query(sql,new_data)

    for row in cc_df.itertuples():
        df_index = getattr(row, 'Index')
        inform_date = getattr(row, 'inform_date')
        try:
            cc_df.at[df_index, 'inform_date'] = time_ms(inform_date)
        except:
            pass
        dunning_record_date = getattr(row, 'dunning_record_date')
        try:
            cc_df.at[df_index, 'dunning_record_date'] = time_ms(dunning_record_date)
        except:
            pass
        overdue_date = getattr(row, 'overdue_date')
        try:
            cc_df.at[df_index, 'overdue_date'] = time_ms(overdue_date)
        except:
            pass
        lawyer_letter_date = getattr(row, 'lawyer_letter_date')
        try:
            cc_df.at[df_index, 'lawyer_letter_date'] = time_ms(lawyer_letter_date)
        except:
            pass
        deduction_date = getattr(row, 'deduction_date')
        try:
            cc_df.at[df_index, 'deduction_date'] = time_ms(deduction_date)
        except:
            pass
        promise_payment_date = getattr(row, 'promise_payment_date')
        try:
            cc_df.at[df_index, 'promise_payment_date'] = time_ms(promise_payment_date)
        except:
            pass
        saler_promise_payment_date = getattr(row, 'saler_promise_payment_date')
        try:
            cc_df.at[df_index, 'saler_promise_payment_date'] = time_ms(saler_promise_payment_date)
        except:
            pass
        feedback_date = getattr(row, 'feedback_date')
        try:
            cc_df.at[df_index, 'feedback_date'] = time_ms(feedback_date)
        except:
            pass
        register_date = getattr(row, 'register_date')
        try:
            cc_df.at[df_index, 'register_date'] = time_ms(register_date)
        except:
            pass
        payment_date = getattr(row, 'payment_date')
        try:
            cc_df.at[df_index, 'payment_date'] = time_ms(payment_date)
        except:
            pass
        overdue_deal_date = getattr(row, 'overdue_deal_date')
        try:
            cc_df.at[df_index, 'overdue_deal_date'] = time_ms(overdue_deal_date)
        except:
            pass
        created_at = getattr(row, 'created_at')
        cc_df.at[df_index, 'created_at'] = time_ms(created_at)
        updated_at = getattr(row, 'updated_at')
        cc_df.at[df_index, 'updated_at'] = time_ms(updated_at)
        # po = getattr(row, 'po')
        # created_at = getattr(row, 'created_at')
        # timestamp = time_ms(created_at)


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




    sql_table = "payment_plan_copy1"
    cc_df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks =PAYMENT_PLAN_TABLE_STRING.format(sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()
    new_data.close()



if __name__ == "__main__":
    # test()
    # change_account_id()
    change()




