import pymysql
class MySqlHelp:
    dbname=''
    user='root'
    passwod='123456'
    host='127.0.0.1'
    port=3306
    def __init__(self,dbName,user='root',password='123456',host='127.0.0.1',port=3306):
        self.dbname=dbName
        self.user=user
        self.password=password
        self.host=host
        self.port=port
        try:
           self.db=pymysql.connect(host=self.host,charset='utf8',user=self.user,password=self.password,db=self.dbname,port=self.port)
        except Exception as e:
            print(e)
        else:
            print(self.dbname + ' 连接成功\n')
    def getdb(self):
        if(self.db==0):
            try:
                self.connect_mysql()
            except Exception as e:
                print(e)
                return 0
        else:
            return self.db
    def showTables(self):
        cursor = self.db.cursor()
        cursor.execute('show tables')
        results=cursor.fetchall()
        for result in results:
            print(result[0])
    def showTable(self,theTable):
        cursor=self.db.cursor()
        cursor.execute("select * from "+theTable)
        results = cursor.fetchall()
        for result in results:
            print(result)
    def showColumn(self,table):
        cursor=self.db.cursor()
        cursor.execute('desc '+table)
        results = cursor.fetchall()
        for result in results:
            print(result[0])
    def insertInto(self,theTable,myValues):
        cursor = self.db.cursor()
        try:
            results = "(1,"
            for value in myValues:
                results = results + "'" + value + "',"
            results = results[:-1]
            results += ")"
            results.encode("utf-8").decode("latin1")
            cursor.execute("insert into "+theTable+" values " + results)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()