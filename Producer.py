# -*- coding: UTF-8 -*-
from spiders.Tu11Spider import Tu11Spider
from spiders.umeiccSpider import umeiccSpider

__author__ = 'tzq'
import sys
import threading


class producer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self, name="producer Thread")
        self.index = index
        self.meituiwang = Tu11Spider()
        self.umeiccSpider = umeiccSpider()

    def run(self):
        # for i in range(1, self.index):
        for i in range(1, self.index):
            try:
                self.meituiwang.getPageImages(i)
                self.umeiccSpider.getPageImages(i)
            except:
                print("开始爬取图片失败:" + str(sys.exc_info()))

    # 解析图片
    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/p/img")
        if len(nodes) == 0:
            nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/img")
        imagesrc = nodes[0].xpath("@src")
        if len(imagesrc) == 0:
            return None
        return imagesrc[0]


if __name__ == '__main__':
    p = producer(59)
    p.start()
