+++
author = "南宫乘风"
title = "企业纯内网二进制完美部署Docker（20.10.7版本）"
date = "2021-08-03 21:43:26"
tags=['docker', 'docker-compose', 'Linux']
categories=['Docker']
image = "post/4kdongman/40.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/119359459](https://blog.csdn.net/heian_99/article/details/119359459)

**目录**

[企业纯内网二进制完美部署Docker（20.10.7版本）](#%E4%BC%81%E4%B8%9A%E7%BA%AF%E5%86%85%E7%BD%91%E4%BA%8C%E8%BF%9B%E5%88%B6%E5%AE%8C%E7%BE%8E%E9%83%A8%E7%BD%B2Docker%EF%BC%8820.10.7%E7%89%88%E6%9C%AC%EF%BC%89)

[Docker下载](#Docker%E4%B8%8B%E8%BD%BD)

[上传解压](#%E4%B8%8A%E4%BC%A0%E8%A7%A3%E5%8E%8B)

[systemd管理docker](#systemd%E7%AE%A1%E7%90%86docker)

[普通用户管理Docker](#%E6%99%AE%E9%80%9A%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86Docker)

[自定义网段](#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%BD%91%E6%AE%B5)

[更改存储路径](#%E6%9B%B4%E6%94%B9%E5%AD%98%E5%82%A8%E8%B7%AF%E5%BE%84)

[如果有数据](#%E5%A6%82%E6%9E%9C%E6%9C%89%E6%95%B0%E6%8D%AE)

[无数据](#%E6%97%A0%E6%95%B0%E6%8D%AE)

[启动并设置开机启动](#%E5%90%AF%E5%8A%A8%E5%B9%B6%E8%AE%BE%E7%BD%AE%E5%BC%80%E6%9C%BA%E5%90%AF%E5%8A%A8)

[docker命令补全方法](#articleContentId)

[1.复制文件](#1.%E5%A4%8D%E5%88%B6%E6%96%87%E4%BB%B6)

[2.安装bash-completion ](#2.%E5%AE%89%E8%A3%85bash-completion%C2%A0)

[ 3.刷新生效](#%C2%A03.%E5%88%B7%E6%96%B0%E7%94%9F%E6%95%88)

[4、测试](#4%E3%80%81%E6%B5%8B%E8%AF%95)

# 企业纯内网二进制完美部署Docker（20.10.7版本）



近期由于公司业务需求，需要使用到Docker。

平常有网环境，直接yum可以安装完成。但是由于服务器在纯内网环境，无法访问公网，所有无法在线直接安装Docker，需要另想方法完成部署安装。

（1）找一台有网机器，使用yum（yumdownloader）把docker包和依赖下载下来，上传在安装 

（2）二进制安装Docker（比较复杂，但是能更好理解和管理Docker，我选择后者）

## Docker下载

Docker版本：20.10.7

Docker版本下载地址：[https://download.docker.com/linux/static/stable/x86_64/](https://download.docker.com/linux/static/stable/x86_64/)

![20210803213054267.png](https://img-blog.csdnimg.cn/20210803213054267.png)



## 上传解压

```
tar zxvf docker-20.10.7.tgz
mv docker/* /usr/bin

```

## **systemd管理docker**

```
cat &gt; /usr/lib/systemd/system/docker.service &lt;&lt; EOF
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target
Requires=docker.socket 
[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always
StartLimitBurst=3
StartLimitInterval=60s
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TasksMax=infinity
Delegate=yes
KillMode=process
OOMScoreAdjust=-500
[Install]
WantedBy=multi-user.target
EOF

```

```
cat &gt; /usr/lib/systemd/system/docker.socket &lt;&lt; EOF
[Unit]
Description=Docker Socket for the API

[Socket]
ListenStream=/var/run/docker.sock
SocketMode=0660
SocketUser=root
SocketGroup=docker

[Install]
WantedBy=sockets.target


EOF

```

## 普通用户管理Docker

```
groupadd  docker 
#添加docker组，二进制不会自动添加的，yum会
usermod -a -G docker user1
#把要管理的用户添加到组里面就行
```

这样在docker组的用户，也有权限管理docker，这边是因为在docker.sock定义了以docker组启动

## 自定义网段

```
mkdir /etc/docker
cat &gt; /etc/docker/daemon.json &lt;&lt; EOF
{
    "bip":"10.10.10.1/24"

}
EOF

```

纯内网Docker-hub无法使用，这里就定义网段，启用初始就会直接定义网段

## 更改存储路径

docker的默认路径是/var/lib/docker

但是有时间这个空间很小，我们需要把目录迁移到足够大的磁盘下

### 如果有数据

```
systemctl stop docker
mkdir /data/service/docker -p
mv /var/lib/docker/* /data/service/docker/
#迁移数据
vim /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd  --graph /data/service/docker

```

### 无数据

```
mkdir /data/service/docker -p

vim /usr/lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd  --graph /data/service/docker
```

## **启动并设置开机启动**

```
systemctl daemon-reload
systemctl start docker
systemctl enable docker

```

## docker命令补全方法

### 1.复制文件

<br> 通过yum安装相同版本的docker。将 /usr/share/bash-completion/completions/docker 文件拷贝到二进制安装的docker服务器上的 /usr/share/bash-completion/completions/ 目录下

### 2.安装bash-completion 



```
yum install -y bash-completion
```

###  3.刷新生效

```
source /usr/share/bash-completion/completions/docker
source /usr/share/bash-completion/bash_completion
```



### 4、测试

```
[root@localhost ~]# docker 
attach     context    exec       import     logout     port       rm         service    system     version    
build      cp         export     info       logs       ps         rmi        stack      tag        volume     
builder    create     help       inspect    network    pull       run        start      top        wait       
commit     diff       history    kill       node       push       save       stats      trust      
config     engine     image      load       pause      rename     search     stop       unpause    
container  events     images     login      plugin     restart    secret     swarm      update

```


