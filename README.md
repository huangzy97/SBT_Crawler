# SBT_Crawler
招标网站信息
## 静态网站抓取  
招标网站python2.7版本
OA抓取需求为抓取官网的新闻放到本地门户作为新闻浏览。需要按照上次新闻图片的ID顺序插入数据，所以每次在连接数据库的时候需要先获取目前表中的最大ID，本次插入数据是基于上次最大ID的基础上，后面在抓取数据的时候带入一个全局变量作为插入ID的列号，这里只取网页的当前页的最大新闻，没有分页  
demo(https://github.com/huangzy97/SBT_Crawler/blob/master/OA_Crawler)
## 动态数据抓取  
