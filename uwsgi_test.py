#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/21 15:52
# 工具：PyCharm
# Python版本：3.7.0

# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]