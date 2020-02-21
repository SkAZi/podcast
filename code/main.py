#!/usr/bin/env python
#coding:utf-8

from bottle import Bottle, get, template, response, static_file
from datetime import datetime
from yaml import load
import os
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

app = Bottle()

def refresh():
    data = load(open('data/data.yaml', 'r'), Loader=Loader)
    ret = []
    for item in data['stream']:
        try:
            size = os.path.getsize(os.path.join('data/files', item['file']))
            item['size'] = size
            ret.append(item)
        except:
            pass
    return (ret, data['meta'])

CACHE, TIME, META = [], None, {}
def get_data():
    global CACHE
    global TIME
    global META
    if not TIME or (datetime.now() - TIME).seconds > 60:
        TIME = datetime.now()
        (CACHE, META) = refresh()
    return CACHE

@app.get('/itunes')
def feed():
    global META
    response.content_type = 'application/rss+xml; charset=UTF-8'
    return template('templates/rss.xml', items=get_data(), meta=META)

@app.get('/itunes/preview')
def preview():
    global META
    response.content_type = 'application/rss+xml; charset=UTF-8'
    return template('templates/rss.xml', items=refresh(), meta=META)

@app.route('/feed/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/root/code/data/files')

if __name__== "__main__":
    app.run(host='0.0.0.0', server='gunicorn', port=8000)