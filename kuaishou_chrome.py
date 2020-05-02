import json
import os
import pycurl
import queue
import re
import sys
import time
import traceback
from threading import Thread
from urllib.parse import urlparse
import certifi
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
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

def auth(url):
    chrome_options2 = webdriver.ChromeOptions()
    chrome_options2.add_argument("--mute-audio")  # 静音
    chrome_options2.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options2.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
    browser2 = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                                options=chrome_options2)
    browser2.get("https://www.baidu.com/")
    read_cookies(browser2)
    browser2.get(url)
    input("是否完成认证（y/n）")
    write_cookie(browser2)
    browser2.quit()

def task():
    time.sleep(2)
    flag=1
    mflag=0
    while flag:
        if not q.empty():
            mydict = q.get()
            try:
                file_name=mydict.get("file_name")
                if file_name=="重复下载":
                    time.sleep(1)
                    print("\033[1;93m下载视频线程：" + file_name + "" + "\033[0m")
                else:
                    video_url=mydict.get("video_url")
                    print("\033[1;93m下载视频线程：" + file_name + "：开始下载" + "\033[0m")
                    downloadFile(file_name, video_url)
                    print("\033[1;93m下载视频线程：" + file_name + "：下载完成" + "\033[0m")
            except:
                print(traceback.format_exc())
                print("下载视频线程：" + mydict + "下载失败")
            mflag=0

        else:
            print("\033[1;93m下载视频线程：当前下载队列为空" + "\033[0m")
            if mflag==6:
                flag=0
            mflag=mflag+1
            time.sleep(10)
    os.system("pause")


def open_brower(browser,ID):
    browser.get("https://www.baidu.com/")
    url = "https://live.kuaishou.com/profile/" + ID
    read_cookies(browser)
    browser.get(url)
    print("检测是否有安全认证弹框？")
    time.sleep(3)
    # body > iframe
    if isSafePresent(browser, "body > iframe"):
        print("存在认证")
        print("打开浏览器中，请在打开的浏览器中完成安全验证，完成验证不要关闭浏览器")
        auth(url)
        open_brower(browser,ID)
    else:
        print("没有安全认证")

def get_video(browser,wait,alreay_li,num):
    for i in range(round(num / 10)):
        li_list = browser.find_elements_by_css_selector(
            "#app > div.profile > div.load-more.profile-content > div:nth-child(3) > ul > li")
        for li in li_list:
            li_text = li.text
            # print(li_text)
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
                time.sleep(1)
                try:
                    element = WebDriverWait(browser, 2).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.pl-modal.alert > div"))
                    )
                    print("出现注意弹框")
                    get_video(browser,wait,num,alreay_li)
                except TimeoutException:
                    print("没有出现弹框")
                finally:
                    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
                    element1 = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, '#app > div.profile > div.photo-preview > div.close')))

                    video = browser.find_element_by_tag_name("video")
                    video_url = video.get_attribute("src")
                    browser.find_element_by_css_selector("#app > div.profile > div.photo-preview > div.close").click()
                    print("\033[1;94m获取链接："+ str({"file_name":file_name,"video_url":video_url})+ "\033[0m")
                    q.put({"file_name":file_name,"video_url":video_url})
            else:
                q.put({"file_name":"重复下载","video_url":""})


def kuaishou():
    kuaishou_flag=input("作者是否有快手号（y/n）：")
    if kuaishou_flag=="y":
        ID = input("输入作者快手号：")
    else:
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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--mute-audio")  # 静音
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
    browser = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                               options=chrome_options)
    wait = WebDriverWait(browser, 10)
    open_brower(browser,ID)

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
    p = Thread(target=task)
    p.start()
    get_video(browser,wait,alreay_li,num)


# body > div.pl-modal.alert > div

if __name__ == "__main__":
    q = queue.Queue()

    if not os.path.exists("download"):
        os.mkdir("download")

    print('''
************************************************************************************************************************
                            快手视频下载小助手 V 0.13
    Github地址：https://github.com/Gaoyongxian666/Kuaishou_bot
    QQ群：1056916780 下载目录：解压目录/download  更新：2020-5-2
    功能：批量下载作品     
    说明：有快手号的，输入快手号。不显示快手号的，或者显示用户ID的：使用作者分享链接的方式。
    允许软件网络访问,登陆是必须操作，为了获取cookie，有了cookie以后不用频繁登陆。
    进行登陆，安全认证使用的压缩包里面的浏览器与外部浏览器无关，程序调起浏览器，主程序会处于阻塞状态。
    登陆完成，安全认证完成不要关闭浏览器，一定要回到主程序里面进行输入，从阻塞状态变成执行状态。
    程序打开的浏览器页面不要自己关闭，主程序里面有提示,按照操作完成。
************************************************************************************************************************''')



    cookie=input("是否完成过登陆（y/n）：")
    if cookie!="y":
        print("\033[1;92m网页登陆：打开浏览器中，允许软件网络访问"+ "\033[0m")
        print("\033[1;92m网页登陆：请在浏览器中完成登陆，登陆后不要关闭浏览器，记得回到主程序输入"+ "\033[0m")

        chrome_options1 = webdriver.ChromeOptions()
        chrome_options1.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
        browser = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                                   options=chrome_options1)
        browser.get("https://live.kuaishou.com/")
        print("************************************************************************************************************************")

        input("\033[1;92m网页登陆：等待完成页面登陆（y/n）："+ "\033[0m")
        print("\033[1;92m网页登陆：开始写入cookie"+ "\033[0m")
        write_cookie(browser)
        print("\033[1;92m网页登陆：写入cookie完成"+ "\033[0m")
        browser.quit()
        print("************************************************************************************************************************")
        kuaishou()

    else:
        kuaishou()










