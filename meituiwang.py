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

reload(sys)
sys.setdefaultencoding('utf-8')


class Meituiwang:
    def __init__(self):
        self.siteURL = {'qingchun': 'http://www.mm131.com/qingchun/list_1_%s.html',
                        'xinggan': 'http://www.mm131.com/xinggan/list_6_%s.html'}

        self.siteUrlSiwa = 'http://www.4493.com/siwameitui/index-%s.htm'
        self.tool = tool.Tool()
        self.HttpHelper = HttpHelper()

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageindex):
        contents = []
        for baseUrl in self.siteURL:
            url = self.siteURL[baseUrl] % str(pageindex)
            if (pageindex == 1):
                url = 'http://www.mm131.com/%s/' % str(baseUrl)
            contenthtml = self.HttpHelper.getHtml(url)
            if contenthtml != None:
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

    # 获取丝袜美腿的图片索引
    def getImageIndexsForSiwai(self, pageindex):
        contents = []
        url = self.siteUrlSiwa % str(pageindex)
        if (pageindex == 1):
            url = 'http://www.4493.com/siwameitui/'
        contenthtml = self.HttpHelper.getHtml(url)
        if contenthtml != None:
            import lxml.html.soupparser as soupparser
            dom = soupparser.fromstring(contenthtml)
            nodes = dom.xpath("//div[@class='mainer']/div[@class='piclist']/ul/li/a")
            for item in nodes:
                # 套图名称： item.tesx
                # 套图URL item.xpath("@href")[0]
                # append 只能添加一个对象
                if (len(item.xpath("span")[0].text) > 0 and len(item.xpath("@href")) > 0):
                    dict = {'Name': item.xpath("span")[0].text, 'Url': item.xpath("@href")[0]}
                    contents.append(dict)
        return contents

    # 分析套图数量
    def getAllnum(self, pagehtml):
        # class="content">
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-page']/span[@class='page-ch']")
        nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/h1/span[2]")
        text = nodes[0].text

        # number = text[1:len(text) - 1]
        number = text
        num = 0
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
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-pic']/a/img")
        nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/p/img")
        if (len(nodes) == 0):
            nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/img")
        imagesrc = nodes[0].xpath("@src")
        if (len(imagesrc) == 0):
            return None
        return imagesrc[0]

    # 获取套图张数并获取图片信息
    def getPageImages(self, index):
        contents = []
        # 获取索引界面 套图地址
        print u"正在收集第", index, u"页的MM信息"
        # contents = self.getContents(i)
        contents = self.getImageIndexsForSiwai(index)
        print u"收集第", index, u"页的MM信息完成"
        if contents != None:
            # 循环套图地址
            print u"开始循环下载", index, u"页的MM信息"
            for item in contents:
                name = item['Name']
                url = item['Url']
                if "http" not in url:
                    url = 'http://www.4493.com' + url
                print u"发现套图", name, u"套图地址是", url,
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
                    # baseurl = url[0:len(url) - 5]
                    baseurl = url[0:len(url) - 5]
                    # name = "D:/性感美女/" + name
                    name = "D:/丝袜美腿/" + name
                    ishaved = self.mkdir(name)
                    if not ishaved:
                        continue
                    threads = []
                    for i in range(1, allnum):
                        # url = baseurl + ".html"
                        url = baseurl
                        if "http" not in url:
                            url = 'http://www.4493.com' + url
                        if (i > 1):
                            # url = baseurl + '_' + str(i) + ".html"
                            url = baseurl + str(i) + ".htm"
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
                imagesurl = self.getImage(pagehtml)
                if (imagesurl != None):
                    filename = name + "/beautiful" + str(index) + imagesurl[-4:]
                    if not os.path.exists(filename):
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
            print u"名为", path, '的文件夹已经创建'
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
                imagesurl = self.getImage(pagehtml)
                if (imagesurl != None):
                    filename = name + "/beautiful" + str(index) + imagesurl[-4:]
                    if not os.path.exists(filename):
                        # 保存图片
                        if not q.full():
                            q.put([imagesurl, filename])
                            print "图片加入下载队列:" + imagesurl + filename
                            print
                        else:
                            print "下载队列已经满了:" + imagesurl + filename
                            print
        except:
            print "图片加入下载队列失败:" + sys.exc_info()[2]
            print


class producer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self, name="producer Thread")
        self.index = index
        self.meituiwang = Meituiwang()

    def run(self):
        global q
        # for i in range(1, self.index):
        if q.qsize() > 100:
            pass
        else:
            for i in range(1, self.index):
                try:
                    print "开始爬取图片信息:"
                    print
                    self.meituiwang.getPageImages(i)
                except:
                    print "开始爬取图片失败:" + sys.exc_info()[2]
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
                pass
            else:
                print '开始下载'
                print
                inageObj = q.get()
                print '正在下载', inageObj[1], inageObj[0]
                print
                self.saveImg(inageObj[0], inageObj[1])
                print 'consumer' + ' ----- Queue Size:' + str(q.qsize())
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
if __name__ == '__main__':
    p = producer(59)
    p.start()
    for i in range(50):
        c = consumer(i)
        c.start()
