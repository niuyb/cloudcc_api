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

#api与cloudcc对象映射关系
ClOUDCC_OBJECT={
    "account":"Account",
    "opportunity":"Opportunity",
}
# -----------------------------------------ACCOUNT-----------------------------------------------
# account api 与 cloudcc映射
ACCOUNT_MAPPING={
    "id":"id",
    "name":"name",
    "zw_back_url":"zwyhxwfx",
    "qy_back_url":"customItem178",
}
# 以下都是接口字段
# 客户  允许  查询 字段名称
ACCOUNT_QUERY_ALLOW=["id","name"]
# 客户  允许  修改 字段名称
ACCOUNT_MODIFY_ALLOW=["name","zw_back_url","qy_back_url"]
# 允许 模糊查询
ACCOUNT_FUZZY_QUERY = ["name"]
# -----------------------------------------OPPORTUNITY-----------------------------------------------
# opportunity api 与 cloudcc映射
OPPORTUNITY_MAPPING={
    "id":"id",
    "name":"name",
    "account_id":"khmc",
}
#允许 查询 字段名称
OPPORTUNITY_QUERY_ALLOW=["id","name","account_id"]
# 允许 模糊查询
OPPORTUNITY_FUZZY_QUERY = ["name"]
# -----------------------------------------ORDER-----------------------------------------------
# order api 与 cloudcc映射
ORDER_MAPPING={
    "id":"id",
    "name":"name",
}
# 订单  允许  查询 字段名称
ORDER_QUERY_ALLOW=["id","name"]



# -----------------------------------------TEMP-----------------------------------------------
QY_token = "457d6a5e009f1ebb0906f03b32d0881f"

ZW_token = "4e33e00381c94a9bba251ebb44996c0f"