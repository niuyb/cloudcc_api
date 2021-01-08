#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/28 17:43
# 工具：PyCharm
# Python版本：3.7.0

ORDER_API_NAME="dingdan"
ORDER_SQL_TABLE="order_back"
ORDER_CLOUMNS_ORDER = ["id","crm_id","po","owner_id","status","account_id","price_id","opportunity_id","created_by","created_at","updated_by","updated_at","amount","discount_amount","contract_status","contract_attribute","contract_id","contract_start","contract_end","contract_back_date","total_performance","approve_date","payback_type","xsy_id"]
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
    "customitem158": "contract_attribute",
    "customitem166": "contract_id",
    "customitem147": "contract_start",
    "customitem148": "contract_end",
    "customitem156": "contract_back_date",
    "customitem164": "total_performance",
    "customitem182": "approve_date",
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
ACCOUNT_API_NAME = "Account"
ACCOUNT_SQL_TABLE = "account_back"
ACCOUNT_CLOUMNS_ORDER = ["id","crm_id","entity_type","account_name","owner_id","level","sea_status","longitude","address","address_province","address_city","address_area","recent_activity_time","recent_activity_by","sea_id","created_by","created_at","updated_by","updated_at","industry_1","industry_2","contact","contact_phone","contact_post","department_top","department","sea_push","push_sea_date","xsy_id"]
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
    "customitem151": "industry_1",
    "customitem162": "industry_2",
    "customitem159": "contact",
    "dianhua": "contact_phone",
    "customItem161": "contact_post",
    # 部门转换
    "dimdepart": "department_top",
    "customitem156": "department",
    "customitem214": "sea_push",
    "customitem216": "push_sea_date",
    "yid":"xsy_id"
}
ACCOUNT_TABLE_STRING = """ALTER table `{}` 
                    MODIFY column `id` varchar(100)  COMMENT '星光自建客户id',
                    MODIFY column `crm_id` varchar(20) COMMENT '销售易客户ID ',
                    MODIFY column `entity_type` varchar(20) COMMENT '客户类型(客户，代理商）',
                    MODIFY column `owner_id` varchar(50) COMMENT '对应星光自建销售id',
                    MODIFY column `account_name` varchar(255) COMMENT '客户名称',
                    MODIFY column `level` varchar(10) COMMENT '客户级别（开发客户、重点客户、正式客户）',
                    MODIFY column `sea_status` varchar(20) COMMENT '公海状态',
                    MODIFY column `longitude` varchar(100) COMMENT '经度',
                    MODIFY column `latitude` varchar(100) COMMENT '纬度',
                    MODIFY column `address` text COMMENT '地址',
                    MODIFY column `address_province` varchar(255) COMMENT '省',
                    MODIFY column `address_city` varchar(255) COMMENT '市',
                    MODIFY column `address_area` varchar(255) COMMENT '区',
                    MODIFY column `recent_activity_time` varchar(20) COMMENT '最新活动记录',
                    MODIFY column `recent_activity_by` varchar(50) COMMENT '最新跟进人 对应星光新建销售id',
                    MODIFY column `sea_id` varchar (50) COMMENT '所属公海',
                    MODIFY column `created_at` varchar(50) COMMENT '创建日期',
                    MODIFY column `created_by` varchar(50) COMMENT '创建人',
                    MODIFY column `updated_at` varchar(50) COMMENT '最新修改日',
                    MODIFY column `updated_by` varchar(50) COMMENT '最新修改人  对应星光新建销售id',
                    MODIFY column `industry_1` varchar(255) COMMENT '一级行业',
                    MODIFY column `industry_2` varchar(255) COMMENT '二级行业',
                    MODIFY column `contact` varchar(255) COMMENT '联系人',
                    MODIFY column `contact_phone` varchar(255) COMMENT '联系电话',
                    MODIFY column `contact_post` varchar(255) COMMENT '联系职务',
                    MODIFY column `department_top` varchar(20) COMMENT '所属事业部  对应星光自建部门id',
                    MODIFY column `department` varchar(20) COMMENT '客户所属部门  对应星光自建部门id',
                    MODIFY column `sea_push` varchar(20) COMMENT '是否为公海池推送客户',
                    MODIFY column `push_sea_date` varchar(20) COMMENT '公海池推送时间' """




USER_API_NAME="Ccuser"
USER_SQL_TABLE="user_back"
USER_DICT={
    "id":"crm_id",
    "name":"username",
    "department":"department_id",
    "isusing":"status",
    "createdate":"hire_date",
    "email":"email",
}
USER_TABLE_STRING = """ALTER table `{}`
                MODIFY column `id` varchar(100) COMMENT "星光自建 用户id",
                MODIFY column `crm_id` varchar(100) COMMENT "crm 用户id",
                MODIFY column `username` varchar(50) COMMENT "用户名称",
                MODIFY column `department_id` varchar(50) COMMENT "部门id",
                MODIFY column `status` tinyint(5) COMMENT "是否在职 1在职 0离职",
                MODIFY column `hire_date` varchar(100) COMMENT "入职时间ms",
                MODIFY column `email` varchar(100) COMMENT "邮箱" """
