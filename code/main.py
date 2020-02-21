#!/usr/bin/env python
#coding:utf-8

from bottle import Bottle, get, template
from datetime import datetime
from yaml import load
import os
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

app = Bottle()
CACHE, TIME = [], None

def get_data():
    global CACHE
    global TIME
    if not TIME or (datetime.now() - TIME).seconds > 10:
        TIME = datetime.now()
        CACHE = []
        data = load(open('data/data.yaml', 'r'), Loader=Loader)
        for item in data:
            try:
                size = os.path.getsize(os.path.join('data/files', item['file']))
                item['size'] = size
                CACHE.append(item)
            except:
                pass
    return CACHE

@app.get('/itunes')
def feed():
    return template('templates/rss.xml', items=get_data())

if __name__== "__main__":
    app.run(host='0.0.0.0', server='gunicorn', port=8000)