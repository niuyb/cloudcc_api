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

    sql = """ select * from user_back """
    df = pd.read_sql_query(sql,new_data)
    sql_index = 0
    for row in df.itertuples():
        index = getattr(row, 'Index')
        account_name = getattr(row, 'username')
        created_at = getattr(row, 'hire_date')
        timestamp  =time_ms(created_at)
        id= create_account_id(account_name, timestamp, sql_index)
        sql_index +=1
        df.at[index, 'istar_id'] = id

    print(df)
    sql_table = "user_back"
    df.to_sql(sql_table, new_data, index=False, if_exists="replace")
    cur, conn = get_conn()

    sql_remarks = """ALTER table `{}`
                    MODIFY column `istar_id` varchar(100) COMMENT "星光自建 用户id",
                    MODIFY column `crm_id` varchar(100) COMMENT "crm 用户id",
                    MODIFY column `username` varchar(50) COMMENT "用户名称",
                    MODIFY column `department_id` varchar(50) COMMENT "部门id",
                    MODIFY column `status` tinyint(5) COMMENT "是否在职 1在职 0离职",
                    MODIFY column `hire_date` varchar(100) COMMENT "入职时间ms" """.format( sql_table)
    cur.execute(sql_remarks)

    cur.close()
    conn.close()


    new_data.close()







test()




