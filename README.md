# SBT_Crawler
招标网站信息
## 静态网站抓取  
招标网站python2.7版本
OA抓取需求为抓取官网的新闻放到本地门户作为新闻浏览。需要按照上次新闻图片的ID顺序插入数据，所以每次在连接数据库的时候需要先获取目前表中的最大ID，本次插入数据是基于上次最大ID的基础上，后面在抓取数据的时候带入一个全局变量作为插入ID的列号，这里只取网页的当前页的最大新闻，没有分页  
# [demo_oracle](https://github.com/huangzy97/SBT_Crawler/blob/master/OA_Crawler)  
## 动态数据抓取 1
http://www.jszb.com.cn/jszb/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012
这个网站是动态加载(URL不变，动态加载)，这个里面用到POST给服务器，然后服务器校验参数ViewState和EVENTVALIDATION,这两个参数不是很理解，F12看了一下，每次刷新页面这两个参数都是动态变化了，但是其他的Form数据是定的。
  
      
### 基本思路是：  
### 1、用Get方式访问一次网站获取到ViewState和EVENTVALIDATION，然后把这两个参数作为Form的数据传给服务器。  
### 2、后面用Post方式带上头信息和Form信息去获取页面信息。  
### 3、抓取数据下载到数据库。  
### PS：  
### 1、ViewState  
当请求某个页面时，ASP.NET把所有控件的状态序列化成一个字符串，然后做为窗体的隐藏属性送到客户端。当客户端把页面回传时，ASP.NET分析回传的窗体属性，并赋给控件对应的值。  
### 2、EVENTVALIDATION  
“id”属性为“__EVENTVALIDATION”的隐藏字段是ASP.NET 2.0的新增的安全措施。该功能可以阻止由潜在的恶意用户从浏览器端发送的未经授权的请求.
为了确保每个回发和回调事件来自于所期望的用户界面元素，ASP.NET运行库将在事件中添加额外的验证层。服务器端通过检验表单提交请求的内容，将其与“id”属性为“__EVENTVALIDATION”隐藏字段中的信息进行匹配。根据匹配结果来验证未在浏览器端添加额外的输入字段（有可能为用户在浏览器端恶意添加的字段），并且该值是在服务器已知的列表中选择的。ASP.NET运行库将在生成期间创建事件验证字段，而这是最不可能获取该信息的时刻。像视图状态一样，事件验证字段包含散列值以防止发生浏览器端篡改。  
### [动态抓取实例](https://github.com/huangzy97/SBT_Crawler/blob/master/Dynamic_crawl.py)   
### [江苏建设工程招标网全部代码](https://github.com/huangzy97/SBT_Crawler/blob/master/JSJSGCZBW_Crawler.py)  
## 动态数据抓取 2
###### http://ggzy.njzwfw.gov.cn/njweb/南京市公共资源交易平台  
