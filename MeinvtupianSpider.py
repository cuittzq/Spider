from BaseSpider import BaseSpider

__author__ = 'tzq139'


class MeinvtupianSpider(BaseSpider):
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
                # doc = dom.parse(dom)/html/body/div/dl/dd
                # /html/body/div/dl/dd
                # //div[@class='main_top']/ul[@class='new public-box']/li/a
                nodes = dom.xpath("//div[@class='page1']/ul/li/a")
                for item in nodes:
                    # 套图名称： item.tesx
                    # 套图URL item.xpath("@href")[0]
                    # append 只能添加一个对象
                    if len(item.xpath("@href")) > 0:
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
        if len(nodes) > 0:
            for i in range(0, len(nodes)):
                images.append(nodes[i].xpath("@src")[0])
        if 0 == len(images):
            return None
        return images
