+++
author = "南宫乘风"
title = "Centos7升级Python3.7.3版本"
date = "2020-04-10 10:47:58"
tags=['linux', '服务器', 'centos', 'python', '升级']
categories=['Python学习']
image = "post/4kdongman/74.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/105428325](https://blog.csdn.net/heian_99/article/details/105428325)

**目录**

 

[前言：](#%E5%89%8D%E8%A8%80%EF%BC%9A)

[正文：](#%E6%AD%A3%E6%96%87%EF%BC%9A)

[1.下载Python3.7.3的镜像](#1.%E4%B8%8B%E8%BD%BDPython3.7.3%E7%9A%84%E9%95%9C%E5%83%8F)

[2、解压 tar -xzvf Python-3.7.3.tgz](#2%E3%80%81%E8%A7%A3%E5%8E%8B%20tar%20-xzvf%20Python-3.7.3.tgz)

[3、cd Python-3.7.3](#3%E3%80%81cd%20Python-3.7.3)

[4、安装到/usr/local目录中](#4%E3%80%81%E5%AE%89%E8%A3%85%E5%88%B0%2Fusr%2Flocal%E7%9B%AE%E5%BD%95%E4%B8%AD)

[5、make &amp;&amp; make altinstall](#5%E3%80%81make%20%26%26%20make%C2%A0altinstall)

[6、验证](#6%E3%80%81%E9%AA%8C%E8%AF%81)

[7、cd /usr/bin](#7%E3%80%81cd%20%2Fusr%2Fbin)

[8、备份之前的python ](#8%E3%80%81%E5%A4%87%E4%BB%BD%E4%B9%8B%E5%89%8D%E7%9A%84python%C2%A0)

[9、创建软连接 ](#9%E3%80%81%E5%88%9B%E5%BB%BA%E8%BD%AF%E8%BF%9E%E6%8E%A5%C2%A0)

[问题](#%E9%97%AE%E9%A2%98)

[1、更改yum脚本的python依赖](#1%E3%80%81%E6%9B%B4%E6%94%B9yum%E8%84%9A%E6%9C%AC%E7%9A%84python%E4%BE%9D%E8%B5%96)[​](#%E2%80%8B)

[2、修改urlgrabber配置文件](#2%E3%80%81%E4%BF%AE%E6%94%B9urlgrabber%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)

[备注：](#%E5%A4%87%E6%B3%A8%EF%BC%9A)

# 前言：

我们使用的centos7镜像，里面都内置的Python，但都是python2的版本，比较落后。

![20200410094932143.png](https://img-blog.csdnimg.cn/20200410094932143.png)

现在有的有Python3已经出来，有的程序运行需要Python3的环境支持。

**安装下面操作，能够正确安装和替换Python2，如果操作有问题请下方留言**

 

# 正文：

 

### 1.下载Python3.7.3的镜像

```
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
```

### 2、解压 tar -xzvf Python-3.7.3.tgz

```
tar -xzvf Python-3.7.3.tgz
```

### 3、cd Python-3.7.3

```
cd Python-3.7.3
```

![20200410095352308.png](https://img-blog.csdnimg.cn/20200410095352308.png)

### 4、安装到/usr/local目录中

```
 ./configure --prefix=/usr/local/python3
```

**执行这步后，会检测程序。等检测完毕，是否有报错或者依赖没安装。**

![20200410095527594.png](https://img-blog.csdnimg.cn/20200410095527594.png)

### 5、make &amp;&amp; make altinstall

```
make &amp;&amp; make altinstall
```

**执行这步后，会进行编译，然后安装程序到指定的目录**

### 6、验证

直接先运行python3，再确认一下版本信息：

![20200410103542694.png](https://img-blog.csdnimg.cn/20200410103542694.png)

### 7、cd /usr/bin

### 8、备份之前的python 

```
mv python python.bak
```

![2020041010390020.png](https://img-blog.csdnimg.cn/2020041010390020.png)

### 9、创建软连接 

```
ln -s /usr/local/python3/bin/python3.7 /usr/bin/python
```

![20200410104048542.png](https://img-blog.csdnimg.cn/20200410104048542.png)

![20200410104207453.png](https://img-blog.csdnimg.cn/20200410104207453.png)

# 问题

![20200410104254815.png](https://img-blog.csdnimg.cn/20200410104254815.png)

### 1、更改yum脚本的python依赖

```
vi /usr/bin/yum
```

**#!/usr/bin/python 改为 #!/usr/bin/python2**

![20200410104331995.png](https://img-blog.csdnimg.cn/20200410104331995.png)

### ![20200410104455768.png](https://img-blog.csdnimg.cn/20200410104455768.png)

### 2、修改urlgrabber配置文件

```
vi /usr/libexec/urlgrabber-ext-down
```

**#!/usr/bin/python 改为 #!/usr/bin/python2**

 

 

# **备注：**

1、3.6的依赖 没有执行 报错了 后续有需要再逐步加上这些依赖吧

```
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
```

2、3.7的依赖包（一定要在安装前先install 否则安装会报错）

```
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel libffi-devel

```

**测试**：输入python 查看最新的版本

![20200410104626467.png](https://img-blog.csdnimg.cn/20200410104626467.png)

 

已经完成，可以正常使用python3了
