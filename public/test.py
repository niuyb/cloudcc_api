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





import random  # 导入标准块的random

if __name__ == '__main__1':
    def get_random_code():
        checkcode = ''
        for i in range(4):  # 循环4次
            index = random.randrange(0, 3)  # 生成0-3中的一个数
            if index != i and index + 1 != i:
                checkcode += chr(random.randint(97, 122))  # 生成a-z中的一个小写字母
            elif index + 1 == i:
                checkcode += chr(random.randint(65, 90))  # 生成A-Z中的大写字母
            else:
                checkcode += str(random.randint(1, 9))  # 生成1-9的一个数字

        return checkcode

if __name__ == '__main__':
    import urllib
    from urllib import parse
    str1 = "鲁商置业+商情+新单"
    str2 = parse.quote(str1)  # quote()将字符串进行编码
    print(str2)
    rawurl = str2
    url = parse.unquote(rawurl)
    print (url)





if __name__ == "__main__2":
    def logging(level):
        def wrapper(func):
            def inner_wrapper(*args, **kwargs):
                print(args)
                print("[{level}]: enter function {func}()".format(level=level,func=func.__name__))
                return func(*args, **kwargs)

            return inner_wrapper

        return wrapper


    @logging(level='INFO')
    def say(something):
        print("say {}!".format(something))


    # 如果没有使用@语法，等同于
    # say = logging(level='INFO')(say)

    @logging(level='DEBUG')
    def do(something):
        print("do {}...".format(something))


    if __name__ == '__main__':
        say('hello')
        do("my work")