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
    #展示某数据库所有的表
    def showColumn(self,table):
        cursor=self.db.cursor()
        cursor.execute('desc '+table)
        results = cursor.fetchall()
        for result in results:
            print(result[0])
    #展示所有的列
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
    #向某表插入values
    def tableExist(self,tableName):
        cursor = self.db.cursor()
        tableName="'"+tableName+"'"
        cursor.execute("SELECT table_name FROM information_schema.TABLES WHERE table_name ="+tableName+"and TABLE_SCHEMA = '"+self.dbname+"'")
        return cursor.fetchall()!=()
    #测试某表是否存在
    def getTableContent(self,tableName):
        try:
            cursor = self.db.cursor()
            cursor.execute("select * from "+tableName)
            return cursor.fetchall()
        except Exception as e:
            print(e)
    #输出某表的全部内容
    def createTable(self,tableName):
        cursor = self.db.cursor()
        sql = "CREATE TABLE if not exists "+tableName+"(Cid int(4) NULL DEFAULT NULL,\
Cname varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
Cteach varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
Clast varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
Ctime varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
Cadr varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
Cday varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
PRIMARY KEY (Cname,Ctime,Cday) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic"
        cursor.execute(sql)
        self.db.commit()
        print(tableName+'建表成功')
    #新建一张表名为class+学号的课程表
    def testUser(self,id,password):
        cursor=self.db.cursor()
        cursor.execute("select * from student where id = '"+str(id)+"' and password = '"+password+"'")
        return cursor.fetchall()!=()
    #测试用户是否存在
    def testUID(self,id):
        cursor=self.db.cursor()
        cursor.execute("select * from student where id = '"+str(id)+"'")
        return cursor.fetchall()!=()
    #测试这个id是否存在
    def updatePassword(self,id,password):
        cursor=self.db.cursor()
        cursor.execute("update student set password='"+password+"' where id ='"+id+"'")
        self.db.commit()
        print(id,"密码修改成功 ",password)
    #更新id的密码
    def insertStudent(self,id,password):
        cursor = self.db.cursor()
        cursor.execute("insert into student values ("+str(id)+",'"+password+"')")
        self.db.commit()
        print(id,password,"插入成功")
    #插入一个新的id 密码
    def __del__(self):
        self.db.close()
    #关闭连接
