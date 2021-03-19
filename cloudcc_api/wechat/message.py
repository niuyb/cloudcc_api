#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/3/9 14:16
# 工具：PyCharm
# Python版本：3.7.0
import base64
import ctypes
import json
import os
import sys

path1 = os.path.abspath('/var/www/cloudcc_api')
sys.path.append(path1)
from public.utils import engine
from settings import settings

import Crypto
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import pandas as pd

# libWeWorkFinanceSdk_C.so linux 不兼容win


"""
encrypt_random_key内容解密说明：
encrypt_random_key是使用企业在管理端填写的公钥（使用模值为2048bit的秘钥），采用RSA加密算法进行加密处理后base64 encode的内容，加密内容为企业微信产生。RSA使用PKCS1。
企业通过GetChatData获取到会话数据后：
a) 需首先对每条消息的encrypt_random_key内容进行base64 decode,得到字符串str1.
b) 使用publickey_ver指定版本的私钥，使用RSA PKCS1算法对str1进行解密，得到解密内容str2.
c) 得到str2与对应消息的encrypt_chat_msg，调用下方描述的DecryptData接口，即可获得消息明文。

"""

class GET_WECHAT_MESSAGE:
    # 获取信息配置
    infos_num = 500
    seq = 2000
    time_out = 10
    database=engine(settings.db_new_data)
    wechat_format = ["msgid","action","from","tolist","roomid","msgtime","msgtype","text"]
    wechat_sql_table="wechat"


    qy_id = "ww60d12cbe3d4a82be"
    private_key = """-----BEGIN RSA PRIVATE KEY-----
    MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC/M6P6gHc4/+L+
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
                 aIqA/AS1LKRDU2AltvTDCx9eSA==
                 -----END RSA PRIVATE KEY-----"""

    secret = "15CWzzgj_YeR6XxWdesGm3ysvbb9L2ALyBzmAmCzM-g"

    @classmethod
    def wechat_msg(cls):
        # 读取sdk文件
        dll = ctypes.cdll.LoadLibrary("/var/www/cloudcc_api/cloudcc_api/wechat/libWeWorkFinanceSdk_C.so")
        # 实例sdk
        new_sdk = dll.NewSdk()
        # 初始化
        result = dll.Init(new_sdk, cls.qy_id.encode(), cls.secret.encode())
        if result != 0:
            return
        private_key = RSA.import_key(cls.private_key)
        cipher = Crypto.Cipher.PKCS1_v1_5.new(private_key)
        while True:
            s = dll.NewSlice()
            # 获取加密信息
            ret = dll.GetChatData(new_sdk, cls.seq,cls.infos_num, '', '',cls.time_out, ctypes.c_long(s))
            # 消息格式
            data = dll.GetContentFromSlice(s)
            data = ctypes.string_at(data, -1).decode("utf-8")
            print(data)
            # 销毁
            dll.FreeSlice(s)
            data = json.loads(data).get('chatdata')
            if not data:
                break
            cls.seq = data[-1].get('seq')
            for msg in data:
                # encrypt_random_key base64
                encrypt_key = cipher.decrypt(base64.b64decode(msg.get('encrypt_random_key')), "ERROR")
                ss = dll.NewSlice()
                # 解密
                dll.DecryptData(encrypt_key, msg.get('encrypt_chat_msg').encode(), ctypes.c_long(ss))
                result = dll.GetContentFromSlice(ss)
                result = ctypes.string_at(result, -1).decode("utf-8")
                result = json.loads(result)
                dll.FreeSlice(ss)
                # print(result)
                wechat_df = pd.DataFrame(columns=cls.wechat_format)
                wechat_dict=result
                text_name = wechat_dict["msgtype"]
                if text_name in ["image","mixed","file","video"]:
                    continue
                else:
                    print(wechat_dict[text_name])
                    wechat_dict["text"] = wechat_dict[text_name]
                    wechat_dict["tolist"] = json.dumps(wechat_dict["tolist"])
                    wechat_dict.pop(text_name,False)
                    wechat_df = wechat_df.append(wechat_dict, ignore_index=True, sort=False)
                    print(wechat_df)
                    wechat_df.to_sql(cls.wechat_sql_table , cls.database, index=False, if_exists="append")
        # 销毁sdk
        dll.DestroySdk(new_sdk)


    def insert_data(cls,data):
        print(cls.database)









if __name__ == '__main__':

    GET_WECHAT_MESSAGE.wechat_msg()