+++
author = "南宫乘风"
title = "MySQL数据物理备份之tar打包备份"
date = "2019-04-21 22:28:12"
tags=[]
categories=['MySQL']
image = "post/4kdongman/32.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/89441218](https://blog.csdn.net/heian_99/article/details/89441218)

复制数据文件方式，可以使用cp或tar<br><br> 1、停止服务

```
[root@localhost mysql]# systemctl stop mysqld
[root@localhost mysql]# netstat -lnupt | grep 3306

```

<br> 2、备份数据文件

```
cd /var/lib/mysql
[root@localhost mysql]# mkdir -p /server/backup
[root@localhost mysql]#tar czf /server/backup/all.`date +%F`.tar.gz *
```

<br><br> 3、将备份文件拷贝到目标服务器

```
scp /server/backup/all.`date +%F`.tar.gz 192.168.95.12:/tmp
```

<br><br> 4、目标服务器停止服务

```
# systemctl stop mysqld
```

<br><br> 5、解压文件至目标服务器数据文件夹

```
# tar xf /tmp/all.tar.gz -C /usr/local/mysql/data
```

<br> 修改权限

```
# chown -R mysql.mysql /usr/local/mysql/data

```

<br> 6、目标服务器启动服务测试

```
# systemctl start mysqld
```

<br>  
