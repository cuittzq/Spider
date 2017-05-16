# coding=utf-8
__author__ = 'tzq'
import tool
import sys
import urllib.request
import chardet


class HttpHelper:
    def __init__(self):
        self.siteURL = 'http://www.4493.com/siwameitui/index-2.htm'
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
            typeEncode = sys.getfilesystemencoding()  ##系统默认编码

            infoencode = chardet.detect(myResponse).get('encoding', 'gb2312')  ##通过第3方模块来自动提取网页的编码

            html = myResponse.decode(infoencode, 'ignore').encode('utf-8')  ##先转换成unicode编码，然后转换系统编码输出
            return html
        except:
            print("Unexpected error:", sys.exc_info()[1])
            return None
