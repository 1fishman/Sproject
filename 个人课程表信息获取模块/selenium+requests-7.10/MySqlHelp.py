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
    def insertInto(self,theTable,myValues,type):
        cursor = self.db.cursor()
        try:
            if type=='class':
                results = "(1,"
            if type=='score':
                results="("
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
    def createTable(self,tableName,type):
        cursor = self.db.cursor()
        if type=='class':
            sql = "CREATE TABLE if not exists "+tableName+"(Cid int(4) NULL DEFAULT NULL,\
Cname varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
Cteach varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
Clast varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
Ctime varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
Cadr varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
Cday varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
PRIMARY KEY (Cname,Ctime,Cday) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic"
        elif type=='score':
            sql = "CREATE TABLE if not exists " + tableName + "(开课学期 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
课程编号 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
课程名称 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
成绩 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
学分 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
总学时 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
考核方式 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
考试性质 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,\
课程属性 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
课程性质 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
通识教育选修课程类别 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
成绩标记 varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,\
PRIMARY KEY (课程名称, 课程编号, 开课学期,考试性质) USING BTREE\
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
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
    def getOptionalScore(self,id,type):
        cursor = self.db.cursor()
        cursor.execute('select sum(学分),课程性质 from '
                       +type+id+' where 课程属性 = "公选" and 成绩 not in ("不及格","---") or 课程属性 = "任选" and 成绩 not in ("不及格","---")GROUP BY 课程性质 ')
        a=cursor.fetchall()
        results = {}
        he = 0
        for i in a:
            if i[1] == '专业拓展':
                results['专业拓展'] = i[0]
            elif i[1] == '创新创业':
                results['创新创业'] = i[0]
            elif i[1] == '专业选修课程':
                results['专业选修课程'] = i[0]
            elif i[1] == '艺术修养与审美':
                results['D模块'] = i[0]
                he += i[0]
            else:
                he += i[0]
        results['通识教育选修课'] = he
        return a,results
    #计算选修学分并返回自己的各个模块的学分
    def getScore(self,id,type):
        cursor = self.db.cursor()
        cursor1= self.db.cursor()
        cursor.execute('select 学分,成绩,开课学期 from '+type+id+' WHERE 考试性质="正常考试" and 成绩标记 <> "缺考" ORDER BY 开课学期')
        cursor1.execute('SELECT SUM(学分),开课学期 FROM '+type+id+' WHERE 考试性质="正常考试" and 成绩标记 <> "缺考" GROUP BY 开课学期')
        result=cursor.fetchall()
        print(result)
        newdict = {}
        for a in cursor1.fetchall():
            newdict[a[1]] = a[0]
        print(newdict)
        def transfe(i):
            if i == '优秀':
                return 95
            elif i == '良好':
                return 85
            elif i == '中等':
                return 75
            elif i == '及格':
                return 65
            elif i == '不及格':
                return 30
            else:
                return float(i)
        sum = 0
        times = []
        resultsMap = {}
        times.append(result[0][2])
        for r in result:
            if r[2] not in times:
                times.append(r[2])
                resultsMap[a] = sum / newdict[a]
                sum = 0
                sum += float(r[0]) * transfe(r[1])
            else:
                a = r[2]
                sum += float(r[0]) * transfe(r[1])
        else:
            resultsMap[a] = sum / newdict[a]
        return resultsMap
    def __del__(self):
        self.db.close()
    #关闭连接
