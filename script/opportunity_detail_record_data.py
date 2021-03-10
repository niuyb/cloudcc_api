#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/2/25 15:30
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


import datetime
import os
import sys
import time

import pymysql
from datetime import timedelta

path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)
from public.Time import Time

import pandas as pd

from public.utils import engine
from script.data_config import OPPORTUNITY_SQL_TABLE, OPPORTUNITY_DETAIL_SQL_TABLE
from settings import settings

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns',None) # 展示所有列
pd.set_option('display.width', None)

class Opportunity_Record():


    def __init__(self,type):
        # week 未来一周内结单
        # month 未来一个月内结单
        # season 未来一个季度内结单
        self.new_data = engine(settings.db_new_data)
        self.today = datetime.date.today()
        self.today_tmp = self.date_ms(str(self.today))
        self.now = datetime.datetime.now()
        self.opportunity_detail_table = OPPORTUNITY_DETAIL_SQL_TABLE
        # self.now = datetime.date.today() + datetime.timedelta(-100)
        self.type = type
        # self.time_dict={
        #     "week":7,
        #     "month":30,
        #     "season":90,
        # }
        self.columns_order=["type","date","id","crm_id","owner_id","name","product_id","amount","opportunity_id","price_unit","created_at","created_by","updated_at","updated_by","close_date"]

    def date_ms(self,date):
        # timestr = '2019-01-14 15:22:18'
        datetime_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
        return obj_stamp

    # 本周第一天 0点0分0秒
    def this_week_start(self):
        week_start_tmp= self.now - timedelta(days=self.now.weekday())
        week_str = week_start_tmp.strftime("%Y-%m-%d")
        week_tmp = self.date_ms(str(week_str))
        print(week_str)
        return week_tmp
    # 本周最后一天  23点59分59秒
    def this_week_end(self):
        week_end_tmp= self.now + timedelta(days=7 - self.now.weekday())
        week_str = week_end_tmp.strftime("%Y-%m-%d")
        week_tmp = self.date_ms(str(week_str))
        print(week_str)
        week_tmp -= 1000
        return week_tmp
    # 本月第一天
    def this_month_start(self):
        month_start_tmp =datetime.datetime(self.now.year, self.now.month, 1)
        month_str = month_start_tmp.strftime("%Y-%m-%d")
        month_tmp = self.date_ms(str(month_str))
        print(month_str)
        return month_tmp
    #本月最后一天
    def this_month_end(self):
        if self.now.month == 12 :
            month_end_tmp = datetime.datetime(self.now.year+1,1, 1)
        else:
            month_end_tmp = datetime.datetime(self.now.year,self.now.month + 1, 1)
        month_str = month_end_tmp.strftime("%Y-%m-%d")
        month_tmp = self.date_ms(str(month_str))
        month_tmp-=1000
        print(month_str,month_tmp)
        return month_tmp
    # 本季度第一天
    def this_quarter_start(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        season_start_tmp = datetime.datetime(self.now.year, month, 1)
        season_str = season_start_tmp.strftime("%Y-%m-%d")
        season_tmp = self.date_ms(str(season_str))
        print(season_str)
        return season_tmp
    # 本季度最后一天
    def this_quarter_end(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        if month == 10:
            season_end_tmp = datetime.datetime(self.now.year+1, 1, 1)
        else:
            season_end_tmp = datetime.datetime(self.now.year, month + 3, 1)
        season_str = season_end_tmp.strftime("%Y-%m-%d")
        season_tmp = self.date_ms(str(season_str))
        season_tmp -= 1000
        print(season_str,season_tmp)
        return season_tmp


    # 下月第一天
    def next_month_start(self):
        t = Time()
        month_str = t.next_month_start()
        month_tmp = self.date_ms(str(month_str).split()[0])
        return month_tmp

    #下月最后一天
    def next_month_end(self):
        t = Time()
        month_str = t.next_month_end()
        month_tmp = self.date_ms(str(month_str).split()[0])
        return month_tmp




    def get_timestamp(self,days):
        # 获取前days天数的时间戳
        try:
            date = datetime.date.today() + datetime.timedelta(days)
            time_tmp = self.date_ms(str(date))
        except:
            time_tmp=""
        return time_tmp

    def get_opportunity(self):
        if self.type =="week":
            today_tmp = self.this_week_start()
            future_tmp = self.this_week_end()
        elif self.type =="month":
            today_tmp = self.this_month_start()
            future_tmp = self.this_month_end()
        elif self.type =="season":
            today_tmp = self.this_quarter_start()
            future_tmp = self.this_quarter_end()
        elif self.type =="dm":
            today_tmp = self.this_month_start()
            future_tmp = self.next_month_end()
        else:
            return "参数有误"
        # 129数据库order
        opp_sql = """ select id,crm_id,owner_id,`name`,product_id,amount,opportunity_id,price_unit,created_at,created_by,updated_at,updated_by,close_date from `%s` 
        where close_date >= "%s" and close_date <= "%s" """%(self.opportunity_detail_table,today_tmp,future_tmp)
        opp_df = pd.read_sql_query(opp_sql, self.new_data)
        opp_df["type"] = self.type
        opp_df["date"] = self.today_tmp
        print(opp_df)
        self.inster_sql(opp_df)

    def get_conn(self):
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

        return cur,conn

    def inster_sql(self,df):
        df = df[self.columns_order]
        df.to_sql("opportunity_detail_record", self.new_data, index=False, if_exists="append")
        cur,conn = self.get_conn()
        sql_remarks = """ALTER table `opportunity_detail_record`
                          MODIFY `type` varchar(10) COMMENT 'week  周记录\r\nmonth 月记录\r\nseason  季度记录  dm 双月',
                          MODIFY `date` varchar(50) COMMENT '记录时间',
                          MODIFY `id` varchar(50) COMMENT '商机明细id',
                          MODIFY `crm_id` varchar(50) COMMENT '商机明细crm_id',
                          MODIFY `owner_id` varchar(50) COMMENT '商机明细所属人',
                          MODIFY `name` varchar(100) COMMENT '商机明细编号',
                          MODIFY `product_id` varchar(50) COMMENT '产品id',
                          MODIFY `amount` varchar(50) COMMENT '数量',
                          MODIFY `opportunity_id` varchar(100) COMMENT '商机id',
                          MODIFY `price_unit` varchar(50) COMMENT '单价',
                          MODIFY `created_at` varchar(50) COMMENT '商机明细创建时间',
                          MODIFY `created_by` varchar(50) COMMENT '商机明细创建人',
                          MODIFY `updated_at` varchar(50) COMMENT '商机明细修改时间',
                          MODIFY `updated_by` varchar(50) COMMENT '商机明细修改人',
                          MODIFY `close_date` varchar(50) COMMENT '结单日期'  """

        cur.execute(sql_remarks)

        cur.close()
        conn.close()




    def close_connent(self):
        self.new_data.close()




if __name__ == "__main__":
    type = sys.argv[1]
    print('type',type)
    # 新曾周维度记录
    # o = Opportunity_Record("week")
    # 新增月度维度记录
    o = Opportunity_Record(type)
    # 新增季度维度记录
    # o = Opportunity_Record("season")
    o.get_opportunity()
