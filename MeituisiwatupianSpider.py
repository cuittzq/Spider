import re
import sys
from BaseSpider import BaseSpider

__author__ = 'tzq139'

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

        # 加入生产队列
    def ProductImage(self, url, name, index):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml != None:
                # 循环抓取套图图片
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
                        else:
                            dbmageInfo = self.DBHelper.GetImageUrlInfo(name, imagesurls[i])
                            if dbmageInfo is None or len(dbmageInfo) == 0:
                                self.DBHelper.InsertImageUrlInfo(name, imagesurls[i])
                                print("图片存入数据库! 当前队列数：" + str(self.q.qsize()))

                    if len(baseimageurl) > 1:
                        for index in range(1, maxnum):
                            dbmageInfo = self.DBHelper.GetImageUrlInfo(name, baseimageurl + str(index) + '.jpg')
                            if dbmageInfo is None or len(dbmageInfo) == 0:
                                self.DBHelper.InsertImageUrlInfo(name, baseimageurl + str(index) + '.jpg')
                                print("图片存入数据库! 当前队列数：" + str(self.q.qsize()))



        except:
            print("图片---" + imagesurls[i] + "加入下载队列失败:" + str(sys.exc_info()))
            # 获取索引界面所有MM的信息，list格式

