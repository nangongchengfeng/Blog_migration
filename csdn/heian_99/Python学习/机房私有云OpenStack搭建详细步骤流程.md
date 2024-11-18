---
title: 机房私有云OpenStack搭建详细步骤流程
date: 2024-10-25 16:28:51
tags: openstack
categories: 项目实战
description: "OpenStack是一个开源的云计算管理平台，旨在为公共及私有云的建设与管理提供软件。它由几个主要的组件组合起来完成一些具体的工作，包括计算、存储和网络资源的管理。OpenStack支持所有类型的云环境，可以简单地实施并大规模扩展，提供了一个丰富、标准化、统一的云计算管理平台。在私有云的部署中，OpenStack提供了强大的灵活性和可扩展性，允许企业根据自己的需求来定制和优化云环境。例如，通过OpenStack，企业可以规划并管理大量虚拟机，提供所需的对象及块存储资源，并实现网络资源的高扩展和自动化管理。"
---
<!--more-->
## OpenStack介绍
OpenStack是一个开源的云计算管理平台，旨在为公共及私有云的建设与管理提供软件。它由几个主要的组件组合起来完成一些具体的工作，包括计算、存储和网络资源的管理。OpenStack支持所有类型的云环境，可以简单地实施并大规模扩展，提供了一个丰富、标准化、统一的云计算管理平台。

在私有云的部署中，OpenStack提供了强大的灵活性和可扩展性，允许企业根据自己的需求来定制和优化云环境。例如，通过OpenStack，企业可以规划并管理大量虚拟机，提供所需的对象及块存储资源，并实现网络资源的高扩展和自动化管理


| 组件       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| Nova       | Compute HyperV管理(libvirt,qumu...)                          |
| Neutron    | 网络和地址管理(原名Quantum)                                  |
| Swift      | 对象存储(Object)                                             |
| Cinder     | 块存储管理(Cinder):主机指虚拟机的存储管理                    |
| Keystone   | 身份认证授权(Identity)                                       |
| Glance     | 镜象管理(Image)，支持本地存储、NFS、Swift、sheepdog和Ceph    |
| Horizon    | UI界面 (Dashboard)                                           |
| Ceilometer | 监控计量(Metering)                                           |
| Heat       | 软件部署(编配Orchestration)                                  |
| Lbass      | 负载均衡，后端可以是各种商业和开源产品，如：F5、Nginx、Haproxy、LVS |
| oslo       | 把所有组件需要用的相同的东西集中起来                         |
| Moniker    | DNS:每个虚拟机，都会自动有一个dns记录                        |
| marconi    | 消息队列扩展(Queue Service)                                  |
| Trove      | Database Service                                             |
| Ironic     | 裸机部署(Bare Metal)                                         |
| Savannah   | Data Processing                                              |
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d6fd4680be1046e299193100e9ff8ebb.png)

## 公司需求
因为公司业务拓展，需要有相关的设备建设对应的环境，我们采购多台服务器，使用raid5在组成存储。在这基础上使用OpenStack搭建私有云，来运行相关的业务和虚拟机。

机房检测环境通常需要一个稳定、安全、可控制的私有云环境。在这样的环境中，OpenStack能够提供以下优势：

1. **自主可控**：企业可以根据自己的需求定制和优化云环境，不受外部云服务提供商的限制。
2. **安全性**：私有云部署在企业内部，可以提供更高的安全和隐私级别，确保敏感数据不被第三方访问。
3. **灵活性**：OpenStack的开源特性使得企业可以灵活地选择硬件和软件，以及如何部署和管理这些资源。
4. **成本效益**：虽然初期建设成本可能较高，但随着业务量的增加，私有云的平均运营成本可能会低于公有云。


## 准备
OS：Centos 7 1804 Minimal
CPU：4c
MEM：8G
xvda：50G 系统盘
xvdb：100G 数据盘
Master IP：192.168.81.40

