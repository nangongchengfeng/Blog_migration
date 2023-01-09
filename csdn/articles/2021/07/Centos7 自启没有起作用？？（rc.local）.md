+++
author = "南宫乘风"
title = "Centos7 自启没有起作用？？（rc.local）"
date = "2021-07-26 16:39:52"
tags=['Linux', '自启']
categories=['错误问题解决']
image = "post/4kdongman/89.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/119112807](https://blog.csdn.net/heian_99/article/details/119112807)

今天机器重启，但是以前加的自启任务的脚本没有执行

**原因：**

在centos7中,/etc/rc.d/rc.local文件的权限被降低了,没有执行权限,需要给它添加可执行权限。

```
chmod +x /etc/rc.d/rc.local
```

<br> 然后就可以在里面添加你要开机自启的命令了

```
vi /etc/rc.d/rc.local
```

![20210726163905909.png](https://img-blog.csdnimg.cn/20210726163905909.png)
