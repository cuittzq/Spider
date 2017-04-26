# -*- coding: UTF-8 -*-
import os
import urllib
import sys

__author__ = 'tzq139'


class filehelper:

    # 创建新目录
    def __init__(self):
        pass

    def mkdir(self, path):
        path = path.strip()
        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # print u"偷偷新建了名字叫做", path, u'的文件夹'
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            # print u"名为", path, '的文件夹已经创建'
            print
            return False

    # 传入图片地址，文件名，保存单张图片
    def saveImg(self, imageURL, fileName):
        f = []
        try:
            u = urllib.urlopen(imageURL)
            data = u.read()
            f = open(fileName, 'wb')
            f.write(data)
            print fileName
            f.close()
        except:
            print "Unexpected error:", sys.exc_info()[2]
        finally:
            f.close()

