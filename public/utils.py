"""定义一些公共方法，项目中每个app，均可调用这些方法"""
import time
from datetime import datetime

import arrow
import pymysql
import redis
import warnings
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from django.conf import settings

"""获取指定范围内的日期列表"""
def gen_date_list(start=None, end=None, fmt=None):
    date_list = []
    if start:
        start = arrow.get(start)
    else:
        # 如果未提供start，取当前时间
        start = arrow.now().floor('month')
    if end:
        end = arrow.get(end)
    else:
        # 如果未提供end，从当前时间后推一个月，然后再前推一天
        end = start.shift(months=1).shift(days=-1)
    for i in arrow.Arrow.range('day', start, end):
        if fmt:
            date = i.strftime(fmt)
        else:
            date = i.datetime
        date_list.append(date)
    return date_list

"""生成指定时间范围的月份列表"""
def gen_month_list(start=None, end=None, fmt=None):
    month_list = []
    if start:
        start = arrow.get(start)
    else:
        # 如果未提供start，取当前时间
        start = arrow.now()
    start = start.floor("month")
    if end:
        end = arrow.get(end)
    else:
        # 如果未提供end，从当前时间后推1年，然后再前推1个月
        end = start.shift(years=1).shift(months=-1)
    end = end.floor("month")
    for i in arrow.Arrow.range("month", start, end):
        if fmt:
            month = i.strftime(fmt)
        else:
            month = i.datetime
        month_list.append(month)
    return month_list

"""获取指定model的values_list"""
def get_value_list(Model, params, key_list):
    value_list = list(Model.objects.filter(**params).values_list(*key_list))
    return value_list

"""将settings中的数据库参数转换成pymysql能够接收的参数"""
def parse_kwargs_for_pymysql(kwargs):
    host = kwargs.get("HOST")
    user = kwargs.get("USER")
    password = kwargs.get("PASSWORD")
    port = kwargs.get("PORT")
    database = kwargs.get("NAME")
    charset = kwargs.get("CHARSET", "utf8")
    return {
        "host": host,
        "port": port,
        "database": database,
        "user": user,
        "password": password,
        "charset": charset
    }


"""使用sql查询数据"""
def get_all_data(database, sql):
    kws = parse_kwargs_for_pymysql(database)
    conn = pymysql.connect(**kws)
    cursor = conn.cursor()
    cursor.execute(sql)
    all_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_data


"""判断一个字符串中是否包含一个列表中的字符串"""
def isInString(string_old, sub_list):
    for s in sub_list:
        if s in string_old:
            return True
    return False

"""pandas查询数据的连接信息"""
# def engine(db_info):
#     engine = create_engine(
#         "mysql+pymysql://{}:{}@{}/{}?charset={}".format(
#             db_info['USER'],
#             db_info['PASSWORD'],
#             db_info['HOST'],
#             db_info['NAME'],
#             'utf8'
#         ), poolclass=NullPool
#     )
#     conn_engine = engine.connect()  # 创建连接
#     return conn_engine
def engine(db_info):
    engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}".format(db_info['DB_USER'],
                                                                           db_info['DB_PWD'],
                                                                           db_info['DB_HOST'],
                                                                           db_info['DB_NAME'],
                                                                           'utf8'), poolclass=NullPool)
    conn_engine = engine.connect()  # 创建连接
    return conn_engine

