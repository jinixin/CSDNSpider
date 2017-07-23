#!/usr/bin/env python
# coding=utf-8

from flask import Flask, send_file, abort

app = Flask(__name__)


@app.route('/picture/<pict_name>')
def show_picture(pict_name):
    pictures = ['article_view_num', 'everyday_view_num', 'ten_day_add_num']
    if pict_name in pictures:
        return send_file('../storage/%s.png' % pict_name, mimetype='image/png', cache_timeout=60 * 10)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
