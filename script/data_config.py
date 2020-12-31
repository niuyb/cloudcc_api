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
    "yid":"xsy_id",
}
ORDER_TABLE_STRING="""ALTER table `{}`
      MODIFY `id` varchar(50) COMMENT '星光自建订单id',
      MODIFY `crm_id` varchar(50) COMMENT 'crm 订单id',
      MODIFY `po` varchar(50) COMMENT '流水号',
      MODIFY `owner_id` varchar(50) COMMENT '销售负责人 对应星光salerid',
      MODIFY `status` varchar(20) COMMENT '订单状态',
      MODIFY `account_id` varchar(50) COMMENT '最终客户id 对应account 星光id',
      MODIFY `price_id` varchar(50) COMMENT '价格表名称',
      MODIFY `opportunity_id` varchar(100) COMMENT '商机id',
      MODIFY `created_by` varchar(50) COMMENT '创建人',
      MODIFY `created_at` varchar(50) COMMENT '创建日期',
      MODIFY `updated_by` varchar(50) COMMENT '最新修改人',
      MODIFY `updated_at` varchar(50) COMMENT '最新修改日期',
      MODIFY `amount` varchar(50) COMMENT '订单总金额',
      MODIFY `discount_amount` varchar(50) COMMENT '总折扣额',
      MODIFY `contract_status` varchar(20) COMMENT '合同状态',
      MODIFY `contract_attribute` varchar(10) COMMENT '合同属性 1新签 2续签',
      MODIFY `contract_id` varchar(50) COMMENT '合同编号',
      MODIFY `contract_start` varchar(50) COMMENT '合同开始日期',
      MODIFY `contract_end` varchar(50) COMMENT '最终合同截止日期',
      MODIFY `contract_back_date` varchar(50) COMMENT '合同归档日期',
      MODIFY `total_performance` varchar(50) COMMENT '业绩核算(成本）总额',
      MODIFY `approve_date` varchar(50) COMMENT '审批通过时间',
      MODIFY `payback_type` varchar(20) COMMENT '回款计划类型',
      MODIFY `xsy_id` varchar(20) COMMENT '销售易id' """





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
