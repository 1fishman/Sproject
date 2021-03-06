import requests
from bs4 import BeautifulSoup
import re
import MySqlHelp
import logging
import getCookies
def getClassRequests(jar,username,userpassword,dbhelp):
    url = 'https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/caslogin.jsp'
    header = {
        'Host': 'ssl.hrbeu.edu.cn',
        'Referer': 'https://ssl.hrbeu.edu.cn/web/1/http/1/cas.hrbeu.edu.cn/cas/login;jsessionid=A8AF30B33E7209CE491BFD4A42219F1D.jvm1?service=http://edusys.hrbeu.edu.cn/jsxsd/framework/xsMain.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    s = requests.session()
    lines = s.get(url, headers=header, verify=False, cookies=jar).text
    lt = BeautifulSoup(lines, "lxml").find("input", attrs={"name": "lt"}).attrs['value']
    execution = BeautifulSoup(lines, "lxml").find("input", attrs={"name": "execution"}).attrs['value']
    data = {
        'username': username,
        'password': userpassword, 'captcha': '',
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'submit': '%E7%99%BB+%E5%BD%95'
    }
    s.post(url, data=data, headers=header, verify=False, cookies=jar)
    dbhelp.createTable('class' + username,'class')
    if (dbhelp.testUID(username)):  # 如果id存在且到这一步说明用户修改密码了
        dbhelp.updatePassword(username,userpassword)  # 修改密码
    else:
        dbhelp.insertStudent(username, userpassword)  # 插入一条新的id 密码
    line = s.get(verify=False, cookies=jar,
                 url='https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL')
    soup=BeautifulSoup(line.text,'lxml')
    results=[]
    for div in soup.find(id='kbtable').find_all('div',class_='kbcontent'):
        CDay = re.findall(r'>([\w[\]\,\(\)\#]+\-{0,1}[\w[\]\,\(\)\#\-]+)',str(div))
        for i in range(0,len(CDay),5):
            result=[]
            result=CDay[i:i+5]
            result.append(div['id'][-3:-2])
            results.append(result)
            dbhelp.insertInto('class' + username, result,'class')  # 插入到数据库里
    return results
#获得class
def getDetailClass1(jar,userName,userpassword,dbhelp):
    url = 'https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/caslogin.jsp'
    header = {
        'Host': 'ssl.hrbeu.edu.cn',
        'Referer': 'https://ssl.hrbeu.edu.cn/web/1/http/1/cas.hrbeu.edu.cn/cas/login;jsessionid=A8AF30B33E7209CE491BFD4A42219F1D.jvm1?service=http://edusys.hrbeu.edu.cn/jsxsd/framework/xsMain.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    s = requests.session()
    lines = s.get(url, headers=header, verify=False, cookies=jar).text
    lt = BeautifulSoup(lines, "lxml").find("input", attrs={"name": "lt"}).attrs['value']
    execution = BeautifulSoup(lines, "lxml").find("input", attrs={"name": "execution"}).attrs['value']
    data = {
        'username': userName,
        'password': userpassword, 'captcha': '',
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'submit': '%E7%99%BB+%E5%BD%95'
    }
    s.post(url, data=data, headers=header, verify=False, cookies=jar)
    url = 'https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/kscj/cjcx_list'
    header = {
        'post': 'https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/kscj/cjcx_list',
        'Host': 'ssl.hrbeu.edu.cn',
        'Referer': 'https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/kscj/cjcx_query.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    data = {
        'kksj': '', 'kcxz': '', 'kcmc': '', 'xsfs': 'all'
    }
    logging.captureWarnings(True)
    lines = s.post(url, data=data, headers=header, verify=False, cookies=jar)
    dbhelp.createTable('score' + userName, 'score')
    soup = BeautifulSoup(lines.text,'lxml')
    trs = soup.find_all("tr")
    results = []
    for i in range(2, len(trs)):
        result = []
        for td in trs[i].find_all('td'):
            a = re.findall(r'>([\w\-\.（）]+)', str(td))
            if a:
                result.append(a[0])
            else:
                result.append(' ')
        newResult = result[1:]
        dbhelp.insertInto("score"+userName,newResult,'score')
        results.append(newResult)
    return results
#获得score
def univeralGetData(userName,userPassword,dbName,type):
    dbhelp = MySqlHelp.MySqlHelp(dbName)
    if(dbhelp.testUser(userName,userPassword)):
        if (dbhelp.tableExist(type + userName)):
            return dbhelp.getTableContent(type + userName)
    jar =getCookies.getCookiesFromTxt()
    if jar==[]:
        return False
    if type=='score':
        return getDetailClass1(jar,userName,userPassword,dbhelp)
    elif type=='class':
        return getClassRequests(jar, userName, userPassword, dbhelp)
# 先向数据库查询 如果存在就返回 不存在就登录并爬取数据存储在数据库里
# getCookies.NatLogin('2016201110', 'liu123654789', True)
#测试并存储cookis用
# classes= univeralGetData('2016201110','liu536842','myclass','class')
# for c in classes:
#     print(c)
#测试class用
# scores=univeralGetData('2016201110','liu536842','myclass','score')
# for s in scores:
#     print(s)
# #测试score用
# all,results =MySqlHelp.MySqlHelp('myclass').getOptionalScore('2016201114','score')
# for a in all:
#     print(a)
# for a,v in results.items():
#     print(a,v)