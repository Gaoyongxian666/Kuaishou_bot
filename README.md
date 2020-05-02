# 快手视频下载小助手 V 0.12
### 只需电脑即可，selenium项目  

 * 项目就在kuaishou_chrome.py ,最后使用pyinstaller打包exe，大约79M
 * V0.1  使用同时电脑和手机自动化项目 
 * V0.11 使用selenium, https://ww.lanzous.com/ic5kdte     
 * V0.12 修复bug，完善流程   https://ww.lanzous.com/ic675uf      
 * V0.13 修复bug，增加使用快手号下载  https://ww.lanzous.com/ic69bkd       

>项目结构源码（因为浏览器太大，上传不了github）： https://ww.lanzous.com/ic69ibg


### 项目如何打包 
> 在output 文件夹中有发布的范本，例如打算发布版本V0.13  
> 蓝奏云： 

1. 在output中复制一份重命名 kuaishou_v0.13  
2. 打开命令行，切换到你的环境
3. cd D:\python_project\Kuaishou_bot\output\kuaishou_v0.13 
4. 压缩打包：pyinstaller -F -i f.ico D:\python_project\Kuaishou_bot\kuaishou_chrome.py
5. dist文件夹中是解压出的exe  
> 说明：Google Chrome是一个绿色版浏览器  

