# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 15:56:28 2019

@author: sbtithzy
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 15:27:52 2019

@author: sbtithzy
"""
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import time
import datetime
start = time.perf_counter()
import  re, requests
import cx_Oracle
######################连接oracle
print (u'连接到oracle数据库...')
#conn = cx_Oracle.connect('sobute_ecology/sobute_ecology918@192.168.101.15/htdit')###OA数据库 
conn = cx_Oracle.connect('HZY_TEST/SBTit123@127.0.0.1/orcl')####本地数据库
print (u'数据库连接成功!')
cur = conn.cursor()
#判断表是否存在，若存在则清空此表
#创建表 address_picture,title,address_title
# =============================================================================
# sql = """CREATE TABLE HZY_ZB_CONTENT(
#                  ID INT,
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
# #ID,PICTUREURL,PICTURENAME,PICTURELINK,PICTUREORDER,PICTURETYPE,EID
# cur.execute(sql)
# conn.commit()
# =============================================================================
sql1 = """select nvl(max(id),0) from HZY_ZB_CONTENT"""
Id = cur.execute(sql1)
li =Id.fetchall()
IdMax = li[0][0]
conn.commit()
cur.execute("Truncate TABLE HZY_ZB_CONTENT")
# 获取网站信息
#url = 'http://www.sobute.com/index.php/news.html'   
url = "http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012"#获取参数网址
#使用正则从url1获取以下参数
r1 = requests.get(url)
r1txt = r1.text
VIEWSTATE =re.findall(r'id="__VIEWSTATE" value="(.*?)" />', r1txt,re.I)
EVENTVALIDATION =re.findall(r'id="__EVENTVALIDATION" value="(.*?)" />', r1txt,re.I)
MaxPage = int(re.findall(r'<font color=\"red\"><b>1/(.*?)</b>', r1txt,re.I)[0])
#url2请求头，请求body
#page = 1
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
# =============================================================================
# 
# data = {
#         "__EVENTTARGET": "MoreInfoList1$Pager",
#         "__EVENTARGUMENT": page,
#         "__LASTFOCUS": "",
#         "__VIEWSTATE": VIEWSTATE,
#         "__VIEWSTATEGENERATOR": "76D0A3AC",
#         "__VIEWSTATEENCRYPTED":"", 
#         "__EVENTVALIDATION":EVENTVALIDATION,
#         "MoreInfoList1$txtProjectName": "",
#         "MoreInfoList1$txtBiaoDuanName":"", 
#         "MoreInfoList1$txtBiaoDuanNo": "",
#         "MoreInfoList1$txtJSDW": "",
#         "MoreInfoList1$StartDate": "",
#         "MoreInfoList1$EndDate": "",
#         "MoreInfoList1$jpdDi": "-1",
#         "MoreInfoList1$jpdXian": "-1"
#         }
# =============================================================================
# =============================================================================
# r = requests.post(url,headers=headers,data=data)
# print(r.headers)
# print(r.text)
# print r'状态码',r.status_code
# =============================================================================
#####              
def getHtml(url,page):
    #global Page
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
    #print r'状态码',r.status_code
    #获取源代码
    text = r.text
    #print text
    return text
#html = getHtml(url)
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
#txt = getUrls(url)
# =============================================================================
# PICTUREORDER = [1,2,3,4,5,6,7,8]
# ID = [IdMax+1,IdMax+2,IdMax+3,IdMax+4,IdMax+5,IdMax+6,IdMax+7,IdMax+8]
# =============================================================================
i = IdMax
#url2 = 'http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/ViewReportDetail.aspx?RowID=675544&categoryNum=012&siteid=1'
url2 = 'http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/ViewReportDetail.aspx?RowID=675670'
def keyWord(txt):
    key_word = ['桥梁','隧道','铁路','公路']##关键字需要推广部补充
    key_word = [word for word in key_word if word in txt]####去掉虚词，保留词根模型
    key_word = '/'.join(key_word)
    return key_word
# =============================================================================
# hh = '苏州公园,桥梁是不是开始了'
# kkk = keyWord(hh)
# =============================================================================

def getContent(url,page): 
    global i,x
    html = getHtml(url,page) 
    #<span id="RptEndDate_23" style="display:inline-block;width:120px;">2019年6月28日</span></td>

    pattern = re.compile('\](.*?)</b></font></td>',re.S)####文章标题 
    pattern21 = re.compile('<span id=\"RptStartDate_23\" style=\"display:inline-block;width:120px;\">(.*?)</span>',re.S)######公告发布时间
    pattern2 = re.compile('<span id=\"RptEndDate_23\" style=\"display:inline-block;width:120px;\">(.*?)</span>',re.S)######公告结束时间
    pattern3 = re.compile('<span id=\"ZB_Type_23\" style=\"display:inline-block;width:97%;\">(.*?)</span>',re.S)####工程类型
    pattern4 = re.compile('<tr id=\"trzygg\" style=\"DISPLAY: none\">(.*?)<tr id=\"Tr17\">',re.S)####正文 
    items1 = re.findall(pattern, html)
    #print (items1[0])
    items21 = re.findall(pattern21, html)###发布日期 
    #print (items21[0])
    items2 = re.findall(pattern2, html)
    #print (items2[0])
    items3 = re.findall(pattern3, html)
    #print (items3[0])
    items4 = re.findall(pattern4, html)    
    htmeString = items4[0]
    keyword = keyWord(htmeString)##获取关键字
    today = datetime.datetime.today().date()
    # 获取正文
    pre = re.compile('>(.*?)<')
    items4[0] = ''.join(pre.findall(htmeString))
    T = items2[0].replace('年','-')
    T = T.replace('月','-')
    T = T.replace('日','')####转化为时间字符串 
    T = datetime.datetime.strptime(T,'%Y-%m-%d').date()  
    #print (items4[0])  
    #print (keyword)
#    result = []
#    result = [i,items1[0],url,items2[0],items3[0],items4[0]] 
    if T > today:####判断截至时间是否大于系统时间 
        
        if keyword:###判断如果没有需要的关键字信息不执行数据插入 
            cur.execute("INSERT INTO HZY_ZB_CONTENT(ID,TITLE,URL,KEYWORD,RELEASE_DATE,NOTICE_END_DATE,\
                                        PROJECT_TYPE,SOURCE,CONTENT) \
                VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (i,items1[0],url,keyword,items21[0],items2[0],items3[0],'江苏省建设工程招标网',items4[0][:2000]))
            conn.commit()    
            x = x + 1
            print (T,today)
            print (u'已完成第%d条数据存储...'  %(x))
#tex = getContent(url2,1)
#txta = ''

#############################
# =============================================================================
# for i in range(0, 1000):
#     review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])###使用正则只保留字母，用空格代替去掉的部分
#     review = review.lower()####将大写变小写
#     review = review.split()###将str变成list
#     ps = PorterStemmer()
#     review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]####去掉虚词，保留词根模型
#     review = ' '.join(review)###将list转化为str，用空格连接
#     corpus.append(review)###生成新的list            
# =============================================================================
#######################  
x = 0           
def main():    
    urls = ['http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012']    
    print (u'开始写入数据库，请稍等...')
   
    for url in urls:
        for page in range(1,MaxPage+1): 
            print (u'正在爬取第%d页数据...'  %(page))
            for url in getUrls('http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012',page):
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
if __name__ == "__main__":  # 判断文件入口
    main()
elapsed = (time.perf_counter() - start)#####时间结束点
print (u'累计用时:',elapsed) #####累计用时
