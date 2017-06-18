from spiders.BaseSpider import BaseSpider

__author__ = 'tzq139'


class umeiccSpider(BaseSpider):
    def __init__(self):
        self.siteURL = {'meinvtupian': 'http://www.umei.cc/meinvtupian/siwameinv/%s.htm'}
        BaseSpider.__init__(self)

    # 获取索引界面所有MM的信息，list格式
    def getContents(self, pageindex):
        contents = []
        for baseUrl in self.siteURL:
            url = self.siteURL[baseUrl] % str(pageindex)
            if 1 == pageindex:
                url = 'http://www.tu11.com/%s/' % str(baseUrl)
            contenthtml = self.HttpHelper.getHtml(url)
            if contenthtml is not None:
                import lxml.html.soupparser as soupparser
                dom = soupparser.fromstring(contenthtml)
                nodes = dom.xpath("//div[@class='page1']/ul/li/a")
                for item in nodes:
                    if len(item.xpath("@href")) > 0:
                        dict = {'Name': item.xpath("@title")[0], 'Url': item.xpath("@href")[0]}
                        contents.append(dict)
        return contents

    # 分析套图数量
    def getAllnum(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
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
        nodes = dom.xpath("//div[@class='center']/div[@class='page-list']/p/img")
        images = []
        if len(nodes) > 0:
            for i in range(0, len(nodes)):
                images.append(nodes[i].xpath("@src")[0])
        if 0 == len(images):
            return None
        return images
