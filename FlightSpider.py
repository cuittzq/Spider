import random
import threading

__author__ = 'tzq139'

import tool
import sys
import datetime
from WebHelper import HttpHelper

reload(sys)
sys.setdefaultencoding('utf-8')


class FlightSpider(threading.Thread):
    def __init__(self, startindex):
        self.tool = tool.Tool()
        threading.Thread.__init__(self, name="producer Thread")
        self.HttpHelper = HttpHelper()
        self.startindex = startindex
        self.airports = ['AAT',
                         'AKA',
                         'AKU',
                         'AQG',
                         'BAV',
                         'BJS',
                         'BHY',
                         'BSD',
                         'CAN',
                         'CGD',
                         'CGO',
                         'CGQ',
                         'CHG',
                         'CHW',
                         'CIF',
                         'CIN',
                         'CKG',
                         'CNI',
                         'CSX',
                         'CTU',
                         'CZX',
                         'DAT',
                         'DAX',
                         'DDG',
                         'DLX',
                         'DNH',
                         'DYG',
                         'ENH',
                         'ENY',
                         'FOC',
                         'FUG',
                         'FYN',
                         'GOQ',
                         'GHN',
                         'HAK',
                         'HEK',
                         'HET',
                         'HFE',
                         'HGH',
                         'HHA',
                         'HLD',
                         'HLH',
                         'HRB',
                         'HTN',
                         'HZG',
                         'INC',
                         'IQM',
                         'IQN',
                         'JDZ',
                         'JGN',
                         'JIU',
                         'JJN',
                         'JMU',
                         'KCA',
                         'KHG',
                         'KHN',
                         'KMG',
                         'KNC',
                         'KOW',
                         'KRL',
                         'KRY',
                         'KWE',
                         'KWL',
                         'LIA',
                         'LHW',
                         'LUZ',
                         'LXA',
                         'LXI',
                         'LYG',
                         'LYA',
                         'LYI',
                         'LZD',
                         'LZH',
                         'MOG',
                         'MXZ',
                         'NAO',
                         'NDG',
                         'NGB',
                         'NKG',
                         'NNG',
                         'NNY',
                         'PEK',
                         'PVG',
                         'SHA',
                         'SHE',
                         'SHS',
                         'SIA',
                         'SWA',
                         'SZX',
                         'SYM',
                         'SYX',
                         'TAO',
                         'TEN',
                         'TGO',
                         'TNA',
                         'TSN',
                         'TXN',
                         'TYN',
                         'URC',
                         'UYN',
                         'WUH',
                         'WXN',
                         'XEN',
                         'XFN',
                         'XIC',
                         'XIL',
                         'XIY',
                         'XIN',
                         'XMN',
                         'XNN',
                         'XUZ',
                         'YIH',
                         'YIN',
                         'YNT',
                         'YLN',
                         'YNJ',
                         'ZAT',
                         'ZGC',
                         'ZHA',
                         'ZUH',
                         'HMI',
                         'HNY',
                         'SHP']
        self.baseurl = 'http://www.ly.com/Flight/FlightQueryInterFace.aspx?' \
                       'Type=QRYFLIGHTINFOFORTQ&sort=0&errinner=&TcA=0&FilterList=&CabinCode=all&FlightNum=&CompanyCode=all&domain=&plat=&' \
                       'key=B9706D48D6D54250A616559CF3620B26&IsRevisionAfter=fznew&querytype=0&' \
                       'fquerykey=82a22ffa-3a2c-4684-b1af-c3b764371139&cztype=&IfVip=0&FqdLoginKey=1457851037912119&FqdMark=2&' \
                       'firstday={0}&isNew=1&offPort={1}&arrPort={2}&date={3}&queryParagraph=1&iid=0.06386499681445312'

    def run(self):
        index = 0
        for endindex in range(2, 60):
            startDate = datetime.date.today() + datetime.timedelta(i)
            otherStyleTime = startDate.strftime("%Y-%m-%d")
            url = self.baseurl.format(otherStyleTime, self.airports[self.startindex], self.airports[endindex],
                                      otherStyleTime)
            contenthtml = self.HttpHelper.getHtml(url)
            index = index + 1
            if (contenthtml != None):
                print (str(index))


class TravelSpider(threading.Thread):
    def __init__(self):
        self.tool = tool.Tool()
        threading.Thread.__init__(self, name="TravelSpider Thread")
        self.HttpHelper = HttpHelper()
        self.baseurl = 'http://www.myjr.net/Item/lists/id/{0}.html'

    def run(self):
        index = 0
        for endindex in range(1, 4):
            url = self.baseurl.format(endindex)
            contenthtml = self.HttpHelper.getHtml(url)
            index = index + 1
            if (contenthtml != None):
                print (str(index))


if __name__ == '__main__':
     for i in range(1, 60):
        p = TravelSpider()
        p.start()
