__author__ = 'tzq139'
import re
import sys

import threadpool

from basetools import tool
from basetools.WebHelper import HttpHelper
from basetools.dbheper import DBHelper


class BaseSpider:
    def __init__(self):
        self.tool = tool.Tool()
        self.HttpHelper = HttpHelper()
        self.DBHelper = DBHelper()
        self.pool = threadpool.ThreadPool(100)

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
                    return
                detailhtml = self.HttpHelper.getHtml(url)
                if detailhtml != None:
                    # 分析套图数量
                    allnum = self.getAllnum(detailhtml)
                    print(u"套图数量", allnum)
                    baseurl = url[0:len(url) - 5]
                    func_varList = []
                    for i in range(1, allnum + 1):
                        if i > 1:
                            url = baseurl + '_' + str(i) + ".html"
                        else:
                            url = baseurl + ".html"
                        print(u"加入生产队列", url)
                        func_varList.append((None, {'url': url, 'name': name}))
                    requests = threadpool.makeRequests(self.ProductImage, func_varList)
                    [self.pool.putRequest(req) for req in requests]
                    self.pool.wait()
            print(u"循环下载", index, u"页的MM信息完成")

    # 加入生产队列
    def ProductImage(self, url, name):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml != None:
                # 循环抓取套图图片
                print("开始循环抓取套图图片" + url)
                imagesurls = self.getImage(pagehtml)
                if imagesurls is not None and len(imagesurls) > 0:
                    maxnum = 50
                    baseimageurl = ''
                    for i in range(0, len(imagesurls)):
                        pattern = re.compile(r'(.*)(\d{2,3})\.jpg')
                        # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
                        match = pattern.findall(imagesurls[i])
                        if match:
                            baseimage = match.pop(0)
                            baseimageurl = baseimage[0]
                            break;
                        else:
                            dbmageInfo = self.DBHelper.GetImageUrlInfo(name, imagesurls[i])
                            if dbmageInfo is None or len(dbmageInfo) == 0:
                                self.DBHelper.InsertImageUrlInfo(name, imagesurls[i])
                                print("图片存入数据库成功!")
                    if len(baseimageurl) > 1:
                        print("baseimageurl：" + str(baseimageurl))
                        print("maxnum：" + str(maxnum))
                        for index in range(1, maxnum):
                            dbmageInfo = self.DBHelper.GetImageUrlInfo(name, baseimageurl + str(index) + '.jpg')
                            if dbmageInfo is None or len(dbmageInfo) == 0:
                                self.DBHelper.InsertImageUrlInfo(name, baseimageurl + str(index) + '.jpg')
                                print("图片存入数据库成功!")
                print("循环抓取套图图片结束" + url)
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
