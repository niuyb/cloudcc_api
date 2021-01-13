#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/7 16:41
# 工具：PyCharm
# Python版本：3.7.0
import pymysql

from public.utils import list_to_sql_string, engine, time_ms, date_ms
from script.data_config import ACCOUNT_DICT, ACCOUNT_SQL_TABLE, USER_SQL_TABLE, \
    ACCOUNT_CLOUMNS_ORDER, OPPORTUNITY_DICT, OPPORTUNITY_SQL_TABLE, OPPORTUNITY_CLOUMNS_ORDER
import pandas as pd

from script.data_utils import create_id
from settings import settings
from datetime import datetime
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列

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

def inster_sql(new_data,sql_table,columns_order,df,local_str):
    cur, conn = get_conn()
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

""" cloudcc account数据入库 """
def account_insert_mysql(data):
    new_data = engine(settings.db_new_data)
    today = str(datetime.now().strftime('%Y-%m-%d'))
    today_stamp = date_ms(today)
    #test
    # id b2bdc1f2a657d490
    # data =[{'leixing': '终端客户', 'parent': None, 'recentactivityrecordtime': None, 'customitem195': None, 'customitem194': None,'createdate': '2021-01-07 15:57:22', 'createbyid': '0052020DA39F266VGBTc', 'highseastatus': '自建', 'fkdwkhyh': None, 'twitter': None, 'lastcontactdate': '2021-01-07 16:05:15', 'zys': None, 'doNotDisturb': 'false', 'isLocked': None, 'customItem148': '主动开拓', 'lockstatus': None, 'fcity': '沧州市', 'id': '0012021A7AF8F65wuyLR', 'fax': None, 'fState': '河北省', 'releasereason': None, 'customItem156': '企业事业部', 'customItem157': '销售一部', 'customItem155': '初次沟通', 'ownerid': '0052020DA39F266VGBTc', 'txdz': None, 'customItem151': '政府', 'customItem159': '李玉清', 'highseaaccountsource': None, 'beizhu': None, 'jingweidula': None, 'cloudcctag': None, 'jingweiduco': None, 'nsr': None, 'fCity': '沧州市', 'srcflg': None, 'ces': None, 'khbh': 'CC20210107130690', 'bjdmx': None, 'weibo': None, 'isDeleted': '0', 'yid': None, 'gsgpdm': None, 'currency': 'CNY', 'lastmodifybyid': '0052020DA39F266VGBTc', 'CCObjectAPI': 'Account', 'customitem146': None, 'facebook': None, 'lqtime': None, 'qyyx': None, 'fstate': '河北省', 'gsownerid': None, 'dimDepart': '销售一部', 'lbsaddress': None, 'customitem148': '主动开拓', 'customitem147': None, 'khxxdz02': None, 'customitem155': '初次沟通', 'show_on_map': None, 'khxxdz01': None, 'is_locked': None, 'khxxdz04': None, 'customitem157': '销售一部', 'recentactivitycreatedby': None, 'khxxdz03': None, 'customitem156': '企业事业部', 'bzhyfldm': None, 'customitem151': '政府', 'khxxdz00': None, 'fdistrict': None, 'khxxdz05': None, 'fkdwdz': None, 'releasetime': None, 'returntimes': None, 'customitem159': '李玉清', 'kddz': None, 'customitem158': None, 'lastmodifydate': '2021-01-07 15:57:22', 'customitem166': None, 'customitem165': None, 'customitem168': None, 'customitem167': None, 'customitem162': '环保局', 'customitem161': None, 'customitem164': '否', 'customitem163': None, 'showOnMap': None, 'postcode': None, 'customitem160': '15803173022', 'ispartner': None, 'lrr': None, 'khdd':None, 'weixin': None, 'name': '沧州市生态环境局', 'fkdwdh': None, 'customitem169': None, 'customitem210': None, 'customitem177': None, 'customItem160': '15803173022', 'fenji': '开发客户', 'customitem212': None, 'customitem179': None, 'customitem178': None, 'customitem211': None, 'employeenumber': None, 'customitem174': None, 'fkdwyhzh': None, 'customitem171': None, 'linkedin': None, 'customitem170': None, 'customItem164': '否', 'customItem162': '环保局', 'wangzhi': None, 'is_deleted': '0', 'recordtype': '2019593FC86B601GFelY', 'customitem214': None, 'zwyhxwfx': None, 'customitem213': '否', 'customitem216': None, 'releasedefinition': None, 'dianhua': '0317-3022715', 'customitem184': None, 'customitem183': None, 'customitem186': None, 'customitem185': None, 'jingweidu': ',', 'dls': None, 'tyshxydm': None, 'donotdisturb': 'false', 'xsdt': None, 'zwzhmc': None, 'iscustomer': None, 'customItem213': '否', 'fhdz': None, 'highSeaStatus': '自建', 'dimdepart': '销售一部', 'khxxdz': '', 'hangye': None, 'sflzqzkh': None}]
    try:
        if data:
            cc_df = pd.DataFrame(columns=list(ACCOUNT_DICT.keys()))
            cc_df = cc_df.append(data, ignore_index=True, sort=False)
            ccdf_name_list = list(ACCOUNT_DICT.keys())
            cc_df = cc_df[ccdf_name_list]
            cc_df = cc_df.rename(columns=ACCOUNT_DICT)
            cc_df["id"]=None

            local_list = cc_df["crm_id"].tolist()
            local_str = list_to_sql_string(local_list)

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

            inster_sql(new_data,ACCOUNT_SQL_TABLE,ACCOUNT_CLOUMNS_ORDER,cc_df,local_str)
            new_data.close()
            return cc_df["id"].tolist()[0]
        else:
            return False
    except Exception as e:
        print(e)
        return False



