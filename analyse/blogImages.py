#!/usr/bin/env python
# coding=utf-8

import os
import sys
import datetime

import matplotlib
matplotlib.use('Agg')  # 适配Linux
from matplotlib import pyplot

from sqltool import SqlTool


class BlogImage(object):
    today = datetime.datetime.today().date()
    ten_day_ago = (today - datetime.timedelta(days=10)).strftime('%Y-%m-%d')

    @staticmethod
    def set_info_and_show(pict, title, pict_name, xlabel, ylabel):
        fig = pyplot.gcf()
        fig.set_size_inches(10, 8)  # 设置图片大小
        pict.title(title)
        pict.xlabel(xlabel)  # x轴名字
        pict.ylabel(ylabel)  # y轴名字
        pyplot.savefig(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '../storage/%s.png' % pict_name))

    @staticmethod
    def x_axle_num2text(x, y, bottom=None):
        fig, ax = pyplot.subplots()
        text_to_x_scale = range(len(x))
        pyplot.bar(text_to_x_scale, y)  # 设置x轴下标
        if bottom:
            pyplot.subplots_adjust(bottom=bottom)  # 调整底部，使文章标题显示完整
        ax.set_xticks(text_to_x_scale)  # 设置x轴刻度
        ax.set_xticklabels(x, rotation='vertical')  # 设置x轴刻度文本

    @classmethod
    def everyday_view_num(cls):
        """生成最近十天博客访问总量图"""
        with SqlTool() as cursor:
            cursor.execute('select sum(number), record_time from read_number group by record_time order by record_time desc limit 10')
            view_num, view_date = zip(*cursor.fetchall())  # 获取访问总量列表和对应日期
        pyplot.plot(view_date, view_num)  # x,y
        cls.set_info_and_show(pyplot, u'最近十天博客的日访问量', 'everyday_view_num', u'日期', u'访问量')

    @classmethod
    def ten_day_add_num(cls):
        """生成博客每篇文章最近十天的访问增量图"""
        with SqlTool() as cursor:
            cursor.execute('select id, title from id_title')
            id_title = dict(cursor.fetchall())  # 产生id到title的哈希映射
            cursor.execute('select id, number from read_number where record_time=%s order by id', (cls.today,))
            view_after = dict(cursor.fetchall())
            view_before = {}.fromkeys(view_after.keys(), 0)
            cursor.execute('select id, number from read_number where record_time=%s order by id', (cls.ten_day_ago,))
            view_before.update(dict(cursor.fetchall()))  # 防止新增文章十天前无记录
        view_diff = dict([(index, view_after[index] - view_before[index]) for index in view_after])  # 计算增量
        add_num, title = [], []
        for index in sorted(view_diff):
            add_num.append(view_diff[index])
            title.append(id_title[index])
        cls.x_axle_num2text(title, add_num, bottom=0.55)
        cls.set_info_and_show(pyplot, u'博客每篇文章最近十天的访问增量', 'ten_day_add_num', u'文章名', u'访问增量')

    @classmethod
    def article_view_num(cls):
        """生成当前博客每篇文章访问量图"""
        with SqlTool() as cursor:
            cursor.execute(
                'select number, title from read_number inner join id_title on read_number.id=id_title.id where record_time=%s order by id_title.id',
                (cls.today,))
            view_num, title = zip(*cursor.fetchall())
        cls.x_axle_num2text(title, view_num, bottom=0.55)
        cls.set_info_and_show(pyplot, u'当前博客每篇文章访问量', 'article_view_num', u'文章名', u'访问量')

    @classmethod
    def everyday_add_view(cls):
        """生成博客每天访问增量图"""
        with SqlTool() as cursor:
            cursor.execute('select sum(number), record_time from read_number group by record_time order by record_time desc limit 51')
            ret = reversed(cursor.fetchall())
        date_list, add_list, yesterday_num = [], [], 0
        for i, (num, view_date) in enumerate(ret):
            date_list.append(view_date)
            add_list.append(num - yesterday_num)
            yesterday_num = num
        cls.x_axle_num2text(date_list[1:], add_list[1:], bottom=0.2)
        cls.set_info_and_show(pyplot, u'博客每天访问增量', 'everyday_add_view', u'日期', u'访问增量')


if __name__ == '__main__':
    BlogImage.everyday_view_num()
    BlogImage.ten_day_add_num()
    BlogImage.article_view_num()
    BlogImage.everyday_add_view()
