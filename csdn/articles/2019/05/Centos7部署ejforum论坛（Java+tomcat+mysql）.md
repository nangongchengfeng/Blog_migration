+++
author = "南宫乘风"
title = "Centos7部署ejforum论坛（Java+tomcat+mysql）"
date = "2019-05-14 23:48:18"
tags=[]
categories=['MySQL']
image = "post/4kdongman/37.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/90217162](https://blog.csdn.net/heian_99/article/details/90217162)

前面搭建Java环境和tomcat环境。

下面进行实战，搭建ejforum论坛

ejforum论坛源码：[https://www.lanzous.com/i45rcoh](https://www.lanzous.com/i45rcoh)

# [Centos7安装MySQL数据库](https://blog.csdn.net/heian_99/article/details/89326404)

# [Centos7安装JDK环境配置](https://blog.csdn.net/heian_99/article/details/90215703)

# [Centos7安装和配置Tomcat8](https://blog.csdn.net/heian_99/article/details/90216301)

ok，下面进行论坛搭建

前提：以上三个配置已经搭建完成。

（1）使用mysql创建数据库

```
mysql&gt; create database ejforum;
Query OK, 1 row affected (0.00 sec)

mysql&gt; show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| ejforum            |
| mysql              |
| performance_schema |
+--------------------+
4 rows in set (0.00 sec)

mysql&gt; GRANT all ON ejforum.* TO "ejforum"@"localhost" IDENTIFIED BY "ejforum";
Query OK, 0 rows affected (0.00 sec)

mysql&gt; flush privileges;
Query OK, 0 rows affected (0.00 sec)

```

![20190514230654545.png](https://img-blog.csdnimg.cn/20190514230654545.png)

 

（2）安装mysql连接器（驱动包）下载地址：[https://dev.mysql.com/downloads/connector/j/5.1.html](https://dev.mysql.com/downloads/connector/j/5.1.html)

![20190514232635203.png](https://img-blog.csdnimg.cn/20190514232635203.png)

 

```
[root@wei mysql-connector-java-5.1.47]# tar zxf mysql-connector-java-5.1.47.tar.gz  

[root@wei mysql-connector-java-5.1.47]# ls
build.xml  mysql-connector-java-5.1.47-bin.jar  README.txt
CHANGES    mysql-connector-java-5.1.47.jar      src
COPYING    README
[root@wei mysql-connector-java-5.1.47]# cp mysql-connector-java-5.1.47.jar /usr/local/tomcat/lib/

```

（3）解压ejforum压缩包，并拷贝到网站的目录

```
[root@wei ejforum-2.3]# rm -rf /usr/local/tomcat/webapps/ROOT/*

[root@wei ~]# unzip ejforum2.3.zip 

```

 

```

[root@wei ~]# cd ejforum-2.3/
[root@wei ejforum-2.3]# ls
ejforum  install
[root@wei ~]# cd ejforum
[root@wei ejforum-2.3]# cp -r * /usr/local/tomcat/webapps/ROOT/

```

（4）编辑WEB-INF文件，指定连接MYSQL数据库用户

```
[root@wei ejforum]# vim /usr/local/tomcat/webapps/ROOT/WEB-INF/conf/config.xml 
[root@wei conf]# pwd
/usr/local/tomcat/webapps/ROOT/WEB-INF/conf

```

```
    DB Connection Pool - Mysql
        &lt;database maxActive="10" maxIdle="10" minIdle="2" maxWait="10000" 
                          username="ejforum" password="ejforum" 
                          driverClassName="com.mysql.jdbc.Driver" 
                          url="jdbc:mysql://localhost:3306/ejforum?characterEncoding=gbk&amp;amp;autoReconnect=true&amp;amp;autoReconnectForPools=true&amp;amp;zeroDateTimeBehavior=convertToNull"
                          sqlAdapter="sql.MysqlAdapter"/&gt;


```

 

![20190514234222299.png](https://img-blog.csdnimg.cn/20190514234222299.png)

（5）重启tomcat服务

```
[root@wei conf]# /usr/local/tomcat/bin/shutdown.sh 
Using CATALINA_BASE:   /usr/local/tomcat
Using CATALINA_HOME:   /usr/local/tomcat
Using CATALINA_TMPDIR: /usr/local/tomcat/temp
Using JRE_HOME:        /usr/java/jdk-12.0.1
Using CLASSPATH:       /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar
NOTE: Picked up JDK_JAVA_OPTIONS:  --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED
[root@wei conf]# /usr/local/tomcat/bin/startup.sh 
Using CATALINA_BASE:   /usr/local/tomcat
Using CATALINA_HOME:   /usr/local/tomcat
Using CATALINA_TMPDIR: /usr/local/tomcat/temp
Using JRE_HOME:        /usr/java/jdk-12.0.1
Using CLASSPATH:       /usr/local/tomcat/bin/bootstrap.jar:/usr/local/tomcat/bin/tomcat-juli.jar
Tomcat started.
```

![20190514234408841.png](https://img-blog.csdnimg.cn/20190514234408841.png)
