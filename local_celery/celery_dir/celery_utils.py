#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 18:02
# 工具：PyCharm
# Python版本：3.7.0
from datetime import datetime

from public.utils import get_conn, date_ms, time_ms, engine, list_to_sql_string, timer
from script.data_config import ACCOUNT_SQL_TABLE
from script.data_utils import create_id
from settings import settings
from settings.config import ACCOUNT_MAPPING
from settings.settings import db_new_data
import pandas as pd

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

# def create_id(name,timestamp,index):
#     if not name:
#         name = ""
#     md5_str = hashlib.md5(
#         name.encode(encoding='UTF-8') + str(timestamp).encode(encoding='UTF-8') + str(index).encode(
#             encoding='UTF-8')).hexdigest()[8:-8]
#     return md5_str

def celery_account_create_id(pd_engine,data):
    data=[{'leixing': '直销客户', 'parent': None, 'recentactivityrecordtime': None, 'customitem195': None, 'customitem194': None,'createdate': '2019-10-31 11:10:00', 'customItem146': '潜在客户', 'createbyid': '0052020BA0ED310Njzu4', 'highseastatus': '已签约', 'fkdwkhyh': None,'twitter': None, 'lastcontactdate': None, 'zys': None, 'doNotDisturb': 'false', 'isLocked': None, 'customItem148': '自动注册', 'lockstatus': '未锁定','fcity': '北京市', 'id': '001202060A951FAKtUyz', 'fax': None, 'fState': '北京市', 'releasereason': None, 'customItem156': '企业事业部','customItem157': '运营支撑部','ownerid': '0052020BA0ED310Njzu4', 'txdz': None, 'customItem151': '企业', 'customItem159': '武迎春', 'highseaaccountsource':None, 'beizhu': None,'jingweidula': '39.972134', 'cloudcctag': None, 'fDistrict': '海淀区', 'jingweiduco': '116.329519', 'nsr': None, 'fCity':'北京市', 'srcflg': None, 'ces': None, 'khbh': 'CC2020123019060', 'bjdmx': None, 'weibo': None, 'isDeleted': '0', 'yid': '\t945793194705289', 'gsgpdm':None, 'currency': 'CNY', 'lastmodifybyid': '0052017BE8702F1PIi4j', 'CCObjectAPI': 'Account', 'customitem146': '潜在客户', 'facebook': None,'lqtime': '2020-04-02 00:00:00', 'qyyx': None, 'fstate': '北京市', 'gsownerid': '0052020AFAB6D07OWA6m', 'dimDepart': '企业产品中心', 'lbsaddress': None,'customitem148': '自动注册', 'customitem147': None, 'khxxdz02': None, 'customitem155': None, 'show_on_map': None, 'khxxdz01': None, 'is_locked':None, 'khxxdz04': None, 'customitem157': '运营支撑部', 'recentactivitycreatedby': None, 'khxxdz03': None, 'customitem156': '企业事业部', 'bzhyfldm':None, 'customitem151': '企业', 'khxxdz00': None, 'fdistrict': '海淀区', 'khxxdz05': None, 'fkdwdz': None, 'releasetime': None, 'returntimes': None,'customitem159': '武迎春', 'kddz': None, 'customitem158': None, 'lastmodifydate': '2021-01-17 13:02:43', 'customitem166': None, 'customitem165':None, 'customitem168': None, 'customitem167': None, 'customitem162': '其他', 'customitem161': '高级客户经理', 'customitem164': '否','customitem163': None, 'showOnMap': None, 'postcode': None, 'customitem160': '\t13699182773', 'ispartner': None, 'lrr': None, 'khdd': None, 'weixin': None,'name': '北京智慧星光运营支撑部', 'fkdwdh': None, 'customitem169': None, 'customitem210': None, 'customitem177': '运营支撑试用账号', 'customItem160':'\t13699182773', 'fenji': '正式客户', 'customitem212': None, 'customitem179': 'ACC201910310026', 'customitem178': 'https://support.istarshine.comCustomerPortrait/index?accountId=OTQ1NzkzMTk0NzA1Mjg5', 'customitem211': None, 'employeenumber': None, 'customitem174': '否', 'fkdwyhzh': None,'customitem171': None, 'linkedin': None, 'customitem170': None, 'customItem164': '否', 'customItem161': '高级客户经理', 'customItem162': '其他','wangzhi': None, 'is_deleted': '0', 'lockStatus': '未锁定', 'recordtype': '2019593FC86B601GFelY', 'customitem214': None, 'zwyhxwfx':'https://support.istarshine.com/CustomerPortrait/index?accountId=OTQ1NzkzMTk0NzA1Mjg5', 'customitem213': None, 'customitem216': None, 'releasedefinition': None,'dianhua': None, 'customitem184': None, 'customitem183': None, 'customitem186': None, 'customitem185': None, 'customItem178':'https://support.istarshine.com/CustomerPortrait/index?accountId=OTQ1NzkzMTk0NzA1Mjg5', 'customItem179': 'ACC201910310026', 'jingweidu': '39.972134,116.329519', 'dls': None,'customItem177': '运营支撑试用账号', 'customItem174': '否', 'tyshxydm': None, 'donotdisturb': 'false', 'isCustomer': '\t1', 'xsdt': None, 'zwzhmc':'运营支撑试用账号', 'iscustomer': '\t1', 'fhdz': None, 'highSeaStatus': '已签约', 'dimdepart': '企业产品中心', 'khxxdz': '', 'hangye': None,'sflzqzkh': None}]
    id_dict={}

    today = str(datetime.now().strftime('%Y-%m-%d'))
    today_stamp = date_ms(today)

    index_sql = """ select count(*) as nums from %s where created_at >= "%s" """ % (ACCOUNT_SQL_TABLE, today_stamp)
    id_index = pd.read_sql_query(index_sql, pd_engine)["nums"].tolist()[0]

    local_crm_list= []
    for data_dict in data:
        local_crm_list.append(data_dict.get("id",""))
    local_str = list_to_sql_string(local_crm_list)
    # 替换id
    id_sql = """ select crm_id,id from {} where crm_id in ({}) """.format(ACCOUNT_SQL_TABLE, local_str)
    id_list = pd.read_sql_query(id_sql, pd_engine).to_dict("records")
    local_id_dict = {}
    if id_list:
        for dict in id_list:
            local_id_dict[dict["crm_id"]] = dict["id"]

    for data_dict in data:
        new_id = local_id_dict.get(data_dict.get("id"))
        if new_id:
            pass
        else:
            account_name = data_dict.get(ACCOUNT_MAPPING.get("name"),"")
            created_at = data_dict.get(ACCOUNT_MAPPING.get("created_at"),"")
            created_stamp = time_ms(created_at)
            crm_id = data_dict.get("id","")
            new_id  = create_id(account_name,created_stamp,id_index)
            print(new_id)
            id_dict[crm_id] = new_id

    id_dict.update(local_id_dict)


    return id_dict



if __name__ == "__main__":
    pd_engine = engine(settings.db_new_data)

    id_dict = celery_account_create_id(pd_engine,"")

    print(id_dict)
    pd_engine.close()

