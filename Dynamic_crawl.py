# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 20:53:34 2019

@author: sbtithzy
"""
import requests
import re
url = "http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012"#获取参数网址
#使用正则从url获取以下参数
r = requests.get(url)
r_txt = r.text
VIEWSTATE =re.findall(r'id="__VIEWSTATE" value="(.*?)" />', r_txt,re.I)
EVENTVALIDATION =re.findall(r'id="__EVENTVALIDATION" value="(.*?)" />', r_txt,re.I)
#url2请求头，请求body
header = {
        "Host":"www.jszb.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012",
        "Connection": "keep-alive",
        "Cookie": "ASP.NET_SessionId=vxvo2pjgqzy4ef55oqh5eq2x",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
        }

data = {
        "__EVENTTARGET": "MoreInfoList1$Pager",
        "__EVENTARGUMENT": "2",
        "__LASTFOCUS": "",
        "__VIEWSTATE": VIEWSTATE,
        "__VIEWSTATEGENERATOR": "76D0A3AC",
        "__VIEWSTATEENCRYPTED":"", 
        "__EVENTVALIDATION":EVENTVALIDATION,
        "MoreInfoList1$txtProjectName": "",
        "MoreInfoList1$txtBiaoDuanName":"", 
        "MoreInfoList1$txtBiaoDuanNo": "",
        "MoreInfoList1$txtJSDW": "",
        "MoreInfoList1$StartDate": "",
        "MoreInfoList1$EndDate": "",
        "MoreInfoList1$jpdDi": "-1",
        "MoreInfoList1$jpdXian": "-1"
        }

r = requests.post(url,headers=header,data=data)

print r'状态码',r.status_code
