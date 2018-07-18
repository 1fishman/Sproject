from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import json
from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar
from dbhelp.models import Student,Score,Class
from django.db.models import Sum
import logging
import requests

def NatLogin(userName, userPassworld, bool):
    if (bool == True):  # 为true就不弹出Chrome
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome = webdriver.Chrome(chrome_options=chrome_options)
    else:
        chrome = webdriver.Chrome()
    chrome.get('https://ssl.hrbeu.edu.cn/por/login_psw.csp')
    chrome.find_element_by_xpath('//*[@id="svpn_name"]').send_keys(userName)
    chrome.find_element_by_xpath('//*[@id="svpn_password"]').send_keys(userPassworld)
    chrome.find_element_by_xpath('//*[@id="logButton"]').click()
    chrome.get(
        'https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/index.jsp')
    cookies = chrome.get_cookies()
    jar=RequestsCookieJar()
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])
    return jar
def getClassRequests(jar, username, userpassword):
    logging.captureWarnings(True)
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
    a = s.post(url, data=data, headers=header, verify=False, cookies=jar)
    if a.url == "https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/caslogin.jsp":
        return False
    line = s.get(verify=False, cookies=jar,
                 url='https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL')
    soup = BeautifulSoup(line.text, 'lxml')
    results = []
    for div in soup.find(id='kbtable').find_all('div', class_='kbcontent'):
        CDay = re.findall(r'>([\w[\]\,\(\)\#]+\-{0,1}[\w[\]\,\(\)\#\-]+)', str(div))
        for i in range(0, len(CDay), 5):
            result = []
            result = CDay[i:i + 5]
            result.append(div['id'][-3:-2])
            results.append(result)
    print('get Classes')
    return results
def aps_test():
    def NatLogin(userName, userPassworld, bool):
        if (bool == True):  # 为true就不弹出Chrome
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome = webdriver.Chrome(chrome_options=chrome_options)
        else:
            chrome = webdriver.Chrome()
        chrome.get('https://ssl.hrbeu.edu.cn/por/login_psw.csp')
        chrome.find_element_by_xpath('//*[@id="svpn_name"]').send_keys(userName)
        chrome.find_element_by_xpath('//*[@id="svpn_password"]').send_keys(userPassworld)
        chrome.find_element_by_xpath('//*[@id="logButton"]').click()
        chrome.get(
            'https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/index.jsp')
        cookies = chrome.get_cookies()
        with open("./templates/cookies/cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'cookies 存储成功')
    print('start')
    NatLogin('2016201110','liu123654789',True)
    print('finish')
def getCookiesFromTxt1():
    jar = RequestsCookieJar()
    with open("./templates/cookies/cookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
    return jar
def login(request):
    if request.method == 'POST':
        print('begin')
        #jar=getCookiesFromTxt1()
        newName=request.POST.get('username',None)
        newPassword=request.POST.get('password',None)
        try:
            student=Student.objects.get(id=newName)
        except Student.DoesNotExist:
            student=Student.objects.create(id=newName,password=newPassword)
        if student.password==newPassword:
            show(request,newName)
            return HttpResponseRedirect('../'+newName+'/show')
        #    student.password=newPassword
        # if getClassRequests(jar,newName,newPassword):
        #     student.save()
        #     return HttpResponseRedirect('/show')

        # else:
        #     print('wrong')
        #     return HttpResponse(json.dumps({'code': 'wro'}), content_type="application/json")
    else:
        # scheduler = BackgroundScheduler()
        # scheduler.add_job(func=aps_test, trigger='date')
        # scheduler.start()
        return render(request,'studentLogin.html')

@login_required
def show(request,user_id):
    context={}
    context['userid']=user_id
    score_list=Score.objects.filter(sid=user_id).exclude(smark='缺考').exclude(checknature='补考').order_by('semester')

    a=score_list.exclude(smark='缺考').exclude(checknature='补考').values('semester').annotate(Sum('credit')).order_by('semester')
    time={}
    for i in a:
        time[i['semester']]=i['credit__sum']
    resultsMap = {}
    count={}
    for score in score_list:
        if score.semester in resultsMap.keys():
            count[score.semester]+=1
            resultsMap[score.semester]+=score.countItem()
        else:
            resultsMap[score.semester]=0
            count[score.semester] = 0
            count[score.semester] += 1
            resultsMap[score.semester] += score.countItem()
    result = []
    for i,v in resultsMap.items():
        a = {}
        a['semester'] = i[0:9]
        a['semester2']=i[10:]
        a['credit'] = v/time[i]
        a['count']=count[i]
        result.append(a)
    print(result)
    context['resultList']=result
    context['score_list'] = score_list
    return render(request,'show.html',context)

def cuteLogin(request):
    return render(request,'cuteLogin.html')
def test(request):
    return render(request,'test.html')