---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-02 19:39:29
description: 服务控制脚本：安装编写控制的脚本服务启动服务服务使用：使用：演示：服务使用：服务服务启动。。。。。。。
image: http://image.ownit.top/4kdongman/29.jpg
tags:
- linux
title: Linux shell 函数应用示例02
---

<!--more-->

# nginx服务控制脚本：

## 安装ngix

```
[root@wei function]# yum install gcc pcre-devel openssl-devel

[root@wei function]# tar xf nginx-1.14.2.tar.gz 
[root@wei function]# cd nginx-1.14.2
[root@wei nginx-1.14.2]# ./configure --prefix=/usr/local/nginx
[root@wei nginx-1.14.2]# make && make instal

```

#   
编写控制nginx的脚本

```
#!/bin/bash
#

nginx_cmd=/usr/local/nginx/sbin/nginx
nginx_conf=/usr/local/nginx/conf/nginx.conf
nginx_pid_file=/usr/local/nginx/logs/nginx.pid
start(){
    $nginx_cmd
    if [ $? -eq 0 ];then
        echo "服务nginx启动.....[ok]"
    fi
}

stop(){
    $nginx_cmd -s stop
    

}

reload(){
    if $nginx_cmd -t &> /dev/null;then
        $nginx_cmd -s reload
    else
        $nginx_cmd -t
    fi

}

status(){
    if [ -e $nginx_pid_file  ];then
        echo "服务nginx(`cat $nginx_pid_file`) is running"
    else
        echo "服务nginx is stopped"
    fi
}


if [ -z $1 ];then
    echo "使用：$0{start|stop|restart|reload|status}"
    exit 9
fi

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    reload)
        reload
        ;;
    *)
        echo "使用：$0{start|stop|restart|reload|status}"
        exit 9
        ;;
esac
```

## 演示：

```
[root@wei init.d]# /etc/init.d/nginx status
服务nginx(4974) is running
[root@wei init.d]# /etc/init.d/nginx statscdsdc
使用：/etc/init.d/nginx{start|stop|restart|reload|status}
[root@wei init.d]# /etc/init.d/nginx stop
[root@wei init.d]# /etc/init.d/nginx status
服务nginx is stopped
[root@wei init.d]# /etc/init.d/nginx start
服务nginx启动.....[ok]
```