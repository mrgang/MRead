#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask,render_template
from flask import request
# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
from lxml import etree
import requests,json
import urllib.parse as UrlPase
from bs4 import BeautifulSoup
app = Flask(__name__)
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36'}

xwb = {
    "肺结核": "手部太渊、鱼际、神门、胸痛点、肺点、全息穴、肺心穴",
    "糖尿病": "阳池、腕骨、内分泌、多汗、口疮、夜尿、心点、命门、盆腔点",
    "类风湿关节炎": "三间、合谷、阳溪、少府、前谷、后溪、液门、中诸、腰腿痛、关节痛",
    "荨麻疹": "合谷、阳溪、神门、后溪、肺点、内分泌、多汗点",
    "慢性胃炎": "二间、三间、太陵、中魁、胃肠痛、腹泻、脾点、足三里",
    "消化性溃疡": "脾点、胃肠痛点、阳池、劳宫、太陵",
    "肺炎球菌性肺炎": "太渊、鱼际、商阳、合谷、咳喘点、肺点",
    "贫血": "神门、太陵、肾穴、手心",
    "慢性肺源性心脏病": "太渊、鱼际、神门、少冲、太陵、心点、肺点",
    "流性性感冒": "肺点、咽喉痛点、头痛点、十宣、液门、中诸、阳谷、商阳、太渊",
    "肝硬变": "肝点、内分泌、脾点、偏头痛点、八邪、中诸、液门",
    "冠心病": "心点、胞痛点、太渊、鱼际、劳宫、太陵",
    "病毒性肝炎": "肝点、头痛点、脾点、膈点、商阳、神门、腕骨、阳谷",
    "慢性支气管炎": "肺点、咳喘点、神门、少府、少商、鱼际、太渊",
    "甲状腺功能亢进症": "内分泌点、神门、少府、少冲、中冲、八邪",
    "尿路感染": "盆腔点、命门点、尿道点、夜尿",
    "营养不良": "脾点、胃痛点、口疮点、头痛点、大陵、神门、胃肠痛点",
    "头痛": "牙签刺激心穴、太陵穴",
    "腹泻": "下痢点",
    "不寐": "神门、心点、多汗点、脑点",
    "躁郁症": "合谷、神门、少冲、阳谷、太陵、十宣、头痛、多汗、脑点（抑郁症持续和缓按摩、躁狂宜强烈刺激方法）",
    "近视眼": "商阳、二间、三间、合谷、前谷、后溪、阳谷、液门、八邪、眼痛",
    "便秘": "右手第２指间有疼痛感指酒精或植物性食物食用过量,左手第２指间有疼痛感指鱼肉或动物性食物食用过量",
    "肺病": "少商",
    "心脏病": "指压心包区、精心区用两手互搓刺激",
    "肠胃病不适": "商阳、食指第一指节",
    "胃炎": "香烟头炙或牙签刺激前头点",
    "肝、胆结石": "连续强力刺激片头点",
    "胆疾": "指压或香烟炙治肝穴可遏制疾病发生",
    "生殖器官异常": "指压命门，对小孩夜间尿也颇有效果。",
    "悸动、气喘": "心包区、中冲、少冲、神门",
    "食欲不振": "手心、胃、脾、大肠区",
    "肩酸": "强刺激合谷穴",
    "慢性肩酸": "以香烟头炙治",
    "胸口郁结": "强刺激胸腹区、胃肠点",
    "失眠": "包心区、手掌区、轻轻按摩中冲穴",
    "整个头痛": "前头点",
    "头心疼痛": "前头点",
    "后脑疼痛": "后头点",
    "头两侧": "片头点",
    "暴饮暴食或宿醉": "前头点",
    "焦虑不安": "中冲、少冲、心穴、太陵、虎边、阳溪、虎边穴是治疗羊癫疯的物效穴",
    "低血压": "心经、心包经、三焦经、神门、太陵、阳池、中诸",
    "发冷": "阳池、关冲、命门刺激阳池最好缓慢、长久，施以缓刺激",
    "急性脑血管病": "脑点、头痛点、二间、合谷、神门、少府、中冲、降压点",
    "眼睛疲劳": "心包区  用发夹的头锐部刺激商阳、少泽穴施以强刺激",
    "牙痛": "肾穴",
    "齿髓发炎": "肾穴",
    "齿粘膜疼痛": "合谷  齿面疼痛强刺激肝穴",
    "睡的拧筋": "香烟头炙治少泽穴、“颈、咽区”、颈顶点",
    "晕车": "神门、关冲、手心",
    "白发": "肾穴、命门  只可轻轻指压，强刺激效果相反",
    "老花眼": "养老穴对上了年纪的人老花眼、眼睛疲劳、眼睛充血非常有效",
    "更年期障碍": "反复刺激肾穴、阳池、二间、关冲",
    "腹胀": "轻按大肠、二间、胃、脾、大肠区",
    "痔疮": "合谷、大肠",
    "关节酸痛": "虎合寸、阳池穴",
    "腰痛": "腰腿点、定腿区、坐骨神经点、腰腿点",
    "胃痛": "数根牙签捆成一束刺激胃肠点落零五",
    "晕眩": "关冲、耳咽区、阳谷、中渚、液门",
    "耳鸣": "肾穴、前谷、关冲、阳谷",
    "气喘": "香烟点炙治咳喘点,有灼热感时立即移开隔一会儿再继续,三~五分钟能压制三间",
    "肌肤老化": "肾穴、阳池、肺穴、关冲",
    "假性近视": "劳宫、肝穴、腕骨",
    "高血压": "阳溪穴、合谷、落零五、降压、神门、心点、阳谷"
}

