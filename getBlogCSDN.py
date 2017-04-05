#!/usr/bin/env python
# coding=utf-8

from os import environ
from time import localtime, strftime
from re import compile, findall, S
from urlparse import urljoin
import MySQLdb
from requests import get


class SqlTool(object):
    """Tool to deal with SQL"""

    def __init__(self, user, pwd, db='blog_csdn', host='localhost', port=3306):
        # print host, port, user, pwd, db
        self.connect = MySQLdb.connect(host=host, port=port, user=user, passwd=pwd, db=db, charset='utf8')
        self.cursor = self.connect.cursor()

    def __enter__(self):
        """back to 'with SqlTool()' """
        return self.cursor

    def __exit__(self, exc_type, exc_instance, traceback):
        """end and clean the result"""
        if exc_instance:
            print exc_instance
        self.cursor.close()
        self.connect.commit()
        self.connect.close()
        return True


class CSDNCrawler(object):
    """Crawler to get every blog's read number"""

    def __init__(self):
        self.regex = {
            'id_title': compile(
                '<span\s+class="link_title"><a\s+href="/\w+/article/details/(\d+)">(.*?<font\s+color="red">\[置顶\]</font>)?(.+?)</a></span>',
                S),
            'id_read': compile('/(\d+)"\s+title="阅读次数">阅读</a>\((\d+)\)</span>'),
            'next_page': compile('</a>\s*<a\s+href="([^><]+)">下一页</a>\s*<a'),
            'check_success': compile('<title>维护-提示页面</title>'),
        }
        self.date = strftime('%Y-%m-%d', localtime())
        self.db_user = environ.get('DB_USER')  # read database user from environment variables
        self.db_pwd = environ.get('DB_PWD')  # read database password from environment variables

    def download_html(self, url):
        """get page source code"""
        HEAD = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55 Safari/537.36'
        }
        while True:
            response = get(url, headers=HEAD)
            if self.regex['check_success'].search(response.content) is None:
                break
        return response.content

    def get_read_number(self, url):
        """use regex to get every blog read number"""
        html = self.download_html(url)

        id_title = self.regex['id_title'].findall(html)
        with SqlTool(self.db_user, self.db_pwd) as cursor:
            for line in id_title:
                cursor.execute('select id from id_title where id=%s', (line[0],))
                if cursor.rowcount == 0:
                    cursor.execute('insert into id_title(id, title) values (%s, %s)', (line[0], line[2].strip()))

        id_read = findall(self.regex['id_read'], html)
        with SqlTool(self.db_user, self.db_pwd) as cursor:
            for line in id_read:
                # print line[0].strip(), line[1].strip()
                cursor.execute('replace into read_number(id, number, record_time) values (%s, %s, %s)',
                               (line[0].strip(), line[1].strip(), self.date))
        return self.regex['next_page'].search(html)  # search 'next_page'

    def get_next_page(self, url):
        """run 'get_read_number()' and check code whether exists next page"""
        while True:
            part_url = self.get_read_number(url)
            if part_url is None:
                break
            else:
                url = urljoin(url, part_url.group(1))


if __name__ == '__main__':
    crawler = CSDNCrawler()
    crawler.get_next_page(environ.get('CSDN_URL'))  # read blog's url from environment variables
