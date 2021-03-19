#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/3/10 13:30
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
import hashlib
import json
import pandas as pd
import pymysql
import requests

from public.cloudcc_utils import cloudcc_get_request_url, cloudcc_get_binding, append_by_api
from public.utils import engine
from script.data_config import ACTIVITY_SQL_TABLE
from settings import settings
from settings.config import ACCESS_URL, ClOUDCC_USERNAME, ClOUDCC_PASSWORD
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列


"""
https://ai.istarshine.com/apiv2/bid/list?date=2021-03-02&appKey=U61fBGDOkn9EXDSrKvuP&sign=f8923e6d82c005ba5d6a657dbf0232f2&timestamp=1614759489000
"""


"""
# 投标开始日期
"start_date": "",
# 附件下载
"download": "",
# 原文链接
"detail_url": "",
#ai_media_id
"uuid":"",

"""


class Append_Hidden_Account():

    def __init__(self):
        # 数据来源接口 配置
        self.appkey = "U61fBGDOkn9EXDSrKvuP"
        self.appsecret = "GX4bHAqqulLZP4wSrbaZLZNvcphG8qld"
        self.ai_url = "https://ai.istarshine.com/apiv2/bid/list?date={}&appKey={}&sign={}&timestamp={}&pageNo={}&pageSize={}"

        # 时间戳
        self.temp = datetime.datetime.now().timestamp()
        self.time_stamp = int(round(self.temp * 1000))
        print(self.time_stamp)
        self.date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        # self.date ="2021-03-18"
        print(self.date)
        self.page_num = 50
        # ai_media
        self.sql_table = "ai_media"

        self.media_dict={
            # 唯一id
            "uuid":"uuid",
            "title":"biaoti",
            "province": "fState",
            "region": "fCity",
            "sub_region": "fDistrict",
            "project_name": "xiangmumc",
            # 项目分类
            "purchase_type": "xiangmufenlei",
            # 发布时间
            "bid_pub_date": "fabushijian",
            "industry": "hangye",
            # 招标单位
            "purchase_agent": "zhaobiaodanwei",
            # 招标单位联系人
            "contact_person": "name",
            # 招标单位联系电话
            "contact_mobile_number": "zhaobiaodwlxdh",
            # 代理机构
            "tender_agent": "dailijigou",
            # 代理机构联系人
            "tender_agent_contact_person": "dljglxr",
            # 代理机构联系电话
            "tender_agent_contact_mobile_number": "dljglianxdh",
            #项目编号
            "project_number": "xnbh",
            # 项目内容
            "purchase_content": "xmnr",
            # 投标开始时间
            "bid_start_date": "ztbkaishisj",
            # 投标截止时间
            "bid_end_date": "zhaotoubiaojzsj",
            # 开标日期
            "bid_open_date": "kaibiaoriq",
            # 资金来源
            "sources_of_funds": "zjly",
            # 投资额
            "investment": "tze",
            # 招标预算
            "tender_price": "zbys",
            #中标金额
            "bid_price": "zbje",
            # 中标单位
            "bid_winner": "zbdw",
            # 中标联合单位
            "bid_union": "zblhdw",
            # 参与投标厂商
            "bid_participant": "cytbcs",
            # 采集时间
            "indate": "caijisj",
            # 评标办法
            "bid_evaluation_method": "pbbf",
            # 网站名称
            "source": "wzmc",
            # 原文链接
            "detail_url": "detailurl",
            # 网站域名
            "source_domain": "wzym",
            # 页面内容
            "content": "ymnr",
            # 附件下载
            "download": "download",
            # 开标日期
            "open_date": "kaibiaoriq",
            # 投标开始日期
            "start_date": "startdate",
        }



        self.HIDDEN_ACCOUNT_API_NAME="Lead"
        self.CLOUDCC_API_ACTION = "insert"



    def get_sign(self):
        try:
            md5_str = hashlib.md5(str(self.appkey).encode(encoding='UTF-8') + str(self.appsecret).encode(encoding='UTF-8') + str(self.time_stamp).encode(encoding='UTF-8')).hexdigest()
            # print(md5_str)
        except:
            return ""
        return md5_str


    def enter_control(self):

        total,data = self.get_hidden(1)
        print("total",total)
        self.insert_cc(data)
        for page in range(1,int(total/self.page_num)+1):
            page+=1
            _,temp_data = self.get_hidden(page)
            self.insert_cc(temp_data)

    def get_hidden(self,start):
        session = requests.session()
        session.keep_alive = False
        sign = self.get_sign()
        hidden_access_url = self.ai_url.format(self.date,self.appkey,sign,self.time_stamp,start,self.page_num)
        try:
            # print(hidden_access_url)
            response = json.loads(session.get(hidden_access_url).text)
            # print(response)
            if int(response['header']["status"]) == 200:
                return response["body"]["total"],response["body"]["list"]
            else:
                return 0,False
        except :
            return 0,False


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

    def insert_cc(self,data_list):

        new_data = engine(settings.db_new_data)

        # total,data_list = self.get_hidden(page)
        # print("total",total)
        ai_df =pd.DataFrame(data_list)
        # try:
        ai_df.to_sql(self.sql_table, new_data, index=False, if_exists="append")
        # except Exception as e:
        #     print(e)
        #     return

        access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
        binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)

        if data_list:
            cc_df = ai_df.rename(columns=self.media_dict)
            ai_df["crm_id"]=""
            cc_dict_list = cc_df.to_dict("records")

            for data in cc_dict_list:
                uuid = data["uuid"]
                # 重载data
                data = [data]
                # crm_id="123123"
                crm_id = append_by_api(access_url,self.CLOUDCC_API_ACTION,self.HIDDEN_ACCOUNT_API_NAME,data,binding)
                cur, conn = self.get_conn()
                if crm_id:
                    try:
                        update_sql = """update {} set in_cloudcc="{}" where uuid="{}" """.format(self.sql_table,crm_id,uuid)
                        # 更新状态
                        cur.execute(update_sql)
                        conn.commit()
                    except Exception as e:
                        print(e)
                        pass
                else:
                    try:
                        update_sql = """update {} set in_cloudcc="false" where uuid="{}" """.format(self.sql_table,uuid)
                        # 更新状态
                        cur.execute(update_sql)
                        conn.commit()
                    except Exception as e:
                        print(e)
                        pass
                cur.close()
                conn.close()

            # print(ai_df)

        else:
            # 获取信息有误
            return False
        new_data.close()



"""
crm_id


00420217BBD89F5EpxRO

004202184764D00jhouO

"""




if __name__ == "__main__":

    aha = Append_Hidden_Account()

    aha.enter_control()
