#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/16 10:22
# 工具：PyCharm
# Python版本：3.7.0
""""""
import hashlib
import json
import pandas as pd

import requests
# 增加重试次数
# requests.DEFAULT_RETRIES = 5
# s.keep_alive = False

from public.utils import get_redis, Result, engine
from settings import settings
from settings.config import CLOUD_REDIS, ACCESS_URL, ClOUDCC_USERNAME, REDIS_EXPIRE, ClOUDCC_PASSWORD


def cloudcc_reload():
    """ 重置access_url  binding """
    try:
        cloud_redis=get_redis(CLOUD_REDIS,"0")
        access_url = cloudcc_get_request_url(ACCESS_URL, ClOUDCC_USERNAME)
        binding = cloudcc_get_binding(access_url, ClOUDCC_USERNAME, ClOUDCC_PASSWORD)
        cloud_redis.set("access_url",access_url)
        cloud_redis.expire("access_url",REDIS_EXPIRE)
        cloud_redis.set("binding",binding)
        cloud_redis.expire("binding",REDIS_EXPIRE)
    except:
        return "获取binding失败"
    return binding


def cloudcc_get_request_url(url,username):
    """ 获取 cloudcc 的请求地址 """
    """ "http://site.cloudcc.com/api/appURL/get?username=" """
    session = requests.session()
    session.keep_alive = False
    cloud_redis=get_redis(CLOUD_REDIS,"0")
    access_url = cloud_redis.get("access_url")
    if access_url:
        return access_url
    else:
        try:
            # print(url + username)
            response = json.loads(session.get(url + username).text)
            # print(response)
            if response.get("success") == True:
                access_url = response.get("result")
            else:
                return "获取cc域名无效"
        except Exception as e:
            return "获取cc域名失败"
        cloud_redis.set("access_url",access_url)
        cloud_redis.expire("access_url",REDIS_EXPIRE)
    return access_url


def cloudcc_get_binding(access_url,username,password):
    """ 获取 cloudcc 的binding """
    """http://test.dev.cloudcc.com/distributor.action?serviceName=upd"""
    session = requests.session()
    session.keep_alive = False
    cloud_redis=get_redis(CLOUD_REDIS,"0")
    binding = cloud_redis.get("binding")
    if binding:
        return binding
    else:
        try:
            access_url = access_url + "/distributor.action?serviceName=clogin&userName=" + username + "&password=" + password
            # print(access_url)
            response = json.loads(session.get(access_url).text)
            # print(response)
            if response.get("result") == True:
                binding = response.get("binding")
            else:
                return "获取binding无效"
        except Exception as e:
            return  "获取binding失败"
        cloud_redis.set("binding",binding)
        cloud_redis.expire("binding",REDIS_EXPIRE)
    return binding


def cloudcc_query_sql(access_url,server_name,objectapi_name,sql,binding):
    """ 通过sql 查询 """
    session = requests.session()
    session.keep_alive = False
    access_url = access_url+"/distributor.action?serviceName="+server_name+"&objectApiName="+objectapi_name+"&expressions="+sql+"&binding="+binding
    try:
        # print(access_url)
        response = json.loads(session.get(access_url).text)
        # print(response)
        if response["result"] == True:
            # print("sql查询",len(response["data"]))
            return response["data"]
        else:
            return "获取data无效,请检查参数"
    except Exception as e:
        print(e)
        return "获取data失败"

# def cloudcc_query_sql_requirement(access_url,server_name,objectapi_name,binding,sql_select_items,sql_filter):
#     """ 自定条件查询 通过sql 查询 """
#     for select_item in sql_select_items:
#         pass
#     select_items = ""
#     sql = """ select {} from {} where {} """.format(select_items,objectapi_name)
#
#     res=cloudcc_query_sql(access_url,server_name,objectapi_name,sql,binding)
#


# 后期调试
def cloudcc_query_name(access_url,server_name,objectapi_name,object_name,binding):
    """ 通过名称具体查询 查询 """
    """ http://test.cloudcc.cn/distributor.action?serviceName=cquery&o bjectApiName=Contact&expressions=name='测试HTTP服务' and email='zxj@cloudcc.com'&binding=6214C265D3AAE7D4AFF6385921E1FB16 """
    session = requests.session()
    session.keep_alive = False
    access_url = access_url + "/distributor.action?serviceName=" + server_name + "&objectApiName=" + objectapi_name + "&expressions=name=" + object_name + "&binding=" + binding
    try:
        # print(access_url)
        response = json.loads(session.get(access_url).text)
        # print(response)
        if response["result"] == True:
            return response["data"]
        else:
            return "获取data无效,请检查参数"
    except:
        return "获取data失败"



def modify_by_api(access_url,server_name,objectapi_name,data,binding):
    session = requests.session()
    session.keep_alive = False
    try:
        data=json.dumps(data)
        access_url = access_url+"/distributor.action?serviceName="+server_name+"&objectApiName="+objectapi_name+"&data="+data+"&binding="+binding
        # print(access_url)
        response = json.loads(session.get(access_url).text)
        # print(response)
        if response["result"] == True:
            return True
        else:
            return False
    except:
        return False





















def get_pick_list_value(access_url,server_name,data):
    session = requests.session()
    session.keep_alive = False
    try:
        data=json.dumps(data)
        access_url = access_url+"/distributor.action?serviceName="+server_name+"&objectApiName="+objectapi_name+"&data="+data+"&binding="+binding
        # print(access_url)
        response = json.loads(session.get(access_url).text)
        # print(response)
        if response["result"] == True:
            return True
        else:
            return False
    except:
        return False






if __name__ == "__main__":
    pass
    # data=cloudcc_query_name("https://k8mm3cmt3235c7ed72cede6e.cloudcc.com","cquery","Account","万科","F4318B05B7C1D4DC0CF165E0AB5421BC")
    # print(data)
    #
    # "0012020FE5A8EB0s9Ahn"
    # data=cloudcc_query_sql("https://k8mm3cmt3235c7ed72cede6e.cloudcc.com","cqlQuery","Account","select  *  from `Account` where id ='0012020B26843C18KDAP'  ","FAB429EB2370B7621897C28A5402DFC1")


    # data=cloudcc_query_sql("https://k8mm3cmt3235c7ed72cede6e.cloudcc.com","cqlQuery","dingdan","""select name,id,byh,yid from `dingdan` where `id` in ('a1320215866B50EliWrK')  and is_deleted="0" ""","558321A23E6CFFB4D290A9B378E68A8B")
    # print(data)

    data=cloudcc_query_sql("https://k8mm3cmt3235c7ed72cede6e.cloudcc.com","cqlQuery","Opportunity","""select * from `Opportunity` where `name` like '%北京天使慧大%' limit 15""","2FFCD37C8BCD5D8D274608BE6C0D4B17")
    print(data)

    # data = modify_by_api("https://k8mm3cmt3235c7ed72cede6e.cloudcc.com","update","Account", [{'id':"0012020FE5A8EB0s9Ahn","name":"万科_modify_by_api"}], "F4318B05B7C1D4DC0CF165E0AB5421BC")
    # print(data)

    # md5_str = hashlib.md5("QY_001".encode(encoding='UTF-8')).hexdigest()
    # print(md5_str)
    # md5_str = hashlib.md5("ZW_001".encode(encoding='UTF-8')).hexdigest()
    # print(md5_str)