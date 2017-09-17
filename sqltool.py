#!/usr/bin/env python
# coding=utf-8

import MySQLdb

from server import cfg


class SqlTool(object):
    """Tool to deal with SQL"""

    def __init__(self):
        self.connect = MySQLdb.connect(
            host=cfg.get('mysql', 'host'),
            port=cfg.getint('mysql', 'port'),
            user=cfg.get('mysql', 'user'),
            passwd=cfg.get('mysql', 'pwd'),
            db=cfg.get('mysql', 'db'),
            charset='utf8',
        )
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
