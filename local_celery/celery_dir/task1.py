#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 10:09
# 工具：PyCharm
# Python版本：3.7.0

import time
from celery_dir import celery_app


@celery_app.task
def add(x, y):
    time.sleep(2)
    return x + y