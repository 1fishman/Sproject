from requests.cookies import RequestsCookieJar
import datetime
import json
from selenium import webdriver
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
    chrome.get(
        'https://ssl.hrbeu.edu.cn/web/1/http/0/cas.hrbeu.edu.cn/cas/login?service=http://edusys.hrbeu.edu.cn/jsxsd/index.jsp')
    try:
        # WebDriverWait(chrome, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        cookies = chrome.get_cookies()
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'cookies 存储成功')
    # 存储cookies
    except:
        print('教务处连接失败')
        return False
    return True
#外网进入内网
def getCookiesFromTxt():
    jar = RequestsCookieJar()
    with open("cookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
    return jar
#读取cookies
#主要是考虑如果外网登录时 第一个人用selenium爬 获得cookies后其他人直接取得cookie
#或者每过一段时间就获得多个cookie然后登录的人直接那这些cookies 用post 登录 比较快速 体验好些


