+++
author = "南宫乘风"
title = "ESXI6.5安装CentOS7教程"
date = "2020-03-16 09:59:18"
tags=['esxi', 'centos7', 'Linux']
categories=[' Linux实战操作']
image = "post/4kdongman/99.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104892517](https://blog.csdn.net/heian_99/article/details/104892517)

VMware三个版本

workstation： 单机级，用在个人桌面系统中，需要操作系统支持

servier：工作组级，用于服务器，需要操作系统支持

esxi：企业级，用于服务器，不需要操作系统支持

Exsi 是一款虚拟化系统，与VMware，VirtualBox不同，它不需要安装在其他操作系统上，直接运行在裸机上；占用系统资源很小，易于管理，所以被大多数中小型公司所使用；

<img alt="" src="https://img-blog.csdn.net/20180803092244598?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1NDI4MjAx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70">

### 安装图解：

镜像已上传到服务器，CentOS7镜像包

![20200316094044629.png](https://img-blog.csdnimg.cn/20200316094044629.png)

新建虚拟机

![20200316094121259.png](https://img-blog.csdnimg.cn/20200316094121259.png)

![2020031609421728.png](https://img-blog.csdnimg.cn/2020031609421728.png)

选择存储

![20200316094300587.png](https://img-blog.csdnimg.cn/20200316094300587.png)

自定义设置

![20200316094537426.png](https://img-blog.csdnimg.cn/20200316094537426.png)

![20200316094607941.png](https://img-blog.csdnimg.cn/20200316094607941.png)

如果配置不够，可进行修改

![20200316094645722.png](https://img-blog.csdnimg.cn/20200316094645722.png)

将镜像加载到新建的虚拟机里，CD/DVD驱动器选择数据存储ISO文件

![20200316094723876.png](https://img-blog.csdnimg.cn/20200316094723876.png)

![20200316094747276.png](https://img-blog.csdnimg.cn/20200316094747276.png)

现在开始运行，首先打开电源,打开控制台

![20200316094819324.png](https://img-blog.csdnimg.cn/20200316094819324.png)

![2020031609501224.png](https://img-blog.csdnimg.cn/2020031609501224.png)

下面步骤就可安装Centos7一样了。

选择自己需求的东西就行，然后开始安装。
