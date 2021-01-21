#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 18:02
# 工具：PyCharm
# Python版本：3.7.0
from public.utils import get_conn
from settings.settings import db_new_data


def inster_sql(new_data,sql_table,columns_order,df,local_str):
    cur, conn = get_conn(host=db_new_data["DB_HOST"],user=db_new_data["DB_USER"],passwd=db_new_data["DB_PWD"],db=db_new_data["DB_NAME"],port=3306)
    try:
        # 删除本次操作的所有local id
        delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(sql_table, local_str)
        cur.execute(delete_sql)
        conn.commit()
        # 入库操作
        df = df[columns_order]
        df.to_sql(sql_table, new_data, index=False, if_exists="append")
    except Exception as e:
        print(e)
        pass
    finally:
        cur.close()
        conn.close()