@app.route('/botAsk',methods=['POST','GET'])
def botAsk():
    if request.method == 'POST':
        origin = request.form['origin']
        action = request.form['action']
        if action == 'ask':
            question = request.form['question']
            try:
                return xwb[question]
            except:
                return "诊断:" + question
        elif action == 'words':
            res = ""
            for k in xwb:
                res += k+"\n"
            return res
    else:
        origin = request.args.get('origin')
        action = request.args.get('action')
        if action == 'ask':
            question = request.args.get('question')
            try:
                return xwb[question]
            except:
                return "诊断:" + question
        elif action == 'words':
            res = ""
            for k in xwb:
                res += k+"\n"
            return res

@app.route('/Analyzer',methods=['POST','GET'])
def analyzer():
    actionType = request.args.get('actionType')
    distination = request.args.get('distination')
    resp = False
    try:
        resp = requests.get(distination, headers=headers, timeout=2)
    except:
        #连接超时，第一次重试
        print('第一次重试')
        try:
            resp = requests.get(distination, headers=headers, timeout=3)
        except:
            # 连接超时，第二次重试
            print('第二次重试')
            try:
                resp = requests.get(distination, headers=headers, timeout=30)
            except:
                print('第二次失败')
                return json.dumps({'success': False})
    if resp and resp.status_code == 200:
        proto, rest = UrlPase.splittype(resp.url)
        host, rest = UrlPase.splithost(rest)
        if actionType == '1':
            #小说首页
            if host == 'm.biqudu.com':
                base_url = proto + '://' + host
                html = etree.HTML(resp.text)
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
                    chaps.append({'name':chap.text,'path':base_url+chap.get('href')})
                totleMenu = html.xpath('/html/body/div[4]/div[7]/a')[0].get('href')

                data = {'host':host,'image':image,'name':name,'author':author,'type':type,'state':state,
                          'uptime':uptime,'latestName':latestName,'latestPath':base_url+latestPath,
                          'lastTen':chaps,'allChapter':base_url+totleMenu}
                result = {'success':True,'data':data}
                return json.dumps(result)
            if host == 'm.qu.la':
                base_url = proto + '://' + host
                html = etree.HTML(resp.text)
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
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                totleMenu = html.xpath('//a[@id="AllChapterList2"]')[0].get('href').strip()

                data = {'host':host,'image':image,'name':name,'author':author,'type':type,'state':state,
                          'uptime':uptime,'latestName':latestName,'latestPath':base_url+latestPath,
                          'lastTen':chaps,'allChapter':base_url+totleMenu}
                result = {'success': True, 'data': data}
                return json.dumps(result)
            if host == 'm.biqudao.com':
                base_url = proto + '://' + host
                html = etree.HTML(resp.text)
                image = html.xpath("//div[@id='thumb']/img")[0].get('src')

                name = str(html.xpath("//span[@class='title']")[0].text)
                author = html.xpath("//li[@class='author']")[0].text
                type = html.xpath("//li[@class='sort']")[0].text.strip()

                state = html.xpath("//ul[@id='book_detail']/li[3]")[0].text.strip()
                uptime = html.xpath("//ul[@id='book_detail']/li[4]")[0].text.strip()
                lastTenChapters = html.xpath("//div[@id='chapterlist']//p/a")
                chaps = []
                for chap in lastTenChapters:
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                totleMenu = html.xpath('/html/body/div[3]/h2[2]/a')[0].get('href')
                latestName=''
                latestPath=''
                if len(chaps) > 0:
                    latestName = chaps[0]['name']
                    latestPath = chaps[0]['path']

                data = {'host':host,'image':image,'name':name,'author':author,'type':type,'state':state,
                          'uptime':uptime,'latestName':latestName,'latestPath':latestPath,
                          'lastTen':chaps,'allChapter':base_url+totleMenu}
                result = {'success': True, 'data': data}
                return json.dumps(result)
            if host == 'm.zwdu.com':
                base_url = proto + '://' + host
                resp.encoding='gbk'
                html = etree.HTML(resp.text)

                image = html.xpath("/html/body/div[4]/div[1]/div[1]/img")[0].get('src')
                name = html.xpath("//div[@class='block_txt2']/p/a/h2")[0].text
                author = html.xpath("//div[@class='block_txt2']/p[2]")[0].text
                type = html.xpath("//div[@class='block_txt2']/p[3]/a")[0].text
                state = html.xpath("//div[@class='block_txt2']/p[4]")[0].text
                uptime = html.xpath("//div[@class='block_txt2']/p[5]")[0].text
                lastTenChapters = html.xpath("//ul[@class='chapter'][1]/li/a")
                chaps = []
                for chap in lastTenChapters:
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                totleMenu = html.xpath("//div[@class='block_txt2']/p/a")[0].get('href')
                latestName = ''
                latestPath = ''
                if len(chaps) > 0:
                    latestName = chaps[0]['name']
                    latestPath = chaps[0]['path']
                data = {'host':host,'image':image,'name':name,'author':author,'type':type,'state':state,
                          'uptime':uptime,'latestName':latestName,'latestPath':latestPath,
                          'lastTen':chaps,'allChapter':base_url+totleMenu}
                result = {'success': True, 'data': data}
                return json.dumps(result)

        if actionType == '2':
            #获取章节内容
            if host == 'm.biqudu.com':
                base_url = proto + '://' + host + '/'+rest.split('/')[1]+'/'
                html = etree.HTML(resp.text)
                title = html.xpath('//div[@class="nr_title"]')[0].text
                preChap = html.xpath('//td[@class="prev"]/a[@id="pt_prev"]')[0].get('href')
                nextChap = html.xpath('//td[@class="next"]/a[@id="pt_next"]')[0].get('href')
                content = etree.tostring(html.xpath('//div[@id="nr1"]')[0], encoding='utf-8')
                data = {'title':title,'preChap':base_url+preChap,'nextChap':base_url+nextChap,
                        'content':BeautifulSoup(content,'lxml').get_text()}
                result = {'success': True, 'data': data}
                return  json.dumps(result)
            if host == 'm.qu.la':
                base_url = proto + '://' + host + '/'+rest.split('/')[1]+'/'+rest.split('/')[2]+'/'
                html = etree.HTML(resp.text)
                title = html.xpath('/html/head/title')[0].text.split('_')[0]
                preChap = html.xpath('//a[@id="pt_prev"]')[0].get('href')
                nextChap = html.xpath('//a[@id="pt_next"]')[0].get('href')
                content = etree.tostring(html.xpath('//div[@id="chaptercontent"]')[0], encoding='utf-8')
                data = {'title':title,'preChap':base_url+preChap,'nextChap':base_url+nextChap,
                        'content':BeautifulSoup(content,'lxml').get_text()}
                result = {'success': True, 'data': data}
                return  json.dumps(result)
            if host == 'm.biqudao.com':
                base_url = proto + '://' + host + '/'+rest.split('/')[1]+'/'
                html = etree.HTML(resp.text)
                title = html.xpath('/html/head/title')[0].text.split('_')[0]
                preChap = html.xpath('//a[@id="pt_prev"]')[0].get('href')
                nextChap = html.xpath('//a[@id="pt_next"]')[0].get('href')
                content = etree.tostring(html.xpath('//div[@id="chaptercontent"]')[0], encoding='utf-8')
                data = {'title':title,'preChap':base_url+preChap,'nextChap':base_url+nextChap,
                        'content':BeautifulSoup(content,'lxml').get_text()}
                result = {'success': True, 'data': data}
                return  json.dumps(result)
            if host == 'm.zwdu.com':
                base_url = proto + '://' + host
                resp.encoding = 'gbk'
                html = etree.HTML(resp.text)
                title = html.xpath('//div[@id="nr_title"]')[0].text
                preChap = html.xpath('//a[@id="pt_prev"]')[0].get('href')
                nextChap = html.xpath('//a[@id="pt_next"]')[0].get('href')
                content = etree.tostring(html.xpath('//div[@id="nr1"]')[0], encoding='utf-8')
                data = {'title': title, 'preChap': base_url+preChap, 'nextChap': base_url+nextChap,
                        'content': BeautifulSoup(content, 'lxml').get_text()}
                result = {'success': True, 'data': data}
                return json.dumps(result)
        if actionType == '3':
            #获取章节目录
            if host == 'm.biqudu.com':
                base_url = proto + '://' + host
                html = etree.HTML(resp.text)
                chapters = html.xpath("/html/body/div[2]/ul//li/a")
                chaps = []
                for chap in chapters:
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                title = html.xpath("//h1[@id='bqgmb_h1']")[0].text
                data = {'chapters':chaps,'title':title}
                result = {'success': True, 'data': data}
                return json.dumps(result)
            if host == 'm.qu.la':
                base_url = proto + '://' + host
                html = etree.HTML(resp.text)
                chapters = html.xpath("//div[@id='chapterlist']//p/a")
                chaps = []
                flag = True
                for chap in chapters:
                    if flag:
                        flag = False
                        continue
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                title = html.xpath("//span[@class='title']")[0].text
                data = {'chapters': chaps, 'title': title}
                result = {'success': True, 'data': data}
                return json.dumps(result)
            if host == 'm.biqudao.com':
                base_url = proto + '://' + host
                html = etree.HTML(resp.text)
                chapters = html.xpath("//div[@id='chapterlist']//p/a")
                chaps = []
                flag = True
                for chap in chapters:
                    if flag:
                        flag = False
                        continue
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                title = html.xpath("//span[@class='title']")[0].text
                data = {'chapters': chaps, 'title': title}
                result = {'success': True, 'data': data}
                return json.dumps(result)
            if host == 'm.zwdu.com':
                base_url = proto + '://' + host
                resp.encoding = 'GBK'
                html = etree.HTML(resp.text)
                chapters = html.xpath("//ul[@class='chapter'][2]//li/a")
                chaps = []
                for chap in chapters:
                    chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                title = html.xpath("//h1[@id='bqgmb_h1']")[0].text
                nextpage = html.xpath("//span[@class='right']/a")[0].get('href')
                while nextpage :
                    resp = requests.get(base_url+nextpage, headers=headers)
                    resp.encoding = 'GBK'
                    html = etree.HTML(resp.text)
                    chapters = html.xpath("//ul[@class='chapter'][2]//li/a")
                    nextpage = html.xpath("//span[@class='right']/a")[0].get('href')
                    for chap in chapters:
                        chaps.append({'name': chap.text, 'path': base_url+chap.get('href')})
                data = {'chapters': chaps, 'title': title}
                result = {'success': True, 'data': data}
                return json.dumps(result)

    return json.dumps({'success':False})
