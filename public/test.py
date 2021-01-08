#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/1/5 9:54
# 工具：PyCharm
# Python版本：3.7.0

# python 2
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# python 3
# import sys
# import importlib
# importlib.reload(sys)
import datetime

from public.utils import engine
from settings import settings
import pandas as pd




a = (datetime.datetime.now()-datetime.timedelta(hours=1.5)).strftime('%Y-%m-%d')
print(a)