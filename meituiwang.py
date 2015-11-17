# -*- coding: UTF-8 -*-
__author__ = 'tzq'
import os
import time
import urllib
import urllib2
import tool
import sys
import chardet
import threading
from WebHelper import HttpHelper
reload(sys)
sys.setdefaultencoding('utf-8')


class Meituiwang:
    def __init__(self):
        self.siteURL = 'http://www.mm131.com/xinggan/list_6_%s.html'
        self.tool = tool.Tool()
        self.HttpHelper = HttpHelper()

    # 保存个人简介
    @staticmethod
    def savemyfiles(content):
        name = 'D:\\test.html'
        f = open(name, "w+")
        print u"正在保存文件", name
        f.write(content.encode('utf-8'))

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageindex):
        url = self.siteURL % str(pageindex)
        contenthtml = self.HttpHelper.getHtml(url)
        if contenthtml != None:
            contents = []
            import lxml.html.soupparser as soupparser
            dom = soupparser.fromstring(contenthtml)
            # doc = dom.parse(dom)/html/body/div/dl/dd
            # /html/body/div/dl/dd
            # //div[@class='main_top']/ul[@class='new public-box']/li/a
            nodes = dom.xpath("//div[@class='main']/dl/dd/a")
            for item in nodes:
                # 套图名称： item.tesx
                # 套图URL item.xpath("@href")[0]
                # append 只能添加一个对象
                if (len(item.xpath("img/@alt")) > 0 and len(item.xpath("@href")) > 0):
                    dict = {'Name': item.xpath("img/@alt")[0], 'Url': item.xpath("@href")[0]}
                    contents.append(dict)
            return contents
        else:
            return None

    # 分析套图数量
    def getAllnum(self, pagehtml):
        # class="content">
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        nodes = dom.xpath("//div[@class='content']/div[@class='content-page']/span[@class='page-ch']")
        text = nodes[0].text
        number = text[1:len(text) - 1]
        num = 0
        try:
            num = int(number)
        except:
            print(number)
            num = 0
        return num

    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        nodes = dom.xpath("//div[@class='content']/div[@class='content-pic']/a/img")
        imagesrc = nodes[0].xpath("@src")
        if (len(imagesrc) == 0):
            return None
        return imagesrc[0]

    # 获取套图张数并获取图片信息
    def getPageImages(self):
        contents = []
        # 获取索引界面 套图地址
        for i in range(1, 59):
            print u"正在收集第", i, u"页的MM"
            contents = self.getContents(i)
            if contents != None:
                # 循环套图地址
                for item in contents:
                    name = item['Name']
                    url = item['Url']
                    print u"发现套图", name, u"套图地址是", url,
                    # 套图地址URL
                    # 得到套图界面代码
                    detailhtml = self.HttpHelper.getHtml(url)
                    allnum = 0
                    ishaved = False
                    if detailhtml != None:
                        # 分析套图数量
                        allnum = self.getAllnum(detailhtml)
                        baseurl = url[0:len(url) - 5]
                        name = "D:/性感美女/" + name
                        ishaved = self.mkdir(name)
                    # 如果有這个文件夹说明上次已经抓取了就不再抓了
                    if (ishaved):
                        threads = []
                        for i in range(1, allnum):
                            url = baseurl + ".html"
                            if (i > 1):
                                url = baseurl + '_' + str(i) + ".html"
                            t1 = threading.Thread(target=self.downloadImage, args=(url, name, i), name=name)
                            threads.append(t1)
                        print u'正在抓取套图' + name
                        for t in threads:
                            t.start()
                        t.join()
                        print u'套图抓取完毕'
        print u"第", i, u"页的MM美照收集完毕"

    def downloadImage(self, url, name, index):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml != None:
                # 循环抓取套图图片
                imagesurl = self.getImage(pagehtml)
                if (imagesurl != None):
                    filename = name + "/beautiful" + str(index) + imagesurl[-4:]
                    # 保存图片
                    self.saveImg(imagesurl, filename)
        except:
            print "保存图片失败:", sys.exc_info()[2]

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        f = []
        try:
            u = urllib.urlopen(imageURL)
            data = u.read()
            f = open(fileName, 'wb')
            f.write(data)
            print fileName
            f.close()
        except:
            print "Unexpected error:", sys.exc_info()[2]
        finally:
            f.close()

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            print u"偷偷新建了名字叫做", path, u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print u"名为", path, '的文件夹已经创建成功'
            return False

    def savePagesInfos(self, start, end):
        for i in range(start, end + 1):
            # print u"正在收集第", i, u"页的糗事"
            self.getPageImages(i)
            time.sleep(1)


# 传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
meituiwang = Meituiwang()
meituiwang.getPageImages()
