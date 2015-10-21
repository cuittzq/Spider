# coding=utf-8
__author__ = 'tzq'
import MySQLdb


class DBHelper:
    def __init__(self):
        self.dbname = 'WeixinUserInfo'
        self.host = '55936bea3d360.gz.cdb.myqcloud.com'
        self.user = 'root'
        self.passwd = 'Tan520521'
        self.port = 3754

    def QueryData(self, quertysql, count):
        try:
            conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd,
                                   db=self.dbname, port=self.port)
            cur = conn.cursor()
            cur.execute(quertysql)
            results = cur.fetchmany(count)
            cur.close()
            conn.close()
            return results
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def InsertData(self,values):
        try:
            conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd,
                                   db=self.dbname, port=self.port)
            cur = conn.cursor()
            values=[]
            for i in range(20):
                values.append((i,'hi rollen'+str(i)))

            cur.executemany('insert into test values(%s,%s)',values)
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
