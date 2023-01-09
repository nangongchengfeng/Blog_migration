+++
author = "南宫乘风"
title = "Mysql主从同步复制（快速构建，基于CP数据备份 恢复）"
date = "2022-05-13 11:43:10"
tags=['mysql', '数据库', 'database']
categories=['MySQL']
image = "post/4kdongman/69.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/124748299](https://blog.csdn.net/heian_99/article/details/124748299)

**目录**



[相关 ](#%E7%9B%B8%E5%85%B3%C2%A0)

[思路](#%E6%80%9D%E8%B7%AF)

[主库](#%E4%B8%BB%E5%BA%93)

[1、检查主库是否开启log-bin](#1%E3%80%81%E6%A3%80%E6%9F%A5%E4%B8%BB%E5%BA%93%E6%98%AF%E5%90%A6%E5%BC%80%E5%90%AFlog-bin)

[2、开启log-bin](#2%E3%80%81%E5%BC%80%E5%90%AFlog-bin)

[3、重启MySQL](#3%E3%80%81%E9%87%8D%E5%90%AFMySQL)

[4、检查生成的log-bin目录](#4%E3%80%81%E6%A3%80%E6%9F%A5%E7%94%9F%E6%88%90%E7%9A%84log-bin%E7%9B%AE%E5%BD%95)

[5、进入MySQL，锁表，记录POS号](#5%E3%80%81%E8%BF%9B%E5%85%A5MySQL%EF%BC%8C%E9%94%81%E8%A1%A8%EF%BC%8C%E8%AE%B0%E5%BD%95POS%E5%8F%B7)

[6、备份mysql文件，解表](#6%E3%80%81%E5%A4%87%E4%BB%BDmysql%E6%96%87%E4%BB%B6%EF%BC%8C%E8%A7%A3%E8%A1%A8)

[7、主库传输mysql文件到从库](#7%E3%80%81%E4%B8%BB%E5%BA%93%E4%BC%A0%E8%BE%93mysql%E6%96%87%E4%BB%B6%E5%88%B0%E4%BB%8E%E5%BA%93)

[8、添加iptables防火墙规则（ip为从库IP）](#8%E3%80%81%E6%B7%BB%E5%8A%A0iptables%E9%98%B2%E7%81%AB%E5%A2%99%E8%A7%84%E5%88%99%EF%BC%88ip%E4%B8%BA%E4%BB%8E%E5%BA%93IP%EF%BC%89)

[从库](#%E4%BB%8E%E5%BA%93)

[1、停止从库的业务程序](#1%E3%80%81%E5%81%9C%E6%AD%A2%E4%BB%8E%E5%BA%93%E7%9A%84%E4%B8%9A%E5%8A%A1%E7%A8%8B%E5%BA%8F)

[2、停止票务开机自启程序](#2%E3%80%81%E5%81%9C%E6%AD%A2%E7%A5%A8%E5%8A%A1%E5%BC%80%E6%9C%BA%E8%87%AA%E5%90%AF%E7%A8%8B%E5%BA%8F)

[3、检查主库是否开启log-bin](#3%E3%80%81%E6%A3%80%E6%9F%A5%E4%B8%BB%E5%BA%93%E6%98%AF%E5%90%A6%E5%BC%80%E5%90%AFlog-bin)

[4、开启log-bin，添加配置，修改id](#4%E3%80%81%E5%BC%80%E5%90%AFlog-bin%EF%BC%8C%E6%B7%BB%E5%8A%A0%E9%85%8D%E7%BD%AE%EF%BC%8C%E4%BF%AE%E6%94%B9id)

[4、停止mysql ，备份目录](#4%E3%80%81%E5%81%9C%E6%AD%A2mysql%20%EF%BC%8C%E5%A4%87%E4%BB%BD%E7%9B%AE%E5%BD%95)

[5、覆盖mysql目录，删除auto.cnf](#5%E3%80%81%E8%A6%86%E7%9B%96mysql%E7%9B%AE%E5%BD%95%EF%BC%8C%E5%88%A0%E9%99%A4auto.cnf)

[6、启动mysql](#6%E3%80%81%E5%90%AF%E5%8A%A8mysql)

[7、启动主从](#7%E3%80%81%E5%90%AF%E5%8A%A8%E4%B8%BB%E4%BB%8E)



# 相关 

相关原理可以查看此博客        

[https://blog.csdn.net/heian_99/article/details/106647572![icon-default.png](https://csdnimg.cn/release/blog_editor_html/release2.1.3/ckeditor/plugins/CsdnLink/icons/icon-default.png)http://xn--mysql-ni1h1kkd34cien8anzj00an2yqrx8k1a1u9c2j7e9svvilaaa](http://xn--mysql-ni1h1kkd34cien8anzj00an2yqrx8k1a1u9c2j7e9svvilaaa)

以下作为 实际操作

环境：

主库：    mysql

从库：        mysql

# 思路

（1）主库A数据全，数据库B空的

（2）锁表数据库A，记录pos号

（3）复制数据库A目录数据（进行cp备份）然后 解锁表

（4）把数据库A备份的数据进行scp 数据库B

（5）把数据库A的目录，进行覆盖数据库B的目录。（数据覆盖，相当于备份恢复）

（6）进行主共同步

**注意：日志格式 **statement  row mixed   建议使用 **mixed**

![20200609163414418.png](https://img-blog.csdnimg.cn/20200609163414418.png)



# 主库

## **1、检查主库是否开启log-bin**

```
[root@92-69-xy-bak ~]# cat /etc/my.cnf | grep log-bin
log-bin=/databak/mysql-bin/mysql-bin

```

## **2、开启log-bin**

如果上面没有显示，需要开启log-bin

```
开启
vim /etc/my.cnf
log-bin=/databak/mysql-bin/mysql-bin
创建目录，授权
mkdir  /databak/mysql-bin
chown  mysql.mysql  /databak/mysql-bin   -R

```

## 3、重启MySQL

重启mysql是因为刚开启log-bin日志，需要生成数据

```
service  mysql restart
```

## **4、检查生成的log-bin****目录**

```
目的：是否开启log-bin成功，是否生成日志数据
```

```
 ls /databak/mysql-bin/

生成的数据
mysql-bin.000001  mysql-bin.000002  mysql-bin.000003  mysql-bin.index

```

## 5、**进入MySQL，锁表，记录POS****号**

```
mysql -ucpms -pudqjHDMkxQfGP4iy
FLUSH TABLES WITH READ LOCK;
show master status;
echo  "日志名字    偏移量"   &gt;  /var/lib/mysql/记录文件

```

## 6、**备份mysql文件，解表**

```
cp  -r    /var/lib/mysql /opt/mysql_bak

UNLOCK TABLES;

```

## **7、主库传输mysql****文件到从库**

```
cd /opt
scp -r mysql_bak soft CMS3.10.21 192.168.0.3:/opt

```

## **8、添加iptables****防火墙规则（ip****为从库IP****）**

```
 vim /etc/sysconfig/iptables
-A INPUT -s 10.92.69.3 -p tcp --dport 3306 -j ACCEPT
/etc/init.d/iptables restart

```



**以上操作主库完成**

# 从库

## **1、停止从库的业务程序**

```
pkill java

```

## **2、停止票务开机自启程序**

```
chkconfig --list | grep cms |awk '{print "chkconfig",$1,"off"}'|bash
```

## 3、**检查主库是否开启log-bin**

```
[root@92-69-xy-bak ~]# cat /etc/my.cnf | grep log-bin
log-bin=/databak/mysql-bin/mysql-bin

```

## 4、**开启log-bin，添加配置，修改id**

如果上面没有显示，需要开启log-bin

```
开启
vim /etc/my.cnf
log-bin=/databak/mysql-bin/mysql-bin

server-id=2

replicate_ignore_table=CMS.QC_TEMP
replicate_ignore_table=CMS.QM_TEMP
replicate_ignore_table=CMS.STORE_IN_TEMP
replicate_ignore_table=CMS.TEMP_POS_SALE_GOODS_ITEM_COST
replicate_ignore_table=CMS.TEMP_POS_REJECT_GOODS_ITEM_COST
replicate_ignore_table=CMS.MER_INTERFACE_DAY_STORE_CHECK
slave-skip-errors = 1062


创建目录，授权
mkdir  /databak/mysql-bin
chown  mysql.mysql  /databak/mysql-bin   -R

```

## 4、**停止mysql ，备份目录**

```
service mysql stop

mv /var/lib/mysql /var/lib/bak_mysql

```

## 5、**覆盖mysql目录，删除auto.cnf**

```
cp -r /opt/mysql_bak /var/lib/mysql

\rm   /var/lib/mysql/auto.cnf

```

## **6、启动mysql**

```
service mysql start
```

## 7、**启动主从**

```
进入mysql
mysql -uroot -p^passswd
停止slave
stop  slave;
写入 配置信息（注意pos号，账号，主库ip 端口）
change master to
master_host='10.92.69.2',
master_port=3306,
master_user='admin',
master_password='udq5545adadefiy',
master_log_file='mysql-bin.000001',
master_log_pos=17503;
开启从库
start  slave;
查看状态
show slave status\G
两个yes为正常，检查pos号是否已经和主库同步

```

以上操作需谨慎，尤其主库上，输入命令需三思（文档仅供参考）
