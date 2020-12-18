# coding=utf-8
import datetime
from datetime import timedelta


class Time():
    '''
    返回今天 明天 昨天 本周第一天最后一天 本月第一天最后一天
    上周第一天最后一天 上月第一天最后一天
    本季度第一天最后一天 上季度第一天最后一天
    本年第一天最后一天 去年第一天最后一天  都为datetime格式
    '''
    def __init__(self):
        self.now = datetime.datetime.now()

    # 上一个小时
    def last_hours(self):
        return self.now - timedelta(hours=1)

    # 今天
    def totay(self):
        return self.now

    # 昨天
    def yesterday(self):
        return self.now - timedelta(days=1)

    # 明天
    def tomorrow(self):
        return self.now + timedelta(days=1)

    # 当前季度
    def now_quarter(self):
        return self.now.month / 3 if self.now.month % 3 == 0 else self.now.month / 3 + 1

    # 本周第一天和最后一天
    def this_week_start(self):
        return self.now - timedelta(days=self.now.weekday())

    def this_week_end(self):
        return self.now + timedelta(days=6 - self.now.weekday())

    # 上周第一天和最后一天
    def last_week_start(self):
        return self.now - timedelta(days=self.now.weekday() + 7)
    def last_week_end(self):
        return self.now - timedelta(days=self.now.weekday() + 1)

    # 本月第一天和最后一天
    def this_month_start(self):
        return datetime.datetime(self.now.year, self.now.month, 1)
    def this_month_end(self):
        return datetime.datetime(self.now.year, self.now.month + 1, 1) - timedelta(days=1)

    # 上月第一天和最后一天
    def last_month_end(self):
        this_month_start = datetime.datetime(self.now.year, self.now.month, 1)
        return (this_month_start - timedelta(days=1))
    def last_month_start(self):
        last_month_end = self.last_month_end()
        return datetime.datetime(last_month_end.year, last_month_end.month, 1)

    # 本季第一天和最后一天
    def this_quarter_start(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        return datetime.datetime(self.now.year, month, 1)
    def this_quarter_end(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        return datetime.datetime(self.now.year, month + 3, 1) - timedelta(days=1)

    # 上季第一天和最后一天
    def last_quarter_end(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        this_quarter_start = datetime.datetime(self.now.year, month, 1)
        last_quarter_end = this_quarter_start - timedelta(days=1)
        return last_quarter_end
    def last_quarter_start(self):
        month = (self.now.month - 1) - (self.now.month - 1) % 3 + 1
        this_quarter_start = datetime.datetime(self.now.year, month, 1)
        last_quarter_end = this_quarter_start - timedelta(days=1)
        return datetime.datetime(last_quarter_end.year, last_quarter_end.month - 2, 1)

    # 本年第一天和最后一天
    def this_year_start(self):
        return datetime.datetime(self.now.year, 1, 1)
    def this_year_end(self):
        return datetime.datetime(self.now.year + 1, 1, 1) - timedelta(days=1)

    # 去年第一天和最后一天
    def last_year_end(self):
        this_year_start = datetime.datetime(self.now.year, 1, 1)
        last_year_end = this_year_start - timedelta(days=1)
        return last_year_end
    def last_year_start(self):
        this_year_start = datetime.datetime(self.now.year, 1, 1)
        last_year_end = this_year_start - timedelta(days=1)
        return datetime.datetime(last_year_end.year, 1, 1)