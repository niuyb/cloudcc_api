#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/28 17:43
# 工具：PyCharm
# Python版本：3.7.0

ORDER_API_NAME="dingdan"
ORDER_SQL_TABLE="order_back"
ORDER_CLOUMNS_ORDER = ["id","crm_id","po","owner_id","status","account_name","account_id","price_id","opportunity_id","created_by","created_at","updated_by","updated_at","amount","discount_amount","contract_status","contract_attribute","contract_id","payment_type","contract_start","contract_end","contract_server_end","contract_back_date","total_performance","approve_date","payback_type","xsy_id","contract_abnormal_status","order_manager"]
ORDER_DICT={
    "id":"crm_id",
    "name":"po",
    "ownerid":"owner_id",
    "poStatus":"status",
    "accountId":"account_name",
    "zzkh":"account_id",
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
    "customitem160": "payment_type",
    "customitem147": "contract_start",
    "customitem148": "contract_end",
    "customitem174": "contract_server_end",
    "customitem156": "contract_back_date",
    "customitem164": "total_performance",
    "customitem182": "approve_date",
    "customitem294": "payback_type",
    "customitem184": "order_manager",
    "customitem210": "contract_abnormal_status",
    "yid":"xsy_id",
}
ORDER_TABLE_STRING="""ALTER table `{}`
      MODIFY `id` varchar(50) COMMENT '星光自建订单id',
      MODIFY `crm_id` varchar(50) COMMENT 'crm 订单id',
      MODIFY `po` varchar(50) COMMENT '流水号',
      MODIFY `owner_id` varchar(50) COMMENT '销售负责人 对应星光salerid',
      MODIFY `status` varchar(20) COMMENT '订单状态',
      MODIFY `account_name` varchar(50) COMMENT '客户id',
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
      MODIFY `contract_abnormal_status` varchar(20) COMMENT '合同异常状态',
      MODIFY `contract_attribute` varchar(10) COMMENT '合同属性 1新签 2续签',
      MODIFY `contract_id` varchar(50) COMMENT '合同编号',
      MODIFY `payment_type` varchar(50) COMMENT '回款方式',
      MODIFY `contract_start` varchar(50) COMMENT '合同开始日期',
      MODIFY `contract_end` varchar(50) COMMENT '合同结束日期',
      MODIFY `contract_server_end` varchar(50) COMMENT '最终合同截止日期',
      MODIFY `contract_back_date` varchar(50) COMMENT '合同归档日期',
      MODIFY `total_performance` varchar(50) COMMENT '业绩核算(成本）总额',
      MODIFY `approve_date` varchar(50) COMMENT '审批通过时间',
      MODIFY `payback_type` varchar(20) COMMENT '回款计划类型',
      MODIFY `order_manager` varchar(50) COMMENT '订单实际负责人 业绩负责人',
      MODIFY `xsy_id` varchar(20) COMMENT '销售易id' """





