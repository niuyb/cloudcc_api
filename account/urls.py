#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/16 9:55
# 工具：PyCharm
# Python版本：3.7.0

from django.urls import re_path, path

from account import views
app_name ="account"

urlpatterns = [
    re_path(r'^api', views.account_api.as_view(), name="account_api"),
    # re_path(r'^data/customer/all$', views.get_data_customer_all, name="data_customer_all"),
]