目标：
1.安装openstack Ocata
2.参考文档 [https://docs.openstack.org/ocata/install-guide-rdo/](https://docs.openstack.org/ocata/install-guide-rdo/)

### 初始化
```bash
#初始化配置
1.配置静态IP
2.关闭 selinux
sed -i "s/SELINUX=.*/SELINUX=disabled/g" /etc/selinux/config
3.关闭 NetworkManger
systemctl stop NetworkManger
systemctl disable NetworkManager
4.关闭 firewalld
systemctl stop firewalld
systemctl disable firewalld
5.配置主机名
hostnamectl set-hostname controller.openstack.fjf
6.重启
reboot
```
### 网络时间协议（NTP）

```bash
1.编辑 /etc/chrony.conf
server ntp1.aliyun.com iburst
server ntp2.aliyun.com iburst
server ntp3.aliyun.com iburst
server 0.centos.pool.ntp.org iburst
server 1.centos.pool.ntp.org iburst
server 2.centos.pool.ntp.org iburst
server 3.centos.pool.ntp.org iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
allow 192.168.0.0/16
logdir /var/log/chrony
2.重启服务
systemctl restart chronyd
```
## 安装OpenStack软件包

```bash

1.准备密码
ADMIN_PASS=Pass@w0rd
CINDER_DBPASS=Pass@w0rd
CINDER_PASS=Pass@w0rd
DASH_DBPASS=Pass@w0rd
DEMO_PASS=Pass@w0rd
GLANCE_DBPASS=Pass@w0rd
GLANCE_PASS=Pass@w0rd
KEYSTONE_DBPASS=Pass@w0rd
METADATA_SECRET=Pass@w0rd
NEUTRON_DBPASS=Pass@w0rd
NEUTRON_PASS=Pass@w0rd
NOVA_DBPASS=Pass@w0rd
NOVA_PASS=Pass@w0rd
PLACEMENT_PASS=Pass@w0rd
RABBIT_PASS=Pass@w0rd
2.配置hosts
echo "192.168.81.40 controller.openstack.fjf" >> /etc/hosts
echo "192.168.81.40 controller" >> /etc/hosts
3.安装openstack yum 源，官方已经移除了ocata的yum源，所以用本地同步好的
mkdir /etc/yum.repos.d/bak
mv /etc/yum.repos.d/* /etc/yum.repos.d/bak/
for i in CentOS-Base.repo  CentOS-OpenStack-Ocata.repo epel.repo;do
  curl -s -o /etc/yum.repos.d/$i http://source.fjf.com/bdata/centos7/$i
done
4.重建yum缓存
yum clean all
yum makecache
5.升级软件
yum upgrade -y
6.内核可能会有更新，重启一次系统
reboot
7.安装openstack client
yum install python-openstackclient -y
```
- 创建目录

```bash
mkdir -p /var/lib/nova
```
- 分区并格式化磁盘

```bash
[root@controller nova]# fdisk /dev/xvdb
Welcome to fdisk (util-linux 2.23.2).
 
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.
 
Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x3974d932.
 
Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-209715199, default 2048):
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-209715199, default 209715199):
Using default value 209715199
Partition 1 of type Linux and of size 100 GiB is set
 
Command (m for help): p
 
Disk /dev/xvdb: 107.4 GB, 107374182400 bytes, 209715200 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x3974d932
 
    Device Boot      Start         End      Blocks   Id  System
/dev/xvdb1            2048   209715199   104856576   83  Linux
 
Command (m for help): w
The partition table has been altered!
 
Calling ioctl() to re-read partition table.
Syncing disks.
[root@controller lib]# mkfs.xfs /dev/xvdb1
```
- 挂载至/var/lib/nova

```bash
mount /dev/xvdb1 /var/lib/nova
编辑/etc/fstab,添加一行
/dev/xvdb1 /var/lib/nova           xfs     defaults        0 0
```
## 部署基础组件
### 安装数据库

```bash
1.安装
yum install mariadb mariadb-server python2-PyMySQL -y
2.配置
cat > /etc/my.cnf.d/openstack.cnf <<EOF
[mysqld]
bind-address = 192.168.81.40
 
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
3.优化参数
在文件 /usr/lib/systemd/system/mariadb.service 的[Service]字段添加下列参数，否则会造成虚拟机创建失败的情况
LimitNOFILE=10000
LimitNPROC=10000
4.启动
systemctl enable mariadb.service
systemctl start mariadb.service
5.设置密码
[root@master ~]# mysql_secure_installation
 
NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!
 
In order to log into MariaDB to secure it, we'll need the current
password for the root user.  If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.
 
Enter current password for root (enter for none): 默认没密码，直接回车
OK, successfully used password, moving on...
 
Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.
 
Set root password? [Y/n] Y
New password: Pass@w0rd
Re-enter new password: Pass@w0rd
Password updated successfully!
Reloading privilege tables..
 ... Success!
 
 
By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.
 
Remove anonymous users? [Y/n] Y
 ... Success!
 
Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.
 
Disallow root login remotely? [Y/n] Y          #禁止root远程登陆，选择为Y之后只有master节点能使用root账号登陆。如果不想这样，按n
 ... Success!
 
By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.
 
Remove test database and access to it? [Y/n] Y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!
 
Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.
 
Reload privilege tables now? [Y/n] Y
 ... Success!
 
Cleaning up...
 
All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.
 
Thanks for using MariaDB!
6.测试一下
[root@master ~]# mysql -uroot -pPass@w0rd
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 16
Server version: 10.3.20-MariaDB MariaDB Server
 
Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.
 
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
 
show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
3 rows in set (0.001 sec)
```

### 安装消息队列服务

```bash
1.安装rabbitmq
yum install rabbitmq-server -y
2.启动
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
3.设置密码
rabbitmqctl add_user openstack Pass@w0rd
4.授权
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
5.开启rabbitmq management方便以后管理
rabbitmq-plugins enable rabbitmq_management
默认密码：guest/guest
后台：192.168.81.40:15672
```
### 安装缓存服务

```bash
1.安装memcached
yum install memcached python-memcached -y
2.修改配置文件
vim /etc/sysconfig/memcached
OPTIONS="-l 127.0.0.1,::1,controller.openstack.fjf"
3.启动
systemctl enable memcached.service
systemctl start memcached.service
```
### 安装键值存储服务

```bash
1.安装etcd
yum install etcd -y
2.配置
cat > /etc/etcd/etcd.conf <<EOF
#[Member]
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
ETCD_LISTEN_PEER_URLS="http://192.168.81.40:2380"
ETCD_LISTEN_CLIENT_URLS="http://192.168.81.40:2379"
ETCD_NAME="controller.openstack.fjf"
#[Clustering]
ETCD_INITIAL_ADVERTISE_PEER_URLS="http://192.168.81.40:2380"
ETCD_ADVERTISE_CLIENT_URLS="http://192.168.81.40:2379"
ETCD_INITIAL_CLUSTER="controller.openstack.fjf=http://192.168.81.40:2380"
ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster-01"
ETCD_INITIAL_CLUSTER_STATE="new"
EOF
3.启动
systemctl enable etcd
systemctl start etcd
```
### 系统参数优化

```bash
1.修改/etc/security/limits.d/20-nproc.conf
*          soft    nproc     65535
root       soft    nproc     unlimited
2.修改
/etc/security/limits.conf
*     soft  nofile  655350
*     hard  nofile  655350
*     soft  nproc   655350
*     hard  nproc   655350

```

## 安装keystone
一. 安装keystone(身份认证服务)

建库，建用户

```bash
[root@controller ~]# mysql -uroot -pPass@w0rd  
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 11
Server version: 10.1.20-MariaDB MariaDB Server
 
Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
 
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
 
MariaDB [(none)]> CREATE DATABASE keystone;
Query OK, 1 row affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
```
安装组件

```bash
yum install openstack-keystone httpd mod_wsgi -y
```
编辑/etc/keystone/keystone.conf文件并完成以下操作：

```bash

1.在该[database]部分中，配置数据库访问：
[database]
# ...
connection = mysql+pymysql://keystone:Pass@w0rd@controller.openstack.fjf/keystone
2.在该[token]部分中，配置Fernet令牌提供者
[token]
# ...
provider = fernet
```
填充身份服务数据库

```bash
su -s /bin/sh -c "keystone-manage db_sync" keystone
```
初始化Fernet密钥存储库

```bash
keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
```
引导身份服务

```bash
keystone-manage bootstrap --bootstrap-password Pass@w0rd \
  --bootstrap-admin-url http://controller.openstack.fjf:5000/v3/ \
  --bootstrap-internal-url http://controller.openstack.fjf:5000/v3/ \
  --bootstrap-public-url http://controller.openstack.fjf:5000/v3/ \
  --bootstrap-region-id RegionOne
```
配置HTTP接口

```bash
vim /etc/httpd/conf/httpd.conf
ServerName controller.openstack.fjf
```
创建链接

```bash
ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/
```
启动

```bash
systemctl enable httpd.service
systemctl start httpd.service
```
创建admin-openrc

```bash
cat > /root/admin-openrc <<EOF
export OS_USERNAME=admin
export OS_PASSWORD=Pass@w0rd
export OS_PROJECT_NAME=admin
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_DOMAIN_NAME=Default
export OS_AUTH_URL=http://controller.openstack.fjf:5000/v3
export OS_IDENTITY_API_VERSION=3
EOF

```
加载admin-openrc

```bash

. admin-openrc
```
创建service

```bash
openstack project create --domain default \
  --description "Service Project" service
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Service Project                  |
| domain_id   | default                          |
| enabled     | True                             |
| id          | 2c7d5b03d68746229cb60b9ae382d0ae |
| is_domain   | False                            |
| name        | service                          |
| parent_id   | default                          |
| tags        | []                               |
+-------------+----------------------------------+
```
验证操作
```
openstack --os-auth-url http://controller.openstack.fjf:5000/v3 \
 --os-project-domain-name Default --os-user-domain-name Default \
 --os-project-name admin --os-username admin token issue
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field      | Value                                                                                                                                                                                   |
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| expires    | 2021-03-18T12:10:01+0000                                                                                                                                                                |
| id         | gAAAAABgUzUJjJTsx4Vz1OY_vBBN28FQC3hH-xpqhITyvjSdF4pOykX8tCd0WX59rChxhC7kWZkrhQygcLj9Ari3pmKcZ5u9Ae4RTYJh1NpF8418xbbZCeZgxbVb9SOUgqCe0ftFzbewGmEL-hxhOmr3rd3WO2HYG47H6CR9WmDzSWsIei2NpPw |
| project_id | 750d6512fc3043d1b1c6d832465cbf9f                                                                                                                                                        |
| user_id    | 99cb132981a74d339868e54a0a4deb3c                                                                                                                                                        |
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

```
## 安装glance
二、安装glance(镜像服务)

建库，建用户

```bash
[root@controller ~]# mysql -uroot -pPass@w0rd 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 3
Server version: 10.1.20-MariaDB MariaDB Server
 
Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
 
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
 
MariaDB [(none)]> CREATE DATABASE glance;
Query OK, 1 row affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'Passw0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'Passw0rd';
Query OK, 0 rows affected (0.00 sec)
```
加载admin-openrc

```bash
. admin-openrc
```
创建用户

```bash

[root@controller ~]# openstack user create --domain default --password-prompt glance
User Password:Pass@w0rd
Repeat User Password:Pass@w0rd
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | 06d7dd9775a3482886790405f3bfe298 |
| name                | glance                           |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```
授权

```bash
openstack role add --project service --user glance admin

```
创建服务

```bash
[root@controller ~]# openstack service create --name glance   --description "OpenStack Image" image
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Image                  |
| enabled     | True                             |
| id          | 56c2b257f48d4d7aa4768a0f1f2367ca |
| name        | glance                           |
| type        | image                            |
+-------------+----------------------------------+
```
创建API接口

```bash
[root@controller ~]# openstack endpoint create --region RegionOne   image public http://controller.openstack.fjf:9292
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | 36c0f0dec23f435fb5e3bbd6ac0ce5ff     |
| interface    | public                               |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 56c2b257f48d4d7aa4768a0f1f2367ca     |
| service_name | glance                               |
| service_type | image                                |
| url          | http://controller.openstack.fjf:9292 |
+--------------+--------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne   image internal http://controller.openstack.fjf:9292
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | 236f70c24afb4049ac2660cbecd0b7a2     |
| interface    | internal                             |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 56c2b257f48d4d7aa4768a0f1f2367ca     |
| service_name | glance                               |
| service_type | image                                |
| url          | http://controller.openstack.fjf:9292 |
+--------------+--------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne   image admin http://controller.openstack.fjf:9292
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | 36f005f69dd74f52b3f5bf0cce3c46d7     |
| interface    | admin                                |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 56c2b257f48d4d7aa4768a0f1f2367ca     |
| service_name | glance                               |
| service_type | image                                |
| url          | http://controller.openstack.fjf:9292 |
+--------------+--------------------------------------+
```
安装和配置组件

```bash

yum install openstack-glance -y
```
编辑/etc/glance/glance-api.conf 

```bash
[database]
# ...
# 注意此处的密码是Passw0rd而不是Pass@w0rd,改组件连接串中不支持'@'符号
connection = mysql+pymysql://glance:Passw0rd@controller.openstack.fjf/glance
 
[keystone_authtoken]
# ...
www_authenticate_uri  = http://controller.openstack.fjf:5000
auth_url = http://controller.openstack.fjf:5000
memcached_servers = controller.openstack.fjf:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = glance
password = Pass@w0rd
 
[paste_deploy]
# ...
flavor = keystone
 
[glance_store]
# ...
stores = file,http
default_store = file
filesystem_store_datadir = /var/lib/glance/images/
```
填充图像服务数据库

```bash
[root@controller ~]# su -s /bin/sh -c "glance-manage db_sync" glance
# 出现此警告可以忽略   
/usr/lib/python2.7/site-packages/oslo_db/sqlalchemy/enginefacade.py:1336: OsloDBDeprecationWarning: EngineFacade is deprecated; please use oslo_db.sqlalchemy.enginefacade
  expire_on_commit=expire_on_commit, _conf=conf)
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> liberty, liberty initial
INFO  [alembic.runtime.migration] Running upgrade liberty -> mitaka01, add index on created_at and updated_at columns of 'images' table
INFO  [alembic.runtime.migration] Running upgrade mitaka01 -> mitaka02, update metadef os_nova_server
INFO  [alembic.runtime.migration] Running upgrade mitaka02 -> ocata_expand01, add visibility to images
INFO  [alembic.runtime.migration] Running upgrade ocata_expand01 -> pike_expand01, empty expand for symmetry with pike_contract01
INFO  [alembic.runtime.migration] Running upgrade pike_expand01 -> queens_expand01
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
Upgraded database to: queens_expand01, current revision(s): queens_expand01
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
Database migration is up to date. No migration needed.
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade mitaka02 -> ocata_contract01, remove is_public from images
INFO  [alembic.runtime.migration] Running upgrade ocata_contract01 -> pike_contract01, drop glare artifacts tables
INFO  [alembic.runtime.migration] Running upgrade pike_contract01 -> queens_contract01
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
Upgraded database to: queens_contract01, current revision(s): queens_contract01
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
Database is synced successfully.
```
启动

```bash
systemctl enable openstack-glance-api.service
systemctl start openstack-glance-api.service
```
## 安装Compute|控制节点

三、安装Compute(计算服务)&Placement(调度服务)

建库，建用户

```bash
[root@controller ~]# mysql -uroot -pPass@w0rd               
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 11
Server version: 10.1.20-MariaDB MariaDB Server
 
Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
 
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
 
MariaDB [(none)]> CREATE DATABASE nova_api;
Query OK, 1 row affected (0.00 sec)
 
MariaDB [(none)]> CREATE DATABASE nova;
Query OK, 1 row affected (0.00 sec)
 
MariaDB [(none)]> CREATE DATABASE nova_cell0;
Query OK, 1 row affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
```
加载admin-openrc

```base
. admin-openrc
```
创建Nova用户

```bash
[root@controller ~]# openstack user create --domain default --password-prompt nova
User Password:Pass@w0rd
Repeat User Password:Pass@w0rd
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | fa90e0ee1be34a7c8d9d77bf2db3ca7e |
| name                | nova                             |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```
授权Nova

```bash
openstack role add --project service --user nova admin
```
创建计算服务

```bash
[root@controller ~]# openstack service create --name nova --description "OpenStack Compute" compute
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Compute                |
| enabled     | True                             |
| id          | 0795642e98ce42c8bac111a21625976c |
| name        | nova                             |
| type        | compute                          |
+-------------+----------------------------------+
```
创建计算API接口

```bash
[root@controller ~]# openstack endpoint create --region RegionOne compute public http://controller.openstack.fjf:8774/v2.1
+--------------+-------------------------------------------+
| Field        | Value                                     |
+--------------+-------------------------------------------+
| enabled      | True                                      |
| id           | f1569159f0444831b29d4e0732aeca27          |
| interface    | public                                    |
| region       | RegionOne                                 |
| region_id    | RegionOne                                 |
| service_id   | 0795642e98ce42c8bac111a21625976c          |
| service_name | nova                                      |
| service_type | compute                                   |
| url          | http://controller.openstack.fjf:8774/v2.1 |
+--------------+-------------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne compute internal http://controller.openstack.fjf:8774/v2.1
+--------------+-------------------------------------------+
| Field        | Value                                     |
+--------------+-------------------------------------------+
| enabled      | True                                      |
| id           | 465c36ab7dcc4e849c835ae9ef174eba          |
| interface    | internal                                  |
| region       | RegionOne                                 |
| region_id    | RegionOne                                 |
| service_id   | 0795642e98ce42c8bac111a21625976c          |
| service_name | nova                                      |
| service_type | compute                                   |
| url          | http://controller.openstack.fjf:8774/v2.1 |
+--------------+-------------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne compute admin http://controller.openstack.fjf:8774/v2.1
+--------------+-------------------------------------------+
| Field        | Value                                     |
+--------------+-------------------------------------------+
| enabled      | True                                      |
| id           | 879816f84f6444b4a65bab6f8d620d08          |
| interface    | admin                                     |
| region       | RegionOne                                 |
| region_id    | RegionOne                                 |
| service_id   | 0795642e98ce42c8bac111a21625976c          |
| service_name | nova                                      |
| service_type | compute                                   |
| url          | http://controller.openstack.fjf:8774/v2.1 |
+--------------+-------------------------------------------+
```
创建placement用户

```bash
[root@controller ~]# openstack user create --domain default --password-prompt placement
User Password:Pass@w0rd
Repeat User Password:Pass@w0rd
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | f0b41802435f4d3dad27c6711bb3de73 |
| name                | placement                        |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```
授权placement

```bash
openstack role add --project service --user placement admin
```
创建调度器服务

```bash
[root@controller ~]# openstack service create --name placement --description "Placement API" placement
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Placement API                    |
| enabled     | True                             |
| id          | 315aa5dae18c4c6bb2a6105f25a11c98 |
| name        | placement                        |
| type        | placement                        |
+-------------+----------------------------------+

```
创建调度器API接口

```bash
[root@controller ~]# openstack endpoint create --region RegionOne placement public http://controller.openstack.fjf:8778
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | bb6eeb117b2c421498bd5d74ab2304e0     |
| interface    | public                               |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 7b2281d9a2e1436e8d6b9721774deb01     |
| service_name | placement                            |
| service_type | placement                            |
| url          | http://controller.openstack.fjf:8778 |
+--------------+--------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne placement internal http://controller.openstack.fjf:8778
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | fed2080d301247e4b9cb9e2b2a4bde55     |
| interface    | internal                             |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 7b2281d9a2e1436e8d6b9721774deb01     |
| service_name | placement                            |
| service_type | placement                            |
| url          | http://controller.openstack.fjf:8778 |
+--------------+--------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne placement admin http://controller.openstack.fjf:8778
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | 3d255c3a2ebb4d249f063e1392767fd7     |
| interface    | admin                                |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 7b2281d9a2e1436e8d6b9721774deb01     |
| service_name | placement                            |
| service_type | placement                            |
| url          | http://controller.openstack.fjf:8778 |
+--------------+--------------------------------------+
```
安装和配置组件

```bash
yum install openstack-nova-api openstack-nova-conductor   openstack-nova-console openstack-nova-novncproxy   openstack-nova-scheduler openstack-nova-placement-api -y
```
编辑/etc/nova/nova.conf

```bash
[DEFAULT]
# ...
enabled_apis = osapi_compute,metadata
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
my_ip = 192.168.81.40
connection = mysql+pymysql://nova:Pass@w0rd@controller.openstack.fjf/nova_api
transport_url = rabbit://openstack:Pass@w0rd@controller.openstack.fjf
 
[api_database]
# ...
connection = mysql+pymysql://nova:Pass@w0rd@controller.openstack.fjf/nova_api
 
[database]
# ...
connection = mysql+pymysql://nova:Pass@w0rd@controller.openstack.fjf/nova
 
[api]
# ...
auth_strategy = keystone
 
[keystone_authtoken]
# ...
auth_uri = http://controller.openstack.fjf:5000
auth_url = http://controller.openstack.fjf:35357
memcached_servers = controller.openstack.fjf:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = Pass@w0rd
 
[vnc]
enabled = true
# ...
vncserver_listen = $my_ip
vncserver_proxyclient_address = $my_ip
novncproxy_base_url = http://controller.openstack.fjf:6080/vnc_auto.html
 
[glance]
# ...
api_servers = http://controller.openstack.fjf:9292
[oslo_concurrency]
# ...
lock_path = /var/lib/nova/tmp
 
[placement]
# ...
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller.openstack.fjf:35357/v3
username = placement
password = Pass@w0rd
```
编辑/etc/httpd/conf.d/00-nova-placement-api.conf，尾部添加

```bash
<Directory /usr/bin>
   <IfVersion >= 2.4>
      Require all granted
   </IfVersion>
   <IfVersion < 2.4>
      Order allow,deny
      Allow from all
   </IfVersion>
</Directory>
```
重启httpd

```bash
systemctl restart httpd
```
初始化数据

```bash
[root@controller ~]# su -s /bin/sh -c "nova-manage api_db sync" nova
[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova
[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
5d590937-4a0e-488e-9766-9db19d151a51
[root@controller ~]# su -s /bin/sh -c "nova-manage db sync" nova
# 警告信息可以忽略
/usr/lib/python2.7/site-packages/pymysql/cursors.py:170: Warning: (1831, u'Duplicate index `block_device_mapping_instance_uuid_virtual_name_device_name_idx`. This is deprecated and will be disallowed in a future release.')
  result = self._query(query)
/usr/lib/python2.7/site-packages/pymysql/cursors.py:170: Warning: (1831, u'Duplicate index `uniq_instances0uuid`. This is deprecated and will be disallowed in a future release.')
  result = self._query(query)
[root@controller ~]# nova-manage cell_v2 list_cells
# 验证数据
+-------+--------------------------------------+--------------------------------------------------+---------------------------------------------------------------+
|  Name |                 UUID                 |                  Transport URL                   |                      Database Connection                      |
+-------+--------------------------------------+--------------------------------------------------+---------------------------------------------------------------+
| cell0 | 00000000-0000-0000-0000-000000000000 |                      none:/                      | mysql+pymysql://nova:****@controller.openstack.fjf/nova_cell0 |
| cell1 | 5d590937-4a0e-488e-9766-9db19d151a51 | rabbit://openstack:****@controller.openstack.fjf |    mysql+pymysql://nova:****@controller.openstack.fjf/nova    |
+-------+--------------------------------------+--------------------------------------------------+---------------------------------------------------------------+
```
启动服务

```bash

systemctl enable openstack-nova-api.service   openstack-nova-consoleauth.service openstack-nova-scheduler.service   openstack-nova-conductor.service openstack-nova-novncproxy.service
systemctl start openstack-nova-api.service   openstack-nova-consoleauth.service openstack-nova-scheduler.service   openstack-nova-conductor.service openstack-nova-novncproxy.service
```
## 安装Compute|计算节点
四、安装Compute(计算服务)，为了节省资源可以将计算节点和控制节点安装在一起这样控制节点也可以运行虚拟机

安装组件

```bash
yum install openstack-nova-compute
```

编辑配置/etc/nova/nova.conf，如果是在控制节点上添加计算服务则不需要修改

```bash
[DEFAULT]
# ...
enabled_apis = osapi_compute,metadata
my_ip = 192.168.81.40
use_neutron = True
firewall_driver = nova.virt.firewall.NoopFirewallDriver
transport_url = rabbit://openstack:Pass@w0rd@controller.openstack.fjf
 
[api]
# ...
auth_strategy = keystone
 
[keystone_authtoken]
# ...
auth_uri = http://controller.openstack.fjf:5000
auth_url = http://controller.openstack.fjf:35357
memcached_servers = controller.openstack.fjf:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = nova
password = Pass@w0rd
 
[vnc]
# ...
enabled = True
vncserver_listen = 0.0.0.0
vncserver_proxyclient_address = $my_ip
novncproxy_base_url = http://controller.openstack.fjf:6080/vnc_auto.html
 
[glance]
# ...
api_servers = http://controller.openstack.fjf:9292
 
[oslo_concurrency]
# ...
lock_path = /var/lib/nova/tmp
 
[placement]
# ...
os_region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller.openstack.fjf:35357/v3
username = placement
password = Pass@w0rd
```
检查是否支持硬件虚拟化

```bash
[root@controller ~]# egrep -c '(vmx|svm)' /proc/cpuinfo
8
# 如果结果为0，则需要添加以下配置
编辑 /etc/nova/nova.conf
[libvirt]
# ...
virt_type = qemu
```
启动服务

```bash
systemctl enable libvirtd.service openstack-nova-compute.service
systemctl start  libvirtd.service openstack-nova-compute.service
```
添加计算节点到元数据库

```bash

. admin-openrc
# 扫描计算主机
[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
Found 2 cell mappings.
Skipping cell0 since it does not contain hosts.
Getting computes from cell 'cell1': 5d590937-4a0e-488e-9766-9db19d151a51
Checking host mapping for compute host 'controller.openstack.fjf': deb6c5fe-24a6-4b1e-af8f-fe448491a565
Creating host mapping for compute host 'controller.openstack.fjf': deb6c5fe-24a6-4b1e-af8f-fe448491a565
Found 1 unmapped computes in cell: 5d590937-4a0e-488e-9766-9db19d151a51
# 查看主机状态
[root@controller ~]# openstack hypervisor list                                          
+----+--------------------------+-----------------+---------------+-------+
| ID | Hypervisor Hostname      | Hypervisor Type | Host IP       | State |
+----+--------------------------+-----------------+---------------+-------+
|  1 | controller.openstack.fjf | QEMU            | 192.168.81.40 | up    |
+----+--------------------------+-----------------+---------------+-------+
```
注意：添加计算节点后必须在控制节点执行nova-manage cell_v2 discover_hosts才能发现新的计算节点，可以调整/etc/nova/nova.conf中的参数discover_hosts_in_cells_interval = 300，表示为300s自动扫描一次
## 安装neutron
五、安装neutron(网络服务)

建库，建用户

```bash

[root@controller ~]# mysql -uroot -pPass@w0rd              
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 3182
Server version: 10.1.20-MariaDB MariaDB Server
 
Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.
 
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
 
MariaDB [(none)]> CREATE DATABASE neutron;
Query OK, 1 row affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
 
MariaDB [(none)]> GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'Pass@w0rd';
Query OK, 0 rows affected (0.00 sec)
```
加载admin-openrc

```bash

. admin-openrc
```
创建用户

```bash

[root@controller ~]# openstack user create --domain default --password-prompt neutron
User Password:
Repeat User Password:
+---------------------+----------------------------------+
| Field               | Value                            |
+---------------------+----------------------------------+
| domain_id           | default                          |
| enabled             | True                             |
| id                  | c6ea433a2f83472f8218b60dbdf1827a |
| name                | neutron                          |
| options             | {}                               |
| password_expires_at | None                             |
+---------------------+----------------------------------+
```
授权

```bash

openstack role add --project service --user neutron admin
```
创建服务

```bash
[root@controller ~]# openstack service create --name neutron --description "OpenStack Networking" network
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Networking             |
| enabled     | True                             |
| id          | 9b2865e3489c4da3b6c250abf2e73e80 |
| name        | neutron                          |
| type        | network                          |
+-------------+----------------------------------+
```
创建API接口

```bash
[root@controller ~]# openstack endpoint create --region RegionOne network public http://controller.openstack.fjf:9696
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | f3a7c91366d84b49aa84841585ee3d36     |
| interface    | public                               |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 9b2865e3489c4da3b6c250abf2e73e80     |
| service_name | neutron                              |
| service_type | network                              |
| url          | http://controller.openstack.fjf:9696 |
+--------------+--------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne network internal http://controller.openstack.fjf:9696
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | e5bac77508904343b93f12a19294a7dd     |
| interface    | internal                             |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 9b2865e3489c4da3b6c250abf2e73e80     |
| service_name | neutron                              |
| service_type | network                              |
| url          | http://controller.openstack.fjf:9696 |
+--------------+--------------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne network admin http://controller.openstack.fjf:9696
+--------------+--------------------------------------+
| Field        | Value                                |
+--------------+--------------------------------------+
| enabled      | True                                 |
| id           | 20e22cf74f9b4ac99ee20bc95cfd3433     |
| interface    | admin                                |
| region       | RegionOne                            |
| region_id    | RegionOne                            |
| service_id   | 9b2865e3489c4da3b6c250abf2e73e80     |
| service_name | neutron                              |
| service_type | network                              |
| url          | http://controller.openstack.fjf:9696 |
+--------------+--------------------------------------+
```
安装网络组件，有两种Provider networks和Self-service networks，Self-service networks提供L3（三层路由）的能力，因为网络组件部署后无法更改，所以使用Self-service networks，其可以涵盖更多的网络类型方便以后网络变化

```bash
yum install openstack-neutron openstack-neutron-ml2 openstack-neutron-linuxbridge ebtables -y
```
编辑配置文件

 编辑/etc/neutron/neutron.conf

```bash
[database]
# ...
connection = mysql+pymysql://neutron:Pass@w0rd@controller.openstack.fjf/neutron
 
[DEFAULT]
# ...
core_plugin = ml2
service_plugins = router
allow_overlapping_ips = true
transport_url = rabbit://openstack:Pass@w0rd@controller.openstack.fjf
auth_strategy = keystone
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true
 
[keystone_authtoken]
# ...
auth_uri = http://controller.openstack.fjf:5000
auth_url = http://controller.openstack.fjf:35357
memcached_servers = controller.openstack.fjf:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = neutron
password = Pass@w0rd
 
[nova]
# ...
auth_url = http://controller.openstack.fjf:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = nova
password = Pass@w0rd
 
[oslo_concurrency]
# ...
lock_path = /var/lib/neutron/tmp
```
编辑/etc/neutron/plugins/ml2/ml2_conf.ini

```bash
[ml2]
# ...
type_drivers = flat,vlan,vxlan
tenant_network_types = vxlan
mechanism_drivers = linuxbridge,l2population
extension_drivers = port_security
 
[ml2_type_flat]
# ...
flat_networks = provider
 
[ml2_type_vlan]
# ...
network_vlan_ranges = physvlan:1:1000
 
[ml2_type_vxlan]
# ...
vni_ranges = 1:1000
 
[securitygroup]
# ...
enable_ipset = true
```
编辑/etc/neutron/plugins/ml2/linuxbridge_agent.ini

```bash
[linux_bridge]
physical_interface_mappings = provider:eth0
 
[vxlan]
enable_vxlan = true
local_ip = 192.168.81.40
l2_population = true
 
[securitygroup]
# ...
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver
```
编辑/etc/neutron/l3_agent.ini

```bash
[DEFAULT]
# ...
interface_driver = linuxbridge
```
编辑/etc/neutron/dhcp_agent.ini

```bash
[DEFAULT]
# ...
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true
```
编辑/etc/neutron/metadata_agent.ini

```bash
[DEFAULT]
# ...
nova_metadata_host = controller.openstack.fjf
# 共享密钥随机生成一个
metadata_proxy_shared_secret = RpP55i3dSRRoHq8x
```
编辑/etc/nova/nova.conf

```bash
[neutron]
# ...
url = http://controller.openstack.fjf:9696
auth_url = http://controller.openstack.fjf:35357
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = Pass@w0rd
service_metadata_proxy = true
metadata_proxy_shared_secret = RpP55i3dSRRoHq8x
```
创建配置链接

```bash
ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
```
初始化数据库

```bash
[root@controller ~]# su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
  Running upgrade for neutron ...
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> kilo, kilo_initial
INFO  [alembic.runtime.migration] Running upgrade kilo -> 354db87e3225, nsxv_vdr_metadata.py
INFO  [alembic.runtime.migration] Running upgrade 354db87e3225 -> 599c6a226151, neutrodb_ipam
INFO  [alembic.runtime.migration] Running upgrade 599c6a226151 -> 52c5312f6baf, Initial operations in support of address scopes
INFO  [alembic.runtime.migration] Running upgrade 52c5312f6baf -> 313373c0ffee, Flavor framework
INFO  [alembic.runtime.migration] Running upgrade 313373c0ffee -> 8675309a5c4f, network_rbac
INFO  [alembic.runtime.migration] Running upgrade 8675309a5c4f -> 45f955889773, quota_usage
INFO  [alembic.runtime.migration] Running upgrade 45f955889773 -> 26c371498592, subnetpool hash
INFO  [alembic.runtime.migration] Running upgrade 26c371498592 -> 1c844d1677f7, add order to dnsnameservers
INFO  [alembic.runtime.migration] Running upgrade 1c844d1677f7 -> 1b4c6e320f79, address scope support in subnetpool
INFO  [alembic.runtime.migration] Running upgrade 1b4c6e320f79 -> 48153cb5f051, qos db changes
INFO  [alembic.runtime.migration] Running upgrade 48153cb5f051 -> 9859ac9c136, quota_reservations
INFO  [alembic.runtime.migration] Running upgrade 9859ac9c136 -> 34af2b5c5a59, Add dns_name to Port
INFO  [alembic.runtime.migration] Running upgrade 34af2b5c5a59 -> 59cb5b6cf4d, Add availability zone
INFO  [alembic.runtime.migration] Running upgrade 59cb5b6cf4d -> 13cfb89f881a, add is_default to subnetpool
INFO  [alembic.runtime.migration] Running upgrade 13cfb89f881a -> 32e5974ada25, Add standard attribute table
INFO  [alembic.runtime.migration] Running upgrade 32e5974ada25 -> ec7fcfbf72ee, Add network availability zone
INFO  [alembic.runtime.migration] Running upgrade ec7fcfbf72ee -> dce3ec7a25c9, Add router availability zone
INFO  [alembic.runtime.migration] Running upgrade dce3ec7a25c9 -> c3a73f615e4, Add ip_version to AddressScope
INFO  [alembic.runtime.migration] Running upgrade c3a73f615e4 -> 659bf3d90664, Add tables and attributes to support external DNS integration
INFO  [alembic.runtime.migration] Running upgrade 659bf3d90664 -> 1df244e556f5, add_unique_ha_router_agent_port_bindings
INFO  [alembic.runtime.migration] Running upgrade 1df244e556f5 -> 19f26505c74f, Auto Allocated Topology - aka Get-Me-A-Network
INFO  [alembic.runtime.migration] Running upgrade 19f26505c74f -> 15be73214821, add dynamic routing model data
INFO  [alembic.runtime.migration] Running upgrade 15be73214821 -> b4caf27aae4, add_bgp_dragent_model_data
INFO  [alembic.runtime.migration] Running upgrade b4caf27aae4 -> 15e43b934f81, rbac_qos_policy
INFO  [alembic.runtime.migration] Running upgrade 15e43b934f81 -> 31ed664953e6, Add resource_versions row to agent table
INFO  [alembic.runtime.migration] Running upgrade 31ed664953e6 -> 2f9e956e7532, tag support
INFO  [alembic.runtime.migration] Running upgrade 2f9e956e7532 -> 3894bccad37f, add_timestamp_to_base_resources
INFO  [alembic.runtime.migration] Running upgrade 3894bccad37f -> 0e66c5227a8a, Add desc to standard attr table
INFO  [alembic.runtime.migration] Running upgrade 0e66c5227a8a -> 45f8dd33480b, qos dscp db addition
INFO  [alembic.runtime.migration] Running upgrade 45f8dd33480b -> 5abc0278ca73, Add support for VLAN trunking
INFO  [alembic.runtime.migration] Running upgrade 5abc0278ca73 -> d3435b514502, Add device_id index to Port
INFO  [alembic.runtime.migration] Running upgrade d3435b514502 -> 30107ab6a3ee, provisioning_blocks.py
INFO  [alembic.runtime.migration] Running upgrade 30107ab6a3ee -> c415aab1c048, add revisions table
INFO  [alembic.runtime.migration] Running upgrade c415aab1c048 -> a963b38d82f4, add dns name to portdnses
INFO  [alembic.runtime.migration] Running upgrade kilo -> 30018084ec99, Initial no-op Liberty contract rule.
INFO  [alembic.runtime.migration] Running upgrade 30018084ec99 -> 4ffceebfada, network_rbac
INFO  [alembic.runtime.migration] Running upgrade 4ffceebfada -> 5498d17be016, Drop legacy OVS and LB plugin tables
INFO  [alembic.runtime.migration] Running upgrade 5498d17be016 -> 2a16083502f3, Metaplugin removal
INFO  [alembic.runtime.migration] Running upgrade 2a16083502f3 -> 2e5352a0ad4d, Add missing foreign keys
INFO  [alembic.runtime.migration] Running upgrade 2e5352a0ad4d -> 11926bcfe72d, add geneve ml2 type driver
INFO  [alembic.runtime.migration] Running upgrade 11926bcfe72d -> 4af11ca47297, Drop cisco monolithic tables
INFO  [alembic.runtime.migration] Running upgrade 4af11ca47297 -> 1b294093239c, Drop embrane plugin table
INFO  [alembic.runtime.migration] Running upgrade 1b294093239c -> 8a6d8bdae39, standardattributes migration
INFO  [alembic.runtime.migration] Running upgrade 8a6d8bdae39 -> 2b4c2465d44b, DVR sheduling refactoring
INFO  [alembic.runtime.migration] Running upgrade 2b4c2465d44b -> e3278ee65050, Drop NEC plugin tables
INFO  [alembic.runtime.migration] Running upgrade e3278ee65050 -> c6c112992c9, rbac_qos_policy
INFO  [alembic.runtime.migration] Running upgrade c6c112992c9 -> 5ffceebfada, network_rbac_external
INFO  [alembic.runtime.migration] Running upgrade 5ffceebfada -> 4ffceebfcdc, standard_desc
INFO  [alembic.runtime.migration] Running upgrade 4ffceebfcdc -> 7bbb25278f53, device_owner_ha_replicate_int
INFO  [alembic.runtime.migration] Running upgrade 7bbb25278f53 -> 89ab9a816d70, Rename ml2_network_segments table
INFO  [alembic.runtime.migration] Running upgrade a963b38d82f4 -> 3d0e74aa7d37, Add flavor_id to Router
INFO  [alembic.runtime.migration] Running upgrade 3d0e74aa7d37 -> 030a959ceafa, uniq_routerports0port_id
INFO  [alembic.runtime.migration] Running upgrade 030a959ceafa -> a5648cfeeadf, Add support for Subnet Service Types
INFO  [alembic.runtime.migration] Running upgrade a5648cfeeadf -> 0f5bef0f87d4, add_qos_minimum_bandwidth_rules
INFO  [alembic.runtime.migration] Running upgrade 0f5bef0f87d4 -> 67daae611b6e, add standardattr to qos policies
INFO  [alembic.runtime.migration] Running upgrade 89ab9a816d70 -> c879c5e1ee90, Add segment_id to subnet
INFO  [alembic.runtime.migration] Running upgrade c879c5e1ee90 -> 8fd3918ef6f4, Add segment_host_mapping table.
INFO  [alembic.runtime.migration] Running upgrade 8fd3918ef6f4 -> 4bcd4df1f426, Rename ml2_dvr_port_bindings
INFO  [alembic.runtime.migration] Running upgrade 4bcd4df1f426 -> b67e765a3524, Remove mtu column from networks.
INFO  [alembic.runtime.migration] Running upgrade 67daae611b6e -> 6b461a21bcfc, uniq_floatingips0floating_network_id0fixed_port_id0fixed_ip_addr
INFO  [alembic.runtime.migration] Running upgrade 6b461a21bcfc -> 5cd92597d11d, Add ip_allocation to port
INFO  [alembic.runtime.migration] Running upgrade 5cd92597d11d -> 929c968efe70, add_pk_version_table
INFO  [alembic.runtime.migration] Running upgrade 929c968efe70 -> a9c43481023c, extend_pk_with_host_and_add_status_to_ml2_port_binding
INFO  [alembic.runtime.migration] Running upgrade a9c43481023c -> 804a3c76314c, Add data_plane_status to Port
INFO  [alembic.runtime.migration] Running upgrade 804a3c76314c -> 2b42d90729da, qos add direction to bw_limit_rule table
INFO  [alembic.runtime.migration] Running upgrade 2b42d90729da -> 62c781cb6192, add is default to qos policies
INFO  [alembic.runtime.migration] Running upgrade 62c781cb6192 -> c8c222d42aa9, logging api
INFO  [alembic.runtime.migration] Running upgrade c8c222d42aa9 -> 349b6fd605a6, Add dns_domain to portdnses
INFO  [alembic.runtime.migration] Running upgrade 349b6fd605a6 -> 7d32f979895f, add mtu for networks
INFO  [alembic.runtime.migration] Running upgrade 7d32f979895f -> 594422d373ee, fip qos
INFO  [alembic.runtime.migration] Running upgrade b67e765a3524 -> a84ccf28f06a, migrate dns name from port
INFO  [alembic.runtime.migration] Running upgrade a84ccf28f06a -> 7d9d8eeec6ad, rename tenant to project
INFO  [alembic.runtime.migration] Running upgrade 7d9d8eeec6ad -> a8b517cff8ab, Add routerport bindings for L3 HA
INFO  [alembic.runtime.migration] Running upgrade a8b517cff8ab -> 3b935b28e7a0, migrate to pluggable ipam
INFO  [alembic.runtime.migration] Running upgrade 3b935b28e7a0 -> b12a3ef66e62, add standardattr to qos policies
INFO  [alembic.runtime.migration] Running upgrade b12a3ef66e62 -> 97c25b0d2353, Add Name and Description to the networksegments table
INFO  [alembic.runtime.migration] Running upgrade 97c25b0d2353 -> 2e0d7a8a1586, Add binding index to RouterL3AgentBinding
INFO  [alembic.runtime.migration] Running upgrade 2e0d7a8a1586 -> 5c85685d616d, Remove availability ranges.
```
重启Nova服务

```bash
systemctl restart openstack-nova-api.service
```
启动网络服务

```bash
systemctl enable neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service neutron-l3-agent.service
systemctl start neutron-server.service neutron-linuxbridge-agent.service neutron-dhcp-agent.service neutron-metadata-agent.service neutron-l3-agent.service
```
## 安装dashboard
安装Dashboard(WEB管理控制台)

安装组件

```bash
yum install openstack-dashboard -y
```
编辑配置/etc/openstack-dashboard/local_settings，如果是在控制节点上添加计算服务则不需要修改

```bash
OPENSTACK_HOST = "controller.openstack.fjf"
ALLOWED_HOSTS = ['controller.openstack.fjf', '192.168.81.40','localhost']
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
         'LOCATION': 'controller.openstack.fjf:11211',
    }
}
OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST
OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = True
OPENSTACK_API_VERSIONS = {
    "identity": 3,
    "image": 2,
    "volume": 2,
}
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = "Default"
OPENSTACK_KEYSTONE_DEFAULT_ROLE = "admin"
OPENSTACK_NEUTRON_NETWORK = {
    ...
    'enable_router': False,
    'enable_quotas': False,
    'enable_distributed_router': False,
    'enable_ha_router': False,
    'enable_lb': False,
    'enable_firewall': False,
    'enable_vpn': False,
    'enable_fip_topology_check': False,
}
TIME_ZONE = "Asia/Shanghai"

```
重启服务

```bash
systemctl restart httpd.service memcached.service
```
访问控制台：http://192.168.81.40/dashboard
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8adb54b355c54a008942b84ee42c5f65.png)
账号/密码

