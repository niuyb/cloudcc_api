#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 10:08
# 工具：PyCharm
# Python版本：3.7.0


# redis://:password@hostname:port/db_number
BROKER_URL = 'redis://192.168.185.129:6379/1'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://192.168.185.129:6379/2'  # 指定 Backend

CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC
# CELERY_TIMEZONE='UTC'

CELERY_TASK_RESULT_EXPIRES= 30*60

CELERY_IMPORTS = (                                  # 指定导入的任务模块
    'local_celery.celery_dir.task1',
    'local_celery.celery_dir.task2'
)