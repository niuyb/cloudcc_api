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
from script.data_utils import create_account_id, create_opportunity_id
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

    sql = """ select * from opportunity_back """
    df = pd.read_sql_query(sql,new_data)
    sql_index = 0
    for row in df.itertuples():
        index = getattr(row, 'Index')
        account_name = getattr(row, 'opportunity_name')
        created_at = getattr(row, 'created_at')
        timestamp  =time_ms(created_at)
        id= create_opportunity_id(account_name, timestamp, sql_index)
        sql_index +=1
        df.at[index, 'id'] = id

    print(df)
    sql_table = "opportunity_back"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = """ALTER table `%s`
                      MODIFY `id` varchar(50) COMMENT '星光自建商机id',
                      MODIFY `crm_id` varchar(50) COMMENT 'crm商机id',
                      MODIFY `entity_type` varchar(20) COMMENT '业务类型',
                      MODIFY `opportunity_name` varchar(500) COMMENT '商机名称',
                      MODIFY `owner_id` varchar (100) COMMENT '星光自建销售id',
                      MODIFY `price_id` varchar(50) COMMENT '价格表id',
                      MODIFY `account_id` varchar(100) COMMENT '最终客户id ',
                      MODIFY `money` varchar(50) COMMENT '商机金额',
                      MODIFY `intended_product` varchar(500) COMMENT '意向产品',
                      MODIFY `sale_stage` varchar(50) COMMENT '销售阶段',
                      MODIFY `win_rate` varchar (10) COMMENT '赢率',
                      MODIFY `close_date` varchar(50) COMMENT '结单日期',
                      MODIFY `saler_promise` varchar(50) COMMENT '销售承诺',
                      MODIFY `project_budget` varchar(255) COMMENT '成本预算',
                      MODIFY `created_at` varchar(50) COMMENT '创建日期',
                      MODIFY `created_by` varchar(50) COMMENT '创建人',
                      MODIFY `updated_at` varchar(50) COMMENT '最新修改日期',
                      MODIFY `updated_by` varchar(50) COMMENT '最新修改人',
                      MODIFY `contact` varchar(100) COMMENT '商机联系人',
                      MODIFY `position` text COMMENT '联系人职务',
                      MODIFY `xsy_id` text COMMENT '销售易id' """ % sql_table
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()







test()