```bash
cat admin-openrc
# 这个账号密码就是用来登陆控制台的，如果要求输入域则参考OS_USER_DOMAIN_NAME
export OS_USERNAME=admin
export OS_PASSWORD=Pass@w0rd
export OS_USER_DOMAIN_NAME=Default

```
下载并导入镜像
导入镜像

下载镜像

```bash
#测试镜像：cirros，最小的一种镜像，只有16M，方便测试
wget http://download.cirros-cloud.net/0.5.1/cirros-0.5.1-x86_64-disk.img
#Centos7镜像
http://cloud.centos.org/centos/7/images/
#其他类型镜像
https://docs.openstack.org/image-guide/obtain-images.html
```
加载admin-openrc

```bash
. admin-openrc
```
导入镜像

```bash
openstack image create "cirros" --file cirros-0.5.1-x86_64-disk.img --disk-format qcow2 --container-format bare --public
+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| checksum         | 1d3062cd89af34e419f7100277f38b2b                     |
| container_format | bare                                                 |
| created_at       | 2021-03-26T11:09:11Z                                 |
| disk_format      | qcow2                                                |
| file             | /v2/images/b3befb16-19c7-4775-ac0a-1961ff269461/file |
| id               | b3befb16-19c7-4775-ac0a-1961ff269461                 |
| min_disk         | 0                                                    |
| min_ram          | 0                                                    |
| name             | cirros                                               |
| owner            | 750d6512fc3043d1b1c6d832465cbf9f                     |
| protected        | False                                                |
| schema           | /v2/schemas/image                                    |
| size             | 16338944                                             |
| status           | active                                               |
| tags             |                                                      |
| updated_at       | 2021-03-26T11:09:11Z                                 |
| virtual_size     | None                                                 |
| visibility       | public                                               |
+------------------+------------------------------------------------------+
```
## 创建网络&虚拟机


