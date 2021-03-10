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

path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

from public.Time import Time

import pymysql
from datetime import timedelta

import pandas as pd

from public.utils import engine, list_to_sql_string
from script.data_config import OPPORTUNITY_SQL_TABLE
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
        self.opportunity_record_table = "opportunity_record_copy1"
        self.opportunity_table = OPPORTUNITY_SQL_TABLE

        # self.now = datetime.date.today() + datetime.timedelta(-100)
        self.type = type
        # self.time_dict={
        #     "week":7,
        #     "month":30,
        #     "season":90,
        # }
        self.columns_order=["id","type","date","opportunity_name","intended_product","money","sale_stage","win_rate","saler_promise","close_date","owner_id","next_saler_promise","next_sale_stage"]

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
        return week_tmp
    # 本周最后一天   23点59分59秒
    def this_week_end(self):
        week_end_tmp= self.now + timedelta(days=7 - self.now.weekday())
        week_str = week_end_tmp.strftime("%Y-%m-%d")
        week_tmp = self.date_ms(str(week_str))
        week_tmp -= 1000
        return week_tmp
    # 本月第一天
    def this_month_start(self):
        month_start_tmp =datetime.datetime(self.now.year, self.now.month, 1)
        month_str = month_start_tmp.strftime("%Y-%m-%d")
        month_tmp = self.date_ms(str(month_str))
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
        return month_tmp
    # 本季度第一天
    def this_quarter_start(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        season_start_tmp = datetime.datetime(self.now.year, month, 1)
        season_str = season_start_tmp.strftime("%Y-%m-%d")
        season_tmp = self.date_ms(str(season_str))
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
        month_tmp += 86400000
        return month_tmp

    # 上周第一天
    def last_week_start(self):
        last_week_start = self.now - timedelta(days=self.now.weekday() + 7)
        last_week_start = str(last_week_start).split()[0]
        last_week_tmp = self.date_ms(last_week_start)
        return last_week_tmp
    # 上月最后一天
    def last_month_end(self):
        last_month_end = datetime.datetime(self.now.year, self.now.month, 1)
        last_month_end =  last_month_end - timedelta(days=1)
        last_month_end = str(last_month_end).split()[0]
        last_month_tmp = self.date_ms(last_month_end)
        return last_month_tmp
    # 上个月第一天
    def last_month_start(self):
        last_month_end = datetime.datetime(self.now.year, self.now.month, 1)
        last_month_end =  last_month_end - timedelta(days=1)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        last_month_start = str(last_month_start).split()[0]
        last_month_tmp = self.date_ms(last_month_start)
        return last_month_tmp

    # 上个双月第一天
    def last_dm_start(self):
        last_month_end = datetime.datetime(self.now.year, self.now.month, 1)
        last_month_end =  last_month_end - timedelta(days=1)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        last_month_start =  last_month_start - timedelta(days=1)
        last_month_start = datetime.datetime(last_month_start.year, last_month_start.month, 1)
        last_month_start = str(last_month_start).split()[0]
        last_month_tmp = self.date_ms(last_month_start)
        # last_month_tmp += 86400000
        return last_month_tmp



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
            last_tmp = self.last_week_start()
        elif self.type =="month":
            last_tmp = self.last_month_start()
            # last_tmp = self.this_month_start()
        elif self.type =="dm":
            last_tmp = self.last_dm_start()
        else:
            return "参数有误"
        # 129数据库order
        record_sql = """ select * from `%s` where `date` = "%s" and `type` = "%s" """%(self.opportunity_record_table,last_tmp,self.type)
        record_df = pd.read_sql_query(record_sql, self.new_data)
        opp_sql = """ select id,sale_stage as next_sale_stage,saler_promise as next_saler_promise from `%s` """%(self.opportunity_table)
        opp_df = pd.read_sql_query(opp_sql, self.new_data)
        record_df = record_df.drop(["next_saler_promise","next_sale_stage"], axis=1)
        record_df = pd.merge(record_df, opp_df, how='left', on="id")

        # print(record_df)
        self.inster_sql(record_df)

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

        cur, conn = self.get_conn()
        delete_id_list = df["id"]
        delete_nums = len(delete_id_list)
        deleted_times = int(delete_nums / 1000) + 1
        for i in range(1, deleted_times + 1):
            # delete_str = ",".join(delete_id_list[(i - 1) * 1000:i * 1000])
            delete_str = list_to_sql_string(delete_id_list[(i - 1) * 1000:i * 1000])
            delete_sql = """ delete from {} WHERE id in ({}) """.format(self.opportunity_record_table, delete_str)
            cur.execute(delete_sql)
            conn.commit()
        df = df[self.columns_order]
        df.to_sql(self.opportunity_record_table, self.new_data, index=False, if_exists="append")
        sql_remarks = """ALTER table `{}` 
                          MODIFY `type` varchar(10) COMMENT 'week  周记录\r\nmonth 月记录\r\nseason  季度记录  dm 双月',
                          MODIFY `date` varchar(50) COMMENT '记录时间',
                          MODIFY `id` varchar(50) COMMENT '商机id',
                          MODIFY `opportunity_name` varchar(500) COMMENT '商机名称',
                          MODIFY `intended_product` varchar(500) COMMENT '意向产品',
                          MODIFY `money` varchar(255) COMMENT '商机金额',
                          MODIFY `sale_stage` varchar(50) COMMENT '销售阶段',
                          MODIFY `win_rate` varchar(50) COMMENT '赢率',
                          MODIFY `saler_promise` varchar(50) COMMENT '销售承诺',
                          MODIFY `next_saler_promise` varchar(50) COMMENT '下个维度销售承诺',
                          MODIFY `next_sale_stage` varchar(50) COMMENT '下个维度销售阶段',
                          MODIFY `close_date` varchar(50) COMMENT '结单日期',
                          MODIFY `owner_id` varchar(50) COMMENT '销售id'  """.format(self.opportunity_record_table)
        cur.execute(sql_remarks)

        cur.close()
        conn.close()




    def close_connent(self):
        self.new_data.close()




if __name__ == "__main__":

    # type = sys.argv[1]
    type = "week"
    print('type',type)
    #
    # # 新曾周维度记录
    o = Opportunity_Record(type)
    # # 新增月度维度记录
    # # o = Opportunity_Record("month")
    # # 新增季度维度记录
    # # o = Opportunity_Record("season")
    #
    o.get_opportunity()
    o.close_connent()

