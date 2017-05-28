#!/usr/bin/env python
# coding=utf-8

from bs4 import BeautifulSoup
from blogPageViews import CSDNCrawler
from sqltool import SqlTool


class CSDNBackup(CSDNCrawler):
    def __init__(self):
        super(CSDNBackup, self).__init__()

    def backup(self):
        with SqlTool(db='blog_csdn') as cursor:
            cursor.execute('select id, author from id_title')
            id_list = cursor.fetchall()
        article_hash = {}
        for line in id_list:
            url = 'http://blog.csdn.net/%s/article/details/%s' % (line[1], line[0])  # construct the url of article
            html = self.download_html(url)
            soup = BeautifulSoup(html, 'lxml')  # get BeautifulSoup object from source code
            if soup.find(id='article_content'):
                article_hash[line[0]] = soup.find(id='article_content').get_text().strip()  # get article's content
            else:
                print "%s - %s can't backup!" % (line[1], line[0])

        with SqlTool(db='blog_csdn') as cursor:
            for id in article_hash:
                cursor.execute("""update id_title set content=%s where id=%s""", (article_hash[id], id))


if __name__ == '__main__':
    blog = CSDNBackup()
    blog.backup()
