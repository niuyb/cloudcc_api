#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/28 17:05
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



import hashlib

import numpy as np
import pymysql

import time
from datetime import datetime
import pandas as pd

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)


"""
order_id 生成规则

年份取后两位

"ZO" + md5('order_name + timestamp')+ index

"""


class Order_Data():
    def __init__(self):

        self.id_per ="ZO"
        self.conn33 = engine(settings.dbinfo33)
        # self.db_xgyypt = engine(GlobalVar.db_xgyypt)
        self.new_data = engine(settings.db_new_data)
        self.order_deal={
            "salerA":"None",
            "salerB": "None",
            "salerC": "None",
            "salerA_amount": "None",
            "salerB_amount": "None",
            "salerC_amount": "None",
            "contractid": "None",
            "contract_back_date": "None",
            "approve_date": "None",
            "payback_type": "None,nan",
            "amount":"nan",
            "discount_amount": "nan",
            "contract_status": "nan",
            "total_performance": "nan",
            "updated_by":"nan",
            "created_by":"nan",
            "ownerid": "nan",
            "account_id": "nan",
            "opportunity_id": "nan",
            "contract_end":"nan",
        }
        self.columns_order = ["id","crm_id","po","entity_type","ownerid","status","account_id","priceid","opportunity_id","created_by","created_at","updated_by","updated_at","amount","discount_amount","contract_status","contract_attribute","contractid","contract_start","contract_end","contract_back_date","total_performance","salerA","salerB","salerC","salerA_amount","salerB_amount","salerC_amount","approve_date","payback_type"]
        self.ignore_key_list=["id","crm_id"]

    def time_ms(self,date):
        try:
            if date:
                datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
                obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
                obj_stamp = str(obj_stamp)
            else:
                obj_stamp = ""
            return obj_stamp
        except:
            # print(date,type(date))
            return ""

    def ms_date(self,ms_time):
        ms_time = int(ms_time)
        time_local = time.localtime(ms_time / 1000)
        date = time.strftime("%Y%m%d", time_local)
        return date[2:]

    def create_id(self,item_name,create_timestamp,index):
        md5_str = hashlib.md5(item_name.encode(encoding='UTF-8')+create_timestamp.encode(encoding='UTF-8')).hexdigest()[8:-8]
        md5_str = md5_str + index
        md5_str = self.id_per+md5_str
        return md5_str

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

    def deal_df(self,order_df,key,type):
        if type.find(",") >0:
            type_list = type.split(",")
            for type in type_list:
                order_df.loc[order_df[key] == type, key] = ""
        else:
            pass
            order_df.loc[order_df[key] == type, key] = ""
        return order_df

    # "opp_id", "opportunityid", "opp_id","crm_opp_id"
    def merge_df(self,main_df,right_df,user_key,user_crm_key,key,crm_key):
        right_df = right_df.rename(columns={user_key: key,user_crm_key:crm_key})
        main_df = pd.merge(main_df, right_df, how='left', on=crm_key)
        main_df = main_df.drop([crm_key], axis=1)
        return main_df

    def get_crm_data(self):
        # 33数据库order
        order_sql = """  select id as crm_id,po,entityType as entity_type,ownerId as crm_ownerid,poStatus as status,accountId as crm_account_id,
          priceId as priceid,opportunityId as crm_opp_id,createdAt as created_at,createdBy as crm_created_by,updatedAt as updated_at,updatedBy as crm_updated_by,
          amount as amount,totalDiscountAmount as discount_amount,dbcSelect3 as contract_status,dbcVarchar1 as contractid,dbcDate5 as contract_start,dbcDate7 as contract_end,
          dbcDate6 as contract_back_date,dbcReal2 as total_performance,dbcRelation3 as salerA,dbcRelation4 as salerB,dbcRelation5 as salerC,dbcReal1 as salerA_amount,
            dbcReal4 as salerB_amount,dbcReal5 as salerC_amount,dbcDate8 as approve_date,dbcSelect17 as payback_type,dbcSelect4 as contract_attribute from `order` """
        order_df = pd.read_sql_query(order_sql, self.conn33)
        order_df["id"]=""
        # opporunity_id 特殊处理
        order_df["crm_opp_id"] = order_df["crm_opp_id"].replace(np.nan, 0)
        order_df["crm_opp_id"] = order_df["crm_opp_id"].astype(int)
        order_df = order_df.astype(str)
        order_df['type_33'] = "1"
        print("33数据库中order有",order_df.shape)
        # 129数据库order
        new_order_sql = """ select * from `order` """
        new_order_df = pd.read_sql_query(new_order_sql, self.new_data)
        new_order_df = new_order_df.astype(str)
        new_order_df['type_129'] = "1"
        print("129数据库中order有",new_order_df.shape)

        user_sql ="""  select istar_id as ownerid,owner_id as crm_ownerid from `user`  """
        user_df = pd.read_sql_query(user_sql, self.new_data)
        user_df = user_df.astype(str)

        account_sql ="""  select id as account_id,crm_id as crm_account_id from `account`  """
        account_df = pd.read_sql_query(account_sql, self.new_data)
        account_df = account_df.astype(str)

        opp_sql ="""  select id as opportunity_id,crm_id as crm_opp_id from `opportunity` """
        opp_df = pd.read_sql_query(opp_sql, self.new_data)
        opp_df = opp_df.astype(str)
        # print(opp_df)

        # ownerid  crmid -> istar_id
        order_df = self.merge_df(order_df, user_df, "ownerid", "crm_ownerid", "ownerid", "crm_ownerid")
        # account_id  crmid -> istar_id
        order_df = self.merge_df(order_df, account_df, "account_id", "crm_account_id", "account_id","crm_account_id")
        # # created_by  crmid -> istar_id
        order_df = self.merge_df(order_df, user_df, "ownerid", "crm_ownerid", "created_by","crm_created_by")
        # # update_by  crmid -> istar_id
        order_df = self.merge_df(order_df, user_df, "ownerid", "crm_ownerid", "updated_by","crm_updated_by")
        # # # opportunityid  crmid -> istar_id
        order_df = self.merge_df(order_df, opp_df, "opportunity_id", "crm_opp_id", "opportunity_id","crm_opp_id")
        # order_df["id"]=""
        for row in order_df.itertuples():
            index = getattr(row, 'Index')

            # recent_activity_time = getattr(row, 'recent_activity_time')
            created_at = getattr(row, 'created_at')
            updated_at = getattr(row, 'updated_at')
            contract_start = getattr(row, 'contract_start')
            contract_back_date = getattr(row, 'contract_back_date')
            approve_date = getattr(row, 'approve_date')
            # crm_id = getattr(row, 'crm_id')
            # account_df.set_value(index, 'id', self.create_id(account_name,created_at_timestamp))
            order_df.at[index, 'created_at'] = self.time_ms(created_at)
            order_df.at[index, 'updated_at'] = self.time_ms(updated_at)
            order_df.at[index, 'contract_start']= self.time_ms(contract_start)
            order_df.at[index,"contract_back_date"] = self.time_ms(contract_back_date)
            order_df.at[index,"approve_date"] = self.time_ms(approve_date)

        # 取差集获取新增
        order_add_df = order_df.append(new_order_df,sort=False)
        order_add_df = order_add_df.drop_duplicates(subset=['crm_id'], keep=False)
        # 生成id 处理时间
        order_add_df["id"]=""
        for row in order_add_df.itertuples():
            index = getattr(row, 'Index')
            crm_id = getattr(row, 'crm_id')
            order_add_df.at[index, 'id'] = self.create_id(crm_id)
        print("新增数据",order_add_df.shape)
        # 查找是否存在33库表中已删除的id
        deleted_list = order_add_df.loc[order_add_df["type_129"] == "1","crm_id"].tolist()
        # 删除id
        for deleted_id in deleted_list:
            new_order_df = new_order_df.drop(new_order_df[new_order_df['crm_id'] == deleted_id].index)
            order_add_df = order_add_df.drop(order_add_df[order_add_df['crm_id'] == deleted_id].index)
        # 合并新增数据
        # 这里记录修改记录
        new_order_df = new_order_df.append(order_add_df,sort=False)
        # 查找修改的信息index
        new_order_df.sort_values("crm_id", inplace=True,ascending=True,axis=0)
        # new_order_df  重置index
        new_order_df = new_order_df.reset_index(drop=True)
        new_order_df = new_order_df[self.columns_order]
        # order_df  重置index
        order_df.sort_values("crm_id", inplace=True,ascending=True,axis=0)
        order_df = order_df.reset_index(drop=True)
        order_df = order_df[self.columns_order]
        new_order_df = new_order_df.astype(str)
        order_df = order_df.astype(str)
        # 处理空值
        for key,type in self.order_deal.items():
            order_df = self.deal_df(order_df,key,type)
        # 处理空值
        for key,type in self.order_deal.items():
            new_order_df = self.deal_df(new_order_df,key,type)
        #找出修改行列
        print(order_df.shape)
        print(new_order_df.shape)
        order_modify_df = order_df==new_order_df
        # print(order_modify_df)
        # 修改行列
        for key in self.columns_order:
            print(key)
            if key in self.ignore_key_list:
                continue
            modify_list = list(order_modify_df.loc[order_modify_df[key] == False].index)
            col_index = int(self.columns_order.index(key))
            print(modify_list)
            if modify_list:
                for modify_index in modify_list:
                    modify_index = int(modify_index)
                    # 这里记录修改记录
                    print("修改",new_order_df.iloc[modify_index, col_index],order_df.iloc[modify_index, col_index])
                    new_order_df.iloc[modify_index, col_index] = order_df.iloc[modify_index, col_index]
            else:
                continue

        # print(new_order_df)
        return  new_order_df

    def inster_sql(self,df):
        df = df[self.columns_order]
        df.to_sql("order", self.new_data, index=False, if_exists="replace")
        cur,conn = self.get_conn()

        sql_remarks = """ALTER table `order` ADD PRIMARY KEY (id),
                         MODIFY `id` varchar(50) COMMENT '星光自建订单id',
                         MODIFY `crm_id` varchar(50) COMMENT 'crm 订单id',
                         MODIFY `po` varchar(50) COMMENT '流水号',
                         MODIFY `entity_type` varchar(20) COMMENT '订单类型',
                         MODIFY `ownerid` varchar(50) COMMENT '销售负责人 对应星光salerid',
                         MODIFY `status` varchar(20) COMMENT '订单状态',
                         MODIFY `account_id` varchar(50) COMMENT '最终客户id 对应account 星光id',
                         MODIFY `priceid` varchar(50) COMMENT '价格表名称',
                         MODIFY `opportunity_id` varchar(100) COMMENT '商机id',
                         MODIFY `created_by` varchar(50) COMMENT '创建人',
                         MODIFY `created_at` varchar(50) COMMENT '创建日期',
                         MODIFY `updated_by` varchar(50) COMMENT '最新修改人',
                         MODIFY `updated_at` varchar(50) COMMENT '最新修改日期',
                         MODIFY `amount` varchar(50) COMMENT '订单总金额',
                         MODIFY `discount_amount` varchar(50) COMMENT '总折扣额',
                         MODIFY `contract_status` varchar(20) COMMENT '合同状态',
                         MODIFY `contract_attribute` varchar(10) COMMENT '合同属性 1新签 2续签',
                         MODIFY `contractid` varchar(50) COMMENT '合同编号',
                         MODIFY `contract_start` varchar(50) COMMENT '合同开始日期',
                         MODIFY `contract_end` varchar(50) COMMENT '最终合同截止日期',
                         MODIFY `contract_back_date` varchar(50) COMMENT '合同归档日期',
                         MODIFY `total_performance` varchar(50) COMMENT '业绩核算(成本）总额',
                         MODIFY `salerA` varchar(20) COMMENT '销售A',
                         MODIFY `salerB` varchar(20) COMMENT '销售B',
                         MODIFY `salerC` varchar(20) COMMENT '销售C',
                         MODIFY `salerA_amount` varchar(50) COMMENT '销售A拆分金额',
                         MODIFY `salerB_amount` varchar(50) COMMENT '销售B拆分金额',
                         MODIFY `salerC_amount` varchar(50) COMMENT '销售C拆分金额',
                         MODIFY `approve_date` varchar(50) COMMENT '审批通过时间',
                         MODIFY `payback_type` varchar(20) COMMENT '回款计划类型' """
        cur.execute(sql_remarks)

        cur.close()
        conn.close()

    def close_connent(self):
        self.conn33.close()
        self.new_data.close()


    def get_cloudcc_order(self):
        try:
            access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            print("获取binding失败,请检查配置")
            return False
        try:
            sql_string = """ select {} from {} limit 7000 """
            # sql = sql_string.format("*", "dingdan")
            sql = sql_string.format("*", "Account")
            # data = cloudcc_query_sql(access_url, "cqlQuery", "dingdan", sql, binding)

            # sql = """  select count(*) from Account """

            data = cloudcc_query_sql(access_url, "cqlQuery", "Account", sql, binding)

            print(data)
            order_df = pd.DataFrame(data)
        except:
            print("获取cloudcc数据失败")
            return False


        print(len(data))
        print("----------------")
        print(order_df)








if __name__ == "__main__":

    o = Order_Data()


    # df = o.get_crm_data()
    # # print(order_df)
    # o.inster_sql(df)
    # o.close_connent()

    o.get_cloudcc_order()












