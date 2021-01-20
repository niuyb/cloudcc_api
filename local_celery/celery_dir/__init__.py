#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 10:07
# 工具：PyCharm
# Python版本：3.7.0

from celery import Celery

celery_app = Celery('demo')                                # 创建 Celery 实例
celery_app.config_from_object('celery_dir.celery_config')   # 通过 Celery 实例加载配置模块