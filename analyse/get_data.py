#!/usr/bin/env python
# coding=utf-8

import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import os
import datetime
from sqltool import SqlTool
from mail import send_email


def get_add_num_every_blog():
    today = datetime.datetime.today().date()
    yesterday = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    with SqlTool() as cursor:
        cursor.execute('select id, title from id_title')
        id2title = dict(cursor.fetchall())
        cursor.execute('select id, number from read_number where record_time="%s"' % today)
        id2num_now = dict(cursor.fetchall())
        cursor.execute('select id, number from read_number where record_time="%s"' % yesterday)
        id2num_before = dict(cursor.fetchall())
    total = sum(id2num_now.values())
    total_add = sum(id2num_now.values()) - sum(id2num_before.values())
    every_add = dict([(id2title[pid], id2num_now[pid] - id2num_before[pid]) for pid in id2title])
    every_add_list = [(pid, add_num) for pid, add_num in every_add.items()]
    every_add_list.sort(key=lambda x: x[1])
    every_add_str = os.linesep.join(['%s: %s' % (pid, add_num) for pid, add_num in every_add_list])
    msg = """
    博客总访问量: %d, 总增加量: %d;
    每片文章增量:
    %s
    """ % (total, total_add, every_add_str)
    send_email(msg)


if __name__ == '__main__':
    get_add_num_every_blog()
