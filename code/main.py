#!/usr/bin/env python
#coding:utf-8

from bottle import Bottle, get, template, response
from datetime import datetime
from yaml import load
import os
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

app = Bottle()

def refresh():
    ret = []
    for item in load(open('data/data.yaml', 'r'), Loader=Loader):
        try:
            size = os.path.getsize(os.path.join('data/files', item['file']))
            item['size'] = size
            ret.append(item)
        except:
            pass
    return ret

CACHE, TIME = [], None
def get_data():
    global CACHE
    global TIME
    if not TIME or (datetime.now() - TIME).seconds > 60:
        TIME = datetime.now()
        CACHE = refresh()
    return CACHE

@app.get('/itunes')
def feed():
    response.content_type = 'application/rss+xml; charset=UTF-8'
    return template('templates/rss.xml', items=get_data())

@app.get('/itunes/preview')
def preview():
    response.content_type = 'application/rss+xml; charset=UTF-8'
    return template('templates/rss.xml', items=refresh())

if __name__== "__main__":
    app.run(host='0.0.0.0', server='gunicorn', port=8000)