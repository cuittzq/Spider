# coding=utf-8
__author__ = 'Administrator'
import urllib
import urllib2
import httplib
import json
import re
import tool


# 糗事百科 http://www.boqingguan.com/
class Meinvboqing:
    def __init__(self):
        self.siteURL = 'http://www.qiushibaike.com/'
        self.tool = tool.Tool()

    def getAjaxLogin(self):
        # loginurl = self.siteURL + 'Ajax/Login'
        data = {'name': 'tzq123',
                'pass': '123456'}
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
        #
        postdata = urllib.urlencode(data).encode(encoding='UTF8')

        # req = urllib2.Request(url=loginurl,
        #                       data=data)
        # myResponse = urllib2.urlopen(req).read().decode('utf-8')



        headersdata = {"Host": "www.boqingguan.com",
                       "Content-type": "text/html; charset=gb2312",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                       "Accept-Encoding": "gzip,deflate,sdch",
                       "Accept-Language": "zh-CN,zh;q=0.8",
                       "Cache-Control": "max-age=0",
                       "Connection": "keep-alive",
                       "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0",
                       "Cookie": "uua=25329813-7dc2-4819-b7de-82f7885d8d4a; Hm_lvt_e0d6338cf40a95fc0aed6b37f32cf584=1445304521,1445321194; Hm_lpvt_e0d6338cf40a95fc0aed6b37f32cf584=1445321194"}


        params = urllib.urlencode({'param': json.dumps({'name': 'tzq123',
                                                        'pass': '123456'})})
        print params
        req = urllib2.Request('http://www.boqingguan.com/Ajax/Login', postdata)
        req.headers = headersdata
        resp = urllib2.urlopen(req).read()
        print(resp)


meinvboqing = Meinvboqing()
meinvboqing.getAjaxLogin()
