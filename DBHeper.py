# coding=utf-8
__author__ = 'tzq'
import MySQLdb
import sys


class DBHelper:
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def __init__(self):
        self.dbname = 'SpiderDB'
        self.host = '55936bea3d360.gz.cdb.myqcloud.com'
        self.user = 'root'
        self.passwd = 'Tan520521'
        self.port = 3754

    def QueryData(self, quertysql, count):
        try:
            conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd,
                                   db=self.dbname, port=self.port, charset="utf8")
            cur = conn.cursor()
            cur.execute(quertysql)
            results = cur.fetchmany(count)
            cur.close()
            conn.close()
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def InsertData(self, JokerName, JokeContent, Lauds):
        try:
            conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd,
                                   db=self.dbname, port=self.port, charset="utf8")
            cur = conn.cursor()
            cur.execute("insert into Qiushibaike(JokerName ,JokeContent, Lauds, IsDelete) value (%s,%s,0,0)",
                        (str(JokerName), str(JokeContent)))
            print "Number of rows updated: %d" % cur.rowcount
            cur.close()
            conn.close()

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
