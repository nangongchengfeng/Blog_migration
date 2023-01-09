+++
author = "南宫乘风"
title = "Linux文件增删改"
date = "2019-01-06 13:58:06"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/80.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/85924646](https://blog.csdn.net/heian_99/article/details/85924646)

**Linux目录/文件增删改**

**创建文件**

**(1)**

**# touch  &lt;文件名称&gt;**

**![2019010613380274.png](https://img-blog.csdnimg.cn/2019010613380274.png)**

 

**(2)**

**花括号展开**

**touch /root/{1,3,9}.txt**

**![20190106134002790.png](https://img-blog.csdnimg.cn/20190106134002790.png)**

**touch /root/{0..100}.txt  批量创建文件**

**![20190106134135947.png](https://img-blog.csdnimg.cn/20190106134135947.png)**

**删除文件**

**rm -f [文件名] **

**-rf  代表强制删除**

**![20190106134510587.png](https://img-blog.csdnimg.cn/20190106134510587.png)**

**批量删除文件**

**rm -f *txt**

**![20190106134738416.png](https://img-blog.csdnimg.cn/20190106134738416.png)**

 

**复制文件**

**cp 只能复制文件**

**cp -r  可以复制目录**

**# cp [option] 源文件  目标文件**

```
[root@zhang ~]# mkdir /root/{linux,windown}
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# touch /root/linux/{1,2,3}.txt
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# cd linux/
[root@zhang linux]# ls
1.txt  2.txt  3.txt
[root@zhang linux]# cd /r
root/ run/  
[root@zhang linux]# cd /root/
[root@zhang ~]# cp /root/linux/1.txt /root/windown/
[root@zhang ~]# cd windown/
[root@zhang windown]# ls
1.txt
[root@zhang windown]# cd ..
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# cp /root/linux/2.txt /root/windown/2.jpg
[root@zhang ~]# cd windown/
[root@zhang windown]# ls
1.txt  2.jpg

```

** -r   复制文件目录**

```
[root@zhang ~]# cp -r /root/linux/ windown/
[root@zhang ~]# ls
anaconda-ks.cfg  linux  mysql57-community-release-el7-8.noarch.rpm  windown
[root@zhang ~]# cd windown/
[root@zhang windown]# ls
1.txt  2.jpg  linux
[root@zhang windown]# cd linux/
[root@zhang linux]# ls
1.txt  2.txt  3.txt

```

**-fn 强制覆盖**

```
[root@zhang ~]# cp -fn /root/linux/1.txt /root/windown/
```

**移动文件**

**#mv 源文件 目标文件**

 

**文件重名**

**![2019010613525846.png](https://img-blog.csdnimg.cn/2019010613525846.png)**

 

 

**![20190106135739271.png](https://img-blog.csdnimg.cn/20190106135739271.png)**
