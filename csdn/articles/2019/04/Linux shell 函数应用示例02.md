+++
author = "南宫乘风"
title = "Linux shell 函数应用示例02"
date = "2019-04-02 19:39:29"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/71.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88979279](https://blog.csdn.net/heian_99/article/details/88979279)

# nginx服务控制脚本：

## 安装ngix

```
[root@wei function]# yum install gcc pcre-devel openssl-devel

[root@wei function]# tar xf nginx-1.14.2.tar.gz 
[root@wei function]# cd nginx-1.14.2
[root@wei nginx-1.14.2]# ./configure --prefix=/usr/local/nginx
[root@wei nginx-1.14.2]# make &amp;&amp; make instal


```

# <br>编写控制nginx的脚本

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
    if $nginx_cmd -t &amp;&gt; /dev/null;then
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

 