# api 名称
OPPORTUNITY_API_NAME = "Opportunity"
# 数据库名称
OPPORTUNITY_SQL_TABLE = "opportunity_back"
# 入库顺序
OPPORTUNITY_CLOUMNS_ORDER = ["id","crm_id","entity_type","opportunity_name","owner_id","price_id","account_id","money","intended_product","sale_stage","win_rate","close_date","saler_promise","project_budget","created_by","created_at","updated_by","updated_at","contact","position","phone","xsy_id"]
# api 与数据库字段映射关系
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
    "customitem165": "contact",
    "customitem166": "position",
    "customitem222":"phone",
    "yid": "xsy_id"
}
# 数据库类型格式
OPPORTUNITY_TABLE_STRING = """ALTER table `{}`
                  MODIFY `id` varchar(50) COMMENT '星光自建商机id',
                  MODIFY `crm_id` varchar(50) COMMENT 'crm商机id',
                  MODIFY `entity_type` varchar(20) COMMENT '业务类型',
                  MODIFY `opportunity_name` varchar(500) COMMENT '商机名称',
                  MODIFY `owner_id` varchar (100) COMMENT '星光自建销售id',
                  MODIFY `price_id` varchar(50) COMMENT '价格表id',
                  MODIFY `account_id` varchar(100) COMMENT '最终客户id ',
                  MODIFY `money` varchar(50) COMMENT '商机金额',
                  MODIFY `intended_product` varchar(500) COMMENT '意向产品',
                  MODIFY `sale_stage` varchar(50) COMMENT '销售阶段',
                  MODIFY `win_rate` varchar (10) COMMENT '赢率',
                  MODIFY `close_date` varchar(50) COMMENT '结单日期',
                  MODIFY `saler_promise` varchar(50) COMMENT '销售承诺',
                  MODIFY `project_budget` varchar(255) COMMENT '成本预算',
                  MODIFY `created_at` varchar(50) COMMENT '创建日期',
                  MODIFY `created_by` varchar(50) COMMENT '创建人',
                  MODIFY `updated_at` varchar(50) COMMENT '最新修改日期',
                  MODIFY `updated_by` varchar(50) COMMENT '最新修改人',
                  MODIFY `contact` varchar(100) COMMENT '商机联系人',
                  MODIFY `position` text COMMENT '联系人职务',
                  MODIFY `phone` varchar(100) COMMENT '电话',
                  MODIFY `xsy_id` text COMMENT '销售易id' """





ORDER_DETAIL_API_NAME="ddmx"
ORDER_DETAIL_SQL_TABLE="order_detail_back"
ORDER_DETAIL_CLOUMNS_ORDER = ["id","crm_id","order_id","owner_id","name","contract_status","attribute","product_id","contract_back_date","performance","account_id","amount","server_start","server_end","contract_end","created_by","created_at","updated_by","updated_at","xsy_id"]
ORDER_DETAIL_DICT={
    "id":"crm_id",
    "orderid":"order_id",
    "ownerid":"owner_id",
    # api 无po
    # "po":"po",
    "name":"name",
    "customitem162": "contract_status",
    "customitem156": "attribute",
    "productid":"product_id",
    "customitem163":"contract_back_date",
    "customitem125": "performance",
    "zzkhmc":"account_id",
    "customitem183":"amount",
    "customitem129":"server_start",
    "customitem130": "server_end",
    "customitem187": "contract_end",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
    "yid":"xsy_id",
}
ORDER_DETAIL_TABLE_STRING = """ALTER table `{}`
                  MODIFY `id` varchar(50) COMMENT 'id',
                  MODIFY `crm_id` varchar(50) COMMENT 'crm id   orderproduct 表中id',
                  MODIFY `order_id` varchar(50) COMMENT '星光自建订单id',
                  MODIFY `name` varchar(255) COMMENT '序号',
                  MODIFY `contract_status` varchar(50) COMMENT '合同状态',
                  MODIFY `attribute` varchar(50) COMMENT '属性 1新单 2续单',
                  MODIFY `product_id` varchar(50) COMMENT '产品id',
                  MODIFY `contract_back_date` varchar(50) COMMENT '合同归档日期',
                  MODIFY `performance` varchar(100) COMMENT '业绩核算金额',
                  MODIFY `owner_id` varchar(50) COMMENT '订单所属销售,星光自建销售id',
                  MODIFY `account_id` varchar(50) COMMENT '客户id',
                  MODIFY `amount` varchar(50) COMMENT '订单总金额',
                  MODIFY `server_start` varchar(50) COMMENT '服务开始日期',
                  MODIFY `server_end` varchar(50) COMMENT '服务结束日期',
                  MODIFY `contract_end` varchar(50) COMMENT '最终合同截止日期', 
                  MODIFY `created_at` varchar(50) COMMENT '创建日期', 
                  MODIFY `created_by` varchar(50) COMMENT '创建人', 
                  MODIFY `updated_at` varchar(50) COMMENT '更新日期', 
                  MODIFY `updated_by` varchar(50) COMMENT '更新人', 
                  MODIFY `xsy_id` varchar(50) COMMENT '销售易id'  """