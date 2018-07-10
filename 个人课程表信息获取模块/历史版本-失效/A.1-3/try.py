import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import MySqlHelp
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
def CalssLogin(chrome,userName,userPassword):
    chrome.get('https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/index.jsp')
    try:
        WebDriverWait(chrome, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        chrome.find_element_by_xpath('//*[@id="username"]').send_keys(userName)
        chrome.find_element_by_xpath('//*[@id="password"]').send_keys(userPassword)
        chrome.find_element_by_xpath('//*[@id="fm1"]/li[4]/input[4]').click()
        chrome.get('https://ssl.hrbeu.edu.cn/web/1/http/1/edusys.hrbeu.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL')
        return chrome
    except Exception as e:
        print(e)
        return []
#登录教务处
def getClass(chrome):
    if(chrome==[]):
        return []
    result=[]
    for oneClass in chrome.find_element_by_xpath('//*[@id="kbtable"]').find_elements_by_class_name('kbcontent'):
        if(len(oneClass.text)==1):
            continue
        fonts =oneClass.text.split('\n---------------------\n')
        a = oneClass.get_attribute('id')
        CDay = re.match(r'(\w*-)(\d)', a).group(2)
        for font in fonts:
            font+='\n'+CDay
            result.append(font)
        # for font in oneClass.find_elements_by_tag_name('font'):
        #     print(font.text,font.get_attribute('title'))
    return result
#获得课程list

chrome=CalssLogin( NatLogin ('2016201110','liu123654789',True),'2016201110','liu536842')
myclasses=getClass(chrome)
dbhelp = MySqlHelp.MySqlHelp('myclass')
for myclass in myclasses:
    lists=myclass.split('\n')
    dbhelp.insertInto('class2016201110',lists)
    print(lists)