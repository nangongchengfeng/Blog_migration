+++
author = "南宫乘风"
title = "kibana和中文分词器analysis-ik的安装使用"
date = "2019-11-26 09:48:45"
tags=[]
categories=[' Linux实战操作']
image = "post/4kdongman/34.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103250453](https://blog.csdn.net/heian_99/article/details/103250453)

## [Centos7安装elasticSearch6](https://blog.csdn.net/heian_99/article/details/102835825)

**上面讲述了elasticSearch6的安装和使用教程。**

**下面讲一下elasticsearch6的管理工具Kibana。**

**Kibana是一个开源的分析和可视化平台，设计用于和Elasticsearch一起工作。**

**你用Kibana来搜索，查看，并和存储在Elasticsearch索引中的数据进行交互。**

**你可以轻松地执行高级数据分析，并且以各种图标、表格和地图的形式可视化数据。**

**Kibana使得理解大量数据变得很容易。它简单的、基于浏览器的界面使你能够快速创建和共享动态仪表板，实时显示Elasticsearch查询的变化**

## Kibana安装教程

### 1、拷贝kibana-5.6.4-linux-x86_64.tar 到/opt下

### 2、解压缩

### 3、进入kibana主目录的config目录下

![20191126094059392.png](https://img-blog.csdnimg.cn/20191126094059392.png)

### 4、修改配置文件

```
vim  kibana.yml
```

![20191126094152322.png](https://img-blog.csdnimg.cn/20191126094152322.png)

### 5、启动，在 kibana主目录bin目录下执行

```
nohup  ./kibana  &amp;
```

### 6、然后ctrl+c退出

**执行ps -ef **

**![20191126094246102.png](https://img-blog.csdnimg.cn/20191126094246102.png)**

**如上图,1757号进程就是kibana的进程**

### 7、用浏览器打开

![20191126094331706.png](https://img-blog.csdnimg.cn/20191126094331706.png)

点击左边菜单DevTools

在Console中

执行 get _cluster/health   

右边的结果中，status为yellow或者green。

表示es启动正常，并且与kibana连接正常。

 

## analysis-ik安装教程【简单】

### 1、上传文件到服务器

### 2、解压

### 3、移动到ElasticSearch6下的plugins

### 4、重新启动就可以了

![20191126094814987.png](https://img-blog.csdnimg.cn/20191126094814987.png)

 