@app.route('/Search',methods=['POST','GET'])
def search():
    keyword = request.args.get('q')
    result = []
    #biqudu搜索
    resp = requests.get("http://zhannei.baidu.com/api/customsearch/searchwap?s=13603361664978768713&q="+keyword, headers=headers)
    if resp.status_code == 200:
        searchResult = json.loads(resp.text)['results']
        if len(searchResult) > 2:
            for i in range(3):
                url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                result.append({'url': url})

                # name = searchResult[i]['name']
                # author = searchResult[i]['author_name']
                # image = searchResult[i]['image'].replace('http','https').replace('www','m')
                # newestChapter_headline = searchResult[i]['newestChapter_headline']
                #
                # newestChapter_url = searchResult[i]['newestChapter_url'].replace('http','https').replace('www','m')
                #
                # url = searchResult[i]['url'].replace('http','https').replace('www','m')
                # result.append({'name':name,'author':author,'image':image,
                #                'newestChapter_headline':newestChapter_headline,
                #                'newestChapter_url':newestChapter_url,
                #                'url':url})
    # m.qu.la搜索
    resp = requests.get("http://zhannei.baidu.com/api/customsearch/searchwap?s=920895234054625192&q=" + keyword,
                        headers=headers)
    if resp.status_code == 200:
        searchResult = json.loads(resp.text)['results']
        if len(searchResult) > 2:
            for i in range(3):
                url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                result.append({'url': url})
                # name = searchResult[i]['name']
                # author = searchResult[i]['author_name']
                # image = searchResult[i]['image'].replace('http', 'https').replace('www', 'm')
                # newestChapter_headline = searchResult[i]['newestChapter_headline']
                #
                # newestChapter_url = searchResult[i]['newestChapter_url'].replace('http', 'https').replace('www', 'm')
                #
                # url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                # result.append({'name': name, 'author': author, 'image': image,
                #                'newestChapter_headline': newestChapter_headline,
                #                'newestChapter_url': newestChapter_url,
                #                'url': url})
    # m.biqudao.com搜索
    resp = requests.get(
        "http://zhannei.baidu.com/api/customsearch/searchwap?s=3654077655350271938&q=" + keyword,
        headers=headers)
    if resp.status_code == 200:
        searchResult = json.loads(resp.text)['results']
        if len(searchResult) > 2:
            for i in range(3):
                url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                result.append({'url': url})
                # name = searchResult[i]['name']
                # author = searchResult[i]['author_name']
                # image = searchResult[i]['image'].replace('http', 'https').replace('www', 'm')
                # newestChapter_headline = searchResult[i]['newestChapter_headline']
                #
                # newestChapter_url = searchResult[i]['newestChapter_url'].replace('http', 'https').replace('www',
                #                                                                                           'm')
                #
                # url = searchResult[i]['url'].replace('http', 'https').replace('www', 'm')
                # result.append({'name': name, 'author': author, 'image': image,
                #                'newestChapter_headline': newestChapter_headline,
                #                'newestChapter_url': newestChapter_url,
                #                'url': url})
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
            result.append({'url': url})

            # name = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('title')
            # url = cp.xpath("/html/body/div/div[2]/h3/a")[0].get('href')
            # author = cp.xpath("/html/body/div/div[2]/div/p/span[2]")[0].text.strip()
            # image = cp.xpath("/html/body/div/div/a/img")[0].get('src')
            # newestChapter_headline = cp.xpath("/html/body/div/div[2]/div/p[4]/a")[0].text
            # newestChapter_url = cp.xpath("/html/body/div/div[2]/div/p[4]/a")[0].get('href')
            # result.append({'name': name, 'author': author, 'image': image,
            #                'newestChapter_headline': newestChapter_headline,
            #                'newestChapter_url': newestChapter_url,
            #                'url': url})
    return json.dumps(result)

if __name__ == '__main__':
    http_server = WSGIServer(('', 8083), app)
    http_server.serve_forever()