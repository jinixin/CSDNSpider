#!/usr/bin/env python
# coding=utf-8


import matplotlib.pyplot as pyplot
from sqltool import SqlTool


class BlogImage(object):
    def __init__(self):
        pass

    @classmethod
    def everyday_view_num(cls):
        with SqlTool(db='blog_csdn') as cursor:
            cursor.execute('select sum(number) from read_number group by record_time order by record_time desc limit 10')
            view_num = cursor.fetchall()  # get the sum of view
            cursor.execute('select record_time from read_number group by record_time order by record_time desc limit 10')
            view_date = cursor.fetchall()  # get date

        pyplot.title('the views of blog in the last 10 days')
        pyplot.xlabel('date')
        pyplot.ylabel('view number')
        pyplot.plot(view_date, view_num)  # x, y
        pyplot.show()


if __name__ == '__main__':
    BlogImage.everyday_view_num()
