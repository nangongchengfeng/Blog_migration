+++
author = "南宫乘风"
title = "Minio--Mysql存储桶通知配置"
date = "2021-09-22 15:59:58"
tags=['mysql', '数据库']
categories=['Kubernetes']
image = "post/4kdongman/08.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/120416564](https://blog.csdn.net/heian_99/article/details/120416564)

**！！！中文社区中说的config.json的方式已经打算被废弃了，所以现在最好通过minio客户端的方式进行处理了**

· **在目标mysql创建数据库miniodb（要用默认字符集，不然会报错）**

· **在minio client的可执行目录下执行如下命令，查看是否已经存在配置**

```
mc --insecure admin config get minio notify_mysql
```

**添加Mysql通知配置**

```
 mc admin config set minio notify_mysql:mysql table="minio_log" dsn_string="minio:minio@tcp(192.168.1.200:3306)/minio"
```

步骤：先创建minio的数据库，编码默认一下，在执行这条命令，但是会报错。

发现报错，错误如下：

```
Error: Error 1071: Specified key was too long; max key length is 3072 bytes
```

解决办法：手动创建记录表就可以了

```
CREATE TABLE `minio_log` (
  `key_name` varchar(1000) DEFAULT NULL,
  `value` longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

关联event事件

```
 mc event add minio/k8s/ arn:minio:sqs::mysql:mysql

查看
mc event list minio/k8s/
```

 重启server服务，直接命令重启

```
 mc admin service restart minio/k8s/
```

![20210922155940242.png](https://img-blog.csdnimg.cn/20210922155940242.png)

 
