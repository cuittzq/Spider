# coding=utf-8
__author__ = 'tzq'
import MySQLdb


class DBHelper:
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
            # KeyID JokerName JokeContent Lauds IsDelete sql_content = "insert into table(key1,key2,key3) values (%s,%s,%s)"%(value1,value2,value3)
            contensql = "insert into Qiushibaike(JokerName ,JokeContent, Lauds, IsDelete,) values (%s,%s,%d,0)" % (str(JokerName), str(JokeContent), int(Lauds))
            cur.execute(contensql)
            # sql_content = "insert into Qiushibaike(JokerName ,JokeContent, Lauds, IsDelete,) values (?,?,?,0)"
            # cur.execute(sql_content, (JokerName, JokeContent, Lauds))
            cur.close()
            conn.close()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
