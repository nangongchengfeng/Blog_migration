+++
author = "南宫乘风"
title = "Linux用户环境配置文件"
date = "2019-01-25 21:36:47"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/07.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86651933](https://blog.csdn.net/heian_99/article/details/86651933)

<br>**用户操作环境配置文件：**

**从/etc/skel目录复制过来**

**![20190125210956175.png](https://img-blog.csdnimg.cn/20190125210956175.png)**

**.bashrc             打开新终端           /etc/bashrc<br> .bash_profile       用户登录系统         /ect/profile<br> .bash_logout        注销系统             **

<br>**示例：设置命令别名**

## **临时命令别名（关机重启，就没有了）**

**# alias 命令别名=‘命令’**

```
alias ipshow='cat /etc/sysconfig/network-scripts/ifcfg-ens33'
```

![20190125211616558.png](https://img-blog.csdnimg.cn/20190125211616558.png)

## <br>**永久别名（可以一直存在）**

**针对单个用户设置别名**

（1）创建hei用户，修改vim /home/hei/.bashrc 

![20190125212504317.png](https://img-blog.csdnimg.cn/20190125212504317.png)

（2）进入  /home/hei/.bashrc ，在最后一行添加  ** alias ipshow=' cat /etc/sysconfig/network-scripts/ifcfg-ens33' 保存退出**

![20190125212435357.png](https://img-blog.csdnimg.cn/20190125212435357.png)

（3）切换到hei用户下查看

![2019012521312935.png](https://img-blog.csdnimg.cn/2019012521312935.png)

<br>**针对所有用户设置别名**

**这个方法和上面的一样，只需要修改的文件不一样。下面已经列出**

**（1）修改/etc/bashrcde文件**

**（2）添加命令别名代码**

**（3）刷新文件即可**<br>  

```
root@wei ~]# vim /etc/bashrc
 
   alias ipshow=' cat /etc/sysconfig/network-scripts/ifcfg-ens33'
[root@wei ~]# source /etc/bashrc
```

<br>  

 

 

 
