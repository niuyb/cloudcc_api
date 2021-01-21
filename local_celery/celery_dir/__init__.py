#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 10:07
# 工具：PyCharm
# Python版本：3.7.0

from celery import Celery

"""
celery 此处当前主要负责被动更新功能,让接口返回更快,异步更新数据库
文件根目录是 local_celery

"""

celery_app = Celery('cloudcc_api')                                # 创建 Celery 实例
celery_app.config_from_object('local_celery.celery_dir.celery_config')   # 通过 Celery 实例加载配置模块