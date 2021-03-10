#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/3/9 9:26
# 工具：PyCharm
# Python版本：3.7.0
import base64
import sys,os
path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)

from cloudcc_api.wechat.local_rsa import RSACipher

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
NewDKey = d.Init(r,b"ww60d12cbe3d4a82be",b"15CWzzgj_YeR6XxWdesGm4xEz-_pW_d0ZdcDRxzFzcw")
slice = Slice_t()

tes2  = d.GetChatData(r,0,1,"","",10,ctypes.byref(slice))
print(tes2)

local_str = slice.buf
data = json.loads(local_str)
print(data)

chatdata= data.get("chatdata")
chatdata = chatdata[0]
encrypt_key = chatdata.get("encrypt_random_key")
print(type(encrypt_key),encrypt_key)
encrypt_msg = chatdata.get("encrypt_chat_msg")
print(type(encrypt_msg),encrypt_msg)

encrypt_key_64=base64.b64encode(encrypt_key.encode('utf-8'))


private_pem = """MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC/M6P6gHc4/+L+
                 Is7k3ekYYRdYvJBsHR4C0IbtW760hMrubRKxguc03N0khQRYkjXtZwB9F3tMNOb3
                 s/AJybDX1qYleCEdy2UoudjcJel4LpCxRMkKFmO/j3U4lavT1TnJ2Sw77KeMS8+U
                 BL/oo9ZpunZ7ZuFdcJ0O6OHbYnPirarls5B6z0TwYWy1vMtnPMw92QQpXJOaazcj
                 sRwKnKmFOTdUxwIwxIIiEFdFIewoZltXMttH3FfpxTITjOgmNbyCTcNvsjTHRr63
                 DM1r3OWvIDGNYa81ClQLV6G/9w/J5FkY3eOI9DfftGh582EM4oJ3YDyyYrNCZcz9
                 xbOGya7bAgMBAAECggEBAL6K2QyIP8f3AiCfUa21FFluUJTm/cowTjsh0oTynB9M
                 AuwOmMV8HauJu3xsbwNRWhqnPk5rOz2brt0FXd5zOCAw0kye5enKS5qFcv8ZbQyO
                 4zU1xl+eJnO9pGTqi11Erh1gpvtlASgIWOo6vYE63S9qWi7qPQcgdfRo0sQN3kzz
                 ak5X1JcyzaB3wuUe5tr9ZgnO5XenLCQzsYptLr8sXnExfLEbVNVkGYvxlcHf5XZE
                 Os0OOo4E2SfxfrEesiDqHeLKkwVmC8UK9qlAn4LklSMZDIsif3EhmmD+dyHZwyC7
                 wNpuVcrcyRaAcu8a5ssCN3uoW7LIVGIGhZjhxxblC9kCgYEA4Dtxfi2cg/j/Zin/
                 +zUeVKvhOEYVWidtnsP//6bVj6WVsjFuBRpIE6Qa2nYL7xVeI3cyClPIeDtQgzHy
                 q46+pwhkKw1V7V0viB2/H/Za40F3R6BZ1TZTGjAcTXW9yQ+TbD315oDDoRXcNahG
                 2j4trqQfuDPY/in2BxVkWJt7g/0CgYEA2ko7iaALLFp+v21ZTsN39jMOcYRNG9OU
                 p2XGvDjmTK26uaXntpbNRpvco0Rtd5+UDbWokchPAHl8ehiYLomAkQKUQJAzgGgX
                 uVf//2wHlcyBFkfUnWLRKSPxZC3fdtAVLMDh7XtTNEL2HKyoKBGHjIm5DRNwjNGu
                 rpN4Wij3ObcCgYBSDM5Zunz0Oa/TBXlaxbQkjYRrIBH+HEFbgCLzvGuXFaMyQi4d
                 BeHr9fexitKRGMOKvLn912yaujGa4DMJHcGbw1FMA6Q2qAuVhjUCkBXv5GuuNPnK
                 MAe2pHYmzfe1U9LBH+cUAngTQLmElN/gSjJTHlFRCP/U+SvCqcw/NB29TQKBgQDF
                 b5biJ8tzVnaFldXNE6cRG6TYr50+qeQudDOIUr6aZBgbih9GWqdYUekCEwYfyEoV
                 DFVnZhFukHMxy8T5cozCm96TdtneLkgm750v3PoPV2T6TgXURGiCGWxf+82+nP5J
                 +DtgnMbo4hfQX6nIc/Jx/q9NUGPgOlcQt3mHsr3JiQKBgQDHTw6ol8JBao9m1etx
                 VFwF2iu0e9oTs8Bi9n5YgS0D2mAuxzUs9kBVzDMuvS2NArZGuxY1RCrDlJKp+8Hu
                 RtC7e6hJEJoOat7QivNjAO95I3gfrlVbR5XVtJ51Bve+Eh71rhEQd7X6CrErhpbz
                 aIqA/AS1LKRDU2AltvTDCx9eSA=="""


print(type(encrypt_key_64),encrypt_key_64)
print(type(private_pem),private_pem)


cipher = RSACipher()
encrypt_key_str2 = cipher.decrypt_with_private_key(encrypt_key_64)

# encrypt_key_str2 = decryptByPrivateKey(encrypt_key_64,private_pem)

rsa_slice = Slice_t()
ret=d.DecryptData(encrypt_key_str2,encrypt_msg,rsa_slice)
print(ret)











