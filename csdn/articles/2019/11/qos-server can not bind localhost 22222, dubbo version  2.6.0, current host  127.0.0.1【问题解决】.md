+++
author = "南宫乘风"
title = "qos-server can not bind localhost:22222, dubbo version: 2.6.0, current host: 127.0.0.1【问题解决】"
date = "2019-11-19 16:36:56"
tags=[]
categories=['Java', '错误问题解决']
image = "post/4kdongman/19.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103145574](https://blog.csdn.net/heian_99/article/details/103145574)

好吧，这个问题比较low，但是记录一下，以免后期遗忘。

说白了，这个问题就是端口被占用了。

问题：

```
qos-server can not bind localhost:22222, dubbo version: 2.6.0, current host: 127.0.0.1
java.net.BindException: Address already in use: bind
```

看翻译：【22222端口被占用】

![20191119163341972.png](https://img-blog.csdnimg.cn/20191119163341972.png)

解决办法：

[解决端口被占用的问题（80、222222、3306）等等](https://blog.csdn.net/heian_99/article/details/103089408)

查看占用程序的pid

```
netstat -ano | findstr 22222
```

通过pid，停止程序

```
taskkill /f /pid 20720
```

看截图：

![2019111916364082.png](https://img-blog.csdnimg.cn/2019111916364082.png)

 

 