def opportunity_into_mysql(data):
    new_data = engine(settings.db_new_data)
    today = str(datetime.now().strftime('%Y-%m-%d'))
    today_stamp = date_ms(today)
    # test
    # id 9ddf8a1bf6d48236
    # data=[{'customitem199': None, 'customitem231': None, 'customitem198': None, 'customitem234': '集团', 'customitem233': '企业', 'customitem195': None, 'recentactivityrecordtime': '2020-10-29 00:00:00', 'customitem194': None, 'customitem230': None, 'customitem197': None, 'jine': '60000', 'customitem196': None, 'createdate': '2020-08-21 11:48:00', 'customitem193': None, 'loststageid': None, 'pricebook2id': None, 'createbyid': '0052020A8D8B44BQLOfD', 'customItem263': '已领取', 'ywjhsm': None, 'ywlx': '产品新单', 'sjlx': None, 'latestcontact': None, 'isLocked': None, 'lockstatus': '未锁定', 'customitem239': None, 'commitmentFlg': '否', 'id': '0022021FAD3F80BcQobP', 'priceid': 'a0720208E1B9A9FMsTxU', 'customitem236': None, 'customitem238': None, 'gcz': None, 'customitem237': None, 'customitem243': None, 'customitem245': None, 'customitem244': None, 'customitem240': None, 'ownerid': '0052020A8D8B44BQLOfD', 'commitmentflg': '否', 'customitem247': None, 'customitem246': None, 'customitem249': None, 'customitem248': None, 'htsx': None, 'jingweidula': None, 'customitem253': '安徽省', 'cloudcctag': None, 'customitem250': None, 'customitem252': None, 'customitem251': None, 'jingweiduco': None, 'zhzqzkh': None, 'dqzj': None, 'isDeleted': '0', 'yid': '\t1363425390330269', 'bz': None, 'currency': 'CNY', 'customitem258': None, 'lastmodifybyid': '0052020A8D8B44BQLOfD', 'customitem257': None, 'customitem139': None, 'customitem259': None, 'CCObjectAPI': 'Opportunity', 'sourceid': None, 'customitem265': None, 'sybzj': None, 'customitem267': None, 'customitem145': None, 'customitem266': None, 'customitem261': None, 'customitem140': None, 'customitem263': '已领取', 'customitem142': None, 'sz': None, 'customitem262': None, 'customitem141': None, 'actualcost': None, 'customItem253': '安徽省', 'knx': '0', 'dimDepart': '一区安徽', 'jsrq': '2021-12-02 00:00:00', 'forecasttype': None, 'lbsaddress': None, 'customitem269': None, 'customitem148': None, 'priceId': 'a0720208E1B9A9FMsTxU', 'customitem268': None, 'customitem147': None, 'xyb': None, 'khxxdz02': None, 'khmc': '00120218C661F78uKtV8', 'khxxdz01': None, 'customitem154': None, 'is_locked': None, 'khxxdz04': None, 'customitem157': None, 'khxxdz03': None, 'customitem156': None, 'customitem151': None, 'customitem272': None, 'customitem150': None, 'customitem271': None, 'khxxdz00': None, 'customitem153': None, 'customitem152': None, 'customItem222': '0551-63659958', 'sqfzr': None, 'customItem223': '待提交', 'customitem270': None, 'customItem220': '可以续单', 'customItem187': '未成交', 'customItem188': '企业事业部', 'khxxdz05': None, 'ddyy': None, 'customItem229': 'OPP202008210076', 'customItem226': '开发客户', 'customitem159': None, 'customitem158': None, 'lastmodifydate': '2020-10-29 11:45:00', 'customitem166': None, 'customitem165': '企划部', 'customitem201': None, 'customitem200': None, 'zzkh': '00120218C661F78uKtV8', 'customitem162': '主动开拓', 'customitem161': '企业', 'customitem164': '标准化产品-舆情秘书服务系统', 'customItem233': '企业', 'customItem234': '集团', 'customitem160': None, 'name': '同庆楼商情', 'campaign': None, 'jieduan': '潜在商机(新)', 'customitem203': None, 'customitem202': None, 'customitem204': None, 'customItem165': '企划部', 'customItem164': '标准化产品-舆情秘书服务系统', 'customItem161': '企业', 'customItem162': '主动开拓', 'is_deleted': '0', 'lockStatus': '未锁定', 'recordtype': None, 'customitem218': '待提交', 'customitem217': None, 'customitem219': '待提交', 'customitem214': None, 'projectbudget': None, 'zwyhxwfx': None, 'customitem213': None, 'customitem216': None, 'customitem215': None, 'customitem188': '企业事业部', 'customitem221': None, 'customitem220': '可以续单', 'customitem187': '未成交', 'customitem223': '待提交', 'customitem222': '0551-63659958', 'customitem186': None, 'customitem185': None, 'sjbh': 'CCSJ2021010347224', 'jingweidu': ',', 'dls': None, 'jzds': None, 'stageupdatedat': None, 'customItem219': '待提交', 'customItem218': '待提交', 'ddsm': None, 'zwzhmc': None, 'customitem229': 'OPP202008210076', 'dlsqr': None, 'customitem228': None, 'dimdepart': '一区安徽', 'khxxdz': '', 'recentActivityRecordTime': '2020-10-29 00:00:00', 'customitem225': None, 'customitem224': None, 'customitem227': None, 'customitem226': '开发客户'}]
    try:
        if data:
            cc_df = pd.DataFrame(columns=list(OPPORTUNITY_DICT.keys()))
            cc_df = cc_df.append(data,ignore_index=True,sort=False)
            ccdf_name_list = list(OPPORTUNITY_DICT.keys()) + ["is_deleted"]
            cc_df = cc_df[ccdf_name_list]
            cc_df = cc_df.rename(columns=OPPORTUNITY_DICT)
            cc_df["id"] = None

            # 本次操作的cc id
            # operate_list = cc_df["crm_id"].tolist()
            # operate_str = list_to_sql_string(operate_list)
            # local_sql = """ select id,crm_id,account_id from `{}` where crm_id in ({})""".format(OPPORTUNITY_SQL_TABLE,operate_str)
            # local_df = pd.read_sql_query(local_sql,new_data)
            # 本次操作local数据库id
            local_list = cc_df["crm_id"].tolist()
            local_str = list_to_sql_string(local_list)
            print(local_str)

            index_sql = """ select count(*) as nums from %s where created_at >= "%s" """ % (OPPORTUNITY_SQL_TABLE, today_stamp)
            id_index = pd.read_sql_query(index_sql,new_data)["nums"].tolist()[0]
            id_dict={}
            for row in cc_df.itertuples():
                df_index = getattr(row, 'Index')
                crm_id = getattr(row, 'crm_id')
                close_date = getattr(row, 'close_date')
                try:
                    cc_df.at[df_index, 'close_date'] = time_ms(close_date)
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
                po = getattr(row, 'opportunity_name')
                created_at = getattr(row, 'created_at')
                timestamp = time_ms(created_at)
                id = getattr(row, 'id')
                if isinstance(id,str):
                    pass
                else:
                    id = create_id(po, timestamp, id_index)
                    cc_df.at[df_index, 'id'] = id
                id_index+=1

                id_dict[crm_id] = id


            # 在这里替换想相应的id
            # account_id
            cc_account_str = list_to_sql_string(cc_df["account_id"].dropna().tolist())
            local_account_sql = """ select id as local_account_id,crm_id as account_id  from `{}` where crm_id in ({})""".format(ACCOUNT_SQL_TABLE,cc_account_str)
            local_account_df = pd.read_sql_query(local_account_sql,new_data)
            cc_df = pd.merge(cc_df, local_account_df, how='left', on="account_id")
            cc_df = cc_df.drop(["account_id"],axis=1)
            cc_df = cc_df.rename(columns={"local_account_id":"account_id"})
            #owner_id
            local_user_sql = """select `id` as local_owner_id ,crm_id as owner_id from {}""".format(USER_SQL_TABLE)
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

            inster_sql(new_data, OPPORTUNITY_SQL_TABLE, OPPORTUNITY_CLOUMNS_ORDER, cc_df,local_str)
            # print("入库",cc_df.shape)
            print(cc_df)
            new_data.close()

            # return cc_df[["id","crm_id"]].to_dict(orient='records')
            return id_dict
        else:
            return False
    except Exception as e:
        print(e)
        return False


