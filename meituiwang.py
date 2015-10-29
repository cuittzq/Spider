# -*- coding: UTF-8 -*-
__author__ = 'tzq'
import os
import time
import urllib
import urllib2
import re
import tool
import chardet
from dbheper import *

reload(sys)
sys.setdefaultencoding('utf-8')


class Meituiwang:
    def __init__(self):
        self.siteURL = 'http://www.mm131.com/'
        self.tool = tool.Tool()

    # 保存个人简介
    @staticmethod
    def savemyfiles(content):
        name = 'D:\\test.html'
        f = open(name, "w+")
        print u"正在保存文件", name
        f.write(content.encode('utf-8'))

    # 解析页面
    def getHtml(self, pageurl):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.4493.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
        }
        req = urllib2.Request(
            url='http://www.xmeise.com/neiyi/siwa/',
            headers=headers
        )


        reqtest = urllib2.Request('http://www.xmeise.com/neiyi/siwa/')
        content = urllib2.urlopen(reqtest).read()
        typeEncode = sys.getfilesystemencoding()  ##系统默认编码
        infoencode = chardet.detect(content).get('encoding', 'utf-8')  ##通过第3方模块来自动提取网页的编码
        html = content.decode(infoencode, 'ignore').encode(typeEncode)  ##先转换成unicode编码，然后转换系统编码输出
        print html

        r = urllib2.urlopen(req)
        # 返回网页内容
        html = r.read()
        # 返回的报头信息
        receive_header = r.info()
        # sys.getfilesystemencoding()
        # 转码:避免输出出现乱码
        html = html.decode('gbk', 'ignore').encode('utf-8')
        # unicode(html, "gb18030").encode("utf8")
        self.savemyfiles(html)
        print html
        return html

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageIndex):
        url = self.siteURL % (int(pageIndex))
        page = self.getHtml(url)
        # 套图url http://www.4493.com/siwameitui/31362/1.htm
        # 封面：http://img.1985t.com/uploads/previews/2015/03/0-dnVJdg.jpg
        # 主题：''''''''
        # 时间：2015-03-17
        pattern = re.compile(
            '<li class="left-list_li"><a target="_blank" href="(.*?)">.*?</a></li>',
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
