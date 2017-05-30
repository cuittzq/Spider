# coding=utf-8
from importlib import reload
import sys

__author__ = 'tzq'
import time
import urllib.request
import re

from basetools.dbheper import *
from basetools import tool

reload(sys)


# 糗事百科 http://www.qiushibaike.com/textnew/page/35
class Qiushibaike:
    # 页面初始化
    def __init__(self):
        self.siteURL = 'http://www.qiushibaike.com/textnew/page/'
        self.tool = tool.Tool()

    # 解析页面
    def getHtml(self, pageurl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
        }
        req = urllib.request.Request(
            url=pageurl,
            headers=headers
        )
        try:
            myResponse = urllib.request.urlopen(req).read()
            html = myResponse.decode('utf-8', 'ig').encode('utf-8')  ##先转换成unicode编码，然后转换系统编码输出
            return html
        except:
            print
            "Unexpected error:", sys.exc_info()[2]
            return None

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageIndex):
        url = self.siteURL + str(pageIndex)
        pagehtml = self.getHtml(url)
        pattern = re.compile(
            '<div class="article block untagged mb15" .*?class="author clearfix".*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?class="number">(\d*)</i> 好笑</span>',
            re.S)
        items = re.findall(pattern, pagehtml)
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

            print(u"发现一位糗友,名字叫", item[0], u"他讲了一个笑话", item[1], u",收到了", item[2], u"个赞")
            dbheper = DBHelper()
            dbheper.InsertData(item[0].encode('utf-8').replace('\n', ''), item[1].encode('utf-8').replace('\n', ''),
                               item[2].encode('utf-8'))

    def savePagesInfos(self, start, end):
        for i in range(start, end + 1):
            print(u"正在收集第", i, u"页的糗事")
            self.savePageInfo(i)
            time.sleep(1)


# 传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
qiushibaike = Qiushibaike()
qiushibaike.savePagesInfos(1, 35)
