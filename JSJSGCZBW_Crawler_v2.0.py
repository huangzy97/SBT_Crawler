# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:56:22 2019
@author: sbtithzy
"""
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import time
import datetime
start = time.perf_counter()
import  re, requests
import cx_Oracle
x = 0           
# 连接oracle数据库
print (u'连接到oracle数据库...')
conn = cx_Oracle.connect('账号/密码@IP地址/数据库名称')##需要连接的数据库 
print (u'数据库连接成功!')
cur = conn.cursor()
# 创建表 
# =============================================================================
# sql = """CREATE TABLE FR_OM_ZB_T(
#                  ID INT,
#                  CITY  VARCHAR2(1000),
#                  TITLE VARCHAR2(1000),
#                  URL  VARCHAR2(1000),
#                  KEYWORD VARCHAR2(1000),
#                  RELEASE_DATE  VARCHAR2(1000),
#                  NOTICE_END_DATE VARCHAR2(1000),
#                  PROJECT_TYPE VARCHAR2(1000),
#                  SOURCE  VARCHAR2(1000),
#                  CONTENT NCLOB
#                  )"""
# 
#
# cur.execute(sql)
# conn.commit()
# =============================================================================
# 获取当前表的最大ID 
sql1 = """select nvl(max(id),0) from FR_OM_ZB_T"""
Id = cur.execute(sql1)
li =Id.fetchall()
IdMax = li[0][0]
conn.commit()
cur.execute("Truncate TABLE FR_OM_ZB_T")
# 获取网站信息 
url = "http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012"#获取参数网址
# 使用正则从url获取以下参数
r1 = requests.get(url)
r1txt = r1.text
VIEWSTATE =re.findall(r'id="__VIEWSTATE" value="(.*?)" />', r1txt,re.I)
EVENTVALIDATION =re.findall(r'id="__EVENTVALIDATION" value="(.*?)" />', r1txt,re.I)
MaxPage = int(re.findall(r'<font color=\"red\"><b>1/(.*?)</b>', r1txt,re.I)[0])
# 头信息 
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
    r = requests.post(url,headers=headers,data=data,timeout = 20)
    text = r.text
    return text
def getUrls(url,page):
    html = getHtml(url,page)
    pattern = re.compile('ViewReportDetail(.*?)\"',re.S)
    items = re.findall(pattern, html)
    urls = []
    for item in items:
        urls.append('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/ViewReportDetail' + item)       
    return urls
def getCity(url,page):
    html = getHtml(url,page)
    pattern = re.compile('ViewReportDetail.(.*?)\"',re.S)
    pattern2 = re.compile('title=\"\[(.*?)\]',re.S)  
    items = re.findall(pattern, html)
    items2 = re.findall(pattern2, html)
    addrs = []
    for addr in items2:
        addrs.append(addr)
    urls = []
    for item in items:
        urls.append('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/ViewReportDetail.' + item)       
    return [urls,addrs]
def keyWord(txt):
    key_word = ['桥梁','隧道','铁路','公路','城墙']##关键字需要推广部补充
    key_word = [word for word in key_word if word in txt]###
    key_word = '/'.join(key_word)
    return key_word
def getContent(url,page): 
    global i,x
    html = getHtml(url,page) 
    #<span id="RptEndDate_23" style="display:inline-block;width:120px;">2019年6月28日</span></td>
    note = getCity('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012',page)
    pattern = re.compile('\](.*?)</b></font></td>',re.S)####文章标题 
    pattern21 = re.compile('<span id=\"RptStartDate_23\" style=\"display:inline-block;width:120px;\">(.*?)</span>',re.S)######公告发布时间
    pattern2 = re.compile('<span id=\"RptEndDate_23\" style=\"display:inline-block;width:120px;\">(.*?)</span>',re.S)######公告结束时间
    pattern3 = re.compile('<span id=\"ZB_Type_23\" style=\"display:inline-block;width:97%;\">(.*?)</span>',re.S)####工程类型
    pattern4 = re.compile('<tr id=\"trzygg\" style=\"DISPLAY: none\">(.*?)<tr id=\"Tr17\">',re.S)####正文 
    items1 = re.findall(pattern, html)##标题
    items21 = re.findall(pattern21, html)###发布日期 
    items2 = re.findall(pattern2, html)###截止日期
    items3 = re.findall(pattern3, html)###工程类型
    items4 = re.findall(pattern4, html)###正文 
    htmeString = items4[0]
    keyword = keyWord(htmeString)##获取关键字
    today = datetime.datetime.today().date()
    # 获取正文
    pre = re.compile('>(.*?)<')####清理HTML标签
    items4[0] = ''.join(pre.findall(htmeString))
    T = items2[0].replace('年','-')
    T = T.replace('月','-')
    T = T.replace('日','')####转化为时间字符串 
    T = datetime.datetime.strptime(T,'%Y-%m-%d').date() 
    kk = note[0][:].index(url)#获取city的index
    city = note[1][kk]
    if T > today:####判断截至时间是否大于系统时间         
        if 1:###判断如果没有需要的关键字信息不执行数据插入 
            cur.execute("INSERT INTO FR_OM_ZB_T(ID,CITY,TITLE,URL,KEYWORD,RELEASE_DATE,NOTICE_END_DATE,\
                                        PROJECT_TYPE,SOURCE) \
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (i,city,items1[0],url,keyword,items21[0],items2[0],items3[0],'江苏省建设工程招标网'))
            conn.commit()    
            x = x + 1
            #print (T,today)
            print (u'已完成第%d条数据存储...'  %(x))
# main函数
def main():    
    urls = ['http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012']    
    print (u'开始爬取数据，请稍等...')  
    for url in urls:
        for page in range(1,MaxPage+1):#MaxPage 
            print (u'正在爬取第%d页数据...'  %(page))
            for url in getUrls('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012',page):
                #print (url)
                try:  
                    getContent(url,page)
                    #print u'已完成第%s页第%s条数据存储...'  %(page,x)                  
                    global i
                    #x = x + 1                    
                    i = i + 1
                except Exception as e:
                    print (e)              
    print (u'累计写入数据%d条'%(x))
    print (u'数据存储结束！')
 # 程序入口       
if __name__ == "__main__":  # 判断文件入口
    main()
elapsed = (time.perf_counter() - start)#####时间结束点
print (u'累计用时:',elapsed) #####累计用时
