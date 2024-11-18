---
author: 南宫乘风
categories:
- 项目实战
date: 2024-06-20 17:00:04
description: 、背景在很多组织中，需要对用户和系统进行统一的身份认证和授权管理。为了实现这一目标，通常会使用轻量级目录访问协议来构建集中化的身份认证和授权服务。而在生产环境中，为了保证高可用性和可扩展性，需要构建主。。。。。。。
image: ../../title_pic/63.jpg
slug: '202406201700'
tags:
- php
- 服务器
- 开发语言
title: 生产环境OpenLDAP主从集群
---

<!--more-->

## 1、背景
在很多组织中，需要对用户和系统进行统一的身份认证和授权管理。为了实现这一目标，通常会使用LDAP（轻量级目录访问协议）来构建集中化的身份认证和授权服务。而在生产环境中，为了保证高可用性和可扩展性，需要构建OpenLDAP主从集群来提供稳定的身份认证服务。


## 2、环境
在开始部署之前，需要准备以下环境：

- 操作系统：Centos7
- OpenLDAP版本：OpenLDAP: slapd 2.4.44 
- 服务器数量：2台（1台主服务器和1台从服务器）
- 网络环境：两台服务器应在同一局域网内，确保网络连接稳定
##  3、主节点安装
清参考下方链接
[https://blog.csdn.net/heian_99/article/details/138963912](https://blog.csdn.net/heian_99/article/details/138963912)

![在这里插入图片描述](../../image/59148cabef2b4bb2b026c31ab3ea80dc.png)

## 4、从节点安装
假设master节点的地址为192.168.102.20。对于master节点，完全参照前述章节操作并配置好。

对于slave节点，也参照前述章节安装并配置，但只到执行ldapdomain.ldif文件后就行。也就是设置了管理员用户账号就行，不用添加部门或其它人员信息。另外，phpLDAPadmin可以安装。

### 1、配置master节点
在master节点上，我们需要导入相关的信息。

创建syncprov_mod.ldif文件：

```bash
cat > syncprov_mod.ldif << "EOF"
dn: cn=module,cn=config
objectClass: olcModuleList
cn: module
olcModulePath: /usr/lib64/openldap
olcModuleLoad: syncprov.la
EOF
```
执行：

```bash
ldapadd -Y EXTERNAL -H ldapi:/// -f syncprov_mod.ldif
```

创建syncprov.ldif文件：

```bash
cat > syncprov.ldif << "EOF"
dn: olcOverlay=syncprov,olcDatabase={2}hdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcSyncProvConfig
olcOverlay: syncprov
olcSpCheckpoint: 1 1
olcSpSessionLog: 1024
EOF
```
执行：

```bash
ldapadd -Y EXTERNAL -H ldapi:/// -f syncprov.ldif
```

### 2、配置slave节点
在slave节点上配置主从。

创建rp.ldif文件：

```bash
cat > rp.ldif << "EOF"
dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcSyncRepl
olcSyncRepl: rid=001
    provider=ldap://192.168.102.20:389
    bindmethod=simple
    binddn="cn=Manager,dc=fujfu,dc=com"
    credentials=examplePassword
    searchbase="dc=fujfu,dc=com"
    scope=sub
    schemachecking=on
    type=refreshAndPersist
    retry="30 5 300 3"
    attrs="*,+"
    interval=00:00:02:00
EOF
```
provider表示master的地址，其他的都是些基础信息。需要注意的是认证用户一定要使用超级管理员，如果使用普通用户连接master的话，slave将不会同步用户的密码字段信息。credentials是管理员的密码。
执行：

```bash
ldapmodify -Y EXTERNAL -H ldapi:/// -f rp.ldif
```

除此之外，为了优化openldap的查询速度，我们添加了相关字段属性的索引。

```bash
cat > index.ldif << "EOF"
dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcDbIndex
olcDbIndex: uid eq,pres
olcDbIndex: uniqueMember eq,pres
olcDbIndex: uidNumber,gidNumber eq,pres
olcDbIndex: member,memberUid eq,pres
olcDbIndex: entryUUID eq
olcDbIndex: entryCSN eq
EOF
```
执行：

```bash
ldapadd -Y EXTERNAL -H ldapi:/// -f index.ldif
```
### 3、验证主从正确性
slave机器上配置完毕后，无需重启master机器和slave机器的slapd服务。

在slave机器上查看openldap日志，如下：

```bash
journalctl -u slapd -n 100 -f
```
![在这里插入图片描述](../../image/2e1c0382b524416784e37028f67972f3.png)
通过上图，我们可以很明显的看到slave机器上slapd服务没有报错，而且已经在同步相关openldap数据。

现在切换到master机器上查看openldap日志，如下：

```bash
journalctl -u slapd -n 100 -f
```
![在这里插入图片描述](../../image/8156c4fc8ec64ec3ad3fd628fa61b532.png)
通过上图我们也可以发现master没有报错，而且也看到slave机器已经在同步信息了。

现在我们再使用phpLDAPadmin工具，登录slave查看相关信息，如下：
![在这里插入图片描述](../../image/0623a1554d584eff844ba9bf9fd60113.png)

通过上图，我们可以看到slave节点上已经有账号信息了。这也就说明OpenLDAP的master-slave已经在正常同步数据。

### 4、测试
可测试如下两点：
1、在master节点上修改用户字段信息，slave节点上应能同步到修改信息。
2、在slave节点修改用户字段信息，应该无法操作。因为我们采用的主从模式中，slave节点是自读的。

如果测试无问题，说明我们的主从的确正常运行。
LDAP查看命令
附ldap查看配置命令：
ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=config
ldapsearch -x cn=test -b dc=local,dc=cn
