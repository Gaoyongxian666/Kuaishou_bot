import json
import os
import pycurl
import re
import sys
import time
from threading import Thread
from urllib.parse import urlparse

import certifi
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def read_cookies(driver):
    with open("cookies.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            driver.add_cookie(cookie)

def write_cookie(driver):
    cookies = driver.get_cookies()
    with open("cookies.txt", "w") as fp:
        json.dump(cookies, fp)

def fileNum(path):
    fileNum=0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            fileNum = fileNum + 1  # 统计文件数量
    return fileNum


def downloadFile(name, video_url):
    with open("download/" + name, 'wb') as f:
        c = pycurl.Curl()
        c.setopt(pycurl.USERAGENT,
                 "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")  # 配置请求HTTP头的User-Agent
        c.setopt(c.URL, video_url)
        c.setopt(c.CAINFO, certifi.where())
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

def isSafePresent(browser,css):
    flag = True
    try:
        browser.find_element_by_css_selector(css)
        return flag

    except:
        flag = False
        return flag




def kuaishou():
    line = input("输入作者分享链接：")
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url_list = re.findall(pattern, line)
    html_url = url_list[0]
    # print(html_url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Mobile Safari/537.36'
    }
    r = requests.get(html_url, headers=header)
    reditList = r.history
    last_url = reditList[len(reditList) - 1].headers["location"]
    print("获取链接："+last_url)
    path = urlparse(last_url).path
    ID = path.split("/")[3]
    print("获取ID："+ID)
    print("是否安全认证弹框，完成或者直接关掉那个认证弹框")


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--mute-audio")  # 静音

    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    chrome_options.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
    browser = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                               options=chrome_options)
    wait = WebDriverWait(browser, 10)

    browser.get("https://www.baidu.com/")
    url = "https://live.kuaishou.com/profile/" + ID

    read_cookies(browser)

    browser.get(url)
    # time.sleep(3)
    # print(11111111111111111111)
    # body > iframe
    if isSafePresent(browser,"body > iframe"):
        print("存在认证")
        input("存在认证,请退出程序，不使用无头浏览器，完成安全认证。。。")

        # browser.switch_to.default_content()
        # print(browser.page_source)
        # time.sleep(3)
        # browser.find_element_by_css_selector(".icon_close").click()
        # js = '''var a=document.getElementsByTagName("iframe");'''
        # # box.parentNode.removeChild(box);
        # browser.execute_script(js) body > div.slide_puzzle > div > div.container_head > span
        # js2="a.parentNode.removeChild(a);"
        # browser.execute_script(js2)body > iframe

        # iframe = browser.find_elements_by_tag_name("iframe")[0]
    else:
        print("没有安全认证")


    time.sleep(1)
    element1 = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#app > div.profile > div.load-more.profile-content > div.tab > span.active')))
    raw_num = browser.find_element_by_css_selector(
        "#app > div.profile > div.load-more.profile-content > div.tab > span.active").text.strip()
    re_num = re.match(".*?(\d+).*?", raw_num, re.S)
    num = int(re_num.group(1))
    print("作者的作品数：" + str(num))
    alreay_li = []
    for i in range(round(num / 10)):
        li_list = browser.find_elements_by_css_selector(
            "#app > div.profile > div.load-more.profile-content > div:nth-child(3) > ul > li")
        for li in li_list:
            li_text = li.text
            print(li_text)
            if li_text not in alreay_li:
                alreay_li.append(li_text)
                raw_name = li_text.strip().replace("\n", "-")
                raw_file_name = raw_name.replace(" ", "")
                raw_file_name = re.sub('[\/:*?"<>|]', '-', raw_file_name)
                if len(raw_file_name) > 50:
                    raw_file_name = raw_file_name[:49]
                else:
                    raw_file_name = raw_file_name
                myfileNum = fileNum("download")
                k = "%03d" % (myfileNum + 1)
                file_name = str(k) + raw_file_name + ".mp4"
                browser.execute_script("arguments[0].scrollIntoView();", li)
                time.sleep(1)
                browser.execute_script('arguments[0].scrollIntoView(false);', li)

                li.click()
                element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
                element1 = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#app > div.profile > div.photo-preview > div.close')))

                video = browser.find_element_by_tag_name("video")
                video_url = video.get_attribute("src")
                browser.find_element_by_css_selector("#app > div.profile > div.photo-preview > div.close").click()
                print("\033[1;93m下载视频线程：" + file_name + ".mp4：开始下载" + "\033[0m")
                downloadFile(file_name, video_url)
                print("\033[1;93m下载视频线程：" + file_name + ".mp4：下载完成" + "\033[0m")
                time.sleep(1)


