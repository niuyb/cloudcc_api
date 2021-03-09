#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/3/9 9:26
# 工具：PyCharm
# Python版本：3.7.0


import sys,os

path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

from ctypes import *
import ctypes
import json
import requests



# dll = ctypes.cdll.LoadLibrary(r'D:\file\1_A_ZHXG\cloudcc_api\cloudcc_api\wechat\WeWorkFinanceSdk_C.h')
# dll.NewSdk.argtypes = []
# dll.NewSdk.restype = ctypes.c_void_p


class Slice_t(Structure):
    _fields_ = [
        ("buf",ctypes.c_char_p),
        ("len", ctypes.c_int)
    ]

class MediaData_t(Structure):
    _fields_ = [
        ("outindexbuf",ctypes.c_char_p),
        ("out_len", ctypes.c_int),
        ("data", ctypes.c_char_p),
        ("data_len", ctypes.c_int),
        ("is_finish", ctypes.c_int)
    ]


d = cdll.LoadLibrary("./cloudcc_api/wechat/libWeWorkFinanceSdk_C.so")
print(d)
r = d.NewSdk()
print(r)
NewDKey = d.Init(r,b"ww60d12cbe3d4a82be",b"15CWzzgj_YeR6XxWdesGmwB7O974dVmSgkm57uZG1Nk")
slice = Slice_t()

tes2  = d.GetChatData(r,0,1,"","",10,ctypes.byref(slice))
print(tes2)

local_str = slice.buf
data = json.loads(local_str)
print(data)
encrypt_key = data.get("encrypt_random_key")
encrypt_msg = data.get("encrypt_chat_msg")

rsa_slice = Slice_t()

ret=d.DecryptData(encrypt_key,encrypt_msg,rsa_slice)
print(ret)