# 数据库名称
ACCOUNT_API_NAME = "Account"
ACCOUNT_SQL_TABLE = "account_back"
ACCOUNT_CLOUMNS_ORDER = ["id","crm_id","entity_type","account_name","owner_id","level","sea_status","longitude","address","address_province","address_city","address_area","recent_activity_time","recent_activity_by","sea_id","created_by","created_at","updated_by","updated_at","industry_1","industry_2","contact","contact_phone","contact_post","department_top","department","sea_push","push_sea_date","xsy_id","zw_back_url","qy_back_url"]
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
    "zwyhxwfx":"zw_back_url",
    "customitem178": "qy_back_url",
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
                    MODIFY column `push_sea_date` varchar(20) COMMENT '公海池推送时间',
                    MODIFY column `xsy_id` varchar(50) COMMENT '销售易id',
                    MODIFY column `zw_back_url` text COMMENT '政务用户行为分析',
                    MODIFY column `qy_back_url` text COMMENT '企业用户行为分析' """




USER_API_NAME="Ccuser"
USER_SQL_TABLE="user_back"
USER_DICT={
    "id":"crm_id",
    "name":"username",
    "department":"department_id",
    "isusing":"status",
    "createdate":"hire_date",
    "role": "crm_role",
    "email":"email",
}
USER_TABLE_STRING = """ALTER table `{}`
                MODIFY column `id` varchar(100) COMMENT "星光自建 用户id",
                MODIFY column `crm_id` varchar(100) COMMENT "crm 用户id",
                MODIFY column `username` varchar(50) COMMENT "用户名称",
                MODIFY column `department_id` varchar(50) COMMENT "部门id",
                MODIFY column `status` tinyint(5) COMMENT "是否在职 1在职 0离职",
                MODIFY column `hire_date` varchar(100) COMMENT "入职时间ms",
                MODIFY column `crm_role` varchar(100) COMMENT "crm 角色",
                MODIFY column `department_name` varchar(100) COMMENT "部门名称",
                MODIFY column `email` varchar(100) COMMENT "邮箱" """
# api 名称
OPPORTUNITY_API_NAME = "Opportunity"
# 数据库名称
OPPORTUNITY_SQL_TABLE = "opportunity_back"
# 入库顺序
OPPORTUNITY_CLOUMNS_ORDER = ["id","crm_id","entity_type","type","opportunity_name","owner_id","price_id","account_name","account_id","money","intended_product","sale_stage","win_rate","close_date","saler_promise","project_budget","created_by","created_at","updated_by","updated_at","contact","position","phone","xsy_id","week_top","month_top","season_top","saler_per","opportunity_num","url","zw_back_url","qy_back_url"]
# api 与数据库字段映射关系
OPPORTUNITY_DICT = {
    "id": "crm_id",
    "ywlx": "entity_type",
    "name": "opportunity_name",
    "ownerid": "owner_id",
    "priceid": "price_id",
    "sjlx":"type",
    "khmc":"account_name",
    "zzkh": "account_id",
    "jine": "money",
    "customitem164": "intended_product",
    "jieduan": "sale_stage",
    "knx": "win_rate",
    "jsrq": "close_date",
    "customitem262": "saler_promise",
    "projectBudget": "project_budget",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
    "customitem165": "contact",
    "customitem166": "position",
    "customitem222":"phone",
    "yid": "xsy_id",
    "customitem267": "week_top",
    "customitem268": "month_top",
    "customitem269": "season_top",
    "sqfzr": "saler_per",
    "sjbh": "opportunity_num",
    "customitem231":"qy_back_url",
    "zwyhxwfx": "zw_back_url",
}

# 数据库类型格式
OPPORTUNITY_TABLE_STRING = """ALTER table `{}`
                  MODIFY `id` varchar(50) COMMENT '星光自建商机id',
                  MODIFY `crm_id` varchar(50) COMMENT 'crm商机id',
                  MODIFY `entity_type` varchar(20) COMMENT '业务类型',
                  MODIFY `type` varchar(20) COMMENT '业务类型',
                  MODIFY `opportunity_name` varchar(500) COMMENT '商机名称',
                  MODIFY `owner_id` varchar (100) COMMENT '星光自建销售id',
                  MODIFY `price_id` varchar(50) COMMENT '价格表id',
                  MODIFY `account_name` varchar(100) COMMENT '客户id',
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
                  MODIFY `xsy_id` text COMMENT '销售易id',
                  MODIFY `week_top` varchar(50) COMMENT '周top',
                  MODIFY `month_top` varchar(100) COMMENT '月top',
                  MODIFY `season_top` text COMMENT '季度top',
                  MODIFY `saler_per` varchar(100) COMMENT '	售前负责人',
                  MODIFY `opportunity_num` varchar(100) COMMENT '商机编号',
                  MODIFY `url` varchar(100) COMMENT '商机网址',
                  MODIFY `zw_back_url` text COMMENT '政务用户行为分析',
                  MODIFY `qy_back_url` text COMMENT '企业用户行为分析' """





ORDER_DETAIL_API_NAME="ddmx"
ORDER_DETAIL_SQL_TABLE="order_detail_back"
ORDER_DETAIL_CLOUMNS_ORDER = ["id","crm_id","order_id","owner_id","name","contract_status","attribute","product_id","contract_back_date","saler_amount","performance_acount","performance","account_id","amount","server_start","server_end","contract_end","created_by","created_at","updated_by","updated_at","xsy_id"]
ORDER_DETAIL_DICT={
    "id":"crm_id",
    "orderid":"order_id",
    "ownerid":"owner_id",
    # api 无po
    # "po":"po",
    "name":"name",
    # "customitem162": "contract_status",
    "customitem149": "attribute",
    "productid":"product_id",
    "ddmxxsje":"saler_amount",
    "yjifsr":"performance_acount",
    # contract_back_date 从order中关联
    # "customitem163":"contract_back_date",
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
                  MODIFY `performance_acount` varchar(50) COMMENT '业绩核算人',
                  MODIFY `performance` varchar(100) COMMENT '业绩核算金额',
                  MODIFY `saler_amount` varchar(100) COMMENT '销售金额',
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



PRODUCT_LINE_API_NAME="cpx"
PRODUCT_LINE_SQL_TABLE="product_line_back"
PRODUCT_LINE_CLOUMNS_ORDER = ["id","crm_id","name"]
PRODUCT_LINE_DICT={
    "id":"crm_id",
    "name":"name",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
PRODUCT_LINE_TABLE_STRING = """ALTER table `{}`
                          MODIFY `id` varchar(50) COMMENT '星光自建产品线id',
                          MODIFY `crm_id` varchar(50) COMMENT 'crm_产品线id',
                          MODIFY `name` varchar(200) COMMENT '产品线名',
                          MODIFY `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY `created_by` varchar(50) COMMENT '创建人', 
                          MODIFY `updated_at` varchar(50) COMMENT '更新日期', 
                          MODIFY `updated_by` varchar(50) COMMENT '更新人' """


PRODUCT_API_NAME="Product"
PRODUCT_SQL_TABLE="product_back"
PRODUCT_CLOUMNS_ORDER = ["id","crm_id","name"]
PRODUCT_DICT={
    "id":"crm_id",
    "name":"product_name",
    "cpdj": "price_unit",
    "customitem147": "product_line",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
PRODUCT_TABLE_STRING= """ALTER table `{}` 
                          MODIFY `id` varchar(100) COMMENT 'id',
                          MODIFY `crm_id` varchar(100) COMMENT 'crm_产品id',
                          MODIFY `product_name` varchar(255) COMMENT '产品名称',
                          MODIFY `price_unit` varchar(255) COMMENT '标准价',
                          MODIFY `product_line` varchar(255) COMMENT '产品线(实体)',
                          MODIFY `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY `created_by` varchar(50) COMMENT '创建人', 
                          MODIFY `updated_at` varchar(50) COMMENT '更新日期', 
                          MODIFY `updated_by` varchar(50) COMMENT '更新人' """

# ORDER_CHANGE
ORDER_CHANGE_API_NAME="ddbg"
ORDER_CHANGE_SQL_TABLE="order_change"
ORDER_CHANGE_CLOUMNS_ORDER = ["id","crm_id" ,"owner_id","status" ,"department","content" ,"order_id","changed_at","contract_money" ,"changed_money" ,"performance","changed_performance","changed_type","created_at","created_by","updated_at","updated_by"]
ORDER_CHANGE_DICT={
    "id":"crm_id",
    "ownerid":"owner_id",
    "customitem1":"order_id",
    "customitem10": "changed_at",
    "customitem18": "contract_money",
    "customitem19": "changed_money",
    "customitem20":"performance",
    "customitem21": "changed_performance",
    "customitem4": "changed_type",
    "spzt": "status",
    "ssbm": "department",
    "customitem5": "content",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
ORDER_CHANGE_TABLE_STRING= """ALTER table `{}` 
                          MODIFY `id` varchar(100) COMMENT 'id',
                          MODIFY `crm_id` varchar(100) COMMENT 'crm_订单变更id',
                          MODIFY `owner_id` varchar(255) COMMENT '所有人id',
                          MODIFY `status` varchar(255) COMMENT '审批状态',
                          MODIFY `department` varchar(255) COMMENT '所有人部门',
                          MODIFY `content` text COMMENT '变更后内容', 
                          MODIFY `order_id` varchar(50) COMMENT '订单id', 
                          MODIFY `changed_at` varchar(50) COMMENT '审批通过时间', 
                          MODIFY `contract_money` varchar(100) COMMENT '变更前合同金额',
                          MODIFY `changed_money` varchar(255) COMMENT '变更后合同金额（元）',
                          MODIFY `performance` varchar(255) COMMENT '变更前实际金额（元）',
                          MODIFY `changed_performance` varchar(255) COMMENT '变更后实际金额（元）',
                          MODIFY `changed_type` varchar(50) COMMENT '变更类型', 
                          MODIFY `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY `created_by` varchar(50) COMMENT '创建人', 
                          MODIFY `updated_at` varchar(50) COMMENT '更新日期', 
                          MODIFY `updated_by` varchar(50) COMMENT '更新人' """




# ORDER_CHANGE
PAYMENT_PLAN_API_NAME="hkjh"
PAYMENT_PLAN_SQL_TABLE="payment_plan"
PAYMENT_PLAN_CLOUMNS_ORDER = ["id","crm_id","name","owner_id","order_id","industry_l1","inform_date","dunning_num","dunning_team_record","dunning_record_date","dunning_team_owner","level","payment_batch","payment_plan_review","paid_back_situation","remarks","contract","lawyer_letter_date","deduction_by","deduction_reason","deduction_date","deduction_progress","promise_payment_date","saler_promise_payment_date","is_agent","is_client","is_inform","dunning_owner","call_back_status","overdue_status","feedback_date","register_date","code","resigners_order","payment_date","payment_amount","litigation_decision","overdue_deal_date","dunning_reason","overdue_hand_over","overdue_deal","overdue_type","created_by","created_at","updated_by","updated_at"]
PAYMENT_PLAN_DICT={
    "id":"crm_id",
    "name":"name",
    "ownerid": "owner_id",
    "orderId":"order_id",
    "yjhy":"industry_l1",
    "cghfsrq":"inform_date",
    # "chkx":"call_back",
    "ckhbh":"dunning_num",
    "csxzgt":"dunning_team_record",
    "ckxzgtjlgxsj":"dunning_record_date",
    "ckxzfzer11":"dunning_team_owner",
    "swbgjjb":"level",
    # "hkyyqts":"overdue_date",
    "hkqc":"payment_batch",
    # "actualAmount":"payment_actual_money",
    "hkjhsfsh":"payment_plan_review",
    # "hkjhwhkje":"count_unpaid_amount",
    "hbqk":"paid_back_situation",
    "beizhu":"remarks",
    "customit12":"contract",
    "lshfsrq":"lawyer_letter_date",
    # 所属部门
    "kkty":"deduction_by",
    "kkyy":"deduction_reason",
    "kkrq":"deduction_date",
    "kfjz":"deduction_progress",
    "cnhkrqsd":"promise_payment_date",
    "cnhkrq":"saler_promise_payment_date",
    "sfdls":"is_agent",
    "sfgskh":"is_client",
    "sfyfcgh":"is_inform",
    "bqckfzr":"dunning_owner",
    "bqhkzt":"call_back_status",
    "bqyqzt":"overdue_status",
    "bcfkrqbt":"feedback_date",
    "larq":"register_date",
    "code":"code",
    "rwlzrydd":"resigners_order",
    "planTime":"payment_date",
    "amount":"payment_amount",
    "sssxpdjcs":"litigation_decision",
    "yqclbfgxsj":"overdue_deal_date",
    "yqwhkxxyy":"dunning_reason",
    "yqkxjj":"overdue_hand_over",
    "yqkxclbf":"overdue_deal",
    "yqlx":"overdue_type",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}

""" 'hkjhwhkje', 'actualAmount', 'chkx', 'hkyyqts' 
                                MODIFY column `overdue_date` varchar(50) COMMENT '回款已逾期天数', 
                                MODIFY column `count_unpaid_amount` varchar(50) COMMENT '回款计划未回款金额（计算）', 
                                MODIFY column `call_back` varchar(50) COMMENT '催回款项', 
                                MODIFY column `payment_actual_money` varchar(50) COMMENT '回款计划实际回款金额', 

"""

PAYMENT_PLAN_TABLE_STRING= """ALTER table `{}` 
                                MODIFY column `id` varchar(50) COMMENT 'id', 
                                MODIFY column `crm_id` varchar(50) COMMENT 'crm_id', 
                                MODIFY column `name` varchar(50) COMMENT '回款计划编号', 
                                MODIFY column `owner_id` varchar(50) COMMENT '回款计划所有人', 
                                MODIFY column `order_id` varchar(50) COMMENT '订单id', 
                                MODIFY column `industry_l1` varchar(50) COMMENT '一级行业', 
                                MODIFY column `inform_date` varchar(50) COMMENT '催告函发送日期', 
                                MODIFY column `dunning_num` varchar(50) COMMENT '催款函编号', 
                                MODIFY column `dunning_team_record` varchar(50) COMMENT '催款小组沟通记录', 
                                MODIFY column `dunning_record_date` varchar(50) COMMENT '催款小组沟通记录更新时间', 
                                MODIFY column `dunning_team_owner` varchar(50) COMMENT '催款小组负责人', 
                                MODIFY column `level` varchar(50) COMMENT '商务部跟进级别', 
                                MODIFY column `payment_batch` varchar(50) COMMENT '回款期次', 
                                MODIFY column `payment_plan_review` varchar(50) COMMENT '回款计划是否审核', 
                                MODIFY column `paid_back_situation` varchar(50) COMMENT '回补情况', 
                                MODIFY column `remarks` text COMMENT '备注', 
                                MODIFY column `contract` text COMMENT '客户联系人、联系方式、详细地址（申请发送律师函必填项）', 
                                MODIFY column `department` varchar(50) COMMENT '所属部门', 
                                MODIFY column `lawyer_letter_date` varchar(50) COMMENT '律师函发送日期', 
                                MODIFY column `deduction_by` varchar(50) COMMENT '扣款人员', 
                                MODIFY column `deduction_reason` varchar(50) COMMENT '扣款原因', 
                                MODIFY column `deduction_date` varchar(50) COMMENT '扣款日期', 
                                MODIFY column `deduction_progress` varchar(50) COMMENT '扣费进展（未回款的5%）', 
                                MODIFY column `promise_payment_date` varchar(50) COMMENT '承诺回款日期锁定（逾期扣费依据）', 
                                MODIFY column `saler_promise_payment_date` varchar(50) COMMENT '承诺回款日期（销售填写）', 
                                MODIFY column `is_agent` varchar(50) COMMENT '是否代理商', 
                                MODIFY column `is_client` varchar(50) COMMENT '是否公司客户', 
                                MODIFY column `is_inform` varchar(50) COMMENT '是否已发催告函', 
                                MODIFY column `dunning_owner` varchar(50) COMMENT '本期催款负责人（必填）', 
                                MODIFY column `call_back_status` varchar(50) COMMENT '本期回款状态', 
                                MODIFY column `overdue_status` varchar(50) COMMENT '本期逾期状态', 
                                MODIFY column `feedback_date` varchar(50) COMMENT '本次反馈日期（必填）', 
                                MODIFY column `register_date` varchar(50) COMMENT '立案日期', 
                                MODIFY column `code` varchar(50) COMMENT '编号', 
                                MODIFY column `resigners_order` varchar(50) COMMENT '若为离职人员订单（填写离职人员姓名）', 
                                MODIFY column `payment_date` varchar(50) COMMENT '计划回款日期', 
                                MODIFY column `payment_amount` varchar(50) COMMENT '计划回款金额', 
                                MODIFY column `litigation_decision` varchar(50) COMMENT '诉讼时效判定及措施', 
                                MODIFY column `overdue_deal_date` varchar(50) COMMENT '逾期处理办法更新时间', 
                                MODIFY column `dunning_reason` text COMMENT '逾期未回款详细原因（申请发送律师函必填项）', 
                                MODIFY column `overdue_hand_over` varchar(50) COMMENT '逾期款项交接', 
                                MODIFY column `overdue_deal` varchar(50) COMMENT '逾期款项处理办法', 
                                MODIFY column `overdue_type` varchar(50) COMMENT '逾期类型（必填）', 
                                MODIFY column `created_at` varchar(50) COMMENT '创建日期', 
                                MODIFY column `created_by` varchar(50) COMMENT '创建人', 
                                MODIFY column `updated_at` varchar(50) COMMENT '更新日期', 
                                MODIFY column `updated_by` varchar(50) COMMENT '更新人' """





# ORDER_CHANGE
PAYMENT_RECORD_API_NAME="hkjl"
PAYMENT_RECORD_SQL_TABLE="payment_record"
PAYMENT_RECORD_CLOUMNS_ORDER = ["id","crm_id","name","owner_id","contract_id","contract_status","overdue_date","payment_batch","payment_plan_id","remarks","actual_payment_date","actual_payment_amount","back_date","code","payment_date","payment_amount","order_id","order_actual_owner","order_owner","created_by","created_at","updated_by","updated_at"]
PAYMENT_RECORD_DICT={
    "id":"crm_id",
    "name":"name",
    "ownerid":"owner_id",
    "contractid":"contract_id",
    "htzt":"contract_status",
    # "htbh1":"contract_num",
    "customitem150":"overdue_date",
    "hkqc":"payment_batch",
    "hkjh":"payment_plan_id",
    "cloudcctag": "remarks",
    "actualTime":"actual_payment_date",
    "amount":"actual_payment_amount",
    "accountId":"account_id",
    "gdrq":"back_date",
    # 所属部门
    "code":"code",
    "jhhkrq":"payment_date",
    "jhhkje":"payment_amount",
    "orderId":"order_id",
    "ddsjfzr":"order_actual_owner",
    "ddsyr":"order_owner",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
"""
MODIFY column `contract_num` varchar(50) COMMENT '合同编号',

"""
PAYMENT_RECORD_TABLE_STRING= """ALTER table `{}` 
                                MODIFY column `id` varchar(50) COMMENT 'id',
                                MODIFY column `crm_id` varchar(50) COMMENT 'crm_id',
                                MODIFY column `name` varchar(50) COMMENT '回款记录',
                                MODIFY column `owner_id` varchar(50) COMMENT '所有人',
                                MODIFY column `contract_id` varchar(50) COMMENT '合同',
                                MODIFY column `contract_status` varchar(50) COMMENT '合同状态',
                                MODIFY column `overdue_date` varchar(50) COMMENT '回款已逾期天数',
                                MODIFY column `payment_batch` varchar(50) COMMENT '回款期次',
                                MODIFY column `payment_plan_id` varchar(50) COMMENT '回款计划id',
                                MODIFY column `remarks` varchar(50) COMMENT '备注',
                                MODIFY column `actual_payment_date` varchar(50) COMMENT '实际回款日期',
                                MODIFY column `actual_payment_amount` varchar(50) COMMENT '实际回款金额',
                                MODIFY column `account_id` varchar(50) COMMENT '客户名称',
                                MODIFY column `back_date` varchar(50) COMMENT '归档日期',
                                MODIFY column `department` varchar(50) COMMENT '所属部门',
                                MODIFY column `code` varchar(50) COMMENT '编号',
                                MODIFY column `payment_date` varchar(50) COMMENT '计划回款日期',
                                MODIFY column `payment_amount` varchar(50) COMMENT '计划回款金额',
                                MODIFY column `order_id` varchar(50) COMMENT '订单',
                                MODIFY column `order_actual_owner` varchar(50) COMMENT '订单实际负责人',
                                MODIFY column `order_owner` varchar(50) COMMENT '订单所有人',
                                MODIFY column `created_at` varchar(50) COMMENT '创建日期', 
                                MODIFY column `created_by` varchar(50) COMMENT '创建人', 
                                MODIFY column `updated_at` varchar(50) COMMENT '更新日期', 
                                MODIFY column `updated_by` varchar(50) COMMENT '更新人' """




ACTIVITY_API_NAME="Activity"
ACTIVITY_SQL_TABLE="activity"
ACTIVITY_CLOUMNS_ORDER = ["id","crm_id","name"]
ACTIVITY_DICT={
    "id":"crm_id",
    "name":"name",
    "subject":"subject",
    "relateobj":"object_type",
    "relateid": "object_id",
    "remark":"remark",
    "ownerid":"owner_id",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
ACTIVITY_TABLE_STRING = """ALTER table `{}`
                          MODIFY column `id` varchar(50) COMMENT '星光自建 activity id',
                          MODIFY column `crm_id` varchar(50) COMMENT 'crmid',
                          MODIFY column `name` text COMMENT 'name',
                          MODIFY column `subject` varchar(100) COMMENT '类型名称',
                          MODIFY column `object_type` varchar(100) COMMENT '对象类型 1客户2商机',
                          MODIFY column `object_id` varchar(100) COMMENT '对象id',
                          MODIFY column `remark` text COMMENT '备注',
                          MODIFY column `owner_id` varchar(200) COMMENT '所属人',
                          MODIFY column `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY column `created_by` varchar(50) COMMENT '创建人', 
                          MODIFY column `updated_at` varchar(50) COMMENT '更新日期', 
                          MODIFY column `updated_by` varchar(50) COMMENT '更新人' """




OPPORTUNITY_DETAIL_API_NAME="sjmx"
OPPORTUNITY_DETAIL_SQL_TABLE="opportunity_detail"
OPPORTUNITY_DETAIL_CLOUMNS_ORDER = ["id","crm_id","owner_id","name","product_id","amount","opportunity_id","price_amount","price_unit","price_id","price_total","close_date","created_by","created_at","updated_by","updated_at"]
OPPORTUNITY_DETAIL_DICT={
    "id":"crm_id",
    "name":"name",
    "ownerid":"owner_id",
    # "cp":"product_id",
    "amount":"amount",
    "opportunityId":"opportunity_id",
    "standardPrice":"price_amount",
    "cpmc":"product_id",
    "priceUnit":"price_unit",
    # "priceTotal":"price_total",
    # "discount":"discount",
    "jgb":"price_id",
    # "discountOff":"discount_off",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
OPPORTUNITY_DETAIL_TABLE_STRING = """ALTER table `{}`
                          MODIFY column `id` varchar(50) COMMENT '星光自建 activity id',
                          MODIFY column `crm_id` varchar(50) COMMENT 'crmid',
                          MODIFY column `owner_id` varchar(50) COMMENT '所有人',
                          MODIFY column `name` text COMMENT '编号',
                          MODIFY column `amount` varchar(100) COMMENT '	数量',
                          MODIFY column `opportunity_id` varchar(100) COMMENT '	商机id',
                          MODIFY column `price_amount` varchar(100) COMMENT '价格表价格',
                          MODIFY column `product_id` varchar(100) COMMENT '	产品名称',
                          MODIFY column `price_unit` varchar(100) COMMENT '	销售单价',
                          MODIFY column `price_id` varchar(100) COMMENT '	价格表',
                          MODIFY column `close_date` varchar(100) COMMENT '	结单日期',
                          MODIFY column `price_total` varchar(100) COMMENT '销售金额  price_unit * amount',
                          MODIFY column `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY column `created_by` varchar(50) COMMENT '创建人', 
                          MODIFY column `updated_at` varchar(50) COMMENT '更新日期', 
                          MODIFY column `updated_by` varchar(50) COMMENT '更新人' """





MICROPOST_API_NAME="getChatters01"
MICROPOST_SQL_TABLE="micropost"
MICROPOST_CLOUMNS_ORDER = ["id","crm_id","target_name","author_name","target_object","target_id","target_type","content","created_by","created_at","isdelete"]
MICROPOST_DICT={
    "id":"crm_id",
    "targetIdname":"target_name",
    "authorIdname":"author_name",
    "targetId":"target_id",
    "targetType":"target_type",
    "editBody":"content",
    "authorId": "created_by",
    "createDateTime1": "created_at",
    "isdelete":"isdelete",
}
MICROPOST_TABLE_STRING = """ALTER table `{}`
                          MODIFY column `id` varchar(50) COMMENT '星光自建 activity id',
                          MODIFY column `crm_id` varchar(50) COMMENT 'crmid',
                          MODIFY column `target_name` text COMMENT '目标名称',
                          MODIFY column `author_name` varchar(100) COMMENT '作者名称',
                          MODIFY column `target_object` varchar(20) COMMENT '目标业务类型',
                          MODIFY column `target_id` varchar(100) COMMENT '目标id',
                          MODIFY column `target_type` varchar(100) COMMENT '目标类型',
                          MODIFY column `content` text COMMENT '内容',
                          MODIFY column `isdelete` varchar(20) COMMENT '是否删除',
                          MODIFY column `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY column `created_by` varchar(50) COMMENT '创建人' """





# 销售负责人&提成信息
BONUS_API_NAME="sfzrtcxx"
BONUS_SQL_TABLE="bouns"
BONUS_CLOUMNS_ORDER = ["id","crm_id","name","order_id","bouns_person","percent","bouns_nums","created_by","created_at","updated_by","updated_at"]
BONUS_DICT={
    "id":"crm_id",
    "name":"name",
    "dingdan":"order_id",
    "customitem195":"bouns_person",
    "customitem197":"percent",
    "djtcr":"bouns_nums",
    "createbyid": "created_by",
    "createdate": "created_at",
    "lastmodifybyid": "updated_by",
    "lastmodifydate": "updated_at",
}
BONUS_TABLE_STRING = """ALTER table `{}`
                          MODIFY column `id` varchar(50) COMMENT '星光自建 bouns id',
                          MODIFY column `crm_id` varchar(50) COMMENT 'crmid',
                          MODIFY column `name` varchar(50) COMMENT '提成人编号',
                          MODIFY column `order_id` varchar(100) COMMENT '订单id',
                          MODIFY column `bouns_person` varchar(50) COMMENT '提成人',
                          MODIFY column `percent` varchar(100) COMMENT '提成人分配比例',
                          MODIFY column `bouns_nums` varchar(100) COMMENT '第几提成人',
                          MODIFY column `created_at` varchar(50) COMMENT '创建日期', 
                          MODIFY column `created_by` varchar(50) COMMENT '创建人', 
                          MODIFY column `updated_at` varchar(50) COMMENT '更新日期', 
                          MODIFY column `updated_by` varchar(50) COMMENT '更新人' """