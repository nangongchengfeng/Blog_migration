---
author: 南宫乘风
categories:
- Linux实战操作
date: 2019-10-10 12:21:17
description: 目录介绍楼主目标：前可撩妹，后可搞运维环境：软件：软件链接：安装前所有准备，上传软件到上的的目录下安装依赖软件和类库安装前的准备安装依赖软件和类库安装前的准备的依赖库的依赖库解压解压进入目录下进入目录。。。。。。。
image: http://image.ownit.top/4kdongman/08.jpg
tags:
- 技术记录
title: Centos7部署分布式文件存储(Fastdfs)
---

<!--more-->

![](http://image.ownit.top/csdn/20191010122208663.gif)

**目录**

 

[FastDFS介绍](#FastDFS%E4%BB%8B%E7%BB%8D)

[楼主目标：前可H5撩妹，后可Linux搞运维](#%E6%A5%BC%E4%B8%BB%E7%9B%AE%E6%A0%87%EF%BC%9A%E5%89%8D%E5%8F%AFH5%E6%92%A9%E5%A6%B9%EF%BC%8C%E5%90%8E%E5%8F%AFLinux%E6%90%9E%E8%BF%90%E7%BB%B4)

[环境：Centos7](#%E7%8E%AF%E5%A2%83%EF%BC%9ACentos7)

[软件：](#%E8%BD%AF%E4%BB%B6%EF%BC%9A)

[软件链接：](#%E8%BD%AF%E4%BB%B6%E9%93%BE%E6%8E%A5%EF%BC%9A)

[安装前所有准备，上传软件到Centos7上的/opt的目录下](#%E5%AE%89%E8%A3%85%E5%89%8D%E6%89%80%E6%9C%89%E5%87%86%E5%A4%87%EF%BC%8C%E4%B8%8A%E4%BC%A0%E8%BD%AF%E4%BB%B6%E5%88%B0Centos7%E4%B8%8A%E7%9A%84%2Fopt%E7%9A%84%E7%9B%AE%E5%BD%95%E4%B8%8B)

[安装依赖软件和类库\(安装前的准备\)](<#安装依赖软件和类库(安装前的准备)>)

[1  fdfs的依赖库](<#1  fdfs的依赖库>)

[A 解压Libfastcommon](<#A 解压Libfastcommon>)

[B 进入Libfastcommon目录下](<#B 进入Libfastcommon目录下>)

[C make编译](<#C make编译>)

[D make install 安装](<#D make install 安装>)

[E libfastcommon.so复制文件到/usr/lib/](<#E libfastcommon.so复制文件到/usr/lib/>)

[2 fastdfs软件\(tracker、storage\)](<#2 fastdfs软件(tracker、storage)>)

[A 新建目录mkdir /opt/fastdfs](<#A 新建目录mkdir /opt/fastdfs>)

[B 解压FastDFS\_v5.05.tar.gz](<#B 解压FastDFS_v5.05.tar.gz>)

[C 进入解压目录](<#C 进入解压目录>)

[D make编译](<#D make编译>)

[E make install 安装](<#E make install 安装>)

[F 进入conf配置目录将文件都拷贝到/etc/fdfs下cp  \*  /etc/fdfs/（安装时自动生成）](<#F 进入conf配置目录将文件都拷贝到/etc/fdfs下cp  *  /etc/fdfs/（安装时自动生成）>)

[G 进入/etc/fdfs/，配置tracker.conf](<#G 进入/etc/fdfs/，配置tracker.conf>)

[H storage的配置\(storage不需要安装，因为安装tracker时已经同时安装\)](<#H storage的配置(storage不需要安装，因为安装tracker时已经同时安装)>)

[3 配置tracker和storage的启动服务](<#3 配置tracker和storage的启动服务>)

[配置tracker启动服务](#%E9%85%8D%E7%BD%AEtracker%E5%90%AF%E5%8A%A8%E6%9C%8D%E5%8A%A1)

[配置storage启动服务](#%E9%85%8D%E7%BD%AEstorage%E5%90%AF%E5%8A%A8%E6%9C%8D%E5%8A%A1)

[将启动脚本加入linux服务](#%E5%B0%86%E5%90%AF%E5%8A%A8%E8%84%9A%E6%9C%AC%E5%8A%A0%E5%85%A5linux%E6%9C%8D%E5%8A%A1)

[​](#%E2%80%8B)

[启动服务](#%E5%90%AF%E5%8A%A8%E6%9C%8D%E5%8A%A1)

[检查服务启动状态](#%E6%A3%80%E6%9F%A5%E6%9C%8D%E5%8A%A1%E5%90%AF%E5%8A%A8%E7%8A%B6%E6%80%81)

[​](#%E2%80%8B)

[4 测试上传](<#4 测试上传>)

[修改/etc/fdfs/client.conf](#%E4%BF%AE%E6%94%B9%2Fetc%2Ffdfs%2Fclient.conf)

[                                    FastDFS整合nginx](<#                                    FastDFS整合nginx>)

[ 5 安装nginx整合插件fastdfs-nginx-module](#%C2%A05%C2%A0%E5%AE%89%E8%A3%85nginx%E6%95%B4%E5%90%88%E6%8F%92%E4%BB%B6fastdfs-nginx-module)

[A 解压FastDFS-nginx-module插件](<#A 解压FastDFS-nginx-module插件>)

[B 修改插件读取fdfs的目录（插件自己的配置文件）](<#B 修改插件读取fdfs的目录（插件自己的配置文件）>)

[C 将FastDFS-nginx-module插件整合fdfs的配置文件拷贝到fdfs的配置目录下\(整合fdfs的配置文件\)](<#C 将FastDFS-nginx-module插件整合fdfs的配置文件拷贝到fdfs的配置目录下(整合fdfs的配置文件)>)

[D 修改/etc/fdfs/mod\_fastdfs.conf配置文件](<#D 修改/etc/fdfs/mod_fastdfs.conf配置文件>)

[6 安装nginx](<#6 安装nginx>)

[创建nginx/client目录](#%E5%88%9B%E5%BB%BAnginx%2Fclient%E7%9B%AE%E5%BD%95)

[安装环境：](#%E5%AE%89%E8%A3%85%E7%8E%AF%E5%A2%83%EF%BC%9A)

[解压nginx](#%E8%A7%A3%E5%8E%8Bnginx)

[进入nginx目录 配置安装环境](<#进入nginx目录 配置安装环境>)

[配置成功](#%E9%85%8D%E7%BD%AE%E6%88%90%E5%8A%9F)

[编译](#%E7%BC%96%E8%AF%91)

[安装](#%E5%AE%89%E8%A3%85)

[编辑nginx.conf](#%E7%BC%96%E8%BE%91nginx.conf)

[启动nginx](#%E5%90%AF%E5%8A%A8nginx)

[设置开机启动](#%E8%AE%BE%E7%BD%AE%E5%BC%80%E6%9C%BA%E5%90%AF%E5%8A%A8)

[需要关闭防火墙](#%E9%9C%80%E8%A6%81%E5%85%B3%E9%97%AD%E9%98%B2%E7%81%AB%E5%A2%99)

[测试](#%E6%B5%8B%E8%AF%95)

[浏览器打开链接](#%E6%B5%8F%E8%A7%88%E5%99%A8%E6%89%93%E5%BC%80%E9%93%BE%E6%8E%A5)

[完美成功，OK了](#%E5%AE%8C%E7%BE%8E%E6%88%90%E5%8A%9F%EF%BC%8COK%E4%BA%86)

[楼主目标：前可H5撩妹，后可Linux搞运维](#%E6%A5%BC%E4%B8%BB%E7%9B%AE%E6%A0%87%EF%BC%9A%E5%89%8D%E5%8F%AFH5%E6%92%A9%E5%A6%B9%EF%BC%8C%E5%90%8E%E5%8F%AFLinux%E6%90%9E%E8%BF%90%E7%BB%B4)

---

# FastDFS介绍

FastDFS是一个开源的轻量级[分布式文件系统](https://baike.baidu.com/item/%E5%88%86%E5%B8%83%E5%BC%8F%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F/1250388)，它对文件进行管理，功能包括：文件存储、文件同步、文件访问（文件上传、文件下载）等，解决了大容量存储和负载均衡的问题。特别适合以文件为载体的在线服务，如相册网站、视频网站等等

# 楼主目标：前可H5撩妹，后可Linux搞运维

![](http://image.ownit.top/csdn/20191010122004230.gif)

OK，废话不多说开始部署

![](http://image.ownit.top/csdn/2019101012205732.gif)

## 环境：Centos7

## 软件：

         FastDFS\_v5.05.tar.gz

          fastdfs-nginx-module\_v1.16.tar.gz

         libfastcommonV1.0.7.tar.gz

         nginx-1.12.2.tar.gz

## 软件链接：

                        <https://www.lanzous.com/b0c1xw7hi>

## 安装前所有准备，上传软件到Centos7上的/opt的目录下

![](http://image.ownit.top/csdn/20191010112815711.png)

## 安装依赖软件和类库\(安装前的准备\)

```
yum install gcc-c++ -y
```

```
yum -y install zlib zlib-devel pcre pcre-devel gcc gcc-c++ openssl openssl-devel libevent libevent-devel perl unzip net-tools wget
```

```
yum install perl*
```

 

## 1  fdfs的依赖库

**Libfastcommon安装过程**

### **A 解压Libfastcommon**

```
tar -zxvf libfastcommon
```

### B 进入**Libfastcommon目录下**

```cpp
cd Libfastcommon
```

### C make编译

```
make
```

### D make install 安装

```
make install
```

### E libfastcommon.so复制文件到/usr/lib/

```
cp /usr/lib64/libfastcommon.so /usr/lib/
```

![](http://image.ownit.top/csdn/20191010113311486.png)

## 2 fastdfs软件\(tracker、storage\)

**配置tracker**

**配置storage**

**\(依赖于：Gcc、libevent、perl\)**

### A 新建目录mkdir /opt/fastdfs

```
mkdir /opt/fastdfs
```

### B 解压FastDFS\_v5.05.tar.gz

```
tar -zxvf FastDFS_v5.05.tar.gz
```

### C 进入解压目录

```
cd  FastDFS
```

### D make编译

```
 ./make.sh
```

### E make install 安装

```
./make.sh install
```

### F 进入conf配置目录将文件都拷贝到/etc/fdfs下cp  \*  /etc/fdfs/（安装时自动生成）

```
cd conf
cp  *  /etc/fdfs/
```

### G 进入/etc/fdfs/，配置tracker.conf

vim /etc/fdfs/tracker.conf ，设置软件数据和日志目录

![](http://image.ownit.top/csdn/20191010113936545.png)

### H storage的配置\(storage不需要安装，因为安装tracker时已经同时安装\)

vim /etc/fdfs/storage.conf

软件目录

![](http://image.ownit.top/csdn/20191010114000411.png)

Storage存储文件的目录（新建mkdir /opt/fastdfs/fdfs\_storage）

```
mkdir /opt/fastdfs/fdfs_storage
```

![](http://image.ownit.top/csdn/20191010114026869.png)

Storage的trackerip

![](http://image.ownit.top/csdn/20191010114046968.png)

## 3 配置tracker和storage的启动服务

### 配置tracker启动服务

**进入/etc/init.d启动脚本目录，默认fastdfs已经生成**

**![](http://image.ownit.top/csdn/2019101011411693.png)**

**Vi fdfs\_trackerd脚本文件**

![](http://image.ownit.top/csdn/20191010114133681.png)

![](http://image.ownit.top/csdn/20191010114142245.png)

**因为启动脚本还在安装目录下，所以我们新建/usr/local/fdfs目录，并且将启动脚本cp到该目录**

```
mkdir /usr/local/fdfs
```

**进入安装目录/opt/FastDFs**

```
cd /opt/FastDFs
cp restart.sh  /usr/local/fdfs/
cp stop.sh  /usr/local/fdfs/
```

### 配置storage启动服务

\(restart和stop脚本已经拷贝到/usr/local/fdfs下，所以storage只需要配置/etc/init.d/fdfs\_storage脚本就可以了\)

vim /etc/init.d/fdfs\_storage

![](http://image.ownit.top/csdn/2019101011443811.png)

![](http://image.ownit.top/csdn/20191010114443611.png)

### 将启动脚本加入linux服务

```
cd /etc/init.d/

chkconfig --add fdfs_trackerd 
chkconfig --add fdfs_storaged 
```

### ![](http://image.ownit.top/csdn/20191010114921821.png)

### 启动服务

```
service fdfs_trackerd start

 service fdfs_storaged start
```

![](http://image.ownit.top/csdn/20191010114915388.png)

### 检查服务启动状态

```
ps -ef |grep fdfs
```

## ![](http://image.ownit.top/csdn/20191010115124913.png)

## 4 测试上传

**FastDFS安装成功可通过/usr/bin/fdfs\_test测试上传、下载等操作。**

### 修改/etc/fdfs/client.conf

```
[root@localhost ~]# vim /etc/fdfs/client.conf


base_path=/opt/fastdfs
tracker_server=192.168.67.163:22122
```

 

![](http://image.ownit.top/csdn/20191010115221436.png)

比如将/root下的图片上传到FastDFS中：

```
/usr/bin/fdfs_test /etc/fdfs/client.conf upload preview.jpg 
```

![](http://image.ownit.top/csdn/20191010115644743.png)

对应的上传路径：

/opt/fastdfs/fdfs\_storage/data /00/00/wKhDo1qipbiAJC6iAAB1tayPlqs094\_big.jpg

![](http://image.ownit.top/csdn/20191010115809831.png)

##                                     **FastDFS整合nginx**

 

##  5 安装nginx整合插件fastdfs-nginx-module

### A 解压FastDFS-nginx-module插件

```
tar -zxvf fastdfs-nginx-module_v1.16.tar.gz 
```

### B 修改插件读取fdfs的目录（插件自己的配置文件）

Vi fastdfs-nginx-module/src/config

# **删除圈中里面的local，就上面两个就可以了**

![](http://image.ownit.top/csdn/20191010120246253.png)

### C 将FastDFS-nginx-module插件整合fdfs的配置文件拷贝到fdfs的配置目录下\(整合fdfs的配置文件\)

FastDFS-nginx-module/src下的mod\_fastdfs.conf拷贝至/etc/fdfs/下\(这里面是两个路径\)

```
cp /opt/fastdfs-nginx-module/src/mod_fastdfs.conf /etc/fdfs/
```

### D 修改/etc/fdfs/mod\_fastdfs.conf配置文件

软件安装目录

![](http://image.ownit.top/csdn/20191010120610455.png)

Tracker\_server地址

![](http://image.ownit.top/csdn/20191010120627188.png)

Web的url是否包含group的路径名

![](http://image.ownit.top/csdn/20191010120641476.png)

上传文件存储目录

![](http://image.ownit.top/csdn/20191010120653805.png)

 

## 6 安装nginx

### 创建nginx/client目录

```
 mkdir -p /var/temp/nginx/client
```

### 安装环境：

安装pcre库

yum \-y install pcre-devel

安装zlib库

yum install \-y zlib-devel

 

### 解压nginx

```
tar -zxvf nginx-1.12.2.tar.gz
```

### 进入nginx目录 配置安装环境

添加fastdfs-nginx-module模块

cd nginx-1.8.0

```
./configure \
--prefix=/usr/local/nginx \
--pid-path=/var/run/nginx/nginx.pid \
--lock-path=/var/lock/nginx.lock \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--with-http_gzip_static_module \
--http-client-body-temp-path=/var/temp/nginx/client \
--http-proxy-temp-path=/var/temp/nginx/proxy \
--http-fastcgi-temp-path=/var/temp/nginx/fastcgi \
--http-uwsgi-temp-path=/var/temp/nginx/uwsgi \
--http-scgi-temp-path=/var/temp/nginx/scgi \
--add-module=/opt/fastdfs-nginx-module/src
```

![](http://image.ownit.top/csdn/20191010121106744.png)

### 配置成功

![](http://image.ownit.top/csdn/20191010121136244.png)

### 编译

```
make
```

### 安装

```
make install
```

 

### 编辑nginx.conf

vim /usr/local/nginx/conf/nginx.conf

![](http://image.ownit.top/csdn/20191010121214375.png)

### 启动nginx

```
/usr/local/nginx/sbin/nginx
```

### 设置开机启动

 vim /etc/rc.d/rc.local

![](http://image.ownit.top/csdn/2019101012125111.png)

 

### 需要关闭防火墙

```
service iptables stop
```

永久关闭 chkconfig  iptables  off

## 测试

```
/usr/bin/fdfs_test /etc/fdfs/client.conf upload preview.jpg 
```

![](http://image.ownit.top/csdn/20191010121425114.png)

### 浏览器打开链接

![]()

## 完美成功，OK了

## 楼主目标：前可H5撩妹，后可Linux搞运维

![](http://image.ownit.top/csdn/20191010121801942.gif)