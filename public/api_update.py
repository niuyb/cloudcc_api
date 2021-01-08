#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/7 16:41
# 工具：PyCharm
# Python版本：3.7.0
import pymysql

from public.utils import list_to_sql_string, engine, time_ms, date_ms
from script.data_config import ACCOUNT_DICT, ACCOUNT_SQL_TABLE, USER_SQL_TABLE, ACCOUNT_TABLE_STRING, \
    ACCOUNT_CLOUMNS_ORDER
import pandas as pd

from script.data_utils import create_id
from settings import settings
from datetime import datetime
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列



def inster_sql(new_data,sql_table,columns_order,df):
    try:
        # 入库操作
        df = df[columns_order]
        df.to_sql(sql_table, new_data, index=False, if_exists="append")
    except Exception as e:
        print(e)



def account_insert_mysql(data):
    new_data = engine(settings.db_new_data)
    today = str(datetime.now().strftime('%Y-%m-%d'))
    today_stamp = date_ms(today)
    #test
    # data =[{'leixing': '终端客户', 'parent': None, 'recentactivityrecordtime': None, 'customitem195': None, 'customitem194': None,'createdate': '2021-01-07 15:57:22', 'createbyid': '0052020DA39F266VGBTc', 'highseastatus': '自建', 'fkdwkhyh': None, 'twitter': None, 'lastcontactdate': '2021-01-07 16:05:15', 'zys': None, 'doNotDisturb': 'false', 'isLocked': None, 'customItem148': '主动开拓', 'lockstatus': None, 'fcity': '沧州市', 'id': '0012021A7AF8F65wuyLR', 'fax': None, 'fState': '河北省', 'releasereason': None, 'customItem156': '企业事业部', 'customItem157': '销售一部', 'customItem155': '初次沟通', 'ownerid': '0052020DA39F266VGBTc', 'txdz': None, 'customItem151': '政府', 'customItem159': '李玉清', 'highseaaccountsource': None, 'beizhu': None, 'jingweidula': None, 'cloudcctag': None, 'jingweiduco': None, 'nsr': None, 'fCity': '沧州市', 'srcflg': None, 'ces': None, 'khbh': 'CC20210107130690', 'bjdmx': None, 'weibo': None, 'isDeleted': '0', 'yid': None, 'gsgpdm': None, 'currency': 'CNY', 'lastmodifybyid': '0052020DA39F266VGBTc', 'CCObjectAPI': 'Account', 'customitem146': None, 'facebook': None, 'lqtime': None, 'qyyx': None, 'fstate': '河北省', 'gsownerid': None, 'dimDepart': '销售一部', 'lbsaddress': None, 'customitem148': '主动开拓', 'customitem147': None, 'khxxdz02': None, 'customitem155': '初次沟通', 'show_on_map': None, 'khxxdz01': None, 'is_locked': None, 'khxxdz04': None, 'customitem157': '销售一部', 'recentactivitycreatedby': None, 'khxxdz03': None, 'customitem156': '企业事业部', 'bzhyfldm': None, 'customitem151': '政府', 'khxxdz00': None, 'fdistrict': None, 'khxxdz05': None, 'fkdwdz': None, 'releasetime': None, 'returntimes': None, 'customitem159': '李玉清', 'kddz': None, 'customitem158': None, 'lastmodifydate': '2021-01-07 15:57:22', 'customitem166': None, 'customitem165': None, 'customitem168': None, 'customitem167': None, 'customitem162': '环保局', 'customitem161': None, 'customitem164': '否', 'customitem163': None, 'showOnMap': None, 'postcode': None, 'customitem160': '15803173022', 'ispartner': None, 'lrr': None, 'khdd':None, 'weixin': None, 'name': '沧州市生态环境局', 'fkdwdh': None, 'customitem169': None, 'customitem210': None, 'customitem177': None, 'customItem160': '15803173022', 'fenji': '开发客户', 'customitem212': None, 'customitem179': None, 'customitem178': None, 'customitem211': None, 'employeenumber': None, 'customitem174': None, 'fkdwyhzh': None, 'customitem171': None, 'linkedin': None, 'customitem170': None, 'customItem164': '否', 'customItem162': '环保局', 'wangzhi': None, 'is_deleted': '0', 'recordtype': '2019593FC86B601GFelY', 'customitem214': None, 'zwyhxwfx': None, 'customitem213': '否', 'customitem216': None, 'releasedefinition': None, 'dianhua': '0317-3022715', 'customitem184': None, 'customitem183': None, 'customitem186': None, 'customitem185': None, 'jingweidu': ',', 'dls': None, 'tyshxydm': None, 'donotdisturb': 'false', 'xsdt': None, 'zwzhmc': None, 'iscustomer': None, 'customItem213': '否', 'fhdz': None, 'highSeaStatus': '自建', 'dimdepart': '销售一部', 'khxxdz': '', 'hangye': None, 'sflzqzkh': None}]
    try:
        if data:
            cc_df = pd.DataFrame(columns=list(ACCOUNT_DICT.keys()))
            cc_df = cc_df.append(data, ignore_index=True, sort=False)
            ccdf_name_list = list(ACCOUNT_DICT.keys())
            cc_df = cc_df[ccdf_name_list]
            cc_df = cc_df.rename(columns=ACCOUNT_DICT)
            cc_df["id"]=None

            index_sql = """ select count(*) as nums from %s where created_at >= "%s" """ % (
            ACCOUNT_SQL_TABLE, today_stamp)
            id_index = pd.read_sql_query(index_sql, new_data)["nums"].tolist()[0]
            for row in cc_df.itertuples():
                df_index = getattr(row, 'Index')
                recent_activity_time = getattr(row, 'recent_activity_time')
                try:
                    cc_df.at[df_index, 'recent_activity_time'] = time_ms(recent_activity_time)
                except:
                    pass
                push_sea_date = getattr(row, 'push_sea_date')
                try:
                    cc_df.at[df_index, 'push_sea_date'] = time_ms(push_sea_date)
                except:
                    pass
                created_at = getattr(row, 'created_at')
                cc_df.at[df_index, 'created_at'] = time_ms(created_at)
                updated_at = getattr(row, 'updated_at')
                cc_df.at[df_index, 'updated_at'] = time_ms(updated_at)
                xsy_id = getattr(row, 'xsy_id')
                try:
                    xsy_id = str(xsy_id).strip()
                except:
                    pass
                cc_df.at[df_index, 'xsy_id'] = xsy_id
                po = getattr(row, 'account_name')
                created_at = getattr(row, 'created_at')
                timestamp = time_ms(created_at)
                id = getattr(row, 'id')
                if isinstance(id, str):
                    pass
                else:
                    id = create_id(po, timestamp, id_index)
                    cc_df.at[df_index, 'id'] = id
                id_index += 1

            # 在这里替换想相应的id
            # owner_id
            local_user_sql = """select `id` as local_owner_id ,crm_id as owner_id from {}""".format(USER_SQL_TABLE)
            local_user_df = pd.read_sql_query(local_user_sql, new_data)
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="owner_id")
            cc_df = cc_df.drop(["owner_id"], axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id": "owner_id"})
            # created_by
            local_user_df = local_user_df.rename(columns={"owner_id": "created_by"})
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="created_by")
            cc_df = cc_df.drop(["created_by"], axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id": "created_by"})
            # updated_by
            local_user_df = local_user_df.rename(columns={"created_by": "updated_by"})
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="updated_by")
            cc_df = cc_df.drop(["updated_by"], axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id": "updated_by"})
            # recent_activity_by
            local_user_df = local_user_df.rename(columns={"updated_by": "recent_activity_by"})
            cc_df = pd.merge(cc_df, local_user_df, how='left', on="recent_activity_by")
            cc_df = cc_df.drop(["recent_activity_by"], axis=1)
            cc_df = cc_df.rename(columns={"local_owner_id": "recent_activity_by"})

            inster_sql(new_data,ACCOUNT_SQL_TABLE,ACCOUNT_CLOUMNS_ORDER,cc_df)
            new_data.close()
            return cc_df["id"].tolist()[0]
    except Exception as e:
        print(e)
        pass






""" cloudcc account数据入库 """
def account_into_mysql(data):
    data =[{'leixing': '终端客户', 'parent': None, 'recentactivityrecordtime': None, 'customitem195': None, 'customitem194': None,'createdate': '2021-01-07 15:57:22', 'createbyid': '0052020DA39F266VGBTc', 'highseastatus': '自建', 'fkdwkhyh': None, 'twitter': None, 'lastcontactdate': '2021-01-07 16:05:15', 'zys': None, 'doNotDisturb': 'false', 'isLocked': None, 'customItem148': '主动开拓', 'lockstatus': None, 'fcity': '沧州市', 'id': '0012021A7AF8F65wuyLR', 'fax': None, 'fState': '河北省', 'releasereason': None, 'customItem156': '企业事业部', 'customItem157': '销售一部', 'customItem155': '初次沟通', 'ownerid': '0052020DA39F266VGBTc', 'txdz': None, 'customItem151': '政府', 'customItem159': '李玉清', 'highseaaccountsource': None, 'beizhu': None, 'jingweidula': None, 'cloudcctag': None, 'jingweiduco': None, 'nsr': None, 'fCity': '沧州市', 'srcflg': None, 'ces': None, 'khbh': 'CC20210107130690', 'bjdmx': None, 'weibo': None, 'isDeleted': '0', 'yid': None, 'gsgpdm': None, 'currency': 'CNY', 'lastmodifybyid': '0052020DA39F266VGBTc', 'CCObjectAPI': 'Account', 'customitem146': None, 'facebook': None, 'lqtime': None, 'qyyx': None, 'fstate': '河北省', 'gsownerid': None, 'dimDepart': '销售一部', 'lbsaddress': None, 'customitem148': '主动开拓', 'customitem147': None, 'khxxdz02': None, 'customitem155': '初次沟通', 'show_on_map': None, 'khxxdz01': None, 'is_locked': None, 'khxxdz04': None, 'customitem157': '销售一部', 'recentactivitycreatedby': None, 'khxxdz03': None, 'customitem156': '企业事业部', 'bzhyfldm': None, 'customitem151': '政府', 'khxxdz00': None, 'fdistrict': None, 'khxxdz05': None, 'fkdwdz': None, 'releasetime': None, 'returntimes': None, 'customitem159': '李玉清', 'kddz': None, 'customitem158': None, 'lastmodifydate': '2021-01-07 15:57:22', 'customitem166': None, 'customitem165': None, 'customitem168': None, 'customitem167': None, 'customitem162': '环保局', 'customitem161': None, 'customitem164': '否', 'customitem163': None, 'showOnMap': None, 'postcode': None, 'customitem160': '15803173022', 'ispartner': None, 'lrr': None, 'khdd':None, 'weixin': None, 'name': '沧州市生态环境局', 'fkdwdh': None, 'customitem169': None, 'customitem210': None, 'customitem177': None, 'customItem160': '15803173022', 'fenji': '开发客户', 'customitem212': None, 'customitem179': None, 'customitem178': None, 'customitem211': None, 'employeenumber': None, 'customitem174': None, 'fkdwyhzh': None, 'customitem171': None, 'linkedin': None, 'customitem170': None, 'customItem164': '否', 'customItem162': '环保局', 'wangzhi': None, 'is_deleted': '0', 'recordtype': '2019593FC86B601GFelY', 'customitem214': None, 'zwyhxwfx': None, 'customitem213': '否', 'customitem216': None, 'releasedefinition': None, 'dianhua': '0317-3022715', 'customitem184': None, 'customitem183': None, 'customitem186': None, 'customitem185': None, 'jingweidu': ',', 'dls': None, 'tyshxydm': None, 'donotdisturb': 'false', 'xsdt': None, 'zwzhmc': None, 'iscustomer': None, 'customItem213': '否', 'fhdz': None, 'highSeaStatus': '自建', 'dimdepart': '销售一部', 'khxxdz': '', 'hangye': None, 'sflzqzkh': None}]
    return "aaaa"


if __name__ == "__main__":
    pass
    # a=account_insert_mysql("1")
