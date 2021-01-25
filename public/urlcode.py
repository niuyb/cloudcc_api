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

from public.utils import engine, list_to_sql_string
from settings import settings
import pandas as pd
pd.set_option('display.max_rows', None) # 展示所有行
pd.set_option('display.max_columns', None) # 展示所有列
pd.set_option('display.width', None)# 展示所有列




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


if __name__ == '__main__1':
    import urllib
    from urllib import parse
    str1="https://support.istarshine.com/DataCount/single_user_activity_count?uid=67358"
    str2 = parse.quote(str1)  # quote()将字符串进行编码
    # str2="%E4%B8%8A%E6%B5%B7%E5%8D%8E%E7%91%9E%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89"
    print(str2)
    rawurl = str2
    url = parse.unquote(rawurl)
    print (url)



if __name__ == '__main__':

    data=[{"CCObjectAPI":"Account","id":"00120200380BC39Vlgpi"},{"CCObjectAPI":"Account","id":"0012020162260358XHfb"},{"CCObjectAPI":"Account","id":"001202039D9C044SyWPr"},{"CCObjectAPI":"Account","id":"00120210EDD0D58HQuVk"},{"CCObjectAPI":"Account","id":"0012021199DBF70KrJlI"},{"CCObjectAPI":"Account","id":"001202129544BC29mtch"},{"CCObjectAPI":"Account","id":"00120212C922FF5EowU5"},{"CCObjectAPI":"Account","id":"0012021326AF953ZPt6S"},{"CCObjectAPI":"Account","id":"001202133A9C37BeaoMY"},{"CCObjectAPI":"Account","id":"0012021361A789AhUcNe"},{"CCObjectAPI":"Account","id":"00120213BA43346Hk9lu"},{"CCObjectAPI":"Account","id":"001202143D9A674FjvrA"},{"CCObjectAPI":"Account","id":"00120214614C800wo9Wl"},{"CCObjectAPI":"Account","id":"0012021484BB2A7Indvo"},{"CCObjectAPI":"Account","id":"0012021494C435BYmc04"},{"CCObjectAPI":"Account","id":"00120214A72739EJmIXg"},{"CCObjectAPI":"Account","id":"00120214EFD3ACEHWK4e"},{"CCObjectAPI":"Account","id":"0012021532135114peKo"},{"CCObjectAPI":"Account","id":"001202158A56CBADqyIf"},{"CCObjectAPI":"Account","id":"00120215EF720ECovE1C"},{"CCObjectAPI":"Account","id":"001202160158DFDTzOE5"},{"CCObjectAPI":"Account","id":"0012021638F06C6QRo8n"},{"CCObjectAPI":"Account","id":"00120216406F49BCONmL"},{"CCObjectAPI":"Account","id":"00120216F57756AQSdhA"},{"CCObjectAPI":"Account","id":"001202171C437ABOr35w"},{"CCObjectAPI":"Account","id":"001202172F531BAn9LS5"},{"CCObjectAPI":"Account","id":"0012021760801B6vAfs6"},{"CCObjectAPI":"Account","id":"00120217C8B571Fudkpb"},{"CCObjectAPI":"Account","id":"00120217F88BCAEfSdsl"},{"CCObjectAPI":"Account","id":"0012021801CED20ifLqs"},{"CCObjectAPI":"Account","id":"001202182BA028DLzwpW"},{"CCObjectAPI":"Account","id":"0012021853334BE5Vb92"},{"CCObjectAPI":"Account","id":"00120218AF19CB8Q5Dwd"},{"CCObjectAPI":"Account","id":"00120218BA92EC5zBmW6"},{"CCObjectAPI":"Account","id":"00120218C2BC8A6N2mhS"},{"CCObjectAPI":"Account","id":"0012021928DCC04w9Xnp"},{"CCObjectAPI":"Account","id":"00120219DD3B2BEfX14j"},{"CCObjectAPI":"Account","id":"0012021A4A79171WL7yp"},{"CCObjectAPI":"Account","id":"0012021A55655AFVbJ8d"},{"CCObjectAPI":"Account","id":"0012021A66A83395YgsV"},{"CCObjectAPI":"Account","id":"0012021A6E73D45LKRPv"},{"CCObjectAPI":"Account","id":"0012021AE200ABBqMDw4"},{"CCObjectAPI":"Account","id":"0012021B19F29A6T8jyd"},{"CCObjectAPI":"Account","id":"0012021B6254E81EXZhw"},{"CCObjectAPI":"Account","id":"0012021B95639E0PAxsu"},{"CCObjectAPI":"Account","id":"0012021BA6824A4eLBoG"},{"CCObjectAPI":"Account","id":"0012021BD40EB6Bg1kr6"},{"CCObjectAPI":"Account","id":"0012021C48D0A56SlIyf"},{"CCObjectAPI":"Account","id":"0012021C7B0E2C9vQFx1"},{"CCObjectAPI":"Account","id":"0012021CFE527C8TNPO7"},{"CCObjectAPI":"Account","id":"0012021D287967A7W0ma"},{"CCObjectAPI":"Account","id":"0012021D419E7F0NHxPv"},{"CCObjectAPI":"Account","id":"0012021D729A5DEK7Tf5"},{"CCObjectAPI":"Account","id":"0012021DB8A6057oehWb"},{"CCObjectAPI":"Account","id":"0012021E3FDD156Nyg5E"},{"CCObjectAPI":"Account","id":"0012021E649E5E4siAgo"},{"CCObjectAPI":"Account","id":"0012021EBB70245MSIRE"},{"CCObjectAPI":"Account","id":"0012021F3EB2E0Du7MKB"},{"CCObjectAPI":"Account","id":"0012021FB5AD23EmMdPB"}]
    print(len(data))
    m_list = []
    for d in data:
        m_list.append(d["id"])

    m_str = list_to_sql_string(m_list)
    print(m_str)


"""
51042   0012021DB8A6057oehWb  国网河北省电力有限公司保定供电公司
"""