创建一个桥接网络，Flat，管理员 -> 网络 -> 网络 -> 创建网络
物理网络名称通过：cat /etc/neutron/plugins/ml2/ml2_conf.ini |grep flat_networks 获取
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/c5aa10b479944b8584abeb29130a5ac3.png)
配置网络信息
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/72e83e0953084a759ce7ab11319710c7.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/949387b0a0d24510801b4fa748eaadbb.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/888a545358dd4cf2ab00ec7975a3b20e.png)
创建实例类型，管理员 -> 计算 -> 实例类型 -> 创建实例类型
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/45422397d25d4c0e9f45c083034715db.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/aa54391c2423430ca63ebe6b88ca5340.png)
创建密钥对，项目 -> 计算 -> 密钥对 -> 导入公钥，创建完会自动下载私钥，也可以导入已经存在的密钥对公钥
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a84626edbfe448cbb9c8ebd8731a80b9.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a466f4c1ddc94b158899e916a32aec07.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/cc50dceb02f941c9ad331e35ad22790a.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/914ce0e922ff4bc88657040b1cde8907.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/dd307e10fcac4686982087e625d52d15.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/94ef5655778948d8968b3b0da64a7a7e.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/43552dc1715e45daaa122a3ede21d38b.png)

可以进入控制台
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/ec81196eb82b4b3e848ad8ddc53d5313.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b0566d45f54146d0b761090c8280ebeb.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/4d6129c9739842ae9a0b6a66542c6a9b.png)
通过SSH连接
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/52d2c910474d45d68de622ca7671a108.png)

