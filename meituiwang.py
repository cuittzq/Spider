# coding=utf-8
__author__ = 'tzq'
import urllib
import urllib2
import re
import tool
import dbheper
from dbheper import *
import os
import time;
import threading;
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Meituiwang:
    def __init__(self):
        self.siteURL = 'http://www.4493.com/siwameitui/index-%d.htm'
        self.tool = tool.Tool()

    # 解析页面
    def getHtml(self, pageurl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(
            url=pageurl,
            headers=headers
        )
        myResponse = urllib2.urlopen(req).read().decode('gb18030')
        unicode(myResponse, errors='ignore')
        return myResponse

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageIndex):
        url = self.siteURL % (pageIndex)
        page = self.getHtml(url)
        # 套图url http://www.4493.com/siwameitui/31362/1.htm
        # 封面：http://img.1985t.com/uploads/previews/2015/03/0-dnVJdg.jpg
        # 主题：''''''''
        # 时间：2015-03-17
        pattern = re.compile(
            '<li><a href="(.*?)" target="_blank"><img src="(.*?)" alt=".*?"/><span>(.*?)</span></a><b class="b1">(.*?)</b><b class="b2">(.*?)</b></li>',
            re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2], item[3]])
        return contents

    # 分析套图数量
    def getAllnum(self, pagehtml):
        pattern = re.compile(
            '<span id="allnum">(\d*)</span>',
            re.S)
        item = re.find(pattern, pagehtml)
        return int(item)

    def getImage(self, pagehtml):
        pattern = re.compile(
            '<img src="(.*?)" alt=".*?">',
            re.S)
        items = re.findall(pattern, pagehtml)
        return items[0]

    # 获取套图张数并获取图片信息
    def getPageImages(self, pageIndex):
        contents = self.getContents(pageIndex)
        # 套图url http://www.4493.com/siwameitui/31362/1.htm
        # 封面：http://img.1985t.com/uploads/previews/2015/03/0-dnVJdg.jpg
        # 主题：''''''''
        # 时间：2015-03-17
        for item in contents:
            print u"发现套图", item[2], u"套图地址是", item[0], u",创建时间", item[3]
            print u"正在偷偷地保存", item[2], "的信息"
            # 套图地址URL
            detailURL = item[0]

            # 得到套图界面代码
            detailhtml = self.getHtml(detailURL)

            # 分析套图数量
            allnum = self.getAllnum(detailhtml)
            # 基础图片
            baseurl = detailURL[-5:]
            self.mkdir(item[2])
            for i in range(1, allnum):
                url = baseurl + i + ".html"
                pagehtml = self.getHtml(url)
                # 循环抓取套图图片
                imagesurl = self.getImage(pagehtml)
                filename = item[2] + str(i)
                # 保存图片
                self.saveImgs(imagesurl, item[2])

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在悄悄保存她的一张图片为", fileName
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
meituiwang.savePagesInfos(2, 10)
