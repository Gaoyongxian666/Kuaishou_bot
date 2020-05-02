# import os
# import pycurl
# import random
# import re
#
# import certifi
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
#
#
# # url="https://v.kuaishou.com/2mGpmP"
# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('--headless')
# # chrome_options.add_argument('--disable-gpu')
# # chrome_options.binary_location = r"D:\python_project\Kuaishou_bot\Google Chrome\chrome.exe"
# #
# # browser = webdriver.Chrome(executable_path=r"D:\python_project\tv\chromedriver.exe",options=chrome_options)
# # browser.set_page_load_timeout(10)  # 设置页面加载超时
# #
# # try:
# #     browser.get(url)
# # except:
# #     print("超时了，强制停止刷新")
# # finally:
# #     html=browser.page_source
# #     soup = BeautifulSoup(html, "lxml")
# #     video_url=soup.video["src"]
# #     print(video_url)
# #     raw_name="xx"
# #     raw_file_name = raw_name.replace(" ", "")
# #     raw_file_name = re.sub('[\/:*?"<>|]', '-', raw_file_name)
# #     file_name=raw_file_name+".mp4"
# #     with open("download/"+file_name, 'wb') as f:
# #            c = pycurl.Curl()
# #            c.setopt(pycurl.USERAGENT,
# #                     "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")  # 配置请求HTTP头的User-Agent
# #            c.setopt(c.URL, video_url)
# #            c.setopt(c.CAINFO, certifi.where())
# #            c.setopt(c.WRITEDATA, f)
# #            c.perform()
# #            c.close()
# #     print(html)
# #     for j in range(22):
# #         k = "%03d" % 1
# #         print(k)
# #
# # browser.close()
#
# totalSize = 0
# fileNum = 0
# dirNum = 0
#
#
# def visitDir(path):
#     global totalSize
#     global fileNum
#     global dirNum
#     for lists in os.listdir(path):
#         sub_path = os.path.join(path, lists)
#         if os.path.isfile(sub_path):
#             fileNum = fileNum + 1  # 统计文件数量
#             totalSize = totalSize + os.path.getsize(sub_path)  # 文件总大小
#         elif os.path.isdir(sub_path):
#             dirNum = dirNum + 1  # 统计文件夹数量
#             visitDir(sub_path)  # 递归遍历子文件夹
#
# visitDir("download")
# print(fileNum)

for j in range(22):
      k = "%03d" % j
      print(k)
print("\033[1;94m网页登陆：请在浏览器中完成登陆，登陆后不要关闭浏览器，记得回到主程序输入" +str({"file_name":1,"video_url":2})+ "\033[0m")
