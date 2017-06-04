#!/usr/bin/env python
# coding=utf-8

import time
from matplotlib import pyplot
from sqltool import SqlTool

pyplot.rcParams['font.sans-serif'] = ['SimHei']
pyplot.rcParams['axes.unicode_minus'] = False


class BlogImage(object):
    def __init__(self):
        pass

    @classmethod
    def everyday_view_num(cls):
        with SqlTool(db='blog_csdn') as cursor:
            cursor.execute('select sum(number), record_time from read_number group by record_time order by record_time desc limit 10')
            view_num, view_date = zip(*cursor.fetchall())  # get the sum of view and date
        pyplot.title(u'最近十天博客的日访问量')
        pyplot.xlabel(u'日期')
        pyplot.ylabel(u'访问量')
        pyplot.plot(view_date, view_num)  # x,y
        pyplot.show()

    @classmethod
    def ten_day_add_num(cls):
        with SqlTool(db='blog_csdn') as cursor:
            cursor.execute('select id, title from id_title')
            id_title = dict(cursor.fetchall())  # 产生id到title的哈希映射
            today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[:11]
            ten_day_ago = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 3600 * 24 * 10))[:11]
            cursor.execute('select id, number from read_number where record_time=%s order by id', (today,))
            id_number_after = cursor.fetchall()
            cursor.execute('select id, number from read_number where record_time=%s order by id', (ten_day_ago,))
            id_number_before = cursor.fetchall()
        view_diff, add_num, title = [], [], []
        map(lambda x, y: view_diff.append((x[0], x[1] - y[1])), id_number_after, id_number_before)
        view_diff = dict(view_diff)  # 产生id到增量的哈希映射
        for article_id in view_diff:
            add_num.append(view_diff[article_id])
            title.append(id_title[article_id])
        fig, ax = pyplot.subplots()
        title_to_x_scale = range(len(title))
        pyplot.bar(title_to_x_scale, add_num)  # 设置x轴下标
        pyplot.subplots_adjust(bottom=0.55)  # 调整底部，使标题显示完整
        ax.set_xticks(title_to_x_scale)  # 设置x轴刻度
        ax.set_xticklabels(title, rotation='vertical')  # 设置x轴刻度文本
        pyplot.title(u'博客每篇文章最近十天的访问增量')
        pyplot.xlabel(u'文章名')
        pyplot.ylabel(u'访问增量')
        pyplot.show()


if __name__ == '__main__':
    BlogImage.everyday_view_num()
    BlogImage.ten_day_add_num()
