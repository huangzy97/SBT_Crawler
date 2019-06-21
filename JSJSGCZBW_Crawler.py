# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 21:17:11 2019

@author: sbtithzy
"""
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import time
start = time.clock()
import urllib2, re, requests, HTMLParser
import cx_Oracle
######################连接oracle
print u'连接到oracle数据库...'
#conn = cx_Oracle.connect('sobute_ecology/sobute_ecology918@192.168.101.15/htdit')###OA数据库 
conn = cx_Oracle.connect('HZY_TEST/SBTit123@127.0.0.1/orcl')####本地数据库
print u'数据库连接成功!'
cur = conn.cursor()
#创建表 address_picture,title,address_title
# =============================================================================
# sql = """CREATE TABLE HZY_ZB_CONTENT(
#                  ID INT,
#                  TITLE VARCHAR2(1000),
#                  URL  VARCHAR2(1000),
#                  NOTICE_END_DATE VARCHAR2(1000),
#                  PROJECT_TYPE VARCHAR2(1000),
#                  CONTENT NCLOB
#                  )"""
# 
# #ID,PICTUREURL,PICTURENAME,PICTURELINK,PICTUREORDER,PICTURETYPE,EID
# cur.execute(sql)
# conn.commit()
# =============================================================================
sql1 = """select nvl(max(id),0) from HZY_ZB_CONTENT"""
Id = cur.execute(sql1)
li =Id.fetchall()
IdMax = li[0][0]
conn.commit()
#判断表是否存在，若存在则清空此表
cur.execute("Truncate TABLE HZY_ZB_CONTENT")
# 获取网站信息
#url = 'http://www.sobute.com/index.php/news.html'   
import requests
import re
url = "http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012"#获取参数网址
#使用正则从url1获取以下参数
r1 = requests.get(url)
r1txt = r1.text
VIEWSTATE =re.findall(r'id="__VIEWSTATE" value="(.*?)" />', r1txt,re.I)
EVENTVALIDATION =re.findall(r'id="__EVENTVALIDATION" value="(.*?)" />', r1txt,re.I)
MaxPage = int(re.findall(r'<font color=\"red\"><b>1/(.*?)</b>', r1txt,re.I)[0])###获取最大页码
headers = {
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
def getHtml(url,page):
    data = {
        "__EVENTTARGET": "MoreInfoList1$Pager",
        "__EVENTARGUMENT": page,
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
    r = requests.post(url,headers=headers,data=data)
    #print r'状态码',r.status_code
    #获取源代码
    text = r.text
    #print text
    return text
# 提取新闻地址
def getUrls(url,page):
    html = getHtml(url,page)
    pattern = re.compile('ViewReportDetail(.*?)&',re.S)
    items = re.findall(pattern, html)
    #print items
    urls = []
    for item in items:
        urls.append('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/ViewReportDetail' + item)       
    return urls
i = IdMax
def getContent(url,page): 
    global i
    html = getHtml(url,page) 
    pattern = re.compile('\](.*?)</b></font></td>',re.S)####文章标题 
    pattern2 = re.compile('<span id=\"RptEndDate_23\" style=\"display:inline-block;width:120px;\">(.*?)</span>',re.S)######公告结束时间
    pattern3 = re.compile('<span id=\"ZB_Type_23\" style=\"display:inline-block;width:97%;\">(.*?)</span>',re.S)####工程类型
    pattern4 = re.compile('<tr id=\"trzygg\" style=\"DISPLAY: none\">(.*?)<tr id=\"Tr17\">',re.S)####正文 
    items1 = re.findall(pattern, html)
    items2 = re.findall(pattern2, html)
    items3 = re.findall(pattern3, html)
    items4 = re.findall(pattern4, html)    
    htmeString = items4[0]
    # 获取正文
    pre = re.compile('>(.*?)<')
    items4[0] = ''.join(pre.findall(htmeString))###清洗HTML标签
    cur.execute("INSERT INTO HZY_ZB_CONTENT(ID,TITLE,URL,NOTICE_END_DATE,\
                                        PROJECT_TYPE,CONTENT) \
                VALUES ('%s','%s','%s','%s','%s','%s')" % (i,items1[0],url,items2[0],items3[0],items4[0][:2000]))
    conn.commit()
txta = ''
def main():    
    urls = ['http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012']    
    print u'开始写入数据库，请稍等...'
    x = 0    
    for url in urls:
        for page in range(1,MaxPage+1): 
            print u'正在存储第%s页数据...'  %(page) 
            for url in getUrls('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012',page):
                try:            
                    getContent(url,page)
                    
                    global i
                    x = x + 1
                    i = i + 1
                except Exception,e:
                    print e              
    print u'累计写入数据%s条'%(x)
    print u'数据存储结束！'
if __name__ == "__main__":  # 判断文件入口
    main()
elapsed = (time.clock() - start)#####时间结束点
print u'累计用时:',elapsed #####累计用时
