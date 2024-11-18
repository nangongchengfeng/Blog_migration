---
author: 南宫乘风
categories:
- MySQL
date: 2021-01-18 19:52:48
description: 目录安装与安装与环境条件环境条件创建主从配置文件创建主从配置文件创建文件创建文件启动容器启动容器销毁两个容器销毁两个容器重建容器重建容器经常拉去数据库做测试，还需要主从，每次环境还要还原，经常重复比较。。。。。。。
image: http://image.ownit.top/4kdongman/75.jpg
tags:
- Docker
- 数据库
- mysql
- docker
- centos
- linux
title: MySQL容器部署及数据持久化（主从复制）
---

<!--more-->

**目录**

[1\. 安装docker与docker-compose](<#1. 安装docker与docker-compose>)

[2\. 环境条件](<#2. 环境条件>)

[3\. 创建主从配置文件](<#3. 创建主从配置文件>)

[4\. 创建docker-compose.yml文件](<#4. 创建docker-compose.yml文件>)

[5\. docker-compose启动mysql容器](<#5. docker-compose启动mysql容器>)

[6\. 销毁两个容器](<#6. 销毁两个容器>)

[7\. 重建MySQL容器](<#7. 重建MySQL容器>)

---

经常拉去数据库做测试，还需要主从，每次环境还要还原，经常重复比较麻烦。

现在采用docker和docker-compose一键构建集成环境，方便测试。

## 1\. 安装docker与docker-compose

```bash
# 卸载老版本docker
[root@docker ~]# yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

[root@docker ~]# yum -y install epel-release wget
[root@docker ~]# wget -O /etc/yum.repos.d/docker-ce.repo https://mirrors.ustc.edu.cn/docker-ce/linux/centos/docker-ce.repo
[root@docker ~]# sed -i 's#download.docker.com#mirrors.tuna.tsinghua.edu.cn/docker-ce#g' /etc/yum.repos.d/docker-ce.repo
[root@docker ~]# yum -y install docker-ce

# 启动并配置镜像加速
[root@docker ~]# systemctl start docker.service && systemctl enable docker.service

[root@docker ~]# cat /etc/docker/daemon.json
{
  "registry-mirrors": ["https://99dxqyb6.mirror.aliyuncs.com"]
}


[root@docker ~]# systemctl restart docker.service
```

 -    安装docker-compose

```bash
[root@docker ~]# curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
[root@docker ~]# chmod +x /usr/local/bin/docker-compose
[root@docker ~]# ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

## 2\. 环境条件

```bash
[root@docker ~]# docker pull mysql:5.7 

[root@Master new_date]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
docker.io/mysql     5.7                 cc8775c0fe94        6 days ago          449 MB


[root@docker ~]# mkdir -p /data/mysql/master/{conf,data}
[root@docker ~]# mkdir -p /data/mysql/slave/conf
[root@docker ~]# mkdir -p /data/mysql/{init-db-m,init-db-s}
[root@docker ~]# chown -R mysql.mysql /data/mysql

# 主库的创建用户SQL脚本
[root@docker ~]# cat /data/mysql/init-db-m/create_user_1.sql
grant all on *.* to 'dumpuser'@'%' identified by '123456';
grant replication slave on *.* to 'repl'@'%' identified by '123456';

# 从库远程备份主库及创建主从通道Bash脚本
[root@docker ~]# cat /data/mysql/init-db-s/dump-repl_1.sh
#!/bin/bash
while ! mysql -uping -p123456 -hmysql_m_compose -P3306 -e "select 1"
do
    sleep 1
done
sleep 3
    mysqldump -udumpuser -p123456 -hmysql_m_compose -P3306 --single-transaction --default-character-set=utf8mb4 --set-gtid-purged=on --master-data=2 --flush-logs --hex-blob --triggers --routines --events --all-databases > /tmp/full.sql
    mysql -uroot -p123456 -e "reset master;"
    mysql -uroot -p123456 -e "source /tmp/full.sql;"
    mysql -uroot -p123456 -e "CHANGE MASTER TO MASTER_HOST='mysql_m_compose',MASTER_USER='repl',MASTER_PASSWORD='123456',MASTER_PORT=3306,MASTER_CONNECT_RETRY=10,MASTER_AUTO_POSITION=1;"
    mysql -uroot -p123456 -e "start slave;"
```

## 3\. 创建主从配置文件

```bash
# mysql_m_compose节点
[root@docker ~]# cat /data/mysql/master/conf/my.cnf
[mysqld]
server_id = 33060000
port = 3306
log_timestamps=SYSTEM
max_allowed_packet = 16M
read_only = 0
character_set_server = utf8mb4
secure_file_priv = ""
max_connect_errors = 100000
interactive_timeout = 1800
wait_timeout = 1800

# BINLOG
log_bin = mysql-bin
binlog_format = row
log_slave_updates = 1
max_binlog_size = 200M
relay_log = relay-bin
sync_binlog = 1

# GTID
gtid_mode = ON
enforce_gtid_consistency = 1
binlog_gtid_simple_recovery = 1

# ENGINE
default_storage_engine = InnoDB
innodb_flush_log_at_trx_commit=1

# ----------------------------------------------------------------------------------------------------------------------

# mysql_s_compose节点
[root@docker ~]# cat /data/mysql/slave/conf/my.cnf
[mysqld]
server_id = 33060001
port = 3306
log_timestamps=SYSTEM
max_allowed_packet = 16M
read_only = 0
character_set_server = utf8mb4
secure_file_priv = ""
max_connect_errors = 100000
interactive_timeout = 1800
wait_timeout = 1800

# BINLOG
log_bin = mysql-bin
binlog_format = row
log_slave_updates = 1
max_binlog_size = 200M
relay_log = relay-bin
sync_binlog = 1

# GTID
gtid_mode = ON
enforce_gtid_consistency = 1
binlog_gtid_simple_recovery = 1

# ENGINE
default_storage_engine = InnoDB
innodb_flush_log_at_trx_commit=1
```

## 4\. 创建docker-compose.yml文件

 -    将init\_sql下的文件映射到`/docker-entrypoint-initdb.d`目录下\(注：/docker-entrypoint-initdb.d下以`sql`或`sh`结尾的文件会在数据库`初始化完成后自动执行`\)

```bash
[root@docker ~]# cat /data/mysql/docker-compose.yml
version: '3'
services:
  mysql_m_compose:
    image: mysql:5.7.30
    container_name: mysql_m
    restart: always
    ports:
      - 33061:3306
    environment:
      - MYSQL_USER=ping
      - MYSQL_PASSWORD=123456
      - MYSQL_ROOT_PASSWORD=123456
    volumes:
      - ./master/conf/my.cnf:/etc/my.cnf
      - ./master/data:/var/lib/mysql
      - ./init-db-m:/docker-entrypoint-initdb.d

  mysql_s_compose:
    image: mysql:5.7.30
    container_name: mysql_s
    restart: always
    ports:
      - 33062:3306
    depends_on:
      - mysql_m_compose
    environment:
      - MYSQL_ROOT_PASSWORD=123456
    volumes:
      - ./slave/conf/my.cnf:/etc/my.cnf
      - ./init-db-s:/docker-entrypoint-initdb.d
```

## 5\. docker-compose启动mysql容器

```bash
[root@docker mysql]# docker-compose up -d
Creating network "mysql_default" with the default driver
Creating mysql_m ... done
Creating mysql_s ... done

[root@docker ~]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                NAMES
35cc9c6fbf52        mysql:5.7.30        "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        33060/tcp, 0.0.0.0:33062->3306/tcp   mysql_s
53a04e176ecc        mysql:5.7.30        "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        33060/tcp, 0.0.0.0:33061->3306/tcp   mysql_m

# 检查主从复制关系
# 主库
mysql>  CREATE DATABASE`db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
mysql_m> use db
Database changed
mysql_m> create table t1(id int,name varchar(32));
Query OK, 0 rows affected (0.01 sec)

mysql_m> insert into t1 values(1,'aa'),(2,'bb'),(3,'cc');
Query OK, 3 rows affected (0.01 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql_m> select  * from db.t1;
+------+------+
| id   | name |
+------+------+
|    1 | aa   |
|    2 | bb   |
|    3 | cc   |
+------+------+
3 rows in set (0.00 sec)

# 从库
mysql_s> select  * from db.t1;
+------+------+
| id   | name |
+------+------+
|    1 | aa   |
|    2 | bb   |
|    3 | cc   |
+------+------+
3 rows in set (0.00 sec)

# 查看主从复制状态信息
mysql> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: mysql_m_compose
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 10
              Master_Log_File: mysql-bin.000004
          Read_Master_Log_Pos: 845
               Relay_Log_File: relay-bin.000004
                Relay_Log_Pos: 1018
        Relay_Master_Log_File: mysql-bin.000004
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB: 
          Replicate_Ignore_DB: 
           Replicate_Do_Table: 
       Replicate_Ignore_Table: 
      Replicate_Wild_Do_Table: 
  Replicate_Wild_Ignore_Table: 
                   Last_Errno: 0
                   Last_Error: 
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 845
              Relay_Log_Space: 1219
              Until_Condition: None
               Until_Log_File: 
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File: 
           Master_SSL_CA_Path: 
              Master_SSL_Cert: 
            Master_SSL_Cipher: 
               Master_SSL_Key: 
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error: 
               Last_SQL_Errno: 0
               Last_SQL_Error: 
  Replicate_Ignore_Server_Ids: 
             Master_Server_Id: 33060000
                  Master_UUID: f28ef661-597b-11eb-beb8-0242ac120002
             Master_Info_File: /var/lib/mysql/master.info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind: 
      Last_IO_Error_Timestamp: 
     Last_SQL_Error_Timestamp: 
               Master_SSL_Crl: 
           Master_SSL_Crlpath: 
           Retrieved_Gtid_Set: f28ef661-597b-11eb-beb8-0242ac120002:10-12
            Executed_Gtid_Set: f28ef661-597b-11eb-beb8-0242ac120002:1-12
                Auto_Position: 1
         Replicate_Rewrite_DB: 
                 Channel_Name: 
           Master_TLS_Version: 
1 row in set (0.00 sec)
```

## 6\. 销毁两个容器

```bash
[root@Master mysql]# ls
docker-compose.yml  init-db-m  init-db-s  master  slave
[root@Master mysql]# docker-compose down
Stopping mysql_s ... done
Stopping mysql_m ... 
Stopping mysql_m ... done
Removing mysql_s ... done
Removing mysql_m ... done
Removing network mysql_default
```

```cpp
[root@Master mysql]#  ll -sh /data/mysql/master/data/
总用量 188M
4.0K -rw-r----- 1 polkitd ssh_keys   56 1月  18 18:57 auto.cnf
4.0K -rw------- 1 polkitd ssh_keys 1.7K 1月  18 18:57 ca-key.pem
4.0K -rw-r--r-- 1 polkitd ssh_keys 1.1K 1月  18 18:57 ca.pem
4.0K -rw-r--r-- 1 polkitd ssh_keys 1.1K 1月  18 18:57 client-cert.pem
4.0K -rw------- 1 polkitd ssh_keys 1.7K 1月  18 18:57 client-key.pem
   0 drwxr-x--- 2 polkitd ssh_keys   48 1月  18 19:09 db
4.0K -rw-r----- 1 polkitd ssh_keys 1.4K 1月  18 18:57 ib_buffer_pool
 76M -rw-r----- 1 polkitd ssh_keys  76M 1月  18 19:34 ibdata1
 48M -rw-r----- 1 polkitd ssh_keys  48M 1月  18 19:34 ib_logfile0
 48M -rw-r----- 1 polkitd ssh_keys  48M 1月  18 18:57 ib_logfile1
 12M -rw-r----- 1 polkitd ssh_keys  12M 1月  18 19:34 ibtmp1
4.0K drwxr-x--- 2 polkitd ssh_keys 4.0K 1月  18 18:57 mysql
4.0K -rw-r----- 1 polkitd ssh_keys  177 1月  18 18:57 mysql-bin.000001
3.0M -rw-r----- 1 polkitd ssh_keys 3.0M 1月  18 18:57 mysql-bin.000002
4.0K -rw-r----- 1 polkitd ssh_keys  241 1月  18 18:57 mysql-bin.000003
4.0K -rw-r----- 1 polkitd ssh_keys  845 1月  18 19:34 mysql-bin.000004
4.0K -rw-r----- 1 polkitd ssh_keys  241 1月  18 19:34 mysql-bin.000005
4.0K -rw-r----- 1 polkitd ssh_keys  194 1月  18 19:34 mysql-bin.000006
4.0K -rw-r----- 1 polkitd ssh_keys  114 1月  18 19:34 mysql-bin.index
 12K drwxr-x--- 2 polkitd ssh_keys 8.0K 1月  18 18:57 performance_schema
4.0K -rw------- 1 polkitd ssh_keys 1.7K 1月  18 18:57 private_key.pem
4.0K -rw-r--r-- 1 polkitd ssh_keys  452 1月  18 18:57 public_key.pem
4.0K -rw-r--r-- 1 polkitd ssh_keys 1.1K 1月  18 18:57 server-cert.pem
4.0K -rw------- 1 polkitd ssh_keys 1.7K 1月  18 18:57 server-key.pem
 12K drwxr-x--- 2 polkitd ssh_keys 8.0K 1月  18 18:57 sys
```

## 7\. 重建MySQL容器

```bash
[root@docker mysql]# docker-compose up -d
Creating network "mysql_default" with the default driver
Creating mysql_m ... done
Creating mysql_s ... done

[root@docker mysql]# docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                NAMES
7cd912fa9721        mysql:5.7.30        "docker-entrypoint.s…"   8 seconds ago       Up 8 seconds        33060/tcp, 0.0.0.0:33062->3306/tcp   mysql_s
d9e3514a1e19        mysql:5.7.30        "docker-entrypoint.s…"   9 seconds ago       Up 8 seconds        33060/tcp, 0.0.0.0:33061->3306/tcp   mysql_m

# 主库
mysql_m> select * from db.t1;
+------+------+
| id   | name |
+------+------+
|    1 | aa   |
|    2 | bb   |
|    3 | cc   |
+------+------+
3 rows in set (0.00 sec)

# 从库
mysql_s> select * from db.t1;
+------+------+
| id   | name |
+------+------+
|    1 | aa   |
|    2 | bb   |
|    3 | cc   |
+------+------+
3 rows in set (0.01 sec)

mysql_s> show slave status\G
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: mysql_m_compose
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 10
              Master_Log_File: mysql-bin.000006
          Read_Master_Log_Pos: 194
               Relay_Log_File: relay-bin.000004
                Relay_Log_Pos: 367
        Relay_Master_Log_File: mysql-bin.000006
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 194
              Relay_Log_Space: 568
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 33060000
                  Master_UUID: f93b936b-9b6b-11ea-9bda-0242c0a82002
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set: f93b936b-9b6b-11ea-9bda-0242c0a82002:1-12
                Auto_Position: 1
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
1 row in set (0.00 sec)
```