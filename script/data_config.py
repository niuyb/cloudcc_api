#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/28 17:43
# 工具：PyCharm
# Python版本：3.7.0


ORDER_DICT={
    "id":"crm_id",
    "name":"po",
    "ownerid":"owner_id",
    "poStatus":"status",
    "accountId":"account_id",
    "orderRelQuotationEntity": "price_id",
    "opportunityId": "opportunity_id",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
    "amount": "amount",
    "totaldiscountamount": "discount_amount",
    "htzt": "contract_status",
    "customItem158": "contract_attribute",
    "customItem166": "contract_id",
    "customItem147": "contract_start",
    "customItem148": "contract_end",
    "customItem156": "contract_back_date",
    "customItem164": "total_performance",
    "customItem182": "approve_date",
    "customitem294": "payback_type",
}

# 数据库名称
ACCOUNT_SQL_TABLE = "account_back"
ACCOUNT_DICT={
    "id":"crm_id",
    "leixing":"entity_type",
    "name":"account_name",
    "ownerid":"owner_id",
    "fenji":"level",
    "highSeaStatus":"sea_status",
    # 两个值合并
    "jingweidu":"longitude",
    # "latitude": "latitude",
    "khxxdz": "address",
    "fState":"address_province",
    "fCity": "address_city",
    "fDistrict": "address_area",
    "recentActivityRecordTime":"recent_activity_time",
    "recentActivityCreatedBy": "recent_activity_by",
    "gsownerid":"sea_id",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
    "customItem151": "industry_1",
    "customItem162": "industry_2",
    "customItem159": "contact",
    "dianhua": "contact_phone",
    "customItem161": "contact_post",
    # 部门转换
    "dimdepart": "department_top",
    "customItem156": "department",
    "customItem214": "sea_push",
    "customItem216": "push_sea_date",
    "yid":"xsy_id"
}

USER_DICT={
    "id":"crm_id",
    "name":"username",
    "department":"department_id",
    "isusing":"status",
    "createdate":"hire_date",
    "email":"email",
}
OPPORTUNITY_SQL_TABLE = "opportunity_back"
OPPORTUNITY_DICT = {
    "id": "crm_id",
    "ywlx": "entity_type",
    "name": "opportunity_name",
    "ownerid": "owner_id",
    "priceid": "price_id",
    "zzkh": "account_id",
    "jine": "money",
    "customItem164": "intended_product",
    "jieduan": "sale_stage",
    "knx": "win_rate",
    "jsrq": "close_date",
    "commitmentFlg": "saler_promise",
    "projectBudget": "project_budget",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
    "customItem165": "contact",
    "customItem166": "position",
    "yid": "xsy_id"

}
