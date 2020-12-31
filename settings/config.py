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
# account api 参数 与 cloudcc映射
ACCOUNT_MAPPING={
    "id":"id",
    "name":"name",
    "zw_back_url":"zwyhxwfx",
    "qy_back_url":"customItem178",
}
# 以下都是接口字段
# 客户  允许查询条件   字段名称
ACCOUNT_QUERY_ALLOW=["id","name"]
# 客户  允许  修改 字段名称    back_url 包括 zw_back_url  qy_back_url
ACCOUNT_MODIFY_ALLOW=["name","back_url"]
# 允许 模糊查询
ACCOUNT_FUZZY_QUERY = ["name"]

# update_append 更新字段
UPDATE_APPEND_ITEMS = ["id", "ownerid", "account_name", "created_at", "address_province", "address_city",
                         "address_area", "industry_1", "industry_2", "level", "sea_status", "contact_phone",
                         "recent_activity_time"]
# -----------------------------------------OPPORTUNITY-----------------------------------------------
# opportunity api 与 cloudcc映射
OPPORTUNITY_MAPPING={
    "id":"id",
    "name":"name",
    "account_id":"khmc",
}
#允许 查询条件 字段名称
OPPORTUNITY_QUERY_ALLOW=["id","name","account_id"]
# 允许 模糊查询
OPPORTUNITY_FUZZY_QUERY = ["name"]
# -----------------------------------------ORDER-----------------------------------------------
# order api 与 cloudcc映射
ORDER_MAPPING={
    "id":"id",
    "name":"name",
}
# 订单  查询条件  查询 字段名称
ORDER_QUERY_ALLOW=["id","name"]



# -----------------------------------------TEMP-----------------------------------------------
PERMISSION_DICT = {
    "account":"QY_ACCOUNT_QUERY",

}




QY_token = "457d6a5e009f1ebb0906f03b32d0881f"
# QY账号允许查询返回的字段
QY_ACCOUNT_QUERY=["id","name","yid"]

ZW_token = "4e33e00381c94a9bba251ebb44996c0f"
# ZW账号允许查询返回的字段
ZW_ACCOUNT_QUERY=["id","name","customItem151","customItem162","fState","fCity","fDistrict","yid"]


