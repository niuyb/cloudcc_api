#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2020/12/30 18:28
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
import hashlib


def create_id(name,timestamp,index):
    if not name:
        name = ""
    md5_str = hashlib.md5(
        str(name).encode(encoding='UTF-8') + str(timestamp).encode(encoding='UTF-8') + str(index).encode(
            encoding='UTF-8')).hexdigest()[8:-8]
    return md5_str



def qy_sign(appkey,appSecret,timestamp):
    sign=hashlib.md5(str(appkey).encode(encoding='UTF-8') + str(appSecret).encode(encoding='UTF-8') + str(timestamp).encode(encoding='UTF-8')).hexdigest()
    return sign



if __name__ == "__main__":
    # create_id("北京世中臻贤教育科技有限公司","1609324317948",1)

    appkey = "U61fBGDOkn9EXDSrKvuP"
    appSecret = "GX4bHAqqulLZP4wSrbaZLZNvcphG8qld"
    timestamp = "1614761616000"
    sign=qy_sign(appkey,appSecret,timestamp)

    print(sign)