def cncurrency(value, capital=True, prefix=False, classical=None):
    '''
    人民币数字转汉字表示 Ver 0.02
    作者: qianjin(AT)ustc.edu
    版权声明:
        只要保留本代码最初作者的电子邮件即可，随便用。用得爽的话，不反对请
    作者吃一顿。
    参数:
    capital:    True   大写汉字金额
                False  一般汉字金额
    classical:  True   圆
                False  元
    prefix:     True   以'人民币'开头
                False, 无开头
    '''
    if not isinstance(value, (Decimal, str, int)):
        msg = '''
        由于浮点数精度问题，请使用考虑使用字符串，或者 decimal.Decimal 类。
        因使用浮点数造成误差而带来的可能风险和损失作者概不负责。
        '''
        warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False
    # 汉字金额前缀
    if prefix is True:
        prefix = '人民币'
    else:
        prefix = ''
    # 汉字金额字符定义
    dunit = ('角', '分')
    if capital:
        num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
        iunit = [None, '拾', '佰', '仟', '万', '拾', '佰', '仟',
                 '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    else:
        num = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')
        iunit = [None, '十', '百', '千', '万', '十', '百', '千',
                 '亿', '十', '百', '千', '万', '十', '百', '千']
    if classical:
        iunit[0] = '圆' if classical else '元'
    # 转换为Decimal，并截断多余小数
    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))
    # 处理负数
    if value < 0:
        prefix += '负'          # 输出前缀，加负
        value = - value         # 取正数部分，无须过多考虑正负数舍入
                                # assert - value + value == 0
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('金额太大了，不知道该怎么表达。')
    istr, dstr = s.split('.')           # 小数部分和整数部分分别处理
    istr = istr[::-1]                   # 翻转整数部分字符串
    so = []     # 用于记录转换结果
    # 零
    if value == 0:
        return prefix + num[0] + iunit[0]
    haszero = False     # 用于标记零的使用
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”
    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append('整')         # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        so.append(num[0])       # 无角有分，添加“零”
        haszero = True          # 标记加过零了
    # 无整数部分
    if istr == '0':
        if haszero:             # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.append(prefix)       # 加前缀
        so.reverse()            # 翻转
        return ''.join(so)
    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:          # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:   # 亿和万之间全部为零的情况
                so.pop()                        # 去掉万
            so.append(iunit[i])
            if n == 0:                          # 处理这些位上为零的情况
                if not haszero:                 # 如果以前没有加过零
                    so.insert(-1, num[0])       # 则在单位后面加零
                    haszero = True              # 标记加过零了
            else:                               # 处理不为零的情况
                so.append(num[n])
                haszero = False                 # 重新开始标记加零的情况
        else:                                   # 在其他位置上
            if n != 0:                          # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False                 # 重新开始标记加零的情况
            else:                               # 处理为零的情况
                if not haszero:                 # 如果以前没有加过零
                    so.append(num[0])
                    haszero = True
    # 最终结果
    so.append(prefix)
    so.reverse()
    return ''.join(so)


# 写代码时用起来比较方便
# 结尾时需要调用 实例.dict()方法 或者 dict(实例) 转成字典
# 转成字典之后，得到{"code": 0, "data": None, "error": ""}
class Result():
    def __init__(self):
        self.code = -1
        self.data = None
        self.msg = ""

    def dict(self):
        return dict(self.__iter__())

    def __iter__(self):
        attrs = dir(self)
        for attr in attrs:
            # 去除自建方法
            if attr.find("__") == 0:
                continue
            value = getattr(self, attr)
            # 不可调用
            if callable(value):
                continue
            yield (attr, value)


"""获取pymysql链接与游标"""
def get_conn(host,user,passwd,db,port=3306):
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=passwd,
        db=db,
        port=port,
        charset='utf8')
    # 获得游标
    cur = conn.cursor()
    return conn, cur


"""连接redis"""
def get_redis(host,db):
    r = redis.StrictRedis(
        host=host,
        port=6379,
        db=db,
        decode_responses=True  # 设置为True返回的数据格式就是str类型
    )
    return r



"""毫秒级别时间戳转成日期 """
def ms_date(ms_time):
    time_local  = time.localtime(ms_time/1000)
    date = time.strftime("%Y-%m-%d", time_local)
    return date
"""毫秒级别时间戳转成时间 """
def ms_time(ms_time):
    time_local  = time.localtime(ms_time/1000)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return date
"""日期转成毫秒级别时间戳 """
def date_ms(date):
    # timestr = '2020-09-14'
    datetime_obj = datetime.strptime(date, "%Y-%m-%d")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return obj_stamp
"""时间转成毫秒级别时间戳 """
def time_ms(date):
    datetime_obj = datetime.strptime(date, "%Y-%m-%d %H:%M")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return obj_stamp