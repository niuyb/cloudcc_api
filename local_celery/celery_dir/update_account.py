#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 18:01
# 工具：PyCharm
# Python版本：3.7.0
from datetime import datetime
import pandas as pd
from local_celery.celery_dir import celery_app
from local_celery.celery_dir.celery_utils import inster_sql
from public.utils import engine, date_ms, list_to_sql_string, time_ms
from script.data_config import ACCOUNT_SQL_TABLE, ACCOUNT_DICT, USER_SQL_TABLE, ACCOUNT_CLOUMNS_ORDER
from script.data_utils import create_id
from settings import settings

""" cloudcc account数据入库 """
@celery_app.task
def account_insert_mysql(id_dict,data):
    """
    account/api
    接口中先查数据库,数据库中无信息则去查询cloudcc之后同步数据库所以此处id均为新增id
    """
    new_data = engine(settings.db_new_data)
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

            for row in cc_df.itertuples():
                df_index = getattr(row, 'Index')
                crm_id = getattr(row, 'crm_id')
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
                cc_df.at[df_index, 'id'] = id_dict.get(crm_id,"")

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
            return cc_df["id"].tolist()
        else:
            return False
    except Exception as e:
        print(e)
        return False