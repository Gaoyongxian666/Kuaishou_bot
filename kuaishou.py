import os
import pycurl
import queue
import sys
from threading import Thread
import certifi
import uiautomator2 as u2
import random
import re
from bs4 import BeautifulSoup
import requests
import time

from selenium import webdriver



def fileNum(path):
    fileNum=0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            fileNum = fileNum + 1  # 统计文件数量
    return fileNum



def task():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    chrome_options.binary_location = os.path.dirname(sys.argv[0]) + "\Google Chrome\chrome.exe"
    browser = webdriver.Chrome(executable_path=os.path.dirname(sys.argv[0]) + "\Google Chrome\chromedriver.exe",
                               options=chrome_options)
    browser.set_page_load_timeout(10)  # 设置页面加载超时
    browser.get("https://www.baidu.com/")
    time.sleep(2)
    flag = 1
    mflag = 0
    while flag:
        if not q.empty():
            line = q.get()
            name_list=re.match(pattern2, line)
            name=name_list.group(1)
            url_list = re.findall(pattern, line)
            html_url = url_list[0]
            try:
                url_list = re.findall(pattern, line)
                html_url = url_list[0]
                try:
                    browser.get(html_url)
                except:
                    print("超时了，强制停止刷新")
                finally:
                    html = browser.page_source
                    soup = BeautifulSoup(html, "lxml")
                    video_url = soup.video["src"]
                    raw_name = name
                    raw_file_name = raw_name.replace(" ", "")
                    raw_file_name = re.sub('[\/:*?"<>|]', '-', raw_file_name)
                    myfileNum=fileNum("download")
                    k="%03d" % (myfileNum+1)
                    file_name = str(k)+raw_file_name + ".mp4"
                    with open("download/" + file_name, 'wb') as f:
                        c = pycurl.Curl()
                        c.setopt(pycurl.USERAGENT,
                                 "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
                        c.setopt(c.URL, video_url)
                        c.setopt(c.CAINFO, certifi.where())
                        c.setopt(c.WRITEDATA, f)
                        c.perform()
                        c.close()
                print("\033[1;93m下载视频线程：" + file_name + "：下载完成" + "\033[0m")
            except:
                print("下载视频线程：" + line + "下载失败")
            mflag = 0

        else:
            print("\033[1;93m下载视频线程：当前下载队列为空" + "\033[0m")
            if mflag == 1:
                flag = 0
            mflag = mflag + 1
            time.sleep(5)
    browser.close()
    os.system("pause")



if __name__ == "__main__":
    print("设置ADB环境变量。。。。")
    work_dir = os.path.dirname(sys.argv[0])
    print(work_dir)
    os.chdir(work_dir)
    line = 'adb.exe  devices'
    print(line)
    os.system(line)
    q = queue.Queue()
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    pattern2 = re.compile(r'(.*?)https.*')

    header_list = [
        # 遨游
        {"user-agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
        # 火狐
        {"user-agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
        # 谷歌
        {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
    ]

    if not os.path.exists("download"):
        os.mkdir("download")

    print('''
************************************************************************************************************************
                                            快手视频下载小助手 V 0.1
                    Github地址：https://github.com/Gaoyongxian666/Kuaishou_bot
                    公众号：我的光印象  QQ群：1056916780 下载目录：解压目录/download
                    功能：批量下载他人作品，他人喜欢，自己作品，自己喜欢，本地下载限制
                    特点：因为是模拟手机操作，本软件可以一直使用，除非你进行了APP升级。
                    说明：本软件基于开源项目uiautomator2项目，所以本项目也是开源的，自己也可进行更改，项目很简单。
                    注意：快手app版本必须是最新版本 V7.3.10.13314  更新时间：2020-4-20
                    在输入下载视频个数前，一定要做好三步：  
                    1.打开调试 USB计算机连接选择传输文件 。。。  
                    2.安装两个APP。。。  
                    3.快手勾选全屏模式，打开第一个要下载的视频（可以暂停）  
                    4.最后输入要下载的视频个数  

                    使用方法：
                    1.初始化：手机打开调试模式，在首次运行本软件出现弹框点击一直允许，USB计算机连接选择传输文件
                    2.首次运行会弹出需要安装2个APP，点击安装,这两个APP都是开源项目可以保证安全性。第一次由于
                    需要初始化，所以比较慢，以后运行不需要这一步会很快的。当看到"设备连接成功"，说明设备初始化成功。

                    3.开始下载：打开本软件之后第一件事是勾选大屏模式，然后打开第一个视频（原理是从当前视频开始向上
                    滑动一个一个下载），必须输入视频数量（在自己的主页或者他人主页可以看到数量，或者自定义）
************************************************************************************************************************
    ''')

    num = input("本次下载视频的数量（不输入默认20，输入完回车,记得看使用方法）：")
    d = u2.connect()
    print(d.info)
    print("设备连接成功！")
    if num != "":
        num = int(num) + int(num) % 10
    else:
        num = 20

    p = Thread(target=task)
    p.start()

    for i in range(num):
        try:
            # 点击分享按钮
            d(resourceId="com.smile.gifmaker:id/forward_icon").click()


            # 点击复制
            d(text="复制链接").click()

            # 获取链接，好像有延时，所以
            time.sleep(0.3)
            raw_url = d.clipboard
            print("\033[1;36m获取分享链接：" + raw_url + "\033[0m")
            q.put(raw_url)

            # 向上滑动,获取下一个
            d(resourceId="com.smile.gifmaker:id/texture_view_frame").swipe("up", steps=14)
        except:
            print("获取分享链接失败")
            time.sleep(4)

