+++
author = "南宫乘风"
title = "Linux 安装后基本优化操作"
date = "2020-09-19 21:55:05"
tags=['运维', 'centos', 'linux', '优化', '安装']
categories=[' Linux实战操作']
image = "post/4kdongman/33.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/108686154](https://blog.csdn.net/heian_99/article/details/108686154)

**目录**

       [1.配置 yum 源](#1.%E9%85%8D%E7%BD%AE%20yum%20%E6%BA%90)

[2.设定 runlevel 3](#2.%E8%AE%BE%E5%AE%9A%20runlevel%203)

[3.精简开机启动服务](#3.%E7%B2%BE%E7%AE%80%E5%BC%80%E6%9C%BA%E5%90%AF%E5%8A%A8%E6%9C%8D%E5%8A%A1)

[4.配置 sudo 授权管理](#4.%E9%85%8D%E7%BD%AE%20sudo%20%E6%8E%88%E6%9D%83%E7%AE%A1%E7%90%86)

[5.ssh 服务](#5.ssh%20%E6%9C%8D%E5%8A%A1)

[6.修改 linux 默认字符集](#6.%E4%BF%AE%E6%94%B9%20linux%20%E9%BB%98%E8%AE%A4%E5%AD%97%E7%AC%A6%E9%9B%86)

[7.服务器时间同步](#7.%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%97%B6%E9%97%B4%E5%90%8C%E6%AD%A5)

[8.加大服务器文件描述符](#8.%E5%8A%A0%E5%A4%A7%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%96%87%E4%BB%B6%E6%8F%8F%E8%BF%B0%E7%AC%A6)

[9.清理 clientmqueue 垃圾文件防止 inode 被占满](#9.%E6%B8%85%E7%90%86%20clientmqueue%20%E5%9E%83%E5%9C%BE%E6%96%87%E4%BB%B6%E9%98%B2%E6%AD%A2%20inode%20%E8%A2%AB%E5%8D%A0%E6%BB%A1)

[10.调整内核优化](#10.%E8%B0%83%E6%95%B4%E5%86%85%E6%A0%B8%E4%BC%98%E5%8C%96)

[11.grep 设置高亮显示](#11.grep%20%E8%AE%BE%E7%BD%AE%E9%AB%98%E4%BA%AE%E6%98%BE%E7%A4%BA)

[Ulimit管理系统资源](#Ulimit%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%E8%B5%84%E6%BA%90)

[linux 上传下载小工具](#linux%20%E4%B8%8A%E4%BC%A0%E4%B8%8B%E8%BD%BD%E5%B0%8F%E5%B7%A5%E5%85%B7)

[tcp/ip 调优](#tcp%2Fip%20%E8%B0%83%E4%BC%98)

[优化总结](#%E4%BC%98%E5%8C%96%E6%80%BB%E7%BB%93)

##  

## 1.配置 yum 源

**1、添加普通用户，使用普通用户 su - root 登陆到 root<br> 2、设置更新源**<br> Linux 下方便安装软件的优秀工具叫做 yum 工具，linux 的二进制软件包一般是 rpm 包，类似windows 下的 exe 程序。<br> 通过 yum 工具安装软件，默认获取 rpm 包的软件配置是从国外 centos 官方源下载。<br> 因此，我们 yum 安装软件速度会比较慢，因此需要把默认获取 rpm 包的配置从国外官方源改为国内。

```
centos 5.8 64 位 yum 源
http://mirrors.sohu.com/help/CentOS-Base-sohu.repo
centos 6.4 64 位 yum 源
http://mirrors.163.com/.help/CentOS6-Base-163.repo
cd /etc/yum.repos.d/ //进入 yum 源7 
/bin/mv CentOS-Base.repo CentOS-Base.repo.ori //备份 yum 源
wget http://mirrors.sohu.com/help/CentOS-Base-sohu.repo //下载 soho 源
/bin/mv CentOS-Base-sohu.repo CentOS-Base.repo
```

<br> 说明：我们现在使用的是互联网上的门户网站提供的 yum 源，将来我们也可以把 iso 镜像或光盘配<br> 置成 yum 源，你还可以自己配置一个像门户网站提供的这种 yum 源<br> 配置公网 yum 源及制作 rpm 包。

<br>**3、使用 yum upgrade 相当于 windows 下的打补丁，这个功能就用到了 yum 源，速度会比较快**

<br>**4、安装必要的软件包**<br>  

```
yum -y install lrzsz
```

<br>**一、关闭 selinux**

由于安装服务、软件中，经常和 selinux 冲突，在国内生产环境中，都是关掉 selinux。

```
vi /etc/selinux/config //配置文件
默认是 enforcing 启用状态
disabled 是完全关闭状态
permissive 是打印警告，selinu 不生效
这种修改只能重启生效
gentenforce 0 临时关闭 selinux，使用 gentenforce 查看当前 selinux 状态
```

### <br>**2.设定 runlevel 3**

```
runlevel 查看当前系统运行级别
vi /etc/inittab //运行级别配置文件
```

### <br>**3.精简开机启动服务**

1、可以使用 setup-system services 里面调整，这样调整起来效率低<br> 2、或者 ntsysv 调出来<br> 3、使用脚本一件关闭

```
#LANG=en
#显示出所有服务的所有运行级别的启动状态 8
chkconfig --list
#停止所有在运行级别 3 上开机启动的服务
for oldboy in `chkconfig --list|grep3:on |awk '{print $1}'`;do chkconfig --level 3
$oldboyoff;done
#在开启常用的服务，crond,network,rsyslog,sshd
for oldboy in crond network rsyslogsshd;do chkconfig --level 3 $oldboy on;done
#显示出所有 3 运行级别下的所有服务(根据需求决定哪个服务启动)
chkconfig --list |grep3:on
```

<br> 刚装完的操作系统，只需要开启几个服务，剩下的以后用到再开，这样安全，遵循最小化原则，没<br> 用的不启动。
- crond 定时任务- network 网络服务- sshd 远程服务- syslog 日志服务
### **4.配置 sudo 授权管理**

<br> 为什么使用 sudo，如果普通用户使用 su - root 切换到管理员。进行非法操作，比如 passwd root<br> 修改 root 密码。那么系统其他用户将无法访问系统。这个普通管理员说白了，已经”功高盖主“<br>**1、在 root 权限下执行 visudo 在 98 行修改。命令使用逗号隔开，使用全路径。**

```
# user MACHINE= COMMANDS
root ALL =（ALL） ALL
用户 机器=（授权哪个角色的权限） /usr/sbin/useradd,/usr/sbin/passwd
如果不授权，默认是不能执行 useradd 命令的
#su - liuyalei //切换到普通用户 liuyalei$sudo /usr/sbin/useradd test //创建 test 用户
```

注意，<br> 前面要加上 sudo，打个比方就是一把钥匙开一把锁。第一次执行 sudo 需要输入普通用户密码，防<br> 止被非法利用。下次 5 分钟内不需要输入密码<br> 如果你是运维经理，带一个小弟，不会吧整个 root 的权限都给他，只给他一些普通权限。目的：既<br> 能让菜的运维干活，又不能威胁系统安全<br> 如果你是小弟，你的运维经历要把自己的账户提升成 root，那么直接复制，把 root 改成经理账号<br> 即可。下次经理直接使用 sudo su - root 就能切到 root 权限下<br> boss ALL =（ALL） ALL<br> 这样做，boss 既有了 root 权限还不知道 root 的密码，但是每次切到 root，都要输入 boss 普通用<br> 户密码，太繁琐了，可以在 visudo 中改成如下，这样就不用输入密码了，但是不安全。

```
boss ALL =（ALL） NOPASSWD： ALL
```

**su 命令总结**<br> 普通用户切换到 root，使用 su - 或者 su - root 需要输入 root 密码<br> 超级用户切换到普通用户不需要密码。但是 centos5.8 会有环境变量问题，需要给普通用户修改环<br> 境变量<br> su 优点是给管理服务器带来方便，但是他的缺点就是大家都知道 root 的密码，而且还能改掉 root<br> 的密码。在一定程度上，对服务器带来了很大的安全隐患。在工作用几乎有一半的问题来自于内部

### 5.ssh 服务

linux 默认管理员 root，port 端口号是 22，为了安全，我们要改掉默认的管理员和端口<br> 配置文件/etc/ssh/sshd_config

```
[root@oldboy ~]# vi /etc/ssh/sshd_config 添加如下内容保存。

52113#→ssh 连接默认的端口，谁都知道，必须要改。
PermitRootLogin no#→root 用户黑客都知道的，禁止它远程登陆。
PermitEmptyPasswords no #→禁止空密码登陆
UseDNSno#→不使用 DNS
GSSAPIAuthentication no

重启 sshd 服务 #
/etc/init.d/sshd restart
```

注意：yum，rpm 安装的软件，启动程序一般都在/etc/init.d

### 6.修改 linux 默认字符集

```
[root@eric6 ~]# cat /etc/sysconfig/i18n //查看 linux 默认的字符集，默认是 UTF-8
LANG="zh_CN.UTF-8"
cp /etc/sysconfig/i18n /etc/sysconfig/i18n.ori //备份默认字符集
echo 'LANG="ZH_CN.GB18030"' &gt;/etc/sysconfig/i18n //修改字符集为 GB18030
```

什么是字符集？<br> 简单的说就是一套文字符号及其编码。常用的字符集有：<br> GBK 定长 双字节 不是国际标准，支持的系统不少<br> UTF-8 非定长 1-4 字节 广泛支持，MYSQL 也使用 UTF-8<br> 这个不一定要修改，有的公司使用的就是 UTF-8，因为 linux 对中文支持不好

### 7.服务器时间同步

如果时间不同步，经常带来业务不正常。如果公司规模小，可以使用联网手动同步，如果服务器多，<br> 可以在公司内部搭建 ntp server。还有一种可能是公司服务器不出外网，比如内部数据库服务器。<br> 可以在内网搭建两台时间服务器，因为一台可能 down 掉，搭建两台可以做到冗余的目的（50 台-100<br> 台以上在用）。

![20200919214559317.png](https://img-blog.csdnimg.cn/20200919214559317.png)

手动同步方法：

```
/sbin/ntpdate time.nist.gov //必须要联网
/usr/sbin/ntpdate time.nist.gov //6.4 在/usr/sbin 下
自动同步方法（每五分钟同步一次）：
echo '#time sync by oldboy at 2010-2-1' &gt;&gt;/var/spool/cron/root
echo '*/5 * * * * /usr/sbin/ntpdate time.nist.gov &gt;/dev/null  2&gt;&amp;1' &gt;&gt;/var/spool/cron/root
```

### 8.加大服务器文件描述符

最简单的说，在 unix/liux 里面，你的服务只要开启一个进程，就要占用文件描述符的。liunx 默认是 1024，如果描述符少了，你的访问量多了，你的服务器支撑不了，所以要把描述符加大。

```
#echo '* - nofile 65535 ' &gt;&gt;/etc/security/limits.conf
#ulimit -n //查看当前文件描述符数量
```

有的时候，你的服务器硬盘/内存没那么大，如果文件描述符过大，访问量过来，有可能把服务器搞垮。但是网友们通常都改成 65535

### 9.清理 clientmqueue 垃圾文件防止 inode 被占满

```
#find /var/spool/clientmqueue/ -type -f |xargs rm -f
```

### 10.调整内核优化

所谓内核优化，主要是在 linux 中针对业务服务应用而进行的系统内核参数优化，优化并无特殊的标准，下面以常见生产环境 linux 的内核优化为例讲解，仅供大家参考：<br>**内核调优**

```
#vi /etc/sysctl.cof
net.ipv4.tcp_fin_timeout = 2
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_keepalive_time = 600
net.ipv4.ip_local_port_range = 4000 65000
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.route.gc_timeout = 100
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_synack_retries = 1
net.core.somaxconn = 16384 12
net.core.netdev_max_backlog = 16384
net.ipv4.tcp_max_orphans = 16384
```

#以下参数是对 iptables 防火墙的优化，防火墙不开会提示，可以忽略不理

```
net.ipv4.ip_conntrack_max = 25000000
net.ipv4.netfilter.ip_conntrack_max=25000000
net.ipv4.netfilter.ip_conntrack_tcp_timeout_established=180
net.ipv4.netfilter.ip_conntrack_tcp_timeout_time_wait=120
net.ipv4.netfilter.ip_conntrack_tcp_timeout_close_wait=60
net.ipv4.netfilter.ip_conntrack_tcp_timeout_fin_wait=120
```

```
[root@eric6 ~]# sysctl -p //使配置文件生效
net.ipv4.ip_forward = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
error: "net.bridge.bridge-nf-call-ip6tables" is an unknown key
error: "net.bridge.bridge-nf-call-iptables" is an unknown key
error: "net.bridge.bridge-nf-call-arptables" is an unknown key
kernel.msgmnb = 65536
kernel.msgmax = 65536
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
net.ipv4.tcp_fin_timeout = 2
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1 13
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_keepalive_time = 600
net.ipv4.ip_local_port_range = 4000 65000
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.route.gc_timeout = 100
net.ipv4.tcp_syn_retries = 1
net.ipv4.tcp_synack_retries = 1
net.core.somaxconn = 16384
net.core.netdev_max_backlog = 16384
net.ipv4.tcp_max_orphans = 16384
error: "net.ipv4.ip_conntrack_max" is an unknown key
error: "net.ipv4.netfilter.ip_conntrack_max" is an unknown key
error: "net.ipv4.netfilter.ip_conntrack_tcp_timeout_established" is an unknown key
error: "net.ipv4.netfilter.ip_conntrack_tcp_timeout_time_wait" is an unknown key
error: "net.ipv4.netfilter.ip_conntrack_tcp_timeout_close_wait" is an unknown key
error: "net.ipv4.netfilter.ip_conntrack_tcp_timeout_fin_wait" is an unknown key 
```

防火墙未开启报错，不用管,5.8 的话，不会报错

### 11.grep 设置高亮显示

```
[root@eric ~]# vi /etc/profile
alias grep='grep --color=auto'
[root@eric ~]# source /etc/profile
```

###  

### Ulimit管理系统资源

具体的 options 含义以及简单示例可以参考以下表格。

![20200919215234278.png](https://img-blog.csdnimg.cn/20200919215234278.png)

![20200919215248854.png](https://img-blog.csdnimg.cn/20200919215248854.png)

### linux 上传下载小工具

```
yum install lrzsz -y
```

### tcp/ip 调优

sysctl 变量修改方法：sysctl –a<br> 使用 sysctl 命令修改系统变量，和通过编辑 sysctl.conf 文件来修改系统变量两种。但并不是所有的<br> 变量都可以在这个模式下设定。<br> 注：sysctl 变量的设置通常是字符串、数字或者布尔型。 (布尔型用 1 来表示'yes'，用 0 来表示'no')。

```
[root@localhost ~]#sysctl -w net.ipv4.tcp_keepalive_time=30
[root@localhost ~]#sysctl -w net.ipv4.tcp_keepalive_probes=2
[root@localhost ~]#sysctl -w net.ipv4.tcp_keepalive_intvl=2
[root@localhost~]# sysctl -a | grep keepalive
net.ipv4.tcp_keepalive_time= 30
net.ipv4.tcp_keepalive_probes= 2
net.ipv4.tcp_keepalive_intvl= 2

执行以下命令使变动立即生效： 
[root@localhost ~]# sysctl
```

 

 

centos 6.4 安装软件包：<br> 软件自定义-基本<br> 性能工具<br> 调试工具兼容程序库 <br> 开发工具<br> 服务器----系统管理工具<br> 系统管理---snmp/系统管理

### <br>**优化总结**
- 01）添加普通用户，通过 sudo 授权管理- 02）定时自动更新服务器时间- 03）配置 yum 更新源- 04）关闭 selinux 和 iptables- 05）调整文件描述符数量- 06）定时自动清理/var/spool/clientmquene/目录垃圾文件，防止 inodes 节点被占满- 07）精简开机自动启动服务（sshd，crond，network，syslog）- 08）内核参数优化/etc/sysctl.config，sysctl -p 生效- 09）更改默认 ssh 服务端口，及禁止 root 用户远程登陆- 10）更改字符集，支持中文- 11）锁定关键系统文件
```
chattr +i /etc/passwd
chattr +i /etc/inittab
chattr +i /etc/group
chattr +i /etc/shadow
chattr +i /etc/gshadow
```
- 12）清空/etc/issue，去除系统及内核版本登陆前的屏幕显示- 13）更改系统登录后的信息 /etc/motd