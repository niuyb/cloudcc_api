# coding=utf-8
import calendar
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

    # 获取当月有多少天
    def get_month_nums(self):
        first_day=self.this_month_start()
        days_num = calendar.monthrange(first_day.year, first_day.month)[1]  # 获取当前月有多少天
        return days_num
    # 下个月的第一天
    def next_month_start(self):
        days_num = self.get_month_nums()
        first_day = self.this_month_start()
        next_month_start = first_day + datetime.timedelta(days=days_num)
        return next_month_start

    #下个月最后一天
    def next_month_end(self):
        next_month_start = self.next_month_start()
        next_month_days = calendar.monthrange(next_month_start.year, next_month_start.month)[1]  # 获取下个月有多少天
        next_month_end = next_month_start + datetime.timedelta(days=next_month_days - 1)
        return next_month_end



if __name__ == "__main__":
    t = Time()
    # print(t.next_month_end())
    print(t.next_month_end())
