import json
from requests.cookies import RequestsCookieJar
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
def NatLogin(userName,userPassworld,bool):
    if(bool==True):#为true就不弹出Chrome
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
    return chrome
#外网进入内网
def classLoginRequests(chrome,username,password):
    chrome.get(
        'https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/index.jsp')
    try:
        WebDriverWait(chrome, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        cookies = chrome.get_cookies()
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
    except:
        print('教务处连接失败')
        return []
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
        'password': password, 'captcha': '',
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'submit': '%E7%99%BB+%E5%BD%95'
    }
    s.post(url, data=data, headers=header, verify=False, cookies=jar)
    line= s.get( headers=header, verify=False, cookies=jar,url='https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL')
    return line.text
#返回了个人的课程表的网页
def getClassRequests(htmlText):
    soup=BeautifulSoup(htmlText,'lxml')
    results=[]
    for div in soup.find(id='kbtable').find_all('div',class_='kbcontent'):
        CDay = re.search(r'>\w+',str(div))
        if CDay:
            result = []
            result.append(div['id'][-3:-2])
            result.append(CDay[0][1:])
            for font in div.find_all('font'):
                result.append(font.text)
            results.append(result)
    return results
a=getClassRequests(classLoginRequests(NatLogin('2016201110','liu123654789',True),'2016201110','liu536842'))
for i in a:
    print(i)
#测试用