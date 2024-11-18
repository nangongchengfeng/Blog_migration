---
author: 南宫乘风
categories:
- Nginx
date: 2019-12-04 18:05:19
description: 、什么是高可用需要两台服务器需要需要虚拟、配置高可用的准备工作需要两台服务器和在两台服务器安装在两台服务器安装、在两台服务器安装使用命令进行安安装之后，在里面生成目录，有文件、完成高可用配置主从配置修。。。。。。。
image: ../../title_pic/35.jpg
slug: '201912041805'
tags:
- 技术记录
title: Nginx 配置高可用的集群
---

<!--more-->

### **1、什么是 nginx 高可用**

![](../../image/20191204175854326.png)

![](../../image/20191204175949542.png)

- （1）需要两台 nginx 服务器
- （2）需要 keepalived
- （3）需要虚拟 ip 

### 2、配置高可用的准备工作

**（1）需要两台服务器 192.168.17.129 和 192.168.17.131**

**（2）在两台服务器安装 nginx**

**（3）在两台服务器安装 keepalived **

### 3、在两台服务器安装 keepalived 

**（1）使用 yum 命令进行安**

```
yum install keepalived –y 
```

![](../../image/20191204180053392.png)

**（2）安装之后，在 etc 里面生成目录 keepalived，有文件 keepalived.conf **

### 4、完成高可用配置（主从配置）

**（1）修改/etc/keepalived/keepalivec.conf 配置文件 **

```bash
global_defs { 
   notification_email { 
     acassen@firewall.loc 
     failover@firewall.loc 
     sysadmin@firewall.loc 
   } 
   notification_email_from Alexandre.Cassen@firewall.loc 
   smtp_server 192.168.17.129 
   smtp_connect_timeout 30 
   router_id LVS_DEVEL 
} 
  
vrrp_script chk_http_port { 
  
   script "/usr/local/src/nginx_check.sh" 
     interval 2      #（检测脚本执行的间隔） 
  
   weight 2 
  
} 
  
vrrp_instance VI_1 {     state BACKUP   # 备份服务器上将 MASTER 改为 BACKUP       interface ens33  //网卡     virtual_router_id 51   # 主、备机的 virtual_router_id 必须相同     priority 90     # 主、备机取不同的优先级，主机值较大，备份机值较小 
    advert_int 1 
  authentication { 
        auth_type PASS 
        auth_pass 1111 
    } 
    virtual_ipaddress {         192.168.17.50 // VRRP H 虚拟地址 
    } 
} 
```

**（2）在/usr/local/src 添加检测脚本**

```bash
#!/bin/bash
 A=`ps -C nginx –no-header |wc -l` 
 if [ $A -eq 0 ];then
	/usr/local/nginx/sbin/nginx     
	sleep 2     
	if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then
		killall keepalived     
	fi 
fi
```

**（3）把两台服务器上 nginx 和 keepalived 启动**

**启动 nginx：./nginx**

**启动 keepalived：systemctl start keepalived.service **

 

### 5、最终测试 

**（1）在浏览器地址栏输入 虚拟 ip 地址 192.168.17.50  **  
 ![](../../image/20191204180432921.png)

![](../../image/20191204180440295.png)

**（2）把主服务器（192.168.17.129）nginx 和 keepalived 停止，再输入 192.168.17.50 **

![](../../image/20191204180459653.png)

![](../../image/20191204180508602.png)

## 相关博文：

### [Nginx 简介与安装、常用的命令和配置文件](https://blog.csdn.net/heian_99/article/details/103264404)

## [nginx 配置实例-反向代理](https://blog.csdn.net/heian_99/article/details/103292763)

### [nginx 配置实例-负载均衡](https://blog.csdn.net/heian_99/article/details/103298249)

### [Nginx 配置实例-动静分离](https://blog.csdn.net/heian_99/article/details/103391378)

### [Nginx 配置高可用的集群](https://blog.csdn.net/heian_99/article/details/103391454)