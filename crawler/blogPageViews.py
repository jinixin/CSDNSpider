#!/usr/bin/env python
# coding=utf-8

import re
import sys
from time import localtime, strftime
from urlparse import urljoin

import requests

from sqltool import SqlTool
from server import cfg


class CSDNCrawler(object):
    """Crawler to get every blog's read number"""

    def __init__(self):
        self.regex = {
            'id_title': re.compile('<span\s+class="link_title"><a\s+href="/\w+/article/details/(\d+)">(.+?)</a>', re.S),
            'id_read': re.compile('/(\d+)"\s+title="阅读次数">阅读</a>\((\d+)\)</span>'),
            'next_page': re.compile('</a>\s*<a\s+href="([^><]+)">下一页</a>\s*<a'),
            'check_success': re.compile('<title>维护-提示页面</title>'),
        }
        self.date = strftime('%Y-%m-%d', localtime())

    def get_username(self, url):
        """get username from url"""
        result = re.search('blog.csdn.net/([\w_@]+)', url)
        self.username = result.group(1)

    def download_html(self, url):
        """get page source code"""
        HEAD = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55 Safari/537.36'
        }
        while True:
            response = requests.get(url, headers=HEAD)
            if self.regex['check_success'].search(response.content) is None:  # get successfully
                break
        return response.content

    def get_read_number(self, url):
        """use regex to get every blog read number"""
        html = self.download_html(url)

        id2title, id_title = {}, self.regex['id_title'].findall(html)
        for line in id_title:
            id2title[int(line[0].strip())] = line[1].replace('<font color="red">[置顶]</font>', '').strip()

        with SqlTool() as cursor:
            for pid, title in id2title.iteritems():
                cursor.execute('select title from id_title where id=%s', (pid,))

                if cursor.rowcount <= 0:
                    cursor.execute('insert into id_title(id, author, title) values (%s, %s, %s)', (
                        pid, self.username, title))
                elif cursor.fetchone()[0] != title.decode('utf-8'):  # update title in db where title changed
                    cursor.execute('update id_title set title=%s where id=%s', (title, pid))

        id_read = re.findall(self.regex['id_read'], html)
        with SqlTool() as cursor:
            for line in id_read:
                cursor.execute('replace into read_number(id, number, record_time) values (%s, %s, %s)',
                               (line[0].strip(), line[1].strip(), self.date))

        return self.regex['next_page'].search(html)  # search 'next_page'

    def get_next_page(self, url):
        """run 'get_read_number()' and check code whether exists next page"""
        self.get_username(url)
        while True:
            part_url = self.get_read_number(url)
            if part_url is None:
                break
            else:
                url = urljoin(url, part_url.group(1))


if __name__ == '__main__':
    try:
        url = cfg.get('csdn', 'target') or sys.argv[1]
        crawler = CSDNCrawler()
        crawler.get_next_page(url)
    except IndexError:
        print '请在config文件或是命令行参数中配置待爬取的CSDN博客地址'