def account_into_mysql(data):
    data =[{'leixing': '终端客户', 'parent': None, 'recentactivityrecordtime': None, 'customitem195': None, 'customitem194': None,'createdate': '2021-01-07 15:57:22', 'createbyid': '0052020DA39F266VGBTc', 'highseastatus': '自建', 'fkdwkhyh': None, 'twitter': None, 'lastcontactdate': '2021-01-07 16:05:15', 'zys': None, 'doNotDisturb': 'false', 'isLocked': None, 'customItem148': '主动开拓', 'lockstatus': None, 'fcity': '沧州市', 'id': '0012021A7AF8F65wuyLR', 'fax': None, 'fState': '河北省', 'releasereason': None, 'customItem156': '企业事业部', 'customItem157': '销售一部', 'customItem155': '初次沟通', 'ownerid': '0052020DA39F266VGBTc', 'txdz': None, 'customItem151': '政府', 'customItem159': '李玉清', 'highseaaccountsource': None, 'beizhu': None, 'jingweidula': None, 'cloudcctag': None, 'jingweiduco': None, 'nsr': None, 'fCity': '沧州市', 'srcflg': None, 'ces': None, 'khbh': 'CC20210107130690', 'bjdmx': None, 'weibo': None, 'isDeleted': '0', 'yid': None, 'gsgpdm': None, 'currency': 'CNY', 'lastmodifybyid': '0052020DA39F266VGBTc', 'CCObjectAPI': 'Account', 'customitem146': None, 'facebook': None, 'lqtime': None, 'qyyx': None, 'fstate': '河北省', 'gsownerid': None, 'dimDepart': '销售一部', 'lbsaddress': None, 'customitem148': '主动开拓', 'customitem147': None, 'khxxdz02': None, 'customitem155': '初次沟通', 'show_on_map': None, 'khxxdz01': None, 'is_locked': None, 'khxxdz04': None, 'customitem157': '销售一部', 'recentactivitycreatedby': None, 'khxxdz03': None, 'customitem156': '企业事业部', 'bzhyfldm': None, 'customitem151': '政府', 'khxxdz00': None, 'fdistrict': None, 'khxxdz05': None, 'fkdwdz': None, 'releasetime': None, 'returntimes': None, 'customitem159': '李玉清', 'kddz': None, 'customitem158': None, 'lastmodifydate': '2021-01-07 15:57:22', 'customitem166': None, 'customitem165': None, 'customitem168': None, 'customitem167': None, 'customitem162': '环保局', 'customitem161': None, 'customitem164': '否', 'customitem163': None, 'showOnMap': None, 'postcode': None, 'customitem160': '15803173022', 'ispartner': None, 'lrr': None, 'khdd':None, 'weixin': None, 'name': '沧州市生态环境局', 'fkdwdh': None, 'customitem169': None, 'customitem210': None, 'customitem177': None, 'customItem160': '15803173022', 'fenji': '开发客户', 'customitem212': None, 'customitem179': None, 'customitem178': None, 'customitem211': None, 'employeenumber': None, 'customitem174': None, 'fkdwyhzh': None, 'customitem171': None, 'linkedin': None, 'customitem170': None, 'customItem164': '否', 'customItem162': '环保局', 'wangzhi': None, 'is_deleted': '0', 'recordtype': '2019593FC86B601GFelY', 'customitem214': None, 'zwyhxwfx': None, 'customitem213': '否', 'customitem216': None, 'releasedefinition': None, 'dianhua': '0317-3022715', 'customitem184': None, 'customitem183': None, 'customitem186': None, 'customitem185': None, 'jingweidu': ',', 'dls': None, 'tyshxydm': None, 'donotdisturb': 'false', 'xsdt': None, 'zwzhmc': None, 'iscustomer': None, 'customItem213': '否', 'fhdz': None, 'highSeaStatus': '自建', 'dimdepart': '销售一部', 'khxxdz': '', 'hangye': None, 'sflzqzkh': None}]
    return "aaaa"


if __name__ == "__main__":
    pass
    # a=account_insert_mysql("1")
    opportunity_into_mysql(1)