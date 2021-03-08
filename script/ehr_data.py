#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-07 10:29:51
# @Author  : ztf (itwhboy@gmail.com)
# @Link    : https://www.baidu.com
# @Version : $Id$

import sys,os
path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

import requests
import json
import pandas as pd
# import config
import hashlib
from public.utils import engine
from settings.settings import db_new_data


class HR(object):
    """易路蓝图数据接口类"""
    def get_employees_t_with_zone(self):
        """人员信息接口"""
        url = 'https://zhxg.peoplus.cn/pull_api/get_employees_t_with_zone'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'data': {'lang': 'zh_CN'}
        }
        data = json.dumps(data)
        result = requests.post(url, data=data, headers=headers)
        return json.loads(result.text)

    def get_departments_with_zone(self):
        """组织信息接口"""
        url = 'https://zhxg.peoplus.cn/pull_api/get_departments_with_zone'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'data': {'lang': 'zh_CN'}
        }
        data = json.dumps(data)
        result = requests.post(url, data=data, headers=headers)
        return json.loads(result.text)

    def get_positions_with_zone(self):
        """岗位信息接口"""
        url = 'https://zhxg.peoplus.cn/pull_api/get_positions_with_zone'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'data': {'lang': 'zh_CN'}
        }
        data = json.dumps(data)
        result = requests.post(url, data=data, headers=headers)
        return json.loads(result.text)


if __name__ == '__main__':
    hr = HR()
    engine_xgyypt =engine(db_new_data)
    # 同步人员信息
    employees = hr.get_employees_t_with_zone()
    employees_df = pd.DataFrame(employees['result']['data']['query_data'][1:], columns=employees['result']['data']['query_data'][0])
    employees_table = employees['result']['data']['model']
    if len(employees_df) > 800:
        unique_list = []
        for index, row in employees_df.iterrows():
            data = row['hiredate'] + row['identification_id']
            hash = hashlib.md5(data.encode('utf-8'))
            unique_list.append(hash.hexdigest())
        employees_df['istarshine_id'] = unique_list
        employees_df.to_sql(employees_table, engine_xgyypt, if_exists='replace', index=False)
    # 修改人员表字段
    employees_update = (
        """
            ALTER table `{}`
            MODIFY column `employee_number` bigint(20) PRIMARY KEY NOT NULL COMMENT '员工编号',
            CHANGE column `name` employee_name varchar(100) DEFAULT NULL COMMENT '员工姓名',
            MODIFY column `work_activity` varchar(100) DEFAULT NULL COMMENT '员工状态',
            MODIFY column `hiredate` varchar(50) DEFAULT NULL COMMENT '入职日期',
            MODIFY column `departure_time` varchar(50) DEFAULT  NULL COMMENT '离职日期',
            MODIFY column `work_email` varchar(100) DEFAULT NULL COMMENT '工作邮件',
            MODIFY column `work_phone` varchar(20) DEFAULT NULL COMMENT '工作电话',
            MODIFY column `dingtalk_account` varchar(100) DEFAULT NULL COMMENT '钉钉USERID',
            CHANGE column `department_id.department_code` department_code varchar(100) DEFAULT NULL COMMENT '组织单元代码',
            CHANGE column `department_id.name` department_name varchar(100) DEFAULT NULL COMMENT '组织单元名称',
            CHANGE column `job_id.job_code` job_code varchar(100) DEFAULT NULL COMMENT '岗位代码',
            CHANGE column `job_id.name` job_name varchar(100) DEFAULT NULL COMMENT '岗位名称',
            MODIFY column `identification_id` varchar(100) DEFAULT NULL COMMENT '证件号码',
            MODIFY column `istarshine_id` varchar(50) DEFAULT NULL COMMENT '唯一ID'
        """.format(employees_table))
    engine_xgyypt.execute(employees_update)
    # 同步组织信息
    departments = hr.get_departments_with_zone()
    departments_df = pd.DataFrame(departments['result']['data']['query_data'][1:], columns=departments['result']['data']['query_data'][0])
    departments_table = departments['result']['data']['model']
    if len(departments_df) > 100:
        departments_df.to_sql(departments_table, engine_xgyypt, if_exists='replace', index=False)
    # 修改组织表字段
    departments_update = (
        """
            ALTER table `{}`
            MODIFY column `department_code` varchar(100) PRIMARY KEY NOT NULL COMMENT '组织单元编号',
            CHANGE column `name` department_name varchar(100) DEFAULT NULL COMMENT '组织单元名称',
            CHANGE column `parent_id.department_code` parent_code varchar(100) DEFAULT NULL COMMENT '上级组织单元编码',
            CHANGE column `parent_id.name` parent_name varchar(100) DEFAULT NULL COMMENT '组织单元名称',
            MODIFY column `active` TINYINT(1) DEFAULT NULL COMMENT '有效'
        """.format(departments_table))
    engine_xgyypt.execute(departments_update)
    # 同步岗位信息
    positions = hr.get_positions_with_zone()
    positions_df = pd.DataFrame(positions['result']['data']['query_data'][1:], columns=positions['result']['data']['query_data'][0])
    positions_table = positions['result']['data']['model']
    if len(positions_df) > 300:
        positions_df.to_sql(positions_table, engine_xgyypt, if_exists='replace', index=False)
    # 修改组织表字段
    positions_update = (
        """
            ALTER table `{}`
            MODIFY column `job_code` varchar(100) PRIMARY KEY NOT NULL COMMENT '岗位编号',
            CHANGE column `name` job_name varchar(100) DEFAULT NULL COMMENT '岗位名称',
            MODIFY column `active` TINYINT(1) DEFAULT NULL COMMENT '有效'
        """.format(positions_table))
    engine_xgyypt.execute(positions_update)
