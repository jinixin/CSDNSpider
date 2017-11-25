#!/usr/bin/env python
# coding=utf-8

from smtplib import SMTP

from server import cfg


def send_email(msg):
    host = cfg.get('mail', 'host')
    port = cfg.getint('mail', 'port')
    account = cfg.get('mail', 'account')
    password = cfg.get('mail', 'password')
    s = SMTP(host=host, port=port)
    s.starttls()
    s.login(account, password)
    to = ['目标邮箱']
    s.sendmail(from_addr=account, to_addrs=to,
               msg='From:%s\r\nTo:%s\r\nSubject:blog_data\r\n\r\n%s' % (account, to, msg))


if __name__ == '__main__':
    send_email('test')
