#!/usr/bin/env python
# coding=utf-8

import re
import sys
from time import localtime, strftime

import requests
from bs4 import BeautifulSoup

from sqltool import SqlTool
from server import cfg


class CSDNCrawler(object):
    """Crawler to get every blog's read number"""

    def __init__(self):
        self.regex = {
            'get_id': re.compile('article/details/(\d+)', re.S),
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
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find_all('li', class_='blog-unit')

        id2title, id2num = {}, {}
        for item in data:
            pid = self.regex['get_id'].search(item.a['href']).group(1)
            title = item.a.find(class_='blog-title').get_text().replace(u'置顶', '')
            read_num = item.a.find(class_='icon-read').parent.get_text()
            if not all([pid, title, read_num]):
                continue
            id2title[pid] = title.strip()
            id2num[pid] = read_num.strip()
            # print pid, title.strip(), read_num.strip()

        with SqlTool() as cursor:
            for pid, title in id2title.items():
                cursor.execute('select title from id_title where id=%s', (pid,))

                if cursor.rowcount <= 0:
                    cursor.execute(
                        'insert into id_title(id, author, title) values (%s, %s, %s)',
                        (pid, self.username, title)
                    )
                elif cursor.fetchone()[0] != title:  # update title in db where title changed
                    cursor.execute('update id_title set title=%s where id=%s', (title, pid))

            for pid, num in id2num.items():
                cursor.execute(
                    'replace into read_number(id, number, record_time) values (%s, %s, %s)',
                    (pid, num, self.date)
                )

        next_page = soup.find('a', rel='next')
        return next_page['href'] if next_page else None

    def get_next_page(self, url):
        """run 'get_read_number()' and check code whether exists next page"""
        self.get_username(url)
        while True:
            url = self.get_read_number(url)
            if url is None:
                break


if __name__ == '__main__':
    try:
        url = cfg.get('csdn', 'target') or sys.argv[1]
        crawler = CSDNCrawler()
        crawler.get_next_page(url)
    except IndexError:
        print '请在config文件或是命令行参数中配置待爬取的CSDN博客地址'
