---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2021-02-25 14:07:58
description: 数据库备份脚本按照时间来创建目录备份数据，需要配合每天早上凌晨点备份数据年月日期时间主机创建备份目录备份数据库生成文件删除超过天的文件，并删除目录压缩备份还原每月备份的数据会放到一个目录，十分乱，不容。。。。。。。
image: http://image.ownit.top/4kdongman/75.jpg
tags:
- mysql
- sql
- 数据库
title: Mysql数据库备份脚本
---

<!--more-->

**数据库备份脚本**

**按照时间来创建目录备份数据，需要配合crontab**

```bash
00 1 * * * root /etc/mysqldumpjumpser.sh
```

每天早上凌晨1点备份数据

```bash
#!/bin/bash
USER=jumpserver
PASS=jumpserver
DBDIR=/databak/Data_Backup
#DAY=`date  +%Y%m%d`
#年月
MONTH=`date +%Y%m`
#日期时间
DT=`date '+%Y%m%d%H%M'`
#主机ip
DBIP=`cat /etc/sysconfig/network-scripts/ifcfg-eth0 | grep IPADDR | awk -F '"' '{print $2}'`
#创建备份目录
mkdir -p $DBDIR/$DBIP/$MONTH
备份数据库
for  dbname in jumpserver
do
	mysqldump  -u$USER   -p$PASS -R    --single-transaction  $dbname 2>>$DBDIR/$DBIP/$MONTH/error-$DT.log   |gzip  > $DBDIR/$DBIP/$MONTH/$dbname-$DBIP-$DT.sql.gz
  	# 生成md5sum文件
 	md5sum $DBDIR/$DBIP/$MONTH/$dbname-$DBIP-$DT.sql.gz > $DBDIR/$DBIP/$MONTH/$dbname-$DBIP-$DT.sql.gz.MD5
done

# check and delete old datafile.
#删除超过30天的文件，并删除目录
del_backup_dir=/databak/Data_Backup/$DBIP
cd $del_backup_dir
if [ $? = 0 ]; then
        find ./ -type f -mtime +30 -exec rm -rf {} \; >/dev/null 2>&1
        find -depth -type d -empty -exec rmdir {} \;
fi

#压缩备份
#mysqldump -uroot -proot --databases abc 2>/dev/null |gzip >/abc.sql.gz
#还原
#gunzip -c abc.sql.gz |mysql -uroot -proot abc
```

![](http://image.ownit.top/csdn/20210306124931833.png)

每月备份的数据会放到一个目录，十分乱，不容易看，这边改进一下

没有多大的改变，就是加了DAY=\`date \-d '-1 days' +\%d\` ：显示上一天的日期，我们crontab是凌晨1点备份，也就是备份上一天的数据。

```bash
#!/bin/bash
USER=jumpserver
PASS=jumpserver
DBDIR=/databak/Data_Backup
DAY=`date -d '-1 days' +%d`
MONTH=`date +%Y%m`
DT=`date '+%Y%m%d%H%M'`
DBIP=`cat /etc/sysconfig/network-scripts/ifcfg-eth0 | grep IP | awk -F '"' '{print $2}'`



mkdir -p $DBDIR/$DBIP/$MONTH/$DAY
for  dbname in jumpserver
do
	mysqldump  -u$USER   -p$PASS -R    --single-transaction  $dbname 2>>$DBDIR/$DBIP/$MONTH/$DAY/error-$DT.log   |gzip  > $DBDIR/$DBIP/$MONTH/$DAY/$dbname-$DBIP-$DT.sql.gz
  	# 生成md5sum文件
 	md5sum $DBDIR/$DBIP/$MONTH/$DAY/$dbname-$DBIP-$DT.sql.gz > $DBDIR/$DBIP/$MONTH/$DAY/$dbname-$DBIP-$DT.sql.gz.MD5
done



# check and delete old datafile.
del_backup_dir=/databak/Data_Backup/$DBIP
cd $del_backup_dir
if [ $? = 0 ]; then
        find ./ -type f -mtime +30 -exec rm -rf {} \; >/dev/null 2>&1
        find -depth -type d -empty -exec rmdir {} \;
fi

#压缩备份
#mysqldump -uroot -proot --databases abc 2>/dev/null |gzip >/abc.sql.gz
#还原
#gunzip -c abc.sql.gz |mysql -uroot -proot abc
```

![](http://image.ownit.top/csdn/2021030612555155.png)

以日期目录分类，可以更方便的清楚