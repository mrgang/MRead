#!/usr/bin/python3
# -*- coding: utf-8 -*-
from lxml import etree
from bs4 import BeautifulSoup
import json,requests
headers = {'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
class Analyzer:
    def mainPage(proto,host,content):
        # 小说首页
        if host == 'm.biqudu.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            image = html.xpath("/html/body/div[4]/div[1]/div/img")[0].get('src')
            name = html.xpath("/html/body/div[4]/div[1]/div[2]//h2")[0].text
            author = html.xpath("/html/body/div[4]/div[1]/div[2]/p[2]")[0].text
            type = html.xpath("/html/body/div[4]/div[1]/div[2]/p[3]")[0].text
            state = html.xpath("/html/body/div[4]/div[1]/div[2]/p[4]")[0].text
            uptime = html.xpath("/html/body/div[4]/div[1]/div[2]/p[5]")[0].text
            latestChapter = html.xpath("/html/body/div[4]/div[1]/div[2]/p[6]/a")[0]
            latestName = latestChapter.text
            latestPath = latestChapter.get('href')
            lastTenChapters = html.xpath("/html/body/div[4]/ul//li/a")
            if not name:
                name = 'null'
            if not latestName:
                latestName = 'null'
            chaps = []
            for chap in lastTenChapters:
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            totleMenu = html.xpath('/html/body/div[4]/div[7]/a')[0].get('href')

            data = {'host': host, 'image': image, 'name': name, 'author': author, 'type': type, 'state': state,
                    'uptime': uptime, 'latestName': latestName, 'latestPath': base_url + latestPath,
                    'lastTen': chaps, 'allChapter': base_url + totleMenu}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.qu.la':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            image = html.xpath("//div[@class='synopsisArea_detail']/img")[0].get('src')

            name = html.xpath("/html/body/header/span[@class='title']")[0].text
            author = html.xpath("//div[@class='synopsisArea_detail']//p[@class='author']")[0].text
            type = html.xpath("//div[@class='synopsisArea_detail']//p[@class='sort']")[0].text.strip()
            state = html.xpath("//div[@class='synopsisArea_detail']//p[2]")[0].text.strip()
            uptime = html.xpath("//div[@class='synopsisArea_detail']//p[3]")[0].text.strip()

            latestChapter = html.xpath("//div[@class='synopsisArea_detail']//p/a")[0]
            latestName = latestChapter.text
            latestPath = latestChapter.get('href')
            lastTenChapters = html.xpath("//div[@id='chapterlist']//p/a")
            chaps = []
            for chap in lastTenChapters:
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            totleMenu = html.xpath('//a[@id="AllChapterList2"]')[0].get('href').strip()

            data = {'host': host, 'image': image, 'name': name, 'author': author, 'type': type, 'state': state,
                    'uptime': uptime, 'latestName': latestName, 'latestPath': base_url + latestPath,
                    'lastTen': chaps, 'allChapter': base_url + totleMenu}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.biqudao.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            image = html.xpath("//div[@id='thumb']/img")[0].get('src')

            name = str(html.xpath("//span[@class='title']")[0].text)
            author = html.xpath("//li[@class='author']")[0].text
            type = html.xpath("//li[@class='sort']")[0].text.strip()

            state = html.xpath("//ul[@id='book_detail']/li[3]")[0].text.strip()
            uptime = html.xpath("//ul[@id='book_detail']/li[4]")[0].text.strip()
            lastTenChapters = html.xpath("//div[@id='chapterlist']//p/a")
            chaps = []
            for chap in lastTenChapters:
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            totleMenu = html.xpath('/html/body/div[3]/h2[2]/a')[0].get('href')
            latestName = ''
            latestPath = ''
            if len(chaps) > 0:
                latestName = chaps[0]['name']
                latestPath = chaps[0]['path']

            data = {'host': host, 'image': image, 'name': name, 'author': author, 'type': type, 'state': state,
                    'uptime': uptime, 'latestName': latestName, 'latestPath': latestPath,
                    'lastTen': chaps, 'allChapter': base_url + totleMenu}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.zwdu.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            image = html.xpath("/html/body/div[4]/div[1]/div[1]/img")[0].get('src')
            name = html.xpath("//div[@class='block_txt2']/p/a/h2")[0].text
            author = html.xpath("//div[@class='block_txt2']/p[2]")[0].text
            type = html.xpath("//div[@class='block_txt2']/p[3]/a")[0].text
            state = html.xpath("//div[@class='block_txt2']/p[4]")[0].text
            uptime = html.xpath("//div[@class='block_txt2']/p[5]")[0].text
            lastTenChapters = html.xpath("//ul[@class='chapter'][1]/li/a")
            chaps = []
            for chap in lastTenChapters:
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            totleMenu = html.xpath("//div[@class='block_txt2']/p/a")[0].get('href')
            latestName = ''
            latestPath = ''
            if len(chaps) > 0:
                latestName = chaps[0]['name']
                latestPath = chaps[0]['path']
            data = {'host': host, 'image': image, 'name': name, 'author': author, 'type': type, 'state': state,
                    'uptime': uptime, 'latestName': latestName, 'latestPath': latestPath,
                    'lastTen': chaps, 'allChapter': base_url + totleMenu}
            result = {'success': True, 'data': data}
            return json.dumps(result)

    def menuPage(proto, host, content):
        # 获取章节目录
        if host == 'm.biqudu.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            chapters = html.xpath("/html/body/div[2]/ul//li/a")
            chaps = []
            for chap in chapters:
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            title = html.xpath("//h1[@id='bqgmb_h1']")[0].text
            data = {'chapters': chaps, 'title': title}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.qu.la':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            chapters = html.xpath("//div[@id='chapterlist']//p/a")
            chaps = []
            flag = True
            for chap in chapters:
                if flag:
                    flag = False
                    continue
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            title = html.xpath("//span[@class='title']")[0].text
            data = {'chapters': chaps, 'title': title}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.biqudao.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            chapters = html.xpath("//div[@id='chapterlist']//p/a")
            chaps = []
            flag = True
            for chap in chapters:
                if flag:
                    flag = False
                    continue
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            title = html.xpath("//span[@class='title']")[0].text
            data = {'chapters': chaps, 'title': title}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.zwdu.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            chapters = html.xpath("//ul[@class='chapter'][2]//li/a")
            chaps = []
            for chap in chapters:
                chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
            title = html.xpath("//h1[@id='bqgmb_h1']")[0].text
            nextpage = html.xpath("//span[@class='right']/a")[0].get('href')
            while nextpage:
                print('huoqu:', base_url + nextpage)
                try:
                    resp = requests.get(base_url + nextpage, headers=headers, timeout=12)
                    resp.encoding = 'GBK'
                    html = etree.HTML(resp.text)
                    chapters = html.xpath("//ul[@class='chapter'][2]//li/a")
                    nextpage = html.xpath("//span[@class='right']/a")[0].get('href')
                    for chap in chapters:
                        chaps.append({'name': chap.text, 'path': base_url + chap.get('href')})
                except:
                    break
            data = {'chapters': chaps, 'title': title}
            result = {'success': True, 'data': data}
            return json.dumps(result)

    def contentPage(proto, host, rest,content):
        # 获取章节内容
        if host == 'm.biqudu.com':
            base_url = proto + '://' + host + '/' + rest.split('/')[1] + '/'
            html = etree.HTML(content)
            title = html.xpath('//div[@class="nr_title"]')[0].text
            preChap = html.xpath('//td[@class="prev"]/a[@id="pt_prev"]')[0].get('href')
            nextChap = html.xpath('//td[@class="next"]/a[@id="pt_next"]')[0].get('href')
            content = etree.tostring(html.xpath('//div[@id="nr1"]')[0], encoding='utf-8')
            data = {'title': title, 'preChap': base_url + preChap, 'nextChap': base_url + nextChap,
                    'content': BeautifulSoup(content, 'lxml').get_text()}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.qu.la':
            base_url = proto + '://' + host + '/' + rest.split('/')[1] + '/' + rest.split('/')[2] + '/'
            html = etree.HTML(content)
            title = html.xpath('/html/head/title')[0].text.split('_')[0]
            preChap = html.xpath('//a[@id="pt_prev"]')[0].get('href')
            nextChap = html.xpath('//a[@id="pt_next"]')[0].get('href')
            content = etree.tostring(html.xpath('//div[@id="chaptercontent"]')[0], encoding='utf-8')
            data = {'title': title, 'preChap': base_url + preChap, 'nextChap': base_url + nextChap,
                    'content': BeautifulSoup(content, 'lxml').get_text()}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.biqudao.com':
            base_url = proto + '://' + host + '/' + rest.split('/')[1] + '/'
            html = etree.HTML(content)
            title = html.xpath('/html/head/title')[0].text.split('_')[0]
            preChap = html.xpath('//a[@id="pt_prev"]')[0].get('href')
            nextChap = html.xpath('//a[@id="pt_next"]')[0].get('href')
            content = etree.tostring(html.xpath('//div[@id="chaptercontent"]')[0], encoding='utf-8')
            data = {'title': title, 'preChap': base_url + preChap, 'nextChap': base_url + nextChap,
                    'content': BeautifulSoup(content, 'lxml').get_text()}
            result = {'success': True, 'data': data}
            return json.dumps(result)
        if host == 'm.zwdu.com':
            base_url = proto + '://' + host
            html = etree.HTML(content)
            title = html.xpath('//div[@id="nr_title"]')[0].text
            preChap = html.xpath('//a[@id="pt_prev"]')[0].get('href')
            nextChap = html.xpath('//a[@id="pt_next"]')[0].get('href')
            content = etree.tostring(html.xpath('//div[@id="nr1"]')[0], encoding='utf-8')
            data = {'title': title, 'preChap': base_url + preChap, 'nextChap': base_url + nextChap,
                    'content': BeautifulSoup(content, 'lxml').get_text()}
            result = {'success': True, 'data': data}
            return json.dumps(result)
    def search(keyword):
        result = []
        # biqudu搜索
        resp = requests.get("http://zhannei.baidu.com/api/customsearch/searchwap?s=13603361664978768713&q=" + keyword,
                            headers=headers)
        if resp.status_code == 200:
            searchResult = json.loads(resp.text)['results']
            if len(searchResult) > 2:
                for i in range(3):
                    url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                    name = searchResult[i]['name']
                    if keyword in name:
                        result.append({'url': url})
        # m.qu.la搜索
        resp = requests.get("http://zhannei.baidu.com/api/customsearch/searchwap?s=920895234054625192&q=" + keyword,
                            headers=headers)
        if resp.status_code == 200:
            searchResult = json.loads(resp.text)['results']
            if len(searchResult) > 2:
                for i in range(3):
                    url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                    name = searchResult[i]['name']
                    if keyword in name:
                        result.append({'url': url})
        # m.biqudao.com搜索
        resp = requests.get(
            "http://zhannei.baidu.com/api/customsearch/searchwap?s=3654077655350271938&q=" + keyword,
            headers=headers)
        if resp.status_code == 200:
            searchResult = json.loads(resp.text)['results']
            if len(searchResult) > 2:
                for i in range(3):
                    url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                    name = searchResult[i]['name']
                    if keyword in name:
                        result.append({'url': url})
        # m.zwdu.com搜索
        resp = requests.get(
            "https://m.zwdu.com/search.php?keyword=" + keyword,
            headers=headers)
        if resp.status_code == 200:
            html = etree.HTML(resp.text)
            cps = html.xpath("//div[@class='result-item result-game-item']")
            mark = 0
            for cpc in cps:
                mark += 1
                if mark > 3: break
                cp = etree.HTML(etree.tostring(cpc))
                url = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('href')
                name = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('title')
                if keyword in name:
                    result.append({'url': url})
        return json.dumps(result)
