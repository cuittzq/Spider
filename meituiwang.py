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


class Meituiwang:
    def __init__(self):
        self.siteURL = 'http://www.4493.com/siwameitui/index-2.htm'
        self.tool = tool.Tool()

    # 解析页面
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
        # 套图url http://www.4493.com/siwameitui/31362/1.htm
        # 封面：http://img.1985t.com/uploads/previews/2015/03/0-dnVJdg.jpg
        # 主题：丝袜美腿性感美女傲人双峰
        # 时间：2015-03-17
        pattern = re.compile(
            '<li><a href="(.*?)" target="_blank"><img src="(.*?)" alt=".*?"/><span>(.*?)</span></a><b class="b1">(.*?)</b><b class="b2">(.*?)</b></li>',
            re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2],item[3]])
        return contents

    # 将一页淘宝MM的信息保存起来
    def savePageInfo(self, pageIndex):
        # 获取第一页淘宝MM列表
        contents = self.getContents(pageIndex)
        for item in contents:

            dbheper = DBHelper()
            dbheper.InsertData(item[0].encode('utf-8').replace('\n', ''), item[1].encode('utf-8').replace('\n', ''),
                               item[2].encode('utf-8'))

    def savePagesInfos(self, start, end):
        for i in range(start, end + 1):
            # print u"正在收集第", i, u"页的糗事"
            self.savePageInfo(i)
            time.sleep(1)
