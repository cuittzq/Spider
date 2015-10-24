# coding=utf-8
__author__ = 'tzq'
import urllib
import urllib2
import re
import tool
import dbheper
from dbheper import *
import os


# 糗事百科 http://www.qiushibaike.com/textnew/page/35
class Qiushibaike:
    # 页面初始化
    def __init__(self):
        self.siteURL = 'http://www.qiushibaike.com/textnew/page/'
        self.tool = tool.Tool()

    def getHtml(self, pageIndex):
        url = self.siteURL + str(pageIndex)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(
            url=url,
            headers=headers
        )
        myResponse = urllib2.urlopen(req).read().decode('utf-8')
        return myResponse

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageIndex):
        page = self.getHtml(pageIndex)
        pattern = re.compile(
            '<div class="article block untagged mb15" .*? class="author">.*?<img src=".*?"./>(.*?)</a>.*?class="content">(.*?)<!--.*?-->.*?</div>.*?<div class="stats">.*?class="number">(\d*)',
            re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2]])
        return contents

    # 将一页淘宝MM的信息保存起来
    def savePageInfo(self, pageIndex):
        # 获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:
            # item[0]昵称,item[1]糗事,item[2]点赞数
            print u"发现一位糗友,名字叫", item[0], u"他讲了一个笑话", item[1], u",收到了", item[2], u"个赞"
            dbheper = DBHelper()
            dbheper.InsertData(item[0].encode('utf-8').replace('\n', ''), item[1].encode('utf-8').replace('\n', ''),
                               item[2].encode('utf-8'))

    def savePagesInfos(self, start, end):
        for i in range(start, end + 1):
            print u"正在收集糗事。。"
            self.savePageInfo(i)


# 传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
qiushibaike = Qiushibaike()
qiushibaike.savePagesInfos(1, 35)
