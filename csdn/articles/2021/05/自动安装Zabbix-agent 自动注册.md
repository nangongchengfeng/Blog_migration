+++
author = "南宫乘风"
title = "自动安装Zabbix-agent 自动注册"
date = "2021-05-22 15:52:23"
tags=['zabbix', 'centos', 'linux']
categories=['Zabbix监控']
image = "post/4kdongman/72.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/117151435](https://blog.csdn.net/heian_99/article/details/117151435)

## [博客](https://ownit.top/)：[https://ownit.top/](https://www.ownit.top/)

## Centos7脚本自动安装并注册zabbix服务端

此脚本可以自动安装zabbix客户端并且配置（注意修改）

```
#zabbix-agent4.0.4
#centos7系列安装zabbix监控
#获取影院IP
#ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"
#首先ip获取要测试一下，双ip，多ip都会有影响
localname=`hostname`
conf="/etc/init.d/zabbix-agent"


installzabbix(){

if [[ -f $conf ]]; then
		echo "zabbix_agentd already install"
	else
		/etc/init.d/zabbix_agentd stop
		rm   -rf     /etc/init.d/zabbix_agentd
		rm   -rf    /usr/local/zabbix  
		yum -y install  https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/4.2/rhel/7/x86_64/zabbix-agent-4.2.8-1.el7.x86_64.rpm
		#delconf
		sed   -i  '/^Server/d'      /etc/zabbix/zabbix_agentd.conf 
		sed   -i  '/^Hostname/d'      /etc/zabbix/zabbix_agentd.conf 
		sed   -i  '/^HostMetadata/d'      /etc/zabbix/zabbix_agentd.conf  
		#addconf
		echo "Server=10.10.10.1"  &gt;&gt; /etc/zabbix/zabbix_agentd.conf 
		echo "ServerActive=10.10.10.1"  &gt;&gt; /etc/zabbix/zabbix_agentd.conf 
		echo "HostMetadata=ownit"   &gt;&gt; /etc/zabbix/zabbix_agentd.conf 
		echo  Hostname=$localname   &gt;&gt; /etc/zabbix/zabbix_agentd.conf 

fi
}
installzabbix

average(){
#负载监控average
echo   "UserParameter=average[*],uptime|awk '{print \$NF}'"   &gt; /etc/zabbix/zabbix_agentd.d/average.conf 
}
average

restzabbix(){
chkconfig zabbix-agent on
systemctl restart zabbix-agent.service
}
restzabbix
```

## zabbix的基本配置文件

```
#zabbix-agent运行的pid
PidFile=/var/run/zabbix/zabbix_agentd.pid
#zabbix-aget运行的日志
LogFile=/var/log/zabbix/zabbix_agentd.log
#zabbix-agent运行的日志大小，当设置为0时，表示不进行日志轮询
LogFileSize=0
#zabbix-agent的目录路径或扩展配置文件路径
Include=/etc/zabbix/zabbix_agentd.d/*.conf
#zabbix server的ip地址，多个ip使用逗号分隔
Server=10.150.11.205,10.50.11.205
#zabbix 主动监控server的ip地址，使用逗号分隔多IP，如果注释这个选项，那么当前服务器的主动监控就被禁用了
ServerActive=10.150.11.205,10.50.11.205
#zabbix-agent的数据源，仅用于主机自动注册功能
HostMetadata=ownit
#zabbix-agent的主机名，必须唯一，区分大小写。Hostname必须和zabbix web上配置的一直，否则zabbix主动监控无法正常工作
Hostname=10.10.3.240
#zabbix-agent是否启用用户自定义监控脚本，1启用，0不启用
UnsafeUserParameters=1

```

## Zabbix服务端配置

 

![20210522155033431.png](https://img-blog.csdnimg.cn/20210522155033431.png)

![20210522155102362.png](https://img-blog.csdnimg.cn/20210522155102362.png)

![20210522155050260.png](https://img-blog.csdnimg.cn/20210522155050260.png)

![20210522155121670.png](https://img-blog.csdnimg.cn/20210522155121670.png)
