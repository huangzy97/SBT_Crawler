# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:11:45 2019
@author: sbtithzy
"""
import time
start = time.clock()
import urllib2, re, requests, HTMLParser
import MySQLdb
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
print('���ӵ�mysql������...')
conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', db='zhaobiao',charset='utf8')
print('���ݿ����ӳɹ�!')
cur = conn.cursor()
#�жϱ��Ƿ���ڣ���������ɾ���˱�
cur.execute("DROP TABLE zb_content2")
#������
sql = """CREATE TABLE zb_content2(
                 title  CHAR(200),
                 address CHAR(200),
                 relese_date  CHAR(200),
                 content  text)"""
cur.execute(sql)
conn.commit()
# ��ȡ��վ��Ϣ
def getHtml(url):
    req = urllib2.Request(url)
    req.headers = headers
    res = urllib2.urlopen(req)  # ����ҳ
    #��ȡԴ����
    text = res.read()
    return text
# ��ȡ��������
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
    pattern = re.compile('<h1 class="detailT">(.*?)</h1>')####��ȡ����
    pattern2 = re.compile('<span>����ʱ��</span><em>(.*?)</em>')######��ȡ����ʱ��
    items = re.findall(pattern, html)
    result = []
    items2 = re.findall(pattern2, html)
    # ��ȡ����
    pattern3 = re.compile('<div class="allNoticCont">(.*?)</div>',re.S)
    items3 = re.findall(pattern3,html)
    ####�������� 
    result = [items[0],url,items2[0],items3[0]]    
    cur.execute("INSERT INTO zb_content2(title,address,relese_date,content) VALUES ('%s','%s','%s','%s');" % (items[0],url,items2[0],items3[0]))
    conn.commit()
def main():    
    urls = [
        'http://www.crecgec.com/forum.php?mod=forumdisplay&fid=2&sortid=12&sortid=12&filter=sortid&mcode=0001&page={}'.format(
            str(i)) for i in range(1, 3)]
    
    print u'��ʼд�����ݿ⣬���Ե�...'
    for url in urls:
        print url
        html = getHtml(url)
        for url in getUrls(url):  
            print url
            try:            
                getContent(url)                
            except Exception,e:
                print e
    print u'�ۼ�д������%s��'%(i*20)
    print u'���ݴ洢������'
if __name__ == "__main__":  # �ж��ļ����
    main()
elapsed = (time.clock() - start)#####ʱ�������
print u'�ۼ���ʱ:',elapsed #####�ۼ���ʱ