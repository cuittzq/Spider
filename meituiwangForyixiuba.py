# -*- coding: UTF-8 -*-
from MeituisiwatupianSpider import MeituisiwatupianSpider

__author__ = 'tzq'
import time
import sys
import queue
import threading


class producer(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self, name="producer Thread")
        self.index = index
        self.meituiwang = MeituisiwatupianSpider()

    def run(self):
        global q
        # for i in range(1, self.index):
        for i in range(1, self.index):
            try:
                if q.qsize() > 100:
                    print
                    "队列已经满了:" + str(q.qsize()) + "休息10s"
                    time.sleep(10)
                    pass
                self.meituiwang.getPageImages(i)
            except:
                print("开始爬取图片失败:" + str(sys.exc_info()))
            print('producer' + ' ----- Queue Size:' + str(q.qsize()))

    # 解析图片
    def getImage(self, pagehtml):
        import lxml.html.soupparser as soupparser
        dom = soupparser.fromstring(pagehtml)
        # nodes = dom.xpath("//div[@class='content']/div[@class='content-pic']/a/img")
        nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/p/img")
        if len(nodes) == 0:
            nodes = dom.xpath("//div[@class='mainer']/div[@class='picmainer']/div[@class='picsbox picsboxcenter']/img")
        imagesrc = nodes[0].xpath("@src")
        if len(imagesrc) == 0:
            return None
        return imagesrc[0]

q = queue.Queue()
q._init(500)

if __name__ == '__main__':
    p = producer(59)
    p.start()
