# coding=utf-8
__author__ = 'tzq'
import MySQLdb
import sys


class DBHelper:
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def __init__(self):
        self.dbname = 'SpiderDB'
        self.host = '192.168.31.150'
        self.user = 'root'
        self.passwd = '123456'
        self.port = 3306

        # self.dbname = 'SpiderDB'
        # self.host = '55936bea3d360.gz.cdb.myqcloud.com'
        # self.user = 'root'
        # self.passwd = 'Tan520521'
        # self.port = 3754

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
        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.dbname, port=self.port,
                               charset="utf8")
        try:
            cur = conn.cursor()
            cur.execute("insert into Qiushibaike(JokerName ,JokeContent, Lauds, IsDelete) value (%s,%s,%s,0);",
                        (str(JokerName), str(JokeContent), int(Lauds)))
            print "Number of rows insert: %d" % cur.rowcount
            cur.close()
            conn.commit()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        finally:
            conn.close()
