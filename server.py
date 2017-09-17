#!/usr/bin/env python
# coding=utf-8

from flask import Flask, send_file, abort
from configparser import ConfigParser

app = Flask(__name__)
cfg = ConfigParser()
cfg.read('config')


@app.route('/picture/<pict_name>')
def show_picture(pict_name):
    pictures = ['article_view_num', 'everyday_view_num', 'ten_day_add_num', 'everyday_add_view']
    if pict_name in pictures:
        return send_file('../storage/%s.png' % pict_name, mimetype='image/png', cache_timeout=60 * 30)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(
        host=cfg.get('server', 'host'),
        port=cfg.getint('server', 'port'),
        debug=cfg.getboolean('server', 'debug'),
    )
