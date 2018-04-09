#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask,request
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
import requests,json
import urllib.parse as UrlPase
app = Flask(__name__)
from HtmlAnalyzer import Analyzer
headers = {'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
@app.route('/Analyzer/<string:action>',methods=['POST','GET'])
def mainPage(action):
    print(action)
    path = request.args.get('path')
    global resp
    resp = False
    try:
        resp = requests.get(path, headers=headers, timeout=2)
    except:
        # 连接超时，第一次重试
        print('第一次重试', path)
        try:
            resp = requests.get(path, headers=headers, timeout=3)
        except:
            # 连接超时，第二次重试
            print('第二次重试', path)
            try:
                resp = requests.get(path, headers=headers, timeout=30)
            except:
                print('第二次失败', path)
                return json.dumps({'success': False})
    if resp and resp.status_code == 200:
        proto, rest = UrlPase.splittype(resp.url)
        host, rest = UrlPase.splithost(rest)
        if host == 'm.zwdu.com':
            resp.encoding = "GBK"
        else:
            resp.encoding = "utf-8"
        content = resp.text
        if action == "mainPage":
            return Analyzer.mainPage(proto, host, content)
        elif action == 'menuPage':
            return Analyzer.menuPage(proto, host, content)
        elif action == 'contentPage':
            return Analyzer.contentPage(proto, host,rest, content)
        else:
            return json.dumps({'success': False,'content':'current.there has not deal with,later will done'})
@app.route('/Search/<string:keyword>',methods=['POST','GET'])
def search(keyword):
    return Analyzer.search(keyword)
if __name__ == '__main__':
    http_server = WSGIServer(('', 8083), app)
    http_server.serve_forever()