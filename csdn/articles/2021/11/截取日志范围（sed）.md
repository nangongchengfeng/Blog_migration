+++
author = "南宫乘风"
title = "截取日志范围（sed）"
date = "2021-11-03 16:53:26"
tags=['apache']
categories=['错误问题解决']
image = "post/4kdongman/88.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/121125188](https://blog.csdn.net/heian_99/article/details/121125188)

 

后续补充

```
sed  -n  '/2021-02-13 21:00:00/,/2021-02-13 22:00:00/p'   /usr/local/apache-tomcat-6.0.45/logs/crm.log   &gt; /opt/crm-`date +%Y-%m-%d-%H-%M`.log
截取某个时间段到某个时间段的日志    
sed  -n  '/2021-01-18 21:10:00/,$p'   /usr/local/apache-tomcat-6.0.45/logs/crm.log   &gt; /opt/crm-`date +%Y-%m-%d-%H-%M`.log 
截取某个时间段到现在的
```
