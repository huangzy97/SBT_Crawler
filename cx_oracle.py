# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:24:51 2019

@author: sbtithzy
"""
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import time
start = time.clock()
import urllib2, re, requests, HTMLParser
import cx_Oracle
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
######################连接oracle
print('连接到oracle数据库...')
conn = cx_Oracle.connect('****/*****@*******/******')##用户名，密码，主机，数据库名
#conn.outputtypehandler = OutputTypeHandler 
print('数据库连接成功!')
cur = conn.cursor()
#判断表是否存在，若存在则删除此表
cur.execute("DROP TABLE zb_content")
#创建表
sql = """CREATE TABLE zb_content(
                 title VARCHAR2(200),
                 address VARCHAR2(200),
                 relese_date VARCHAR2(200),
                 content CLOB
                 )"""
cur.execute(sql)
conn.commit()
#########################
# 获取网站信息
def getHtml(url):
    req = urllib2.Request(url)
    req.headers = headers  
    res = urllib2.urlopen(req)  # 打开网页
    #获取源代码
    text = res.read()
    return text
# 获取文章链接
def getUrls(url):
    html = getHtml(url)
    pattern = re.compile('<a href="article(.*?)"')
    items = re.findall(pattern, html)
    urls = []
    for item in items:
        urls.append('http://www.crecgec.com/article' + item)
    return urls
def getContent(url):
    html = getHtml(url)
    pattern = re.compile('<h1 class="detailT">(.*?)</h1>')####提取标题
    pattern2 = re.compile('<span>发布时间</span><em>(.*?)</em>')######提取发布时间
    items = re.findall(pattern, html)
    result = []
    items2 = re.findall(pattern2, html)
    # 获取正文
    pattern3 = re.compile('<div class="allNoticCont">(.*?)</div>',re.S)
    items3 = re.findall(pattern3,html)
    ####保存数据  
    result = [items[0],url,items2[0],items3[0]] 
    cur.execute("INSERT INTO zb_content(title,address,relese_date,content) VALUES ('%s','%s','%s','%s')" % (items[0],url,items2[0],items3[0]))
    conn.commit()
def main():    
    urls = [
        'http://www.crecgec.com/forum.php?mod=forumdisplay&fid=2&sortid=12&sortid=12&filter=sortid&mcode=0001&page={}'.format(
            str(i)) for i in range(1, 3)]
    
    print u'开始写入数据库，请稍等...'
    x = 0
    for url in urls:
        #print url
        html = getHtml(url)
        for url in getUrls(url):  
            #print url
            try:            
                getContent(url) 
                x = x + 1
            except Exception,e:
                print e
                
    print u'累计写入数据%s条'%(x)
    print u'数据存储结束！'
if __name__ == "__main__":  # 判断文件入口
    main()
elapsed = (time.clock() - start)#####时间结束点
print u'累计用时:',elapsed #####累计用时
