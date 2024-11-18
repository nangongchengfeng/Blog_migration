---
author: 南宫乘风
categories:
- 项目实战
date: 2024-05-16 15:44:43
description: 简介什么是目录服务？一个目录，除了支持基本的查找和更新功能外，是一个特别设计用来搜索和浏览的专门的数据库。目录倾向于包含描述性的、基于属性的信息，并支持精细的过滤能力。目录通常不支持复杂的事务和回滚机。。。。。。。
image: ../../title_pic/76.jpg
slug: '202405161544'
tags:
- java
- 开发语言
- OpenLDAP
- 工具
title: 生产环境 OpenLDAP 部署流程
---

<!--more-->

# **LDAP 简介**

**什么是目录服务(directory service)？**

一个目录，除了支持基本的查找和更新功能外，是一个特别设计用来搜索和浏览的专门的数据库。目录倾向于包含描述性的、基于属性的信息，并支持精细的过滤能力。目录通常不支持复杂的事务和回滚机制，这与关系数据库不一样。

**什么是 LDAP？**

LDAP 代表轻量目录访问协议(Lightweight Directory Access Protocol)。正如名称中所暗示的，它是一个用于访问目录服务的轻量协议，具体来说，是基于 X.500 的目录服务。

什么样的信息可以存储在目录中？LDAP 信息模型是基于条目(entries)的。一个条目(entry)是一些属性的集合，它有一个全局唯一的可辨识名称(Distinguished Name，DN)。DN 用于无歧义地引用该条目。条目的每一个属性都由一个类型(type)和一个或多个值(values)构成。类型通常是一个助记符字符，比如“cn”代表 common name，“mail”代表 email address。值的语法取决于属性类型。比如，一个 cn 属性的值可能是 Babs Jensen，一个 mail 属性的值可能是 babs@example.com，一个 jpegPhoto 属性可能包含一个 JPEG(二进制)格式的照片。


温馨提示：dn 必须是全局唯一的。

LDAP 中，将数据组织成一个树形结构，这与现实生活中的很多数据结构可以对应起来，而不像设计关系型数据库的表，需要进行多种变化。如下图所展示的就是一个树形结构的数据。
![在这里插入图片描述](../../image/c69dce35abf94265bd431a0cf9d0c094.png)
在上图所示的树形结构中，树的根结点是一个组织的域名（node3.com，可以根据自己意愿配），其下分为 2 个部分，分别是 ou=admin 和 dc=hdp，dc=hdp 下面又分 ou=people 和 ou=group。admin 用来管理所有管理人员，people 用来管理登录系统的用户，group 用来管理系统中的用户组。当然，在该图中还可继续增加其他分支。

对于图中所示的树形结构，使用关系数据库来保存数据的话，需要设置多个表，一层一层分别保存，当需要查找某个信息时，再逐层进行查询，最终得到结果。

若使用目录来保存该图中的数据，则更直观。图中每个结点用一个条目来保存，不同类型的结点需要保存的数据可能不同，在 LDAP 中通过一个称为 objectClass 的类型来控制不同结点需要的数据（称为属性）。

