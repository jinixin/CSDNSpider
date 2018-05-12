#!/usr/bin/env python
# coding=utf-8

import re
import sys
from time import localtime, strftime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from sqltool import SqlTool
from server import cfg


class CSDNCrawler(object):
    """ 爬取每篇文章的访问情况 """

    def __init__(self):
        self.regex = {
            'get_id': re.compile('article/details/(\d+)', re.S),
            'check_success': re.compile('<title>维护-提示页面</title>'),
        }
        self.date = strftime('%Y-%m-%d', localtime())

    def get_username(self, url):
        """ 获取博主昵称 """
        result = re.search('blog.csdn.net/([\w_@]+)', url)
        self.username = result.group(1)

    def download_html(self, url):
        """ 获取网页源代码 """
        while True:
            response = requests.get(url, headers={'User-Agent': UserAgent().random})  # 随机产生User-Agent
            if self.regex['check_success'].search(response.content) is None:
                break
        return response.content

    def get_read_number(self, url):
        """ 获取每篇文章标题与访问量 """
        html = self.download_html(url)
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find_all('div', class_='article-item-box')
        if not data:
            return False

        id2title, id2num = {}, {}
        for item in data:
            pid = self.regex['get_id'].search(item.a['href']).group(1)
            title = item.a.get_text().lstrip().lstrip(u'原').strip()
            read_num = item.find(text=re.compile(u'阅读数：\d+')).lstrip(u'阅读数：')

            if not all([pid, title, read_num]):
                continue
            id2title[pid] = title
            id2num[pid] = read_num
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

        return True

    def get_next_page(self, article_list_url):
        """ 获取博客的所有文章链接 """
        self.get_username(article_list_url)
        page = 1
        while True:
            page_url = '%s%d' % (article_list_url, page)
            has_next = self.get_read_number(page_url)
            if not has_next:
                return
            page += 1


if __name__ == '__main__':
    try:
        url = cfg.get('csdn', 'target') or sys.argv[1]
        crawler = CSDNCrawler()
        crawler.get_next_page(url)
    except IndexError:
        print '请在config文件或是命令行参数中配置待爬取的CSDN博客地址'
