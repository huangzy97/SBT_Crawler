# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 08:59:45 2019

@author: sbtithzy
"""
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import time
import datetime
import  re, requests
import cx_Oracle   
start = time.perf_counter()
x = 0     
# connect database
print (u'连接到oracle数据库...')
#conn = cx_Oracle.connect('HZY_TEST/SBTit123@127.0.0.1/orcl')####本地数据库
print (u'数据库连接成功!')
cur = conn.cursor()

# create table 
# =============================================================================
# sql = """CREATE TABLE FR_OM_FSSYB_T(
#                  ID INT,
#                  TITLE VARCHAR2(1000),
#                  RELEASE_DATE  VARCHAR2(1000),
#                  NOTICE_END_DATE VARCHAR2(1000),
#                  URL  VARCHAR2(1000),
#                  KEYWORD VARCHAR2(1000),
#                  SOURCE  VARCHAR2(1000)
#                  )"""
# 
# 
# cur.execute(sql)
# conn.commit()
# =============================================================================

# get max id
sql1 = """select nvl(max(id),0) from FR_OM_FSSYB_T"""
Id = cur.execute(sql1)
li =Id.fetchall()
IdMax = li[0][0]
conn.commit()
cur.execute("Truncate TABLE FR_OM_FSSYB_T")
i = IdMax
num = 0
# get data from website
url_index = 'http://ggzy.njzwfw.gov.cn'
url_target = 'http://ggzy.njzwfw.gov.cn/njweb/gchw/goods.html'
url = 'http://ggzy.njzwfw.gov.cn/njweb/gchw/070001/moreinfogchw.html?_=43527'
#  get max website page
r1txt = requests.get(url).text
MaxPage = int(re.findall(r'<span id=\"index070001\">1/(.*?)</span>',r1txt,re.I)[0])

# define function for get website page all content
def GetHtml(url):
    txt = requests.get(url).text
    return txt

# define function for get urls
def GetFirstUrl(url):
    global MaxPage
    urls = []
    for i in range(2,100):
        urls.append('http://ggzy.njzwfw.gov.cn/njweb/gchw/070001/'+str(i)+'.html')
    return urls   

# define function for get target urls 
def GetTargetUrl(url):
    txt = GetHtml(url)
    result1 = []
    result2 = []
    result3 = []
    result4 = []
    pattern = re.compile(r'<div class=\"ewb-info-num2\" style=\"width:350px;\">(.*?)\" class=\"ewb-info-top2\" style=\"text-align:left;\">',re.S)####项目名称 
    pattern2 = re.compile(r'<div class=\"ewb-info-num2\" style=\"width:290px;margin-right:30px;\">(.*?)\" class=\"ewb-info-top2\">',re.S)######标段名称 
    pattern3 = re.compile(r'window.(.*?);',re.S)##URL
    pattern4 = re.compile(r'<p class=\"ewb-info-top2\">(.*?)</p>',re.S)##URL
    items = re.findall(pattern, txt)
    for item in items:
        result1.append(item[18:])
    items2 = re.findall(pattern2, txt)
    for item in items2:
        result2.append(item[20:])
    items3 = re.findall(pattern3, txt)
    for item in items3:
        result3.append('http://ggzy.njzwfw.gov.cn'+item[6:-2])
    items4 = re.findall(pattern4, txt)
    for item in items4:
        result4.append(item)
    return result3

# define function for get target website content
def KeyWord(txt):
    key_word = ['聚氨酯','聚','渗透结晶','界面剂','砼防护','砼修补','砼修复','防水涂料','拼接胶','结构胶','胶黏剂','环氧','灌浆料','聚合物','防水材料']##关键字需要推广部补充
    key_word = [word for word in key_word if word in txt]####去掉虚词，保留词根模型
    key_word = '/'.join(key_word)
    return key_word

def GetContent(url):
    global x,i
    txt = GetHtml(url)
    result6 = []
    pattern = re.compile(r'<meta name=\"ArticleTitle\" content=\"(.*?)">',re.S)####项目名称 
    pattern2 = re.compile(r'<meta name=\"PubDate\" content=\"(.*?)">',re.S)######发布时间 
    pattern3 = re.compile(r'<meta name=\"Url\" content=\"(.*?)">',re.S)##URL
    pattern4 = re.compile(r'<title>(.*?)</title>',re.S)##Source
    #pattern5 = re.compile(r'<p style=\"text-align: center\" class=\"NewHeadline\">(.*?)window.onload',re.S)##keyword
    #pattern5 = re.compile(r'<p class=\"NewSubtitle\">1(.*?)window.onload',re.S)##keyword
    pattern5 = re.compile(r'<style>(.*?)<script>',re.S)##keyword
    pattern6 = re.compile(r'的截止时间为 (.*?) ，投标人应在截止时间前通过南京市公共资源交易中心货物网上交易平台',re.S)##enddate
    #pattern6 = re.compile(r'的截止时间为 (.*?)</p>',re.S)##enddate
    items1 = re.findall(pattern, txt)# title
    items2 = re.findall(pattern2, txt)#PubDate
    items3 = re.findall(pattern3, txt)#Url
    items4 = re.findall(pattern4, txt)#Source
    items5 = re.findall(pattern5, txt)#keyword
    items6 = re.findall(pattern6, txt)#end_date
    for item in items6:
        result6.append(item[:10])
    htmeString = items5[0]
    pre = re.compile('>(.*?)<')
    items5[0] = ''.join(pre.findall(htmeString))
    keyword = KeyWord(items5[0])##获取关键字
    today = datetime.datetime.today().date()
    if result6:
        T = datetime.datetime.strptime(result6[0],'%Y-%m-%d').date() 
        if T > today:
            if 1:###判断如果没有需要的关键字信息不执行数据插入 
                cur.execute("INSERT INTO FR_OM_FSSYB_T(ID,TITLE,RELEASE_DATE,NOTICE_END_DATE,URL,KEYWORD,SOURCE) \
                            VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (i,items1[0],items2[0],result6[0],items3[0],keyword,items4[0]))
                conn.commit()    
                x = x + 1
                print (u'已完成第%d条数据存储...'  %(x))
def main():    
    page = 0
    urls = ['http://ggzy.njzwfw.gov.cn/njweb/gchw/070001/moreinfogchw.html?_=43527']    
    print (u'开始爬取数据，请稍等...')  
    for url in GetFirstUrl(urls):
        #print (url)
        page += 1
        print (u'正在爬取第%d页数据...'  %(page))           
        for url in GetTargetUrl(url):
            #print (url)
            try:  
                GetContent(url)
                #print u'已完成第%s页第%s条数据存储...'  %(page,x)                  
                global i
                    #x = x + 1                    
                i = i + 1
            except Exception as e:
                global num
                print (e)  
                num += 1
    print (u'累计写入数据%d条'%(x))
    print (u'累计失败%d条'%(num))
    print (u'数据存储结束！')
if __name__ == "__main__":  # 判断文件入口
    main()
elapsed = (time.perf_counter() - start)#####时间结束点
print (u'累计用时:',elapsed) #####累计用时
