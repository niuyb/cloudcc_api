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
from script.data_utils import create_account_id
from settings import settings


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

    sql = """ select * from account_back """
    df = pd.read_sql_query(sql,new_data)
    sql_index = 0
    for row in df.itertuples():
        index = getattr(row, 'Index')
        account_name = getattr(row, 'account_name')
        created_at = getattr(row, 'created_at')
        timestamp  =time_ms(created_at)
        id= create_account_id(account_name, timestamp, sql_index)
        sql_index +=1
        df.at[index, 'id'] = id

    print(df)
    sql_table = "account_back"
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







test()