参考文章：[https://blog.csdn.net/weixin_42578481/article/details/80863890](https://blog.csdn.net/weixin_42578481/article/details/80863890)

**名词解释：**

* DC：domain component，一般为公司名，例如：dc=163,dc=com

* OU：organization unit，为组织单元，最多可以有四级，每级最长 32 个字符，可以为中文

* CN：common name，为用户名或者服务器名，最长可以到 80 个字符，可以为中文

* DN：distinguished name，为一条 LDAP 记录项的名字，有唯一性，例如：dc:”cn=admin,ou=developer,dc=163,dc=com”

**图形示例**

上边来了一堆的名词解释，看的云里雾里，还不是很明白，怎么跟自己的组织架构对应起来呢？看看下边的图是不是清晰明了
![在这里插入图片描述](../../image/5dd3f5188a1445569a8c4aad4d4a8f33.png)

# **部署 OpenLDAP**

### 说明

下面是 LDAP 中的一些术语：

* **entry**(条目)：LDAP 目录中的一个单位。每一个条目都由它的唯一的可辨识名称(**Distinguished**** Name **，** DN**)来唯一确定。

* **attribute**(属性)：与一个 entry 直接关联的信息。比如，如果使用一个 LDAP entry 来代表一个组织的话，那么，与该组织相关联的属性可能包括一个地址、一个传真号码，等等。

一个属性可能有一个单一的值，或者是未排序的、空格分隔开来的值的列表。有一些属性是可选的，有一些则是必须的。必须的属性使用 **objectClass** 定义来指定，可以在 **/etc/openldap/slapd.d/cn=config/cn=schema/** 目录下的 schema 文件中找到。

一个属性和它相应值的断言(assertion)也被称为是一个相对可辨识的名称(**Relative**** Distinguished Name **，** RDN**)。与 Distinguished Name(它是全局唯一的)不同的是，Relative Distinguished Name 只在每个条目中是唯一的。

* **LDIF**：LDAP 数据交换格式(LDAP Data Interchange Format，LDIF)是一个 LDAP entry 的纯文本表现形式。它有如下格式：
![在这里插入图片描述](../../image/b3d1a65babc04001a397961e786ffea7.png)
*id* 是可选的，是一个数字，它由应用程序决定，被用来编辑该条目。每一个条目可以包含任意数量的 *attribute_type* 和 *attribute_value* 对，只要它们都在相应的 schema file 中定义了就行。空白行代表了该条目的结束。

* **schema** 文件：简单来说，可以理解为模板文件，是对 OpenLDAP 配置文件中所能使用的属性进行限定的文件。
### **安装 OpenLDAP 套件**

OpenLDAP 套件包含如下软件包：

| 软件包名         | 说明                                                                                |
| ------------------ | ------------------------------------------------------------------------------------- |
| openldap         | 包含运行 OpenLDAP server 和 client 端应用程序所需的库。                             |
| openldap-clients | 包含命令行工具，用于查看和修改 LDAP server 上的目录。                               |
| openldap-servers | 包含用于配置和运行一个 LDAP server 的服务和工具。这包括一个独立的 LDAP 服务程序，**slapd**。 |
| compat-openldap  | 包含 OpenLDAP 兼容库。                                                              |

要搭建一个基本的 LDAP 服务器，安装如下软件包：

```bash
[root@gw ~]# yum install openldap openldap-clients openldap-servers
```

我这里安装的是 2.4.44 版本的 openldap：

![在这里插入图片描述](../../image/3f2402bc1f6548bdac4da128ea49d8a9.png)
## **启动 OpenLDAP 服务**

直接启动 OpenLDAP 服务并设置开机启动：

```bash
[root@gw ~]# systemctl start slapd
[root@gw ~]# systemctl enable slapd
```

## **配置 OpenLDAP 服务**

OpenLDAP 的配置文件和目录：

| 配置文件 | 说明                                                                                                                           |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------- |
|  **/etc/openldap/ldap.conf**         | 使用 OpenLDAP 库的客户端应用程序的配置文件。包括 ldapadd、ldapsearch、Evolution 等。关于该文件中配置的详细说明，可执行 **man ldap.conf** 命令。 |
|  **/etc/openldap/slapd.d/**         | 包含 slapd 配置文件的目录。关于该目录下配置的详细说明，可执行 **man slapd-config** 命令。                                                          |

注意，OpenLDAP 服务进程已不再从/etc/openldap/slapd.conf 文件读取它的配置，它的是使用位于/etc/openldap/slapd.d/目录下的配置。但是，不要手动去修改里面的配置，而应该使用**客户端工具**，比如 ldapmodify。

该目录下的配置文件的结构类似于下面这样(这里省略了一些配置文件，只是为了便于解释)：

![在这里插入图片描述](../../image/9cb6ab076850434989c39896b9b300f3.png)
可以看到，树的根节点是“**cn=config**”条目，即 **cn=config.ldif** 文件，它包含全局的配置。其它的设置包含在 **cn=config** 文件夹下的各子条目中。

实际来说，cn=config 文件夹下有如下这些文件：

![在这里插入图片描述](../../image/b573e889adc648429587c6ebe6496961.png)

* **cn=schema.ldif** 文件：包含 schema 相关的设置。“**cn=schema,cn=config**”条目包含了该系统的 schema(所有硬编码到 slapd 中的 schema)。

* **olcDatabase={0}config.ldif** 文件：该文件是特殊的，用于设置 OpenLDAP config 数据库自身。

* **olcDatabase={-1}frontend.ldif** 文件：该文件包含 OpenLDAP 前端(front end)的相关配置，并定义了全局的数据库选项，比如访问控制列表(ACL)。该文件是特殊的，它里面的设置会被其它数据库所继承，除非它们显式进行了重新定义。

* **olcDatabase={1}monitor.ldif** 文件：该文件包含 OpenLDAP 监控后端(monitor back end)的相关配置。当启用时，它是自动生成的，并且会使用 OpenLDAP 服务的运行状态信息来动态地更新它。

* **olcDatabase={2}hdb.ldif** 文件：该文件包含 hdb 数据库后端(database back end)的相关配置。默认情况下，OpenLDAP 使用 **hdb** 作为它的数据库后端。不过，官方文档中说，hdb 已弃用，推荐使用 **mdb** 作为数据库后端。

这些文件是自动生成的，不要手动去编辑它，要使用 ldapmodify 这类工具。当然，我们可以使用 cat 命令去查看它的内容。

**ldif 文件的语法**：在 ldif 文件中，'#' 符号开头的行是注释语句。如果某一行以一个空格开头，该行会被认为是前一行的延续(即便上一行是一个注释语句)并且该单一的打头的空格会被移除。不同的条目(entries)之间以空行分隔开。


#### **生成哈希后的密码**

执行 slappasswd 命令，输入你打算使用的密码，生成该密码哈希后的值：

```shell
[root@gw ~]# slappasswd
New password:                                                  # 输入你打算使用的密码
Re-enter new password:                                          # 再次输入
{SSHA}XGQdioFMQPvxjs8z1YeT7RIyn3FJTURB                     # 得到经过哈希后的密码
```

#### **设置 OpenLDAP config 数据库的密码**

随便找个目录，创建个 ldif 文件，文件名随意，只要扩展名是 ldif 就行：

```shell
[root@gw ~]# vim ldaprootpasswd.ldif
dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}XGQdioFMQPvxjs8z1YeT7RIyn3FJTURB
```

* **dn**：这里输入我们想要进行更改的条目的 dn 名称。这里实际指向的是 cn=config/olcDatabase={0}config.ldif 这个文件，即 OpenLDAP 的 config 数据库文件。

* **changetype**：值为 modify，表示我们想要对目标条目进行的是修改操作。

* **add**：值为 olcRootPW，表示我们想要给目标条目添加一个 olcRootPW 属性。

* **olcRootPW**：这里输入前面得到的哈希后的密码字符串。表示我们想要把 olcRootPW 属性的值设为这个值。直接使用明文的密码也可以，但不建议这样做，因为明文密码直接写配置文件中，很容易泄露出去嘛。


ldapadd 是一个往 LDAP 中添加新条目(或给现有条目添加新属性)的工具。使用 ldapadd 命令实际执行该 ldif 文件，对 OpenLDAP 条目进行修改：

```shell
[root@gw ~]# ldapadd -Y EXTERNAL -H ldapi:/// -f ldaprootpasswd.ldif

```

* -Y 选项：指定在连接 LDAP 服务器时所要使用的 SASL 认证机制。EXTERNAL 不知道是什么机制来的，就直接使用吧
* -H 选项：所要连接的 LDAP 服务器的 URI 地址。
* -f 选项：所要执行的 ldif 文件。

#### **配置 LDAP 数据库**

拷贝示例数据库配置文件到 **/var/lib/ldap** 目录(这个是默认的 hdb 数据库后端的数据目录)，并设置所属用户和组(与 slapd 服务程序的属主相同)。这个实际使用的数据库类型为 Oracle Berkeley DB。

```shell
[root@gw ~]# cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG
[root@gw ~]# chown -R ldap:ldap /var/lib/ldap/DB_CONFIG 
[root@gw ~]# systemctl restart slapd
```

从 **/etc/openldap/schema** 目录下导入几个基本的 LDAP schema 文件：

```bash
[root@gw ~]# ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
[root@gw ~]# ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif
[root@gw ~]# ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif
```

接下来，添加你的域到 LDAP。创建一个 ldif 文件，在下面的文件中，**example** 字符串可以使用你的域替代，**olcRootPW** 值则使用哈希得到的密码字符串替代：

```bash
[root@gw ~]# vim ldapdomain.ldif
#修改olcDatabase={1}monitor.ldif文件的olcAccess属性值
dn: olcDatabase={1}monitor,cn=config
changetype: modify
replace: olcAccess
olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth"
  read by dn.base="cn=Manager,dc=example,dc=com" read by * none

#修改olcDatabase={2}hdb.ldif文件的olcSuffix属性值
dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=example,dc=com

#修改olcDatabase={2}hdb.ldif文件的olcRootDN属性值
dn: olcDatabase={2}hdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=Manager,dc=example,dc=com

#向olcDatabase={2}hdb.ldif文件中添加olcRootPW属性和值
dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}XGQdioFMQPvxjs8z1YeT7RIyn3FJTURB

#向olcDatabase={2}hdb.ldif文件中添加olcAccess属性和值，多个olcAccess项
dn: olcDatabase={2}hdb,cn=config
changetype: modify
add: olcAccess
olcAccess: {0}to attrs=userPassword,shadowLastChange by
  dn="cn=Manager,dc=example,dc=com" write by anonymous auth by self write by * none
olcAccess: {1}to dn.base="" by * read
olcAccess: {2}to * by dn="cn=Manager,dc=example,dc=com" write by * read
```

* **olcAccess**：ACL 规则，设置指定用户(by 后接的)对指定资源(条目和/或属性)的权限(read、write)。在 frontend 中设置的 ACL 规则会被附加到其它任意特定数据库的 ACL 规则后。特定数据库的 rootdn 总是具有读写那个数据库所有东西的权限。

* **olcSuffix**：用于指定特定数据库的 DN 后缀。比如，后缀为“dc=example,dc=com”的查询都将被转发到该后端数据库。dc 的值可以自行设定。如有多个，也还可再加，比如“dc=gate,dc=ykd,dc=fujfu,dc=com”。

* **olcRootDN**：用于指定管理该数据库的 Root DN 的名称。默认为空，表示不指定 root 用户。如果 Root DN 是位于 olcSuffix 指定的 DN 后缀的里面，那么也必须使用 olcRootPW 来设定 Root DN 的密码。

执行该 ldif 文件，对 LDAP 实际进行修改：

```bash
[root@gw ~]# ldapmodify -Y EXTERNAL -H ldapi:/// -f ldapdomain.ldif
```


接下来，我们添加一些条目到 LDAP 目录中。创建个 ldif 文件：

```bash
[root@gw ~]# vim baseldapdomain.ldif
dn: dc=example,dc=com
objectClass: top
objectClass: dcObject
objectclass: organization
o: example com
dc: example

dn: cn=Manager,dc=example,dc=com
objectClass: organizationalRole
cn: Manager
description: Directory Manager

dn: ou=People,dc=example,dc=com
objectClass: organizationalUnit
ou: People

dn: ou=Group,dc=example,dc=com
objectClass: organizationalUnit
ou: Group
```

* **o** 属性：在 schema 文件中，o 代表 organizationName，组织名称。

* **dc** 属性：在 schema 文件中，dc 代表 domainComponent，域部件。

* **ou** 属性：在 schema 文件中，ou 代表 organizationalUnitName，组织单元名称。

执行该 ldif 文件。执行该命令后，会提示你输入 LDAP root 用户密码。

```bash
[root@gw ~]# ldapadd -x -W -D "cn=Manager,dc=example,dc=com" -f baseldapdomain.ldif
```

*  **-x** 选项：使用简单认证(simple authentication)而不是 SASL。

*  **-W** 选项：提示输入用于简单认证的密码。这与直接在命令行指定密码是不同的。

*  **-D** 选项：使用指定的 DN 名称来绑定到 LDAP 目录。


接下来，创建一个 LDAP 用户 tecmint，并为它设置一个密码：

```bash
[root@gw ~]# useradd tecmint
[root@gw ~]# passwd tecmint
```

创建一个 ldif 文件，为 LDAP group 进行定义：

```bash
[root@gw ~]# vim ldapgroup.ldif
dn: cn=Manager,ou=Group,dc=example,dc=com
objectClass: top
objectClass: posixGroup
gidNumber: 1002
```

在上面的配置中，gidNumber 是/etc/group 文件中 tecmint 的 GID，并将它添加到 OpenLDAP 目录。

执行该 LDIF 文件：

```bash
[root@gw ~]# ldapadd -x -W -D "cn=Manager,dc=example,dc=com" -f ldapgroup.ldif
```

接下来，创建另一个 ldif 文件，添加 tecmint 用户的定义：

```bash
[root@gw ~]# vim ldapuser.ldif
dn: uid=tecmint,ou=People,dc=example,dc=com
objectClass: top
objectClass: account
objectClass: posixAccount
objectClass: shadowAccount
cn: tecmint
uid: tecmint
uidNumber: 1002
gidNumber: 1002
homeDirectory: /home/tecmint
userPassword: {SSHA}E6DO8V0dK5km8ZTJzCE0QO++/EX8GFax                 #该用户的密码哈希后的字符串
loginShell: /bin/bash
gecos: tecmint
shadowLastChange: 0
shadowMax: 0
shadowWarning: 0
```

执行该 LDIF 文件：

```bash
[root@gw ~]# ldapadd -x -W -D "cn=Manager,dc=example,dc=com" -f ldapuser.ldif
```

## **安装 phpLDAPadmin**

安装 phpLDAPadmin：

```bash
[root@gw ~]# yum install epel-release
[root@gw ~]# yum install phpldapadmin
```

事实上，这不仅安装了 phpldapadmin，还安装了 http、php 等相关的依赖。phpldapadmin 其实就是运行在 httpd 程序的 php 模块上的一个 php 应用。

修改 httpd 配置文件，修改 httpd 与 phpldapadmin 集成的配置文件，如下：

```bash
[root@gw ~]# vim /etc/httpd/conf.d/phpldapadmin.conf
Alias /phpldapadmin /usr/share/phpldapadmin/htdocs
Alias /ldapadmin /usr/share/phpldapadmin/htdocs

<Directory /usr/share/phpldapadmin/htdocs>
  <IfModule mod_authz_core.c>
    # Apache 2.4
    Require all granted
  </IfModule>
  <IfModule !mod_authz_core.c>
    # Apache 2.2
    Order Deny,Allow
    Deny from all
    Allow from 127.0.0.1
    Allow from ::1
  </IfModule>
</Directory>
```

修改 phpldapadmin 的配置文件，如下：

```bash
[root@gw ~]# vim /etc/phpldapadmin/config.php
<?php
$config->custom->session['blowfish'] = '036b0f2d39d36791dd3a8effa7c3411f';              # 值是自动生成的
$config->custom->appearance['hide_template_warning'] = true;                        # 避免不必要的告警信息提示
$config->custom->appearance['minimalMode'] = true;                           # 不要页面头和注脚，使页面更简洁
$config->custom->appearance['friendly_attrs'] = array(
        'facsimileTelephoneNumber'  => 'Fax',
        'gid'                         => 'Group',
        'mail'                        => 'Email',
        'telephoneNumber'           => 'Telephone',
        'uid'                         => 'User Name',
        'userPassword'               => 'Password'
);
$servers = new Datastore();
$servers->newServer('ldap_pla');
$servers->setValue('server','name','Local LDAP Server');
$servers->setValue('server','host','172.31.2.6');                                # LDAP服务器的地址
$servers->setValue('server','port',389);
$servers->setValue('server','base',array('dc=example,dc=com'));               # LDAP域的base DNs
$servers->setValue('login','auth_type','session');
$servers->setValue('appearance','password_hash','');
$servers->setValue('login','attr','dn');                                         # 取消注释
// $servers->setValue('login','attr','uid');                                      # 添加注释
$servers->setValue('unique','attrs',array('uid','sn'));
?>
```

用户登录方式，在此我们使用的是 dn 方式进行登录，phpldapadmin 默认使用的是 uid 方式进行登录。

unique 唯一性，在此我们使用的是 uid 和 sn 作为唯一的标志，这个一定要注意下。特别是从一个用户复制为另外一个用户时，要使用到该配置。

启动 httpd：

```bash
[root@gw ~]# systemctl start httpd 
[root@gw ~]# systemctl enable httpd
```

## **访问 phpLDAPadmin**

访问 phpLDAPadmin 地址 **http://**​***server_ip***​ **/ldapadmin/** ：
![在这里插入图片描述](../../image/d62f8224cbcd480c8ebbf2e88fcebce6.png)
![在这里插入图片描述](../../image/83746165b413425497d8d520d0fd678e.png)
上述截图中，登录 DN，如果是 OpenLDAP 管理员登录的话，使用 cn=Manager,dc=example,dc=com。

如果是 OpenLDAP 普通用户登录的话，使用 uid=tecmint,ou=People,dc=example,dc=com。



