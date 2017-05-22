# -*- coding: UTF-8 -*-
__author__ = 'tzq'
import os
import time
import sys
import queue
import threading

import tool
from WebHelper import HttpHelper
from dbheper import DBHelper


class BaseSpider:
    def __init__(self):
        self.tool = tool.Tool()
        self.HttpHelper = HttpHelper()
        self.DBHelper = DBHelper()

    # 下载图片并保存本地
    def downloadImage(self, url, name, index):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml is not None:
                # 循环抓取套图图片
                imagesurls = self.getImage(pagehtml)
                if imagesurls is not None:
                    for i in range(0, len(imagesurls)):
                        filename = name + "/beautiful" + str(index) + imagesurls[i][-4:]
                        if not os.path.exists(filename):
                            # 保存图片
                            self.filehelper.saveImg(imagesurls[i], filename)
        except:
            print("保存图片失败:", sys.exc_info()[2])
            # 获取套图张数并获取图片信息

    # 解析图片列表并循环解析图片地址
    def getPageImages(self, index):
        # 获取索引界面 套图地址
        print(u"正在收集第", index, u"页的MM信息")
        contents = self.getContents(index)
        print(u"收集第", index, u"页的MM信息完成")
        if contents is not None:
            # 循环套图地址
            print(u"开始循环下载", index, u"页的MM信息")
            for item in contents:
                name = item['Name']
                url = item['Url']
                if "http" not in url:
                    url = 'http://www.yixiuba.com' + url
                # print u"发现套图", name, u"套图地址是", url,
                # 套图地址URL
                # 得到套图界面代码
                detailhtml = self.HttpHelper.getHtml(url)
                if detailhtml != None:
                    # 分析套图数量
                    print(u"分析套图数量", )
                    allnum = self.getAllnum(detailhtml)
                    print(u"套图数量", allnum)
                    baseurl = url[0:len(url) - 5]
                    threads = []
                    for i in range(1, allnum + 1):
                        url = baseurl
                        if "http" not in url:
                            url = 'http://www.yixiuba.com' + url
                        if i > 1:
                            url = baseurl + '_' + str(i) + ".html"
                        else:
                            url = baseurl + ".html"
                        print(u"加入生产队列", url)
                        t1 = threading.Thread(target=self.ProductImage, args=(url, name, i))
                        threads.append(t1)

                    for t in threads:
                        t.setDaemon(True)
                        t.start()
                    t.join()

            print(u"循环下载", index, u"页的MM信息完成")

    # 加入生产队列
    def ProductImage(self, url, name, index):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml != None:
                # 循环抓取套图图片
                imagesurls = self.getImage(pagehtml)
                if imagesurls is not None and len(imagesurls) > 0:
                    for i in range(0, len(imagesurls)):
                        dbmageInfo = self.DBHelper.GetImageUrlInfo(name, imagesurls[i])
                        if dbmageInfo is None or len(dbmageInfo) == 0:
                            self.DBHelper.InsertImageUrlInfo(name, imagesurls[i])
                            print("图片存入数据库! 当前队列数：" + str(q.qsize()))
        except:
            print("图片---" + imagesurls[i] + "加入下载队列失败:" + str(sys.exc_info()))
            # 获取索引界面所有MM的信息，list格式

    # 解析网页套图信息
    def getContents(self, pageindex):
        contents = []
        for baseUrl in self.siteURL:
            url = self.siteURL[baseUrl] % str(pageindex)
            if 1 == pageindex:
                url = 'http://www.tu11.com/%s/' % str(baseUrl)
            contenthtml = self.HttpHelper.getHtml(url)
            if contenthtml is not None:
                import lxml.html.soupparser as soupparser
                dom = soupparser.fromstring(contenthtml)
                # doc = dom.parse(dom)/html/body/div/dl/dd
                # /html/body/div/dl/dd
                # //div[@class='main_top']/ul[@class='new public-box']/li/a
                nodes = dom.xpath("//div[@class='page1']/ul/li/a")
                for item in nodes:
                    # 套图名称： item.tesx
                    # 套图URL item.xpath("@href")[0]
                    # append 只能添加一个对象
                    if len(item.xpath("@href")) > 0:
                        dict = {'Name': item.xpath("@title")[0], 'Url': item.xpath("@href")[0]}
                        contents.append(dict)
        return contents

    # 分析套图数量
    def getAllnum(self, pagehtml):
        # class="content">
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-page']/span[@class='page-ch']")
        nodes = dom.xpath("//div[@class='dede_pages']/ul/li/a")
        text = nodes[0].text

        number = text[1:len(text) - 3]
        try:
            num = int(number)
        except:
            print(number)
            num = 0
        return num

    # 解析图片
    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = /html/body/div[3]/div[3]/p/img
        nodes = dom.xpath("//div[@class='center']/div[@class='page-list']/p/img")
        images = []
        if len(nodes) > 0:
            for i in range(0, len(nodes)):
                images.append(nodes[i].xpath("@src")[0])
        if 0 == len(images):
            return None
        return images


