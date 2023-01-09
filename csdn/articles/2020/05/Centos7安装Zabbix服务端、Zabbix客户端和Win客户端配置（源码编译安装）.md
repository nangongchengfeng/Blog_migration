+++
author = "南宫乘风"
title = "Centos7安装Zabbix服务端、Zabbix客户端和Win客户端配置（源码编译安装）"
date = "2020-05-09 18:03:18"
tags=['linux', 'centos', 'zabbix', '监控', 'zabbix_agent']
categories=['Zabbix监控']
image = "post/4kdongman/03.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/106023595](https://blog.csdn.net/heian_99/article/details/106023595)

**目录**

 

[1、宝塔安装和配置环境](#1%E3%80%81%E5%AE%9D%E5%A1%94%E5%AE%89%E8%A3%85%E5%92%8C%E9%85%8D%E7%BD%AE%E7%8E%AF%E5%A2%83)

[2、安装依赖和编译安装](#2%E3%80%81%E5%AE%89%E8%A3%85%E4%BE%9D%E8%B5%96%E5%92%8C%E7%BC%96%E8%AF%91%E5%AE%89%E8%A3%85)

[3、配置数据库](#3%E3%80%81%E9%85%8D%E7%BD%AE%E6%95%B0%E6%8D%AE%E5%BA%93)

[4、配置Zabbix服务端](#4%E3%80%81%E9%85%8D%E7%BD%AEZabbix%E6%9C%8D%E5%8A%A1%E7%AB%AF)

[5、配置Zabbix的Web端](#5%E3%80%81%E9%85%8D%E7%BD%AEZabbix%E7%9A%84Web%E7%AB%AF)

[6、配置Linux客户端](#6%E3%80%81%E9%85%8D%E7%BD%AELinux%E5%AE%A2%E6%88%B7%E7%AB%AF)

[7、配置Windows客户端](#7%E3%80%81%E9%85%8D%E7%BD%AEWindows%E5%AE%A2%E6%88%B7%E7%AB%AF)

[8、在zabbix服务器添加主机](#%E4%B8%89%E5%9C%A8zabbix%E6%9C%8D%E5%8A%A1%E5%99%A8%E6%B7%BB%E5%8A%A0%E4%B8%BB%E6%9C%BA)

Centos7上使用宝塔面板配置LNMP环境安装zabbix4.2

# 1、宝塔安装和配置环境

**[Centos7安装宝塔控制面板](https://blog.csdn.net/heian_99/article/details/101266165)**

**[Zabbix4.2.2的源码包（包括Win）](https://download.csdn.net/download/heian_99/12403970)**

**L：Linux**

**N：Nginx**

**M：Mysql**

**P：PHP**

![20200509171022419.png](https://img-blog.csdnimg.cn/20200509171022419.png)

![202005091712413.png](https://img-blog.csdnimg.cn/202005091712413.png)/2‘’

# 2、安装依赖和编译安装

```
yum install -y wget telnet net-tools python-paramiko gcc gcc-c++ dejavu-sans-fonts python-setuptools python-devel sendmail mailx net-snmp net-snmp-devel net-snmp-utils freetype-devel libpng-devel perl unbound libtasn1-devel p11-kit-devel OpenIPMI unixODBC  libevent-devel 

```

首先添加zabbix用户和zabbix组

```
groupadd zabbix
useradd -g zabbix -s /sbin/nologin zabbix
```

然后下载zabbix4.2编译安装包

执行

```
wget https://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/4.2.4/zabbix-4.2.4.tar.gz
tar -zxvf zabbix-4.2.4.tar.gz 
cd zabbix-4.2.4
```

执行帮助查看编译安装选项

```
./configure --help
```

![20200509172136180.png](https://img-blog.csdnimg.cn/20200509172136180.png)

我采取的是尽量多安装模块

```
./configure --prefix=/data/zabbix --enable-server --enable-proxy --enable-agent --enable-ipv6  --with-mysql --with-net-snmp --with-libcurl --with-openipmi --with-openssl --with-libcurl --with-libxml2 
```

说明：<br> 1、对于虚拟机监视--with-libcurl和--with-libxml2配置选项是必需的<br> 2、enable proxy,agent是启用代理<br> 3、with-net-snmp with-mysql是配置snmp和mysql支持<br> 4、在编译过程中，如果提示错误，则是某些扩展包没有安装，进行yum安装即可

![20200509172251298.png](https://img-blog.csdnimg.cn/20200509172251298.png)

在检查配置无误后，执行安装

```
make install
```

# 3、配置数据库

然后配置数据库。在宝塔面板中可以查看和修改数据库root密码

![20200509172339296.png](https://img-blog.csdnimg.cn/20200509172339296.png)

![20200509172349206.png](https://img-blog.csdnimg.cn/20200509172349206.png)

完成数据创建后，导入数据库

```
mysql -uzabbix -pzabbix -hlocalhost zabbix &lt; database/mysql/schema.sql
mysql -uzabbix -pzabbix -hlocalhost zabbix &lt; database/mysql/images.sql
mysql -uzabbix -pzabbix -hlocalhost zabbix &lt; database/mysql/data.sql
```

导入完毕后，可以在宝塔面板的phpMyadmin中查看数据库详细

![20200509172420290.png](https://img-blog.csdnimg.cn/20200509172420290.png)

# 4、配置Zabbix服务端

然后进入zabbix安装目录/usr/local/zabbix配置zabbix.conf配置文件

```
vim /data/zabbix/etc/zabbix_server.conf
```

![20200509172717309.png](https://img-blog.csdnimg.cn/20200509172717309.png)

然后关闭centos上防火墙，selinux等

```
systemctl stop firewalld
systemctl disable firewalld
```

Zabbix前端是用PHP编写的，因此要运行它需要PHP支持的Web服务器。只需将PHP文件从frontends / php复制到webserver HTML文档目录即可完成安装。

在使用宝塔面板安装LNMP环境后，会自动配置nginx，同时会在跟目录下创建WWW目录，存放WEB服务器等信息。

![20200509173006151.png](https://img-blog.csdnimg.cn/20200509173006151.png)

### 5、配置Zabbix的Web端

再宝塔面板网站中，添加新的站点

说明<br> 1、域名一般使用公网域名<br> 2、没有公网域名，内网中使用.lcoal或者其他不冲突的域名格式代替即可<br> 3、使用ip地址业务可以

![20200509173107841.png](https://img-blog.csdnimg.cn/20200509173107841.png)

完成域名配置后，将zabbix-4.2.4目录中的frontends / php/下的文件复制到站点目录

```
cd zabbix-4.2.4
cp -r frontends/php/* /www/wwwroot/zabbix/  #此文件就是之前创建的站点
```

完成之后，再软件商店中调整以下php设置

![20200509173136849.png](https://img-blog.csdnimg.cn/20200509173136849.png)

根据zabbix要求，调整max_input_time 由60改为300,同时调整时区date.timezone为.Asia/Shanghai,然后保存设置

![20200509173153451.png](https://img-blog.csdnimg.cn/20200509173153451.png)

**然后启动zabbix和zabbix-agent**

```
/data/zabbix/sbin/zabbix_server
/data/zabbix/sbin/zabbix_agentd 
```

然后再浏览器中输入ip/setup.php(服务器IP地址），进行配置zabbix

![20200509173401552.png](https://img-blog.csdnimg.cn/20200509173401552.png)

提示缺少php ldap的警告

![20200509173421500.png](https://img-blog.csdnimg.cn/20200509173421500.png)

无视，点击下一步<br> 配置mysql

![20200509173433478.png](https://img-blog.csdnimg.cn/20200509173433478.png)

然后这里提示报错。我们需要按照提将文件下载保存为/www/wwwroot/zabbix/conf/zabbix.conf.php"

![20200509173501258.png](https://img-blog.csdnimg.cn/20200509173501258.png)

完成后，zabbix配置完成

![20200509173545188.png](https://img-blog.csdnimg.cn/20200509173545188.png)

以后对 zabbix的维护，包括安全加固，数据备份，新能调优等等，都可以通过宝塔面板进行

# 6、配置Linux客户端

1.添加zabbix用户和组。

```
groupadd   zabbix
useradd zabbix -g  zabbix -s /sbin/nologin
```

2.安装zabbix客户端。

```
tar xvf  zabbix-4.2.4.tar.gz
cd zabbix-4.2.4
./configure --prefix=/data/zabbix_agent --enable-agent
```

```
make &amp;&amp; make install
```

3.添加服务端口和修改启动脚本。

```
echo 'zabbix-agent 10050/tcp #Zabbix Agent' &gt;&gt; /etc/services
echo 'zabbix-agent 10050/udp #Zabbix Agent' &gt;&gt; /etc/services
cp zabbix-4.2.2/misc/init.d/Fedora/core/zabbix_agentd /etc/init.d/
sed -i 's/BASEDIR=\/usr\/local/BASEDIR=\/data\/zabbix/g' /etc/init.d/zabbix_agentd

```

Zabbix agentd使用 chkconfig 将其加入 init 的启动服务

```
chkconfig --add zabbix_agentd
chkconfig --level 345 zabbix_agentd on
```

使用 chkconfig --list 检查一下

```
chkconfig --list | grep zabbix
```

4.修改zabbix_agent配置文件。

```
vim /data/zabbix/etc/zabbix_agentd.conf
```

```
Server=192.168.1.83 //配置zabbix_server服务端服务器的IP地址
ServerActive=192.168.1.83
Hostname=linux_server1 //配置主机名
PidFile=/var/tmp/zabbix_agentd.pid //指定pid路径
LogFile=/var/log/zabbix/zabbix_agentd.log //指定日志文件

```

保存退出

```
mkdir /var/log/zabbix
touch /var/log/zabbix/zabbix_agentd.log
chown -R zabbix.zabbix /var/log/zabbix
```

5.启动客户端服务并进程测试。

```
/etc/init.d/zabbix_agentd start
```

```
ps aux| grep zabbix
```

![20200509175243775.png](https://img-blog.csdnimg.cn/20200509175243775.png)

在zabbix的服务端执行下面的命令测试与客户端是否联通

```
/data/zabbix/bin/zabbix_get -s 192.168.1.160 -p10050 -k”net.if.in[eth0,bytes]”
```

可以得到网卡信息说明客户端与服务端可以正常通信。

# 7、配置Windows客户端

1.从官方下载Zabbix Agent后，压缩包里面有2个目录

<img alt="" src="https://img-blog.csdn.net/20160425113839169">

在C盘下创建一个为zabbix的目录，在bin文件夹下有一个为win32和win64两个目录，每个目录下应该有3个.exe程序，分别为：zabbix_agentd.exe zabbix_get.exe zabbix_sender.exe

2.根据自己的操作系统复制相应的win32/win64里边的数据到刚创建好的c:\zabbix目录下

<img alt="" src="https://img-blog.csdn.net/20160425141815069">

3.复制解压后zabbix_agents_2.4.4.win文件夹conf里的在C盘的zabbix目录下的conf文件夹下有个zabbix_agentd.win.conf修改一下内容重命名zabbix_agentd.conf到c:\zabbix下

>  
 LogFile=c:\zabbix\zabbix_agentd.log<br> Server=&lt;服务端IP地址&gt;<br> Hostname=win_server1 


4.安装zabbix客户端。依次执行 开始–&gt;运行–&gt;cmd(也可以使用win+R快捷键直接打开)，在打开的命令提示符下执行下面的命令

>  
 cd c:\zabbix<br> zabbix_agentd.exe –c c:\zabbix\zabbix_agentd.conf -i 


<img alt="" src="https://img-blog.csdn.net/20160425142439655">

看到上面的信息说明agent已经安装成功了。<br> 5.启动客户端

>  
 zabbix_agentd.exe –s<br> 如果在启动的时候报错，说cannot open config file[C:\zabbix_agentd.conf]: [2] No such file or directory，把配置文件复制到c:\一份即可<br> zabbix_agentd.exe可用参数介绍：<br> -c 指定配置文件所在位置<br> -i 安装客户端<br> -s 启动客户端<br> -x 停止客户端<br> -d 卸载/删除客户端<br><img alt="" src="https://img-blog.csdn.net/20160425143053240"> 


可以看到客户端已经监听在了10050端口上。打开windows管理工具—&gt;服务，查看一下

<img alt="" src="https://img-blog.csdn.net/20160425143209555">

## 8、在zabbix服务器添加主机

![20200509180034899.png](https://img-blog.csdnimg.cn/20200509180034899.png)

![20200509180112477.png](https://img-blog.csdnimg.cn/20200509180112477.png)

 
