+++
author = "南宫乘风"
title = "Python的文件操作"
date = "2019-09-05 13:51:17"
tags=[]
categories=['Python学习']
image = "post/4kdongman/14.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100556433](https://blog.csdn.net/heian_99/article/details/100556433)

## #文件操作<br> #打开<br> #open("文件地址"，"操作形式’)

## 常用四种操作模式<br> '''<br> w：写入<br> r：读取<br> b：二进制<br> a+:追加<br> '''

```
fh=open("E:/Code/Python/python.txt","r")
date=fh.read()
```

## #文件读取

```
date=fh.read()
```

## <br> #读取一行类容

```
line=fh.readline()
```

## #关闭文件

```
fh.close()
```

## #文件写入<br>  

```
date="一起去学习"
fh2=open("E:/Code/Python/python2.txt","w")
fh2.write(date)
fh2.close()

```

 
