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
import datetime
import sys,os
path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

from multiprocessing import Process
import pymysql
import pandas as pd

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, cloudcc_query_sql
from public.utils import engine, list_to_sql_string, time_ms, date_ms
from script.data_config import OPPORTUNITY_SQL_TABLE, OPPORTUNITY_CLOUMNS_ORDER, USER_SQL_TABLE, \
    ACCOUNT_SQL_TABLE, ORDER_API_NAME, ORDER_TABLE_STRING, ORDER_DICT, ORDER_SQL_TABLE, ORDER_CLOUMNS_ORDER, \
    QUOTE_API_NAME, QUOTE_SQL_TABLE, QUOTE_DICT, QUOTE_TABLE_STRING, QUOTE_CLOUMNS_ORDER
from script.data_utils import create_id
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD

pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列




class Order_Data():
    def __init__(self):

        self.access_url  = ''
        self.binding = ''
        self.cloudcc_object=QUOTE_API_NAME
        self.sql_table= QUOTE_SQL_TABLE
        # self.sql_table= "order_back_copy1"
        self.sql_mapping= QUOTE_DICT
        self.sql_table_string = QUOTE_TABLE_STRING
        self.user_table = USER_SQL_TABLE
        self.account_table = ACCOUNT_SQL_TABLE
        self.opportunity_table = OPPORTUNITY_SQL_TABLE

        self.today = (datetime.datetime.now() - datetime.timedelta(hours=1.5)).strftime('%Y-%m-%d')
        # self.today = "2021-03-23"
        self.today_stamp =  date_ms(self.today)
        print(self.today)
        self.one_times_num = 1000
        self.sql_index_list=[]
        self.process_num = 1
        self.columns_order = QUOTE_CLOUMNS_ORDER


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

    def merge_df(self,main_df,right_df,user_key,user_crm_key,key,crm_key):
        right_df = right_df.rename(columns={user_key: key,user_crm_key:crm_key})
        main_df = pd.merge(main_df, right_df, how='left', on=crm_key)
        main_df = main_df.drop([crm_key], axis=1)
        return main_df

    def inster_sql(self, df,local_str):

        new_data = engine(settings.db_new_data)
        cur, conn = self.get_conn()
        try:
            # 删除本次操作的所有local id
            delete_sql = """ delete from {} WHERE crm_id in ({}) """.format(self.sql_table, local_str)
            cur.execute(delete_sql)
            conn.commit()
            # 入库操作
            df = df[self.columns_order]
            df.to_sql(self.sql_table, new_data, index=False, if_exists="append")
            # 修改类型
            sql_remarks = self.sql_table_string.format(self.sql_table)
            cur.execute(sql_remarks)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()
            new_data.close()

    def get_cloudcc_order(self,index):
        if index == 1:
            index = 0
        new_data = engine(settings.db_new_data)
        # try:
        sql_string = """ select {} from {} where left(lastmodifydate,10) = '{}' limit {},{} """
        sql = sql_string.format("*", self.cloudcc_object,self.today,index,self.one_times_num)
        print(sql)
        data = cloudcc_query_sql(self.access_url, "cqlQuery",self.cloudcc_object, sql, self.binding)
        print("查询",len(data))
        if data:

            cc_df = pd.DataFrame(columns=list(self.sql_mapping.keys()))
            cc_df = cc_df.append(data,ignore_index=True,sort=False)
            ccdf_name_list = list(self.sql_mapping.keys()) + ["is_deleted"]
            cc_df = cc_df[ccdf_name_list]
            cc_df = cc_df.rename(columns=self.sql_mapping)

            # 本次操作的cc id
            operate_list = cc_df["crm_id"].tolist()
            operate_str = list_to_sql_string(operate_list)
            local_sql = """ select id,crm_id from `{}` where crm_id in ({})""".format(self.sql_table,operate_str)
            local_df = pd.read_sql_query(local_sql,new_data)
            # 本次操作local数据库id
            local_list = cc_df["crm_id"].tolist()
            local_str = list_to_sql_string(local_list)

            # 删除cc 与 local 中删除的数据
            deleted_list = cc_df.loc[cc_df["is_deleted"] != "0","crm_id"].tolist()
            for deleted_id in deleted_list:
                local_df = local_df.drop(local_df[local_df['crm_id'] == deleted_id].index)
                cc_df = cc_df.drop(cc_df[cc_df['crm_id'] == deleted_id].index)
            print("已删除",len(deleted_list))
            cc_df = cc_df.drop(["is_deleted"],axis=1)


            # 新增 数据
            local_merge_df = local_df[["id","crm_id"]]
            cc_df = pd.merge(cc_df, local_merge_df, how='left', on="crm_id")
            index_sql = """ select count(*) as nums from %s where created_at >= "%s" """%(self.sql_table,self.today_stamp)
            print("index_sql",index_sql)
            id_index = pd.read_sql_query(index_sql,new_data)["nums"].tolist()[0]
            print("id_index",id_index)
            for row in cc_df.itertuples():
                df_index = getattr(row, 'Index')
                created_at = getattr(row, 'created_at')
                cc_df.at[df_index, 'created_at'] = time_ms(created_at)
                updated_at = getattr(row, 'updated_at')
                cc_df.at[df_index, 'updated_at'] = time_ms(updated_at)
                po = getattr(row, 'name')
                created_at = getattr(row, 'created_at')
                timestamp = time_ms(created_at)
                id = getattr(row, 'id')
                if isinstance(id,str):
                    pass
                else:
                    id = create_id(po, timestamp, id_index)
                    # print(id)
                    cc_df.at[df_index, 'id'] = id
                id_index+=1


            # 在这里替换想相应的id
            # account_id
            cc_account_str = list_to_sql_string(cc_df["account_id"].dropna().tolist())
            local_account_sql = """ select id as local_account_id,crm_id as account_id  from `{}` where crm_id in ({})""".format(self.account_table,cc_account_str)
            local_account_df = pd.read_sql_query(local_account_sql,new_data)
            cc_df = pd.merge(cc_df, local_account_df, how='left', on="account_id")
            cc_df = cc_df.drop(["account_id"],axis=1)
            cc_df = cc_df.rename(columns={"local_account_id":"account_id"})
            # opportunity_id
            cc_opportunity_str = list_to_sql_string(cc_df["opportunity_id"].dropna().tolist())
            local_opp_sql = """ select id as local_opportunity_id,crm_id as opportunity_id  from `{}` where crm_id in ({})""".format(self.opportunity_table,cc_opportunity_str)
            local_opp_df = pd.read_sql_query(local_opp_sql,new_data)
            cc_df = pd.merge(cc_df, local_opp_df, how='left', on="opportunity_id")
            cc_df = cc_df.drop(["opportunity_id"],axis=1)
            cc_df = cc_df.rename(columns={"local_opportunity_id":"opportunity_id"})
            #owner_id
            local_user_sql = """select `id` as local_owner_id ,crm_id as owner_id from {}""".format(self.user_table)
            local_user_df = pd.read_sql_query(local_user_sql,new_data)
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="owner_id")
            cc_df = cc_df.drop(["owner_id"],axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id":"owner_id"})
            # created_by
            local_user_df = local_user_df.rename(columns={"owner_id":"created_by"})
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="created_by")
            cc_df = cc_df.drop(["created_by"],axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id":"created_by"})
            # updated_by
            local_user_df = local_user_df.rename(columns={"created_by":"updated_by"})
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="updated_by")
            cc_df = cc_df.drop(["updated_by"],axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id":"updated_by"})

            cc_df = cc_df.drop_duplicates(["crm_id"], keep="first")
            new_data.close()
            # print(cc_df)
            self.inster_sql(cc_df,local_str)
            print("入库",cc_df.shape)

    def get_infos(self,p_index):
        list_index = p_index
        times = int(len(self.sql_index_list) /self.process_num) +2
        try:
            for i in range(times):
                print(self.sql_index_list[list_index])
                self.get_cloudcc_order(self.sql_index_list[list_index])
                list_index += 1
        except Exception as e:
            print("get_infos------",e)
            pass

    def process_data(self):
        try:
            self.access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
            self.binding = cloudcc_get_binding(self.access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        except:
            print("获取binding失败,请检查配置")
            return False
        try:
            count_sql = """  select count(*) as nums from %s where left(lastmodifydate,10) = '%s' """%(self.cloudcc_object,self.today)
            print(count_sql)
            count_data = cloudcc_query_sql(self.access_url, "cqlQuery", self.cloudcc_object, count_sql, self.binding)
            nums = count_data[0].get("nums",0)
            print(count_data)
        except:
            print("获取总数目失败")
            return False
        if nums % self.one_times_num > 0:
            num_times = int(nums / self.one_times_num) + 1
        elif nums % self.one_times_num == 0:
            num_times = int(nums / self.one_times_num)
        else:
            num_times = 0

        for index in range(num_times):
            start = int(index) * self.one_times_num
            if num_times == 1:
                start = 1
            if index == 0:
                start = 1
            self.sql_index_list.append(start)

        print(self.sql_index_list)
        self.sql_index_list = self.sql_index_list[::-1]

        p_l = []
        for i in range(self.process_num):
            p1 = Process(target=self.get_infos,args=(i,))
            p1.start()
            p_l.append(p1)
        for p in p_l:
            p.join()


if __name__ == "__main__":
    o = Order_Data()

    o.process_data()
    # o.get_cloudcc_order(0)












