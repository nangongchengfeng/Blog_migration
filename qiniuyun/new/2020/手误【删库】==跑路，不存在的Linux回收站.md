---
author: 南宫乘风
categories:
- Linux实战操作
date: 2020-07-27 23:14:37
description: 上一章节，讲了自己悲剧的删库事件。原因总结：手贱还是手贱不过大脑没有回收站功能俗话说，吃一堑长一智。接下来就是我的解决方案。给添加一个回收站的功能，这是不是很高大上啊这下就不怕手贱删库了手误删库跑路，。。。。。。。
image: http://image.ownit.top/4kdongman/87.jpg
tags:
- 回收站
- centos
- 删库
- linux
title: 手误【删库】 == 跑路，不存在的    Linux回收站
---

<!--more-->

**上一章节，讲了自己悲剧的删库事件。**

**原因总结：**

**（1）手贱**

**（2）还是手贱**

**（3）不过大脑**

**（4）Linux没有回收站功能**

![](aHR0cDovL2ltZy5kb3V0dWxhLmNvbS9wcm9kdWN0aW9uL3VwbG9hZHMvaW1hZ2UvMjAxOC8wOC8wNC8yMDE4MDgwNDM0OTA5M192SWphd2cuZ2lm)![](format,png)

**俗话说，吃一堑长一智。接下来就是我的解决方案。**

**给Linux添加一个回收站的功能，这是不是很高大上啊**

**这下就不怕手贱删库了**

# [手误【删库】 == 跑路，不存在的 ——删瓦辛格](https://blog.csdn.net/heian_99/article/details/105689982)

 

![](aHR0cDovL2ltZy5kb3V0dWxhLmNvbS9wcm9kdWN0aW9uL3VwbG9hZHMvaW1hZ2UvMjAxOC8wNC8xNC8yMDE4MDQxNDY2NTIyNl95c3JSbksuZ2lm)

 

  
**删除是危险系数很高的操作，一旦误删可能会造成难以估计的损失。**

**在 Linux 系统中这种危险尤为明显，一条简单的语句：rm –rf /\* 就会把整个系统全部删除，而 Linux 并不会因为这条语句的不合理而拒绝执行。**

![](aHR0cDovL2ltZy5kb3V0dWxhLmNvbS9wcm9kdWN0aW9uL3VwbG9hZHMvaW1hZ2UvMjAxNy8wNy8wOS8yMDE3MDcwOTYwODcyMF9WSUxqQlUuZ2lm)

**这时，有个像Windows的那样的回收站是多么的重要啊。下面可以使用代码实现**

 

![](format,png)

 

## rm命令修改

```bash
vim /etc/bashrc  

alias rm=delete  #命令别名，通过delete来实现rm改为mv
alias r=delete
alias rl='ls /trash' #rl 命令显示回收站中的文件
alias ur=undelfile #ur 命令找回回收站的文件
undelfile()
{
    mv /trash/$@ ./
}
delete()
{
if [ ! -d "/trash/" ];then
         mkdir /trash
fi
\mv --backup=numbered $@ /trash/
}
cleartrash()
{
    read -p "clear sure?[n]" confirm
    [ $confirm == 'y' ] || [ $confirm == 'Y' ]  && /bin/rm -rf /trash/*
}
```

 

添加完毕后保存，执行source命令生效

```bash
source /etc/bashrc 
```

![](format,png)

 

## 使用方法

  
**以使用rm（删除），ur（撤销），rl（列出回收站），cleartrash（清空回收站）命令了。**

 

**删除一个文件夹，hellworld下面的文件均被移到回收站中**

```bash
 rm helloworld/  或者 r helloworld/ 或者 delete helloworld/
```

**删除一个文件**

```bash
rm 123.txt 或者 r  123.txt 或者 delete  123.txt
```

![](http://image.ownit.top/csdn/20200727223701681.png)

**列出回收站信息**

![](http://image.ownit.top/csdn/20200727223753250.png)

**要查看回收站内容详细信息，只要加个参数就好**

![](http://image.ownit.top/csdn/20200727223822796.png)

**撤销123.txt**

```bash
ur 123.txt 或者 undelfile  123.txt
```

**撤销helloworld文件夹**

```bash
ur helloworld  或者 undelfile helloworld 
```

![](http://image.ownit.top/csdn/20200727224026135.png)

**清空回收站**

```bash
[root@Master ~]# cleartrash     #会弹出是否清空
clear sure?[n]y
[root@Master ~]# 
```

## **删库，我害怕删库吗**

 

![](aHR0cDovL2ltZy5kb3V0dWxhLmNvbS9wcm9kdWN0aW9uL3VwbG9hZHMvaW1hZ2UvMjAyMC8wNC8xMS8yMDIwMDQxMTU4OTQzMF9Ca3RuZUQuZ2lm)