class MeituisiwatupianSpider(BaseSpider):
    def __init__(self):
        self.siteURL = {'meituisiwatupian': 'http://www.tu11.com/meituisiwatupian/list_2_%s.html',
                        'xingganmeinvxiezhen': 'http://www.tu11.com/xingganmeinvxiezhen/list_2_%s.html',
                        'BEAUTYLEGtuimo': 'http://www.tu11.com/BEAUTYLEGtuimo/list_2_%s.html',
                        'shenghuomeinvzipai': 'http://www.tu11.com/shenghuomeinvzipai/list_2_%s.html'}
        BaseSpider.__init__(self)

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageindex):
        contents = []
        for baseUrl in self.siteURL:
            url = self.siteURL[baseUrl] % str(pageindex)
            if pageindex == 1:
                url = 'http://www.tu11.com/%s/' % str(baseUrl)
            contenthtml = self.HttpHelper.getHtml(url)
            if contenthtml is not None:
                import lxml.html.soupparser as soupparser
                dom = soupparser.fromstring(contenthtml)
                # doc = dom.parse(dom)/html/body/div/dl/dd
                # /html/body/div/dl/dd
                # //div[@class='main_top']/ul[@class='new public-box']/li/a
                nodes = dom.xpath("//div[@class='page1']/ul/li/a")
                for item in nodes:
                    # 套图名称： item.tesx
                    # 套图URL item.xpath("@href")[0]
                    # append 只能添加一个对象
                    if len(item.xpath("@href")) > 0:
                        dict = {'Name': item.xpath("@title")[0], 'Url': item.xpath("@href")[0]}
                        contents.append(dict)
        return contents

    # 分析套图数量
    def getAllnum(self, pagehtml):
        # class="content">
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-page']/span[@class='page-ch']")
        nodes = dom.xpath("//div[@class='dede_pages']/ul/li/a")
        text = nodes[0].text

        number = text[1:len(text) - 3]
        try:
            num = int(number)
        except:
            print(number)
            num = 0
        return num

    # 解析图片
    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = /html/body/div[3]/div[3]/p/img
        nodes = dom.xpath("//div[@class='center']/div[@class='page-list']/p/img")
        images = []
        if len(nodes) > 0:
            for i in range(0, len(nodes)):
                images.append(nodes[i].xpath("@src")[0])
        if len(images) == 0:
            return None
        return images


class MeinvtupianSpider(BaseSpider):
    def __init__(self):
        self.siteURL = {'meinvtupian': 'http://www.umei.cc/meinvtupian/siwameinv/%s.htm'}

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageindex):
        contents = []
        for baseUrl in self.siteURL:
            url = self.siteURL[baseUrl] % str(pageindex)
            if 1 == pageindex:
                url = 'http://www.tu11.com/%s/' % str(baseUrl)
            contenthtml = self.HttpHelper.getHtml(url)
            if contenthtml is not None:
                import lxml.html.soupparser as soupparser
                dom = soupparser.fromstring(contenthtml)
                # doc = dom.parse(dom)/html/body/div/dl/dd
                # /html/body/div/dl/dd
                # //div[@class='main_top']/ul[@class='new public-box']/li/a
                nodes = dom.xpath("//div[@class='page1']/ul/li/a")
                for item in nodes:
                    # 套图名称： item.tesx
                    # 套图URL item.xpath("@href")[0]
                    # append 只能添加一个对象
                    if len(item.xpath("@href")) > 0:
                        dict = {'Name': item.xpath("@title")[0], 'Url': item.xpath("@href")[0]}
                        contents.append(dict)
        return contents

    # 分析套图数量
    def getAllnum(self, pagehtml):
        # class="content">
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-page']/span[@class='page-ch']")
        nodes = dom.xpath("//div[@class='dede_pages']/ul/li/a")
        text = nodes[0].text

        number = text[1:len(text) - 3]
        try:
            num = int(number)
        except:
            print(number)
            num = 0
        return num

        # 解析图片

    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = /html/body/div[3]/div[3]/p/img
        nodes = dom.xpath("//div[@class='center']/div[@class='page-list']/p/img")
        images = []
        if len(nodes) > 0:
            for i in range(0, len(nodes)):
                images.append(nodes[i].xpath("@src")[0])
        if 0 == len(images):
            return None
        return images


class producer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self, name="producer Thread")
        self.index = index
        self.meituiwang = MeituisiwatupianSpider()

    def run(self):
        global q
        # for i in range(1, self.index):
        for i in range(1, self.index):
            try:
                if q.qsize() > 100:
                    print
                    "队列已经满了:" + str(q.qsize()) + "休息10s"
                    time.sleep(10)
                    pass
                self.meituiwang.getPageImages(i)
            except:
                print("开始爬取图片失败:" + str(sys.exc_info()))
            print('producer' + ' ----- Queue Size:' + str(q.qsize()))

    # 解析图片
    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-pic']/a/img")
        nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/p/img")
        if len(nodes) == 0:
            nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/img")
        imagesrc = nodes[0].xpath("@src")
        if len(imagesrc) == 0:
            return None
        return imagesrc[0]


class consumer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self, name="consumer Thread-%d" % index)

    def run(self):
        global q
        while True:
            if q.qsize() < 1:
                threading._sleep(5)
                pass
            else:
                print('开始下载')
                inageObj = q.get()
                print('正在下载', inageObj[1], inageObj[0] + str(q.qsize()))
                self.filehelper.saveImg(inageObj[0], inageObj[1])
                print(inageObj[1], inageObj[0] + '下载完成')


q = queue.Queue()
q._init(500)
if __name__ == '__main__':
    p = producer(59)
    p.start()
    # for i in range(20):
    #     c = consumer(i)
    #     c.start()
