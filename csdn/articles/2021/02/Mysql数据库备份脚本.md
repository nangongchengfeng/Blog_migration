+++
author = "南宫乘风"
title = "Mysql数据库备份脚本"
date = "2021-02-25 14:07:58"
tags=['mysql', 'sql', '数据库']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/69.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/114079900](https://blog.csdn.net/heian_99/article/details/114079900)

**数据库备份脚本**

**按照时间来创建目录备份数据，需要配合crontab**

```
00 1 * * * root /etc/mysqldumpjumpser.sh
```

每天早上凌晨1点备份数据

```
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
	mysqldump  -u$USER   -p$PASS -R    --single-transaction  $dbname 2&gt;&gt;$DBDIR/$DBIP/$MONTH/error-$DT.log   |gzip  &gt; $DBDIR/$DBIP/$MONTH/$dbname-$DBIP-$DT.sql.gz
  	# 生成md5sum文件
 	md5sum $DBDIR/$DBIP/$MONTH/$dbname-$DBIP-$DT.sql.gz &gt; $DBDIR/$DBIP/$MONTH/$dbname-$DBIP-$DT.sql.gz.MD5
done

# check and delete old datafile.
#删除超过30天的文件，并删除目录
del_backup_dir=/databak/Data_Backup/$DBIP
cd $del_backup_dir
if [ $? = 0 ]; then
        find ./ -type f -mtime +30 -exec rm -rf {} \; &gt;/dev/null 2&gt;&amp;1
        find -depth -type d -empty -exec rmdir {} \;
fi

#压缩备份
#mysqldump -uroot -proot --databases abc 2&gt;/dev/null |gzip &gt;/abc.sql.gz
#还原
#gunzip -c abc.sql.gz |mysql -uroot -proot abc
```

![20210306124931833.png](https://img-blog.csdnimg.cn/20210306124931833.png)

每月备份的数据会放到一个目录，十分乱，不容易看，这边改进一下

没有多大的改变，就是加了DAY=`date -d '-1 days' +%d` ：显示上一天的日期，我们crontab是凌晨1点备份，也就是备份上一天的数据。

```
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
	mysqldump  -u$USER   -p$PASS -R    --single-transaction  $dbname 2&gt;&gt;$DBDIR/$DBIP/$MONTH/$DAY/error-$DT.log   |gzip  &gt; $DBDIR/$DBIP/$MONTH/$DAY/$dbname-$DBIP-$DT.sql.gz
  	# 生成md5sum文件
 	md5sum $DBDIR/$DBIP/$MONTH/$DAY/$dbname-$DBIP-$DT.sql.gz &gt; $DBDIR/$DBIP/$MONTH/$DAY/$dbname-$DBIP-$DT.sql.gz.MD5
done



# check and delete old datafile.
del_backup_dir=/databak/Data_Backup/$DBIP
cd $del_backup_dir
if [ $? = 0 ]; then
        find ./ -type f -mtime +30 -exec rm -rf {} \; &gt;/dev/null 2&gt;&amp;1
        find -depth -type d -empty -exec rmdir {} \;
fi

#压缩备份
#mysqldump -uroot -proot --databases abc 2&gt;/dev/null |gzip &gt;/abc.sql.gz
#还原
#gunzip -c abc.sql.gz |mysql -uroot -proot abc
```

![2021030612555155.png](https://img-blog.csdnimg.cn/2021030612555155.png)

以日期目录分类，可以更方便的清楚

 
