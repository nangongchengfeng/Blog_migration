+++
author = "南宫乘风"
title = "Linux查看占用CPU和内存的 的程序"
date = "2020-03-14 21:26:47"
tags=['Linux', '内存', 'CPU', '查询']
categories=[' Linux实战操作']
image = "post/4kdongman/14.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104868409](https://blog.csdn.net/heian_99/article/details/104868409)

占内存的程序命令

```
 ps aux | head -1;ps aux|sort -k4nr|head -5
```

![20200314212600566.png](https://img-blog.csdnimg.cn/20200314212600566.png)

占CPU的程序命令

```
ps aux | head -1;ps aux|sort -k3nr|head -5
```

![20200314212429239.png](https://img-blog.csdnimg.cn/20200314212429239.png)

 

 
