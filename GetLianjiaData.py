# -*- coding: UTF-8 -*-
__author__ = 'tzq'
import time

import tool
from dbheper import *
from WebHelper import HttpHelper

class GetLianjiaData:
    def __init__(self):
        self.siteUrl = 'http://cd.fang.lianjia.com/loupan/pg%s/'
        self.tool = tool.Tool()
        self.HttpHelper = HttpHelper()
        self.DBHelper = DBHelper()
        # 获取索引界面所有MM的信息，list格式

    def getContents(self, pageindex):
        contents = []
        url = self.siteUrl % str(pageindex)
        if pageindex == 1:
            url = 'http://cd.fang.lianjia.com/loupan/'
        contenthtml = self.HttpHelper.getHtml(url)
        if contenthtml is not None:
            import lxml.html.soupparser as soupparser
            dom = soupparser.fromstring(contenthtml)
            # doc = dom.parse(dom)/html/body/div/dl/dd
            # /html/body/div/dl/dd
            # //div[@class='main_top']/ul[@class='new public-box']/li/a
            # //*[@id="house-lst"]/li[4]/div[2]/div[1]/h2/a

            # //*[@id="house-lst"]/li[4]/div[@class='info-panel']/div[@class='col-1']/h2/a

            nodes = dom.xpath("//*[@id='house-lst']/li/div[@class='info-panel']")
            for item in nodes:
                # 套图名称： item.tesx
                # 套图URL item.xpath("@href")[0]
                # append 只能添加一个对象
                try:
                    if len(item.xpath("./div[@class='col-1']/h2/a")) > 0:
                        # 开发商
                        HouseDevelopers = item.xpath("./div[@class='col-1']/h2/a")[0].text
                        # 楼盘地址
                        houseWhere = item.xpath("./div[@class='col-1']/div[@class='where']/span")[0].text
                        # 户型
                        housnumber = item.xpath("./div[@class='col-1']/div[@class='area']")[0].text
                        # 面积
                        measureArea = item.xpath("./div[@class='col-1']/div[@class='area']/span")[0].text
                        others = item.xpath("./div[@class='col-1']/div[@class='other']/span")
                        otherTags = ''
                        housetypes = ''
                        housePeice = 0
                        if (len(others) > 0):
                            for other in others:
                                otherTags += other.text + '|';
                        types = item.xpath("./div[@class='col-1']/div[@class='type']/span")

                        if len(types) > 0:
                            for typeitem in types:
                                housetypes += typeitem.text + '|';

                        if len(item.xpath("./div[@class='col-2']/div[@class='price']")) > 0:
                            # 价格
                            housePeice = item.xpath("./div[@class='col-2']/div[@class='price']/div/span")[0].text

                        dict = {'HouseDevelopers': HouseDevelopers,
                                'houseWhere': houseWhere,
                                'housnumber': housnumber,
                                'measureArea': measureArea,
                                'otherTags': otherTags,
                                'housetypes': housetypes,
                                'housePeice': housePeice}
                        contents.append(dict)
                except:
                    print
                    "Unexpected error:", sys.exc_info()[2]
        return contents


        # 将一页淘宝MM的信息保存起来

    def saveHouseInfo(self, pageIndex):
        # 获取第一页楼盘列表
        contents = self.getContents(pageIndex)
        if contents is not None:
            print("开始循环第", pageIndex, u"页的楼盘信息")
            for item in contents:
                housedevelopers = item['HouseDevelopers']
                houseWhere = item['houseWhere']
                housnumber = item['housnumber']
                measureArea = item['measureArea']
                otherTags = item['otherTags']
                housetypes = item['housetypes']
                housePeice = item['housePeice']
                # developers,housewhere,area,other,type,price
                self.DBHelper.InserHouseDatainfo(housedevelopers, houseWhere, measureArea, otherTags, housetypes,
                                                 int(housePeice))

    def StartSpider(self, start, end):
        for i in range(start, end + 1):
            print(u"正在收集第", i, u"页的楼盘信息")
            self.saveHouseInfo(i)
            time.sleep(1)


getLianjiaData = GetLianjiaData()
getLianjiaData.StartSpider(0, 56)
