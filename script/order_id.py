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

    sql = """ select * from order_back """
    df = pd.read_sql_query(sql,new_data)
    sql_index = 0
    for row in df.itertuples():
        index = getattr(row, 'Index')
        account_name = getattr(row, 'po')
        created_at = getattr(row, 'created_at')
        timestamp  =time_ms(created_at)
        id= create_id(account_name, timestamp, sql_index)
        sql_index +=1
        df.at[index, 'id'] = id

    print(df)
    sql_table = "order_back"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = """ALTER table `{}`
                      MODIFY `id` varchar(50) COMMENT '星光自建订单id',
                      MODIFY `crm_id` varchar(50) COMMENT 'crm 订单id',
                      MODIFY `po` varchar(50) COMMENT '流水号',
                      MODIFY `owner_id` varchar(50) COMMENT '销售负责人 对应星光salerid',
                      MODIFY `status` varchar(20) COMMENT '订单状态',
                      MODIFY `account_id` varchar(50) COMMENT '最终客户id 对应account 星光id',
                      MODIFY `price_id` varchar(50) COMMENT '价格表名称',
                      MODIFY `opportunity_id` varchar(100) COMMENT '商机id',
                      MODIFY `created_by` varchar(50) COMMENT '创建人',
                      MODIFY `created_at` varchar(50) COMMENT '创建日期',
                      MODIFY `updated_by` varchar(50) COMMENT '最新修改人',
                      MODIFY `updated_at` varchar(50) COMMENT '最新修改日期',
                      MODIFY `amount` varchar(50) COMMENT '订单总金额',
                      MODIFY `discount_amount` varchar(50) COMMENT '总折扣额',
                      MODIFY `contract_status` varchar(20) COMMENT '合同状态',
                      MODIFY `contract_attribute` varchar(10) COMMENT '合同属性 1新签 2续签',
                      MODIFY `contract_id` varchar(50) COMMENT '合同编号',
                      MODIFY `contract_start` varchar(50) COMMENT '合同开始日期',
                      MODIFY `contract_end` varchar(50) COMMENT '最终合同截止日期',
                      MODIFY `contract_back_date` varchar(50) COMMENT '合同归档日期',
                      MODIFY `total_performance` varchar(50) COMMENT '业绩核算(成本）总额',
                      MODIFY `approve_date` varchar(50) COMMENT '审批通过时间',
                      MODIFY `payback_type` varchar(20) COMMENT '回款计划类型',
                      MODIFY `xsy_id` varchar(20) COMMENT '销售易id' """.format( sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()







test()




