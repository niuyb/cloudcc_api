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

    sql = """ select * from account_back_copy2 """
    df = pd.read_sql_query(sql,new_data)
    df = df.drop(['id'], axis=1)
    df = pd.merge(df, old_df, how='left', on="crm_id")

    sql_index = 0
    for row in df.itertuples():
        id = getattr(row, 'id')
        if id:
            index = getattr(row, 'Index')
            account_name = getattr(row, 'account_name')
            created_at = getattr(row, 'created_at')
            timestamp  =time_ms(created_at)
            id= create_id(account_name, timestamp, sql_index)
            sql_index +=1
            df.at[index, 'id'] = id

    sql_table = "account_back_copy2"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = """ALTER table `%s` 
                         MODIFY column `id` varchar(100)  COMMENT '星光自建客户id',
                         MODIFY column `crm_id` varchar(20) COMMENT '销售易客户ID ',
                         MODIFY column `entity_type` varchar(20) COMMENT '客户类型(客户，代理商）',
                         MODIFY column `owner_id` varchar(50) COMMENT '对应星光自建销售id',
                         MODIFY column `account_name` varchar(255) COMMENT '客户名称',
                         MODIFY column `level` varchar(10) COMMENT '客户级别（开发客户、重点客户、正式客户）',
                         MODIFY column `sea_status` varchar(20) COMMENT '公海状态',
                         MODIFY column `longitude` varchar(100) COMMENT '经度',
                         MODIFY column `latitude` varchar(100) COMMENT '纬度',
                         MODIFY column `address` text COMMENT '地址',
                         MODIFY column `address_province` varchar(255) COMMENT '省',
                         MODIFY column `address_city` varchar(255) COMMENT '市',
                         MODIFY column `address_area` varchar(255) COMMENT '区',
                         MODIFY column `recent_activity_time` varchar(20) COMMENT '最新活动记录',
                         MODIFY column `recent_activity_by` varchar(50) COMMENT '最新跟进人 对应星光新建销售id',
                         MODIFY column `sea_id` varchar (50) COMMENT '所属公海',
                         MODIFY column `created_at` varchar(50) COMMENT '创建日期',
                         MODIFY column `created_by` varchar(50) COMMENT '创建人',
                         MODIFY column `updated_at` varchar(50) COMMENT '最新修改日',
                         MODIFY column `updated_by` varchar(50) COMMENT '最新修改人  对应星光新建销售id',
                         MODIFY column `industry_1` varchar(255) COMMENT '一级行业',
                         MODIFY column `industry_2` varchar(255) COMMENT '二级行业',
                         MODIFY column `contact` varchar(255) COMMENT '联系人',
                         MODIFY column `contact_phone` varchar(255) COMMENT '联系电话',
                         MODIFY column `contact_post` varchar(255) COMMENT '联系职务',
                         MODIFY column `department_top` varchar(20) COMMENT '所属事业部  对应星光自建部门id',
                         MODIFY column `department` varchar(20) COMMENT '客户所属部门  对应星光自建部门id',
                         MODIFY column `sea_push` varchar(20) COMMENT '是否为公海池推送客户',
                         MODIFY column `push_sea_date` varchar(20) COMMENT '公海池推送时间',
                         MODIFY column `xsy_id` varchar(20) COMMENT '销售易id' """ % sql_table
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()


def change():
    new_data = engine(settings.db_new_data)
    sql = """ select * from account_back_copy """
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
        cc_df.at[df_index, 'created_at'] = time_ms(created_at)
        updated_at = getattr(row, 'updated_at')
        cc_df.at[df_index, 'updated_at'] = time_ms(updated_at)
        xsy_id = getattr(row, 'xsy_id')
        try:
            xsy_id = str(xsy_id).strip()
        except:
            pass
        cc_df.at[df_index, 'xsy_id'] = xsy_id

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
    sql_table = "account_back_copy"
    cc_df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = """ALTER table `%s`
                    MODIFY column `id` varchar(100)  COMMENT '星光自建客户id',
                    MODIFY column `crm_id` varchar(20) COMMENT '销售易客户ID ',
                    MODIFY column `entity_type` varchar(20) COMMENT '客户类型(客户，代理商）',
                    MODIFY column `owner_id` varchar(50) COMMENT '对应星光自建销售id',
                    MODIFY column `account_name` varchar(255) COMMENT '客户名称',
                    MODIFY column `level` varchar(10) COMMENT '客户级别（开发客户、重点客户、正式客户）',
                    MODIFY column `sea_status` varchar(20) COMMENT '公海状态',
                    MODIFY column `longitude` varchar(100) COMMENT '经度',
                    MODIFY column `latitude` varchar(100) COMMENT '纬度',
                    MODIFY column `address` text COMMENT '地址',
                    MODIFY column `address_province` varchar(255) COMMENT '省',
                    MODIFY column `address_city` varchar(255) COMMENT '市',
                    MODIFY column `address_area` varchar(255) COMMENT '区',
                    MODIFY column `recent_activity_time` varchar(20) COMMENT '最新活动记录',
                    MODIFY column `recent_activity_by` varchar(50) COMMENT '最新跟进人 对应星光新建销售id',
                    MODIFY column `sea_id` varchar (50) COMMENT '所属公海',
                    MODIFY column `created_at` varchar(50) COMMENT '创建日期',
                    MODIFY column `created_by` varchar(50) COMMENT '创建人',
                    MODIFY column `updated_at` varchar(50) COMMENT '最新修改日',
                    MODIFY column `updated_by` varchar(50) COMMENT '最新修改人  对应星光新建销售id',
                    MODIFY column `industry_1` varchar(255) COMMENT '一级行业',
                    MODIFY column `industry_2` varchar(255) COMMENT '二级行业',
                    MODIFY column `contact` varchar(255) COMMENT '联系人',
                    MODIFY column `contact_phone` varchar(255) COMMENT '联系电话',
                    MODIFY column `contact_post` varchar(255) COMMENT '联系职务',
                    MODIFY column `department_top` varchar(20) COMMENT '所属事业部  对应星光自建部门id',
                    MODIFY column `department` varchar(20) COMMENT '客户所属部门  对应星光自建部门id',
                    MODIFY column `sea_push` varchar(20) COMMENT '是否为公海池推送客户',
                    MODIFY column `push_sea_date` varchar(20) COMMENT '公海池推送时间' """ % sql_table
    cur.execute(sql_remarks)

    cur.close()
    conn.close()
    new_data.close()

if __name__ == "__main__":

    # test()
    change()




