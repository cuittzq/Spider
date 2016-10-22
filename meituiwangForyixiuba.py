# -*- coding: UTF-8 -*-
__author__ = 'tzq'
import os
import time
import urllib
import urllib2
import tool
import sys
import chardet
import Queue
import threading
from WebHelper import HttpHelper
from dbheper import DBHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class ImageSpider:
    def __init__(self):
        self.siteURL = {'meinvtupianjingpin':'http://www.yixiuba.com/meinvtupianjingpin/list_5_%s.html'}
        #'meituisiwatupian': 'http://www.yixiuba.com/meituisiwatupian/list_2_%s.html',
        self.siteUrlSiwa = 'http://www.4493.com/siwameitui/index-%s.htm'
        self.tool = tool.Tool()
        self.HttpHelper = HttpHelper()
        self.DBHelper = DBHelper()

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageindex):
        contents = []
        for baseUrl in self.siteURL:
            url = self.siteURL[baseUrl] % str(pageindex)
            if (pageindex == 1):
                url = 'http://www.yixiuba.com/%s/' % str(baseUrl)
            contenthtml = self.HttpHelper.getHtml(url)
            if contenthtml != None:
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
                    if (len(item.xpath("@href")) > 0):
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
        if (len(nodes) >0):
            for i in range(0, len(nodes)):
                images.append(nodes[i].xpath("@src")[0])
        if (len(images) == 0):
            return None
        return images

    # 获取套图张数并获取图片信息
    def getPageImages(self, index):
        contents = []
        # 获取索引界面 套图地址
        print u"正在收集第", index, u"页的MM信息"
        contents = self.getContents(index)
        print u"收集第", index, u"页的MM信息完成"
        if contents != None:
            # 循环套图地址
            print u"开始循环下载", index, u"页的MM信息"
            for item in contents:
                name = item['Name']
                url = item['Url']
                if "http" not in url:
                    url = 'http://www.yixiuba.com' + url
                # print u"发现套图", name, u"套图地址是", url,
                # 套图地址URL
                # 得到套图界面代码
                detailhtml = self.HttpHelper.getHtml(url)
                allnum = 0
                ishaved = False
                if detailhtml != None:
                    # 分析套图数量
                    print u"分析套图数量",
                    print
                    allnum = self.getAllnum(detailhtml)
                    print u"套图数量", allnum,
                    print
                    baseurl = url[0:len(url) - 5]
                    threads = []
                    for i in range(1, allnum):
                        url = baseurl
                        if "http" not in url:
                            url = 'http://www.yixiuba.com' + url
                        if (i > 1):
                            url = baseurl + '_'+str(i) + ".html"
                        print u"加入生产队列", url,
                        print
                        # self.ProductImage(url, name, i)
                        t1 = threading.Thread(target=self.ProductImage, args=(url, name, i))
                        threads.append(t1)

                    for t in threads:
                        t.setDaemon(True)
                        t.start()
                    t.join()

            print u"循环下载", index, u"页的MM信息完成"
            print

    # 下载图片
    def downloadImage(self, url, name, index):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml != None:
                # 循环抓取套图图片
                imagesurls = self.getImage(pagehtml)
                if (imagesurls != None):
                    for i in range(0,len(imagesurls)):
                        filename = name + "/beautiful" + str(index) + imagesurls[i][-4:]
                        if not os.path.exists(filename):
                            # 保存图片
                            self.saveImg(imagesurls[i], filename)
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
            # print u"偷偷新建了名字叫做", path, u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print u"名为", path, '的文件夹已经创建'
            print
            return False

    def savePagesInfos(self, start, end):
        for i in range(start, end + 1):
            # print u"正在收集第", i, u"页的糗事"
            self.getPageImages(i)
            time.sleep(1)

    # 加入生产队列
    def ProductImage(self, url, name, index):
        try:
            pagehtml = self.HttpHelper.getHtml(url)
            if pagehtml != None:
                # 循环抓取套图图片
                imagesurls = self.getImage(pagehtml)
                if (imagesurls != None and len(imagesurls) > 0):
                    for i in range(0,len(imagesurls)):
                        ImageInfo =  self.DBHelper.GetImageUrlInfo(name,imagesurls[i]);
                        if ImageInfo != None:
                            self.DBHelper.InsertImageUrlInfo(name,imagesurls[i])
                        # if not os.path.exists(filename):
                        #     # 保存图片
                        #     if not q.full():
                        #         print "图片加入下载队列:" + imagesurls[i] + filename + "队列数：" + str(q.qsize())
                        #         q.put([imagesurls[i], filename])
                        #         print
                        #     else:
                        #         print "下载队列已经满了:" + imagesurls[i] + filename + "队列数：" + str(q.qsize())
                        #         print
        except:
            print "图片---" + imagesurls[i] + "加入下载队列失败:" + str(sys.exc_info())
            print


class producer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self, name="producer Thread")
        self.index = index
        self.meituiwang = ImageSpider()

    def run(self):
        global q
        # for i in range(1, self.index):
        for i in range(1, self.index):
            try:
                if q.qsize() > 100:
                    print "队列已经满了:" + str(q.qsize()) + "休息10s"
                    time.sleep(10)
                    pass

                # print "开始爬取图片信息:"
                # print
                self.meituiwang.getPageImages(i)
            except:
                print "开始爬取图片失败:" + str(sys.exc_info())
            print 'producer' + ' ----- Queue Size:' + str(q.qsize())
            print


# 解析图片
def getImage(self, pagehtml):
    import lxml.html.soupparser as soupparser
    dom = soupparser.fromstring(pagehtml)
    # nodes = dom.xpath("//div[@class='content']/div[@class='content-pic']/a/img")
    nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/p/img")
    if (len(nodes) == 0):
        nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/img")
    imagesrc = nodes[0].xpath("@src")
    if (len(imagesrc) == 0):
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
                print '开始下载'
                print
                inageObj = q.get()
                print '正在下载', inageObj[1], inageObj[0] + str(q.qsize())
                print
                # print 'consumer' + ' ----- Queue Size:' + str(q.qsize())
                # print
                self.saveImg(inageObj[0], inageObj[1])
                print inageObj[1], inageObj[0] + '下载完成'
                print

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


q = Queue.Queue()
q._init(500)
if __name__ == '__main__':
    p = producer(59)
    p.start()
    # for i in range(20):
    #     c = consumer(i)
    #     c.start()
