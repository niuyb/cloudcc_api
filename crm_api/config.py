#!/usr/bin/env python
# encoding: utf-8

# 数据请求格式
# 1成功
# 0无效
#-1异常
RESULT = {"data": [], "code": -1, "msg": ""}


# cloudcc 超管账号   后期修改为公用账号
ClOUDCC_USERNAME = "admin@yqzbw.com"
ClOUDCC_PASSWORD = "zhxg1111"

# 获取cloudcc请求路径
ACCESS_URL = "http://site.cloudcc.com/api/appURL/get?username="

# redis
CLOUD_REDIS = "192.168.185.129"
REDIS_EXPIRE = 30*60

# cloudcc Object 对象
ClOUDCC_OBJECT={
    "account":"Account",
    "opportunity":"Opportunity",
}











# 接口与cloudcc映射
ACCOUNT_MAPPING={
    "id":"id",
    "name":"name",
    "call_back_url":"zwyhxwfx",
}
# 以下都是接口字段
# 客户  允许  查询 字段名称
ACCOUNT_QUERY_ALLOW=["id","name"]
# 客户  允许  修改 字段名称
ACCOUNT_MODIFY_ALLOW=["name","call_back_url"]





# 商机  允许  查询 字段名称
OPPORTUNITY_QUERY_ALLOW=["id","name"]