def safe_kuaishou():
    line = input("输入作者分享链接：")
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url_list = re.findall(pattern, line)
    html_url = url_list[0]
    # print(html_url)
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Mobile Safari/537.36'
    }
    r = requests.get(html_url, headers=header)
    reditList = r.history
    last_url = reditList[len(reditList) - 1].headers["location"]
    print("获取链接："+last_url)
    path = urlparse(last_url).path
    ID = path.split("/")[3]
    print("获取ID："+ID)
    print("是否安全认证弹框，完成或者直接关掉那个认证弹框")


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--mute-audio")  # 静音
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    chrome_options.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
    browser = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                               options=chrome_options)
    wait = WebDriverWait(browser, 10)

    browser.get("https://www.baidu.com/")
    url = "https://live.kuaishou.com/profile/" + ID

    read_cookies(browser)

    browser.get(url)
    # time.sleep(3)
    # print(11111111111111111111)
    # body > iframe
    if isSafePresent(browser,"body > iframe"):

        print("存在认证")
        input("是否安全认证弹框，完成或者直接关掉那个认证弹框（y/n）：")
        # browser.switch_to.default_content()
        # print(browser.page_source)
        # time.sleep(3)
        # browser.find_element_by_css_selector(".icon_close").click()
        # js = '''var a=document.getElementsByTagName("iframe");'''
        # # box.parentNode.removeChild(box);
        # browser.execute_script(js) body > div.slide_puzzle > div > div.container_head > span
        # js2="a.parentNode.removeChild(a);"
        # browser.execute_script(js2)body > iframe

        # iframe = browser.find_elements_by_tag_name("iframe")[0]

    else:
        print("没有安全认证")


    time.sleep(1)
    element1 = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '#app > div.profile > div.load-more.profile-content > div.tab > span.active')))
    raw_num = browser.find_element_by_css_selector(
        "#app > div.profile > div.load-more.profile-content > div.tab > span.active").text.strip()
    re_num = re.match(".*?(\d+).*?", raw_num, re.S)
    num = int(re_num.group(1))
    print("作者的作品数：" + str(num))
    alreay_li = []
    for i in range(round(num / 10)):
        li_list = browser.find_elements_by_css_selector(
            "#app > div.profile > div.load-more.profile-content > div:nth-child(3) > ul > li")
        for li in li_list:
            li_text = li.text
            print(li_text)
            if li_text not in alreay_li:
                alreay_li.append(li_text)
                raw_name = li_text.strip().replace("\n", "-")
                raw_file_name = raw_name.replace(" ", "")
                raw_file_name = re.sub('[\/:*?"<>|]', '-', raw_file_name)
                if len(raw_file_name) > 50:
                    raw_file_name = raw_file_name[:49]
                else:
                    raw_file_name = raw_file_name
                myfileNum = fileNum("download")
                k = "%03d" % (myfileNum + 1)
                file_name = str(k) + raw_file_name + ".mp4"
                browser.execute_script("arguments[0].scrollIntoView();", li)
                time.sleep(1)
                browser.execute_script('arguments[0].scrollIntoView(false);', li)

                li.click()
                element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
                element1 = wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#app > div.profile > div.photo-preview > div.close')))

                video = browser.find_element_by_tag_name("video")
                video_url = video.get_attribute("src")
                browser.find_element_by_css_selector("#app > div.profile > div.photo-preview > div.close").click()
                print("\033[1;93m下载视频线程：" + file_name + ".mp4：开始下载" + "\033[0m")
                downloadFile(file_name, video_url)
                print("\033[1;93m下载视频线程：" + file_name + ".mp4：下载完成" + "\033[0m")
                time.sleep(1)


if __name__ == "__main__":
    if not os.path.exists("download"):
        os.mkdir("download")

    print('''
************************************************************************************************************************
                                                快手视频下载小助手 V 0.11
                        Github地址：https://github.com/Gaoyongxian666/Kuaishou_bot
                        QQ群：1056916780 下载目录：解压目录/download  更新：2020-5-1
                        功能：批量下载作品     
                        说明：允许软件网络访问        
************************************************************************************************************************''')

    print("说明：登陆是必须操作，为了获取cookie，有了cookie以后不用频繁登陆")
    cookie=input("是否完成过登陆（y/n）：")
    if cookie!="y":
        print("打开浏览器中，允许软件网络访问")
        chrome_options1 = webdriver.ChromeOptions()
        chrome_options1.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
        browser = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                                   options=chrome_options1)
        browser.get("https://live.kuaishou.com/")
        print("请在浏览器中完成登陆")
        print("************************************************************************************************************************")

        input("等待完成页面登陆（y/n）：")
        print("开始写入cookie")
        write_cookie(browser)
        print("写入cookie完成")
        browser.quit()
        print("************************************************************************************************************************")
        print("第一次使用有屏幕浏览器，完成安全认证")
        safe_kuaishou()

    else:
        flag=input("是否选择无头浏览器（默认无头浏览器）y/n：")
        if flag!="n":
            kuaishou()
        else:
            safe_kuaishou()










