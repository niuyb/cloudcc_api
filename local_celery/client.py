#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/20 10:04
# 工具：PyCharm
# Python版本：3.7.0


from celery_dir import task1
from celery_dir import task2

task1.add.apply_async(args=[2, 8])        # 也可用 task1.add.delay(2, 8)
task2.multiply.apply_async(args=[3, 7])   # 也可用 task2.multiply.delay(3, 7)

print('hello world')