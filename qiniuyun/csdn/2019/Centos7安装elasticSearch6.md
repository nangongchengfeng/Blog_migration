---
author: 南宫乘风
categories:
- 技术记录
date: 2019-10-31 13:26:55
description: 、：是一个基于的开源搜索引擎。无论在开源还是专有领域，可以被认为是迄今为止最先进、性能最好的、功能最全的搜索引擎库。特点：分布式的实时文件存储，每个字段都被索引并可被搜索分布式的实时分析搜索引擎做不规。。。。。。。
image: ../../title_pic/03.jpg
slug: '201910311326'
tags:
- 技术记录
title: Centos7安装elasticSearch6
---

<!--more-->

 

# Elasticsearch6.0

## 1、Elasticsearch：

Elasticsearch是一个基于[Apache Lucene\(TM\)](https://lucene.apache.org/core/)的开源搜索引擎。无论在开源还是专有领域，Lucene可以被认为是迄今为止最先进、性能最好的、功能最全的搜索引擎库。

**特点：**

1.  分布式的实时文件存储，每个字段都被索引并可被搜索
2.  分布式的实时分析搜索引擎\--做不规则查询
3.  可以扩展到上百台服务器，处理PB级结构化或非结构化数据

Elasticsearch也使用Java开发并使用Lucene作为其核心来实现所有索引和搜索的功能，但是它的目的是通过简单的RESTful API来隐藏Lucene的复杂性，从而让全文搜索变得简单。

ES能做什么？

全文检索（全部字段）、模糊查询（搜索）、数据分析（提供分析语法，例如聚合）

## 2、Elasticsearch使用案例

（1）2013年初，GitHub抛弃了Solr，采取ElasticSearch 来做PB级的搜索。 “GitHub使用ElasticSearch搜索20TB的数据，包括13亿文件和1300亿行代码”

（2）维基百科：启动以elasticsearch为基础的核心搜索架构SoundCloud：“SoundCloud使用ElasticSearch为1.8亿用户提供即时而精准的音乐搜索服务”

（3）百度：百度目前广泛使用ElasticSearch作为文本数据分析，采集百度所有服务器上的各类指标数据及用户自定义数据，通过对各种数据进行多维分析展示，辅助定位分析实例异常或业务层面异常。目前覆盖百度内部20多个业务线（包括casio、云分析、网盟、预测、文库、直达号、钱包、风控等），单集群最大100台机器，200个ES节点，每天导入30TB+数据

（4）新浪使用ES 分析处理32亿条实时日志

（5）阿里使用ES 构建挖财自己的日志采集和分析体系

## 3、同类产品

Solr、ElasticSearch、Hermes（腾讯）（实时检索分析）

1.  Solr、ES

1. 源自搜索引擎，侧重搜索与全文检索。

2. 数据规模从几百万到千万不等，数据量过亿的集群特别少。

有可能存在个别系统数据量过亿，但这并不是普遍现象（就像Oracle的表里的数据规模有可能超过Hive里一样，但需要小型机）。

1.  Hermes

1. 一个基于大索引技术的海量数据实时检索分析平台。侧重数据分析。

2. 数据规模从几亿到万亿不等。最小的表也是千万级别。

在 腾讯17 台TS5机器，就可以处理每天450亿的数据\(每条数据1kb左右\)，数据可以保存一个月之久。

1.  Solr、ES区别

全文检索、搜索、分析。基于lucene

1.  Solr 利用 Zookeeper 进行分布式管理，而 Elasticsearch 自身带有分布式协调管理功能;
2.  Solr 支持更多格式的数据，而 Elasticsearch 仅支持json文件格式；
3.  Solr 官方提供的功能更多，而 Elasticsearch 本身更注重于核心功能，高级功能多有第三方插件提供；
4.  Solr 在传统的搜索应用中表现好于 Elasticsearch，但在处理实时搜索应用时效率明显低于 Elasticsearch-----附近的人

Lucene是一个[开放源代码](https://baike.baidu.com/item/%E5%BC%80%E6%94%BE%E6%BA%90%E4%BB%A3%E7%A0%81/114160)的全文检索引擎工具包，但它不是一个完整的全文检索引擎，而是一个全文检索引擎的架构，提供了完整的查询引擎和索引引擎，部分[文本分析](https://baike.baidu.com/item/%E6%96%87%E6%9C%AC%E5%88%86%E6%9E%90/11046544)引擎

搜索引擎产品简介

## 1 搜索引擎

elasticSearch6（和elasticSearch5的区别在于，root用户权限、一个库能否建立多个表）

 软件链接：https://www.lanzous.com/i73b6pc

## 2 搜索引擎

![](../../image/20191031131720954.png)

文本搜索\(以空间换时间算法\)

于同类产品相比\(solr、hermes\),和solr一样都是基于lucene\(apache\)，默认以集群方式工作

 

搜索引擎\(以百度和goole为例\)的工作原理是什么？

a 爬虫

b 分析

c 查询

 

## 3 elasticSearch\(搜索引擎\)的算法

倒排索引\(在内容上建立索引，用内容去匹配索引\)

Btree（balance tree b-tree）

B+tree

![](../../image/20191031131745628.png)

 

 

 

## ![](../../image/20191031131755825.png)

 

## 4、Elasticsearch安装教程

### 1、准备工作

安装Centos7、建议内存2G以上、安装java1.8环境

### 2、设置IP地址（要有固定的IP）

![](../../image/2019103113141044.png)

### 3、Java环境安装

 1.     解压安装包

```bash
[root@localhost jdk1.8]# tar -zxvf jdk-8u171-linux-x64.tar.gz
```

2、在文件最后添加

```bash
export JAVA_HOME=/opt/es/jdk1.8.0_152
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/LIB:$JRE_HOME/LIB:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
```

![](../../image/20191031131609666.png)

 

3、查看java安装成功

![](../../image/20191031131643951.png)

### 4、配置文件

**elasticSearch.yml（集群配置文件）、jvm.Opitons\(jvm配置文件\)**

 

![](../../image/20191031131858380.png)

### 5、 创建目录 ，上传文件和解压

创建

```
mkdir -p /opt/es
```

 

 

上传

![](../../image/20191031132009311.png)

解压

```bash
tar -zxvf elasticsearch-6.3.1.tar.gz 
```

### 6、 配置

 

es使用最大线程数、最大内存数、访问的最大文件数

 

![](../../image/20191031132100145.png)

### 需要改成其他非用户启动

 

![](../../image/20191031132129272.png)

创建新用户

```
[root@wei bin]# adduser es
```

 

切换es用户下（成功）

```
[root@wei bin]# su es
[es@wei bin]$ 
```

### 7、启动

 

Es的权限问题：

首先用root用户解压

然后用root用户授权

**整个文件夹全部授权（R：表示循环授权）**

```
[root@wei es]# chmod 777 -R elasticsearch-6.3.1
```

**启动后配置**

**elasticSearch.yml、jvm.Opitons**

 

**es使用的jvm的内存大小**

 

 

 

![](../../image/20191031132345612.png)

**elasticSearch.yml中配置es的host地址\(配成本机地址，允许访问\)**

 

![](../../image/201910311323576.png)

**配置完毕启动es\(必须切换到非root用户下\)**

![](../../image/20191031132407722.png)

 

### **8、启动后会报错\(linux的默认线程数、最大文件数、最大内存数都不够\)**

 

![](../../image/20191031132431335.png)

### 9、 修改linux的配置\(配合es的启动需求\)

**两处修改**

**A修改linux的limits配置文件，设置内存线程和文件**

![](../../image/20191031132456546.png)

 

```
* hard nofile 655360
* soft nofile 131072
* hard nproc 4096
* soft nproc 2048
```

**B修改linux的sysctl配置文件，配置系统使用内存**

 

 

 

![](../../image/20191031132529900.png)

```
vm.max_map_count=655360
fs.file-max=655360
```

### 整个es的配置有四处文件需要修改

 

- **elasticSearch.yml es的启动host地址**
- **jvm.options配置es的虚拟机内存**
- **limits.conf配置linux的线程内存和文件**
- **sysctl.conf配置系统允许的软件运行内存**

 

### 10、成功访问

![](../../image/20191031132604889.png)