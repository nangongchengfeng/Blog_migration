+++
author = "南宫乘风"
title = "Linux创建高级用户并删除"
date = "2019-01-03 19:29:30"
tags=['linu']
categories=[' Linux基础']
image = "post/4kdongman/71.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/85711660](https://blog.csdn.net/heian_99/article/details/85711660)

**Linux创建高级用户并删除**

**常见window系统可以创建许多用户，但是linux也可以创建许多用户。**

**方法比window方便简单。**

**（1）添加一个普通用户 ：nangong（名字自己取）**

**![20190103184953829.png](https://img-blog.csdnimg.cn/20190103184953829.png)**

```
useradd nangong

```

**（2）设置用户nangong的密码**

**![2019010318542970.png](https://img-blog.csdnimg.cn/2019010318542970.png)**

 

```
 passwd nangong

```

**（3）在root权限下修改/etc/passwd 里的用户nangong的权限**

```
nangong:x:1000:1000::/home/nangong:/bin/bash

#把两个1000改为0就可以了
nangong:x:0:0::/home/nangong:/bin/bash

```

**![20190103185748386.png](https://img-blog.csdnimg.cn/20190103185748386.png)**

**![20190103190130253.png](https://img-blog.csdnimg.cn/20190103190130253.png)**

**（4）已经成功创建一个高级用户nangong**

**![20190103190411343.png](https://img-blog.csdnimg.cn/20190103190411343.png)**

**（a）删除一个用户，前提，那个用户没有在运行中，不然会提示下面的错误**

**![20190103190706617.png](https://img-blog.csdnimg.cn/20190103190706617.png)**

**解决方法：（1）切换到那个用户，然后连续按两次ctl+d，退出用户**

**                  （2）使用vipw命令 ，删除nangong那行，保存**

**![20190103192234370.png](https://img-blog.csdnimg.cn/20190103192234370.png)**

**                    （3）然后使用vipw -s 命令 ，删除nangong那行，保存**

**![20190103192413723.png](https://img-blog.csdnimg.cn/20190103192413723.png)**

 

**         **

 

**然后就行下来的步骤即可**

**（b）我们来到/home下，可以看到nangong这个用户**

```
cd /home
```

**![20190103191012120.png](https://img-blog.csdnimg.cn/20190103191012120.png)**

**(c)删除这个用户，但是命令不是rm**

**正确命令：**

```
 userdel -r nangong

```

**![20190103192650903.png](https://img-blog.csdnimg.cn/20190103192650903.png)**

**可以直接删除/home 的nangong**

**命令：**

```
rm -rf nangong

```

 
