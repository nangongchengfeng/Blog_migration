+++
author = "南宫乘风"
title = "Python的爬虫利器之urllib"
date = "2019-09-07 17:05:43"
tags=[]
categories=['Python学习']
image = "post/4kdongman/97.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100601716](https://blog.csdn.net/heian_99/article/details/100601716)

#  

# urllib包 

<br> urllib是一个包含几个模块来处理请求的库： <br> - urllib.request发送http请求 <br> - urllib.error处理请求过程中出现的异常 <br> - urllib.parse解析url <br> - urllib.robotparser解析robots.txt文件

一般我们爬虫只需要常用的几个，下面只列出比较常用的函数

```
import urllib.request
```

## urlreteieve：直接下载网页到本地

### 格式

<br> urlreteieve（网址，本地的文件）

示例：

```
import urllib.request
urllib.request.urlretrieve("https://read.douban.com/provider/all","F:/test/down.html")
print("下载完成")
```

![20190907165836862.png](https://img-blog.csdnimg.cn/20190907165836862.png)

## urlcleanup：清楚系统缓存

```
import urllib.request
urllib.request.urlcleanup()
urllib.request.urlretrieve("https://read.douban.com/provider/all","F:/test/down.html")
print("下载完成")
```

## <br> info() ：看相应情况的简介

```
import urllib.request
file=urllib.request.urlopen("https://read.douban.com/provider/all")
print(file.info())
```

![20190907170116450.png](https://img-blog.csdnimg.cn/20190907170116450.png)

## getcode() 返回网页爬取状态码

![20190907170401163.png](https://img-blog.csdnimg.cn/20190907170401163.png)

 

## geturl()  获取当前访问的网页的url

![20190907170456988.png](https://img-blog.csdnimg.cn/20190907170456988.png)
