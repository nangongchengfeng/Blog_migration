+++
author = "南宫乘风"
title = "Python的异常处理"
date = "2019-09-05 14:17:46"
tags=[]
categories=['Python学习']
image = "post/4kdongman/59.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100557054](https://blog.csdn.net/heian_99/article/details/100557054)

## 异常处理<br> 由于我经常爬虫，会因为网络，字符编码集等原因让程序崩溃，从而导致代码停止。

## 为了解决这个问题，我们可以使用异常处理，从而使程序跳过异常，保证程序可以不停止运行。

## 异常处理的格式（这个是最常见的一种，也是最实用的一种）

```
try：
    程序
except Exception as 异常名称：
    异常处理部分
```

## <br><br> 示例

```
try:
    for i in range(0,10):
        print(i)
        if(i==4):
            print(ij)
        print("hello")
except Exception as err:
    print(err)



```

## ![20190905142127445.png](https://img-blog.csdnimg.cn/20190905142127445.png)

## 异常处理过后

```
#让异常后的程序继续
for i in range(0,10):
    try:
        print(i)
        if(i==4):
            print(ij)
    except Exception as err:
        print(err)
```

![20190905142156476.png](https://img-blog.csdnimg.cn/20190905142156476.png)
