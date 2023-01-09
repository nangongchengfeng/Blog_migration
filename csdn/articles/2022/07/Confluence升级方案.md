+++
author = "南宫乘风"
title = "Confluence升级方案"
date = "2022-07-04 10:39:47"
tags=['java', '开发语言']
categories=['软件']
image = "post/4kdongman/10.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/125594954](https://blog.csdn.net/heian_99/article/details/125594954)

## Confluence目前版本

Confluence的授权信息<br> Confluence 6.9.3<br> 版权声明； 2003 - 2018 Atlassian 股份有限公司

![a77130ec53334b82a6a1c1daa7b39e90.png](https://img-blog.csdnimg.cn/a77130ec53334b82a6a1c1daa7b39e90.png)

##  Confluence最新版本

Confluence 7.13.7<br> 地址：https://www.atlassian.com/zh/software/confluence/download-archives

![68dfe15137984fb6919eb252ada6a638.png](https://img-blog.csdnimg.cn/68dfe15137984fb6919eb252ada6a638.png)

## 升级版本选择

原  Confluence 6.9.3 地址下载：https://product-downloads.atlassian.com/software/confluence/do<br> wnloads/atlassian-confluence-6.9.3-x64.bin

新  Confluence 7.13.7 地址下载：https://product-downloads.atlassian.com/software/confluence/d<br> ownloads/atlassian-confluence-7.13.7-x64.bin

## 数据备份

生产环境：127.0.0.1<br> 程序目录：/opt/atlassian<br> 数据目录：/var/atlassian<br> 数据库：mysql 5.6

![c3e593a2fa1844dba095cafa16c1fb9e.png](https://img-blog.csdnimg.cn/c3e593a2fa1844dba095cafa16c1fb9e.png)

##  mysql数据备份

```
cd /opt/mysql_backup
mysqldump -uroot -hlocalhost -p confluence &gt; confluence-20220616.sql
scp confluence-20220616.sql 目标机器
```

## 数据还原

注意：数据库必须使用root 才行，不然会报 数据库触发器失败的错误（错误如下图）

## ![3a382943611e4e21926f0c177656203d.png](https://img-blog.csdnimg.cn/3a382943611e4e21926f0c177656203d.png)

```
[root@localhost ~]# mysql -u root -p
mysql&gt; CREATE DATABASE IF NOT EXISTS confluence DEFAULT CHARSET utf8 COLLATE 
utf8_general_ci;
mysql&gt; use confluence;
mysql&gt; source /root/confluence-20220616.sql;    #注意，这里需要写入confluence.sql的
绝对路径
```

 修改Confluence配置文件中数据库连接为新数据库

```
vi /var/atlassian/application-data/confluence/confluence.cfg.xml
```

## ![c40d4c67d99b4292af43791a18047cfb.png](https://img-blog.csdnimg.cn/c40d4c67d99b4292af43791a18047cfb.png)

##  启动Conflucence

```
授权
chown -R confluence:confluence /opt/atlassian
chown -R confluence:confluence /var/atlassian
切换用户启动
su confluence
/opt/atlassian/confluence/bin/startup.sh
```

## ![9ad51aae5d104ef7ad5689ea73b5df0b.png](https://img-blog.csdnimg.cn/9ad51aae5d104ef7ad5689ea73b5df0b.png)

##  版本更新（ 7.13.7）

```
开始升级
[root@prometheus-server confluence]# ls
atlassian-confluence-6.9.3-x64.bin  atlassian-confluence-7.13.7-x64.bin
[root@prometheus-server confluence]# ./atlassian-confluence-7.13.7-x64.bin 
```

## ![a7046acedd7e4231980bd3a3820c7816.png](https://img-blog.csdnimg.cn/a7046acedd7e4231980bd3a3820c7816.png)

 ![76b402923ebe4d7eab63bf4105c3c460.png](https://img-blog.csdnimg.cn/76b402923ebe4d7eab63bf4105c3c460.png)

##  访问页面（key失效）

## ![1d9b2a8d8dd24fd9b67b25da6e53d7ee.png](https://img-blog.csdnimg.cn/1d9b2a8d8dd24fd9b67b25da6e53d7ee.png)

## 进行破解恢复 

 注意：数据库必须使用root 才行，不然会报 数据库触发器失败的错误

```
vim confluence.cfg.xml
查询新的server.id
    &lt;property name="confluence.setup.server.id"&gt;BJ5V-W7UB-4PO5-2J39&lt;/property&gt;
```

![0b3fa80d06d74f099a3790f6dacfa550.png](https://img-blog.csdnimg.cn/0b3fa80d06d74f099a3790f6dacfa550.png)

##  备份jar包破解

```
sz /opt/atlassian/confluence/confluence/WEB-INF/lib/atlassian-extras-decoder-v2-
3.4.1.jar
```

![da890dcdc2144adba0b8b047ea247c15.png](https://img-blog.csdnimg.cn/da890dcdc2144adba0b8b047ea247c15.png)

 ![1474799696ed4e75946f2c27de0cf13d.png](https://img-blog.csdnimg.cn/1474799696ed4e75946f2c27de0cf13d.png)

破解完成的包 上传到其相应目录  进行重启 

![b53d045039404c778387807ee26c313e.png](https://img-blog.csdnimg.cn/b53d045039404c778387807ee26c313e.png)

```
[root@prometheus-server ~]# mv atlassian-extras-decoder-v2-3.4.1.jar  
/opt/atlassian/confluence/confluence/WEB-INF/lib/
mv: overwrite ‘/opt/atlassian/confluence/confluence/WEB-INF/lib/atlassian-extras-decoder-v2-3.4.1.jar’? y
```

 ![d984601444fa41b2829c9a693eefc894.png](https://img-blog.csdnimg.cn/d984601444fa41b2829c9a693eefc894.png)

##  成功测试

新版测试地址（http://127.0.0.1:8090/） 账号和密码 原有的即可登陆

![a5ffbafb766f43b8a2b1d83af24ef043.png](https://img-blog.csdnimg.cn/a5ffbafb766f43b8a2b1d83af24ef043.png)

 
