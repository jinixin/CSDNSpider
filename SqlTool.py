#!/usr/bin/env python
# coding=utf-8

import MySQLdb


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
