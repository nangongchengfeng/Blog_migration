+++
author = "南宫乘风"
title = "sersync+rsync原理及部署"
date = "2021-01-29 23:09:59"
tags=['linux', 'ssh', 'centos', '服务器']
categories=[' Linux服务应用']
image = "post/4kdongman/15.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/113407684](https://blog.csdn.net/heian_99/article/details/113407684)

## rsync

**1.1 rsync是什么**<br> rsync是一款开源的，快速的、多功能的、可实现全量及增量的本地或远程数据同步备份的优秀工具同步备份的优秀工具

**1.2 rsync的特性如下：**
1. 支持拷贝特殊文件如链接文件，设备等1. 可以有排除指定文件或目录同步的功能，相当于打包命令tar的排除功能。1. 可以做到保持原文件或目录等权限，时间，软硬链接，属主，属组等所有属性均不改变 –p1. 可实现增量同步，即只同步发生变化的数据，因此数据传输效率很高1. 可以使用rcp,rsh,ssh等方式来配置传输文件（rsync本身不对数据加密）1. 可以通过socket（守护进程方式）传输文件和数据（服务端和客户端）1. 支持匿名或认证（无需系统用户）的进程模式传输，可实现方便安全的进行数据备份及镜像1. rsync也相当于ls命令
**1.3 rsync的企业工作场景说明**
1. 两台服务器之间数据同步（定时任务+rsync）1. 实时同步（解决存储服务器的单点问题）
## Rsync+Inotify-tools与Rsync+sersync这两种架构有什么区别

### **1．Rsync+Inotify-tools**

（1）：Inotify-tools只能记录下被监听的目录发生了变化（包括增加、删除、修改），并没有把具体是哪个文件或者哪个目录发生了变化记录下来；<br> （2）：rsync在同步的时候，并不知道具体是哪个文件或者哪个目录发生了变化，每次都是对整个目录进行同步，当数据量很大时，整个目录同步非常耗时（rsync要对整个目录遍历查找对比文件），因此，效率很低。

### **2．Rsync+sersync**

（1）sersync可以记录下被监听目录中发生变化的（包括增加、删除、修改）具体某一个文件或某一个目录的名字；<br> （2）rsync在同步的时候，只同步发生变化的这个文件或者这个目录（每次发生变化的数据相对整个同步目录数据来说是很小的，rsync在遍历查找比对文件时，速度很快），因此，效率很高。

 

### **同步过程：**

1.  在同步服务器上开启sersync服务，sersync负责监控配置路径中的文件系统事件变化；

2.  调用rsync命令把更新的文件同步到目标服务器；

3.  需要在主服务器配置sersync，在同步目标服务器配置rsync server（注意：是rsync服务）

###  同步过程和原理：

1.  用户实时的往sersync服务器上写入更新文件数据；

2.  此时需要在同步主服务器上配置sersync服务；

3.  在另一台服务器开启rsync守护进程服务，以同步拉取来自sersync服务器上的数据；

通过rsync的守护进程服务后可以发现，实际上sersync就是监控本地的数据写入或更新事件；然后，在调用rsync客户端的命令，将写入或更新事件对应的文件通过rsync推送到目标服务器

**小结：当同步的目录数据量不大时，建议使用Rsync+Inotify-tools；当数据量很大（几百G甚至1T以上）、文件很多时，建议使用Rsync+sersync。**

## 三、配置操作

 

**一台装rsync服务  **192.168.0.10

**一台装sersync     **192.168.0.20

**对20网站根目录的/backup目录备份到10的/backup**

**Rsync服务器（备份端磁盘大专门用来存储数据 ,目标机器）：**192.168.0.10

**Sersync服务器（数据源【部署的项目，代码等】,源机器 ）： **192.168.0.20<br>  

### **（1）、使用rsync备份数据 系统用户**

**两台服务器都需要安装rsync**

```
yum -y install xinetd rsync
```

**20需要安装sersync**

**原理：10 上 使用系统配置文件   vim /etc/rsyncd.conf   来备份数据，创建备份账户，最后把rsync以deamon方式运行**

** vim /etc/rsyncd.conf      rsyncd.conf配置文件**

```
#!/bin/bash
uid = root
gid = root
use chroot = no
disable = no
fake super = yes 
max connections = 200
timeout = 300
pid file=/var/run/rsyncd.pid
lock file=/var/run/rsync.lock
log file = /var/log/rsyncd.log
[backup]
path = /backup
ignore errors
read only = false
list = false
hosts allow = 192.168.0.0/24  
host deny = 0.0.0.0/0 
auth users = rsync_backup
secrets file = /etc/rsync.password


[root@backup ~]# useradd -M -s /sbin/nologin rsync   #可以使用rsync，我使用的是root
[root@backup backup]# mkdir /backup/    创建备份的目录
```

创建密码文件

```
[root@backup ~]# echo 'rsync_backup:123456' &gt;/etc/rsync.password
[root@backup ~]# cat /etc/rsync.password
rsync_backup:123456
```

修改权限

```
[root@backup ~]# chmod 600 /etc/rsync.password
[root@backup ~]# ll /etc/rsync.password
-rw-------. 1 root root 20 Jul 24 04:27 /etc/rsync.password

```

启动rsync服务

```
[root@backup ~]# rsync -–daemon

```

加入开机自启动

```
[root@backup ~]# vim /etc/rc.local
# rsync server progress
/usr/bin/rsync --daemon

1.5.7 第六个里程碑-检查  rsync的端口号为873
[root@backup ~]# ss -tlunp|grep rsync
tcp    LISTEN     0      5                     :::873                  :::*      users:(("rsync",2452,5))
tcp    LISTEN     0      5                      *:873                   *:*      users:(("rsync",2452,4))

```

重启rsync

```
[root@rsync-client-sersync ~]# ps -ef | grep rsync
root       1287      1  0 22:52 ?        00:00:00 rsync --daemon
root       1294   1248  0 22:52 pts/0    00:00:00 grep --color=auto rsync
[root@rsync-client-sersync ~]# kill -9 1287
[root@rsync-client-sersync ~]# ps -ef | grep rsync
root       1298   1248  0 22:53 pts/0    00:00:00 grep --color=auto rsync
[root@rsync-client-sersync ~]# rsync --daemon
[root@rsync-client-sersync ~]# ps -ef | grep rsync
root       1300      1  0 22:53 ?        00:00:00 rsync --daemon
root       1302   1248  0 22:53 pts/0    00:00:00 grep --color=auto rsync

重启，就是杀掉rsync的进程，重新rsync --daemon
```

在客户端进行测试（20）

```
[root@rsync-client-sersync ~]# rsync -avz /etc/hosts rsync_backup@192.168.0.10::backup
Password: 
sending incremental file list
hosts

sent 140 bytes  received 43 bytes  33.27 bytes/sec
total size is 158  speedup is 0.86
成功的将hosts文件推向服务器端的/backup目录中

```

客户端添加密码

```
[root@nfs01 tmp]# echo '123456' &gt;/etc/rsync.password   将密码重定向到/etc/rsync.password文件
[root@nfs01 tmp]# cat /etc/rsync.password   查看
123456
[root@nfs01 tmp]# chmod 600 /etc/rsync.password   给/etc/rsync.password文件600的权限

```

```
rsync -avz /etc/hosts rsync_backup@172.16.1.41::backup --password-file=/etc/rsync.password    指定密码文件
```

实例：排除文件

```
[root@backup tmp]# rsync -a –-exclude=/etc/hosts /etc/services 172.16.1.31:/tmp/
–-exclude=/etc/hosts  排除/etc/services中的/etc/hosts文件

--bwlimit=RATE  limt socket I/O bandwidth  传输的时候限速
--delete  让源目录和目标目录一模一样（即：我有什么你就有什么，我没什么你就没有什么）

```
- 实例：无差异同步
```
[root@backup tmp]# rsync -a --delete /tmp/ 172.16.1.31:/tmp/
root@172.16.1.31's password:
--delete  本地有什么，远端就有什么 本地没有什么，远端就没有什么 本地有远端没有，就会删除远
```

### **（2）、使用sersync实时监控推送**

**1****、下载sersync**

 在google code下载sersync的可执行文件版本，里面有配置文件与可执行文件，这用

```
mkdir -p /applition/tools
cd /applition/tools
wgethttps://sersync.googlecode.com/files/sersync2.5.4_64bit_binary_stable_final.tar.gz
【有时下载失败，所有要本地留存才行】
[root@web ~]# tar fxzsersync2.5.4_64bit_binary_stable_final.tar.gz -C /usr/local/
[root@web ~]# cd /usr/local/
[root@cache local]# mv GNU-Linux-x86 sersync
[root@cache local]# treesersync/
sersync/
├── confxml.xml      #   配置文件
└── sersync2         #   二进制文件【启动sersync使用】
 
0 directories, 2 files
```

**2****、配置sersync**

```
[root@cache local]# cp sersync/confxml.xmlsersync/confxml.xml.$(date +%F)
[root@cache local]# ll sersync/confxml.xml
-rwxr-xr-x. 1 root root 2214Oct 26  2011 sersync/confxml.xml
[root@cache local]# llsersync/confxml.xml*
-rwxr-xr-x. 1 root root 2214Oct 26  2011 sersync/confxml.xml
-rwxr-xr-x. 1 root root 2214Jun  5 06:38sersync/confxml.xml.2015-06-05
```

**更改优化sersync配置文件：**

```
     &lt;localpathwatch="/opt/tongbu"&gt;     # 定义本地要同步的目录
         &lt;remote ip="127.0.0.1"name="tongbu1"/&gt;
         &lt;!--&lt;remoteip="192.168.8.39" name="tongbu"/&gt;--&gt;        # 同步到哪台机器上 tongbu模块rsync端模块名字
         &lt;!--&lt;remoteip="192.168.8.40" name="tongbu"/&gt;--&gt;        # 同步到哪台机器上 tongbu模块
     &lt;/localpath&gt;
```

**b****）修改31--34行，认证部分【rsync密码认证】**

```
  &lt;rsync&gt;
            &lt;commonParamsparams="-artuz"/&gt;
            &lt;auth start="false"users="root" passwordfile="/etc/rsync.pas"/&gt;
             &lt;userDefinedPortstart="false" port="874"/&gt;&lt;!-- port=874 --&gt;
             &lt;timeoutstart="false" time="100"/&gt;&lt;!-- timeout=100 --&gt;
             &lt;sshstart="false"/&gt;
         &lt;/rsync&gt;

# ***修改内容为 rsync的密码文件以及 同步所使用的账号类似：
rsync -avzP /data/www/rsync_backup@172.16.1.25::www/ --password-file=/etc/rsync.password
```

```
        &lt;failLog path="/usr/local/sersync/logs/rsync_fail_log.sh"timeToExecute="60"/&gt;&lt;!--default every 60mins execute once--&gt;
# 当同步失败后，日志记录到/usr/local/sersync/logs/rsync_fail_log.sh文件中，并且每60分钟对失败的log进行重新同步
```

**修改后的完整配置文件为：**

```
&lt;?xml version="1.0" encoding="ISO-8859-1"?&gt;
&lt;head version="2.5"&gt;
    &lt;host hostip="localhost" port="8008"&gt;&lt;/host&gt;
    &lt;debug start="false"/&gt;
    &lt;fileSystem xfs="false"/&gt;
    &lt;filter start="false"&gt;
	&lt;exclude expression="(.*)\.svn"&gt;&lt;/exclude&gt;
	&lt;exclude expression="(.*)\.gz"&gt;&lt;/exclude&gt;
	&lt;exclude expression="^info/*"&gt;&lt;/exclude&gt;
	&lt;exclude expression="^static/*"&gt;&lt;/exclude&gt;
    &lt;/filter&gt;
    &lt;inotify&gt;
	&lt;delete start="true"/&gt;
	&lt;createFolder start="true"/&gt;
	&lt;createFile start="false"/&gt;
	&lt;closeWrite start="true"/&gt;
	&lt;moveFrom start="true"/&gt;
	&lt;moveTo start="true"/&gt;
	&lt;attrib start="false"/&gt;
	&lt;modify start="false"/&gt;
    &lt;/inotify&gt;

    &lt;sersync&gt;
	&lt;localpath watch="/etc/openvpn"&gt;
	    &lt;remote ip="192.168.0.10" name="openvpn"/&gt;
	    &lt;!--&lt;remote ip="192.168.8.39" name="tongbu"/&gt;--&gt;
	    &lt;!--&lt;remote ip="192.168.8.40" name="tongbu"/&gt;--&gt;
	&lt;/localpath&gt;
	&lt;rsync&gt;
	    &lt;commonParams params="-artuz"/&gt;
	    &lt;auth start="true" users="rsync_backup" passwordfile="/etc/rsync.password"/&gt;
	    &lt;userDefinedPort start="false" port="874"/&gt;&lt;!-- port=874 --&gt;
	    &lt;timeout start="start" time="100"/&gt;&lt;!-- timeout=100 --&gt;
	    &lt;ssh start="false"/&gt;
	&lt;/rsync&gt;
	&lt;failLog path="/tmp/rsync_fail_log.sh" timeToExecute="60"/&gt;&lt;!--default every 60mins execute once--&gt;
	&lt;crontab start="false" schedule="600"&gt;&lt;!--600mins--&gt;
	    &lt;crontabfilter start="false"&gt;
		&lt;exclude expression="*.php"&gt;&lt;/exclude&gt;
		&lt;exclude expression="info/*"&gt;&lt;/exclude&gt;
	    &lt;/crontabfilter&gt;
	&lt;/crontab&gt;
	&lt;plugin start="false" name="command"/&gt;
    &lt;/sersync&gt;

    &lt;plugin name="command"&gt;
	&lt;param prefix="/bin/sh" suffix="" ignoreError="true"/&gt;	&lt;!--prefix /opt/tongbu/mmm.sh suffix--&gt;
	&lt;filter start="false"&gt;
	    &lt;include expression="(.*)\.php"/&gt;
	    &lt;include expression="(.*)\.sh"/&gt;
	&lt;/filter&gt;
    &lt;/plugin&gt;

    &lt;plugin name="socket"&gt;
	&lt;localpath watch="/opt/tongbu"&gt;
	    &lt;deshost ip="192.168.138.20" port="8009"/&gt;
	&lt;/localpath&gt;
    &lt;/plugin&gt;
    &lt;plugin name="refreshCDN"&gt;
	&lt;localpath watch="/data0/htdocs/cms.xoyo.com/site/"&gt;
	    &lt;cdninfo domainname="ccms.chinacache.com" port="80" username="xxxx" passwd="xxxx"/&gt;
	    &lt;sendurl base="http://pic.xoyo.com/cms"/&gt;
	    &lt;regexurl regex="false" match="cms.xoyo.com/site([/a-zA-Z0-9]*).xoyo.com/images"/&gt;
	&lt;/localpath&gt;
    &lt;/plugin&gt;
&lt;/head&gt;

```

**3****、开启sersync守护进程同步数据**

```
[root@web ~]# /usr/local/sersync/sersync2  -d -r -o /usr/local/sersync/confxml.xml
配置sersync环境变量
[root@web ~]# echo"PATH=$PATH:/usr/local/sersync/"&gt;&gt;/etc/profile
[root@web ~]# source /etc/profile
[root@web ~]# sersync2
```

**启动命令后返回结果如下为正常：**

```
set the system param
execute：echo50000000 &gt; /proc/sys/fs/inotify/max_user_watches
execute：echo 327679&gt; /proc/sys/fs/inotify/max_queued_events
parse the command param
option: -d      run as a daemon
option: -r      rsync all the local files to the remoteservers before the sersync work
option: -o      config xml name：  /usr/local/sersync/confxml.xml
daemon thread num: 10
parse xml config file
host ip : localhost     host port: 8008
daemon start，sersync runbehind the console 
use rsync password-file :
user is rsync_backup
passwordfile is         /etc/rsync.password
config xml parse success
please set /etc/rsyncd.confmax connections=0 Manually
sersync working thread 12  = 1(primary thread) + 1(fail retry thread) + 10(daemon sub threads)
Max threads numbers is: 32 = 12(Thread pool nums) +20(Sub threads)
please according your cpu ，use -n paramto adjust the cpu rate
chmod: cannot access`/usr/local/sersync/logs/rsync_fail_log.sh': No such file or directory
------------------------------------------
rsync the directory recursivlyto the remote servers once
working please wait...
execute command: cd /backup&amp;&amp; rsync -artuz -R --delete ./ --timeout=100 rsync_backup@192.168.0.10::www--password-file=/etc/rsync.password &gt;/dev/null 2&gt;&amp;1 
run the sersync: 
watch path is: /data/www
```

如果你上面的配置和验证都没问题，可以下面的配置了。设置开机自启动

```
#vi /etc/rc.d/rc.local
 
/usr/local/sersync/sersync2 -d -r -o  /usr/local/sersync/confxml.xml ＃设置开机自动运行脚本
 
# chmod +x /etc/rc.d/rc.local
```

添加脚本监控sersync是否正常

```
cd /root
touch check_sersync.sh
chmod 755 check.sersync.sh
vim check_sersync.sh


#!/bin/sh
sersync="/usr/local/sersync/sersync2"
confxml="/usr/local/sersync/confxml.xml"
status=$(ps aux |grep 'sersync2'|grep -v 'grep'|wc -l)
if [ $status -eq 0 ];
then
$sersync -d -r -o $confxml &amp;
else
exit 0;
fi

check_sersync.sh
```

```
#vi /etc/crontab
 
*/5 * * * * root /root/check_sersync.sh &gt;/dev/null 2&gt;&amp;1  #每隔5分钟执行一次脚本

```

注意：

　　1、手动执行check_sersync.sh检测sersync是否运行正常。

　　2、如果着急测试，不用等重启服务器后执行，先执行　
| 1 | `/``usr``/``local``/``sersync``/``sersync2 ``-``d ``-``r ``-``o  ``/``usr``/``local``/``sersync``/``confxml.xml` 

`/``usr``/``local``/``sersync``/``sersync2 ``-``d ``-``r ``-``o  ``/``usr``/``local``/``sersync``/``confxml.xml`

　　3、在源服务器指定目录下对文件文件夹做出更改，查看目标服务器同步目录下是否同步成功。

```
1 -v, --verbose 详细模式输出
  2 
  3 -q, --quiet 精简输出模式
  4 
  5 -c, --checksum 打开校验开关，强制对文件传输进行校验
  6 
  7 -a, --archive 归档模式，表示以递归方式传输文件，并保持所有文件属性，等于-rlptgoD
  8 
  9 -r, --recursive 对子目录以递归模式处理
 10 
 11 -R, --relative 使用相对路径信息
 12 
 13 -b, --backup 创建备份，也就是对于目的已经存在有同样的文件名时，将老的文件重新命名为~filename。可以使用--suffix选项来指定不同的备份文件前缀。
 14 
 15 --backup-dir 将备份文件(如~filename)存放在在目录下。
 16 
 17 -suffix=SUFFIX 定义备份文件前缀
 18 
 19 -u, --update 仅仅进行更新，也就是跳过所有已经存在于DST，并且文件时间晚于要备份的文件。(不覆盖更新的文件)
 20 
 21 -l, --links 保留软链结
 22 
 23 -L, --copy-links 想对待常规文件一样处理软链结
 24 
 25 --copy-unsafe-links 仅仅拷贝指向SRC路径目录树以外的链结
 26 
 27 --safe-links 忽略指向SRC路径目录树以外的链结
 28 
 29 -H, --hard-links 保留硬链结
 30 
 31 -p, --perms 保持文件权限
 32 
 33 -o, --owner 保持文件属主信息
 34 
 35 -g, --group 保持文件属组信息
 36 
 37 -D, --devices 保持设备文件信息
 38 
 39 -t, --times 保持文件时间信息
 40 
 41 -S, --sparse 对稀疏文件进行特殊处理以节省DST的空间
 42 
 43 -n, --dry-run现实哪些文件将被传输
 44 
 45 -W, --whole-file 拷贝文件，不进行增量检测
 46 
 47 -x, --one-file-system 不要跨越文件系统边界
 48 
 49 -B, --block-size=SIZE 检验算法使用的块尺寸，默认是700字节
 50 
 51 -e, --rsh=COMMAND 指定使用rsh、ssh方式进行数据同步
 52 
 53 --rsync-path=PATH 指定远程服务器上的rsync命令所在路径信息
 54 
 55 -C, --cvs-exclude 使用和CVS一样的方法自动忽略文件，用来排除那些不希望传输的文件
 56 
 57 --existing 仅仅更新那些已经存在于DST的文件，而不备份那些新创建的文件
 58 
 59 --delete 删除那些DST中SRC没有的文件
 60 
 61 --delete-excluded 同样删除接收端那些被该选项指定排除的文件
 62 
 63 --delete-after 传输结束以后再删除
 64 
 65 --ignore-errors 及时出现IO错误也进行删除
 66 
 67 --max-delete=NUM 最多删除NUM个文件
 68 
 69 --partial 保留那些因故没有完全传输的文件，以是加快随后的再次传输
 70 
 71 --force 强制删除目录，即使不为空
 72 
 73 --numeric-ids 不将数字的用户和组ID匹配为用户名和组名
 74 
 75 --timeout=TIME IP超时时间，单位为秒
 76 
 77 -I, --ignore-times 不跳过那些有同样的时间和长度的文件
 78 
 79 --size-only 当决定是否要备份文件时，仅仅察看文件大小而不考虑文件时间
 80 
 81 --modify-window=NUM 决定文件是否时间相同时使用的时间戳窗口，默认为0
 82 
 83 -T --temp-dir=DIR 在DIR中创建临时文件
 84 
 85 --compare-dest=DIR 同样比较DIR中的文件来决定是否需要备份
 86 
 87 -P 等同于 --partial
 88 
 89 --progress 显示备份过程
 90 
 91 -z, --compress 对备份的文件在传输时进行压缩处理
 92 
 93 --exclude=PATTERN 指定排除不需要传输的文件模式
 94 
 95 --include=PATTERN 指定不排除而需要传输的文件模式
 96 
 97 --exclude-from=FILE 排除FILE中指定模式的文件
 98 
 99 --include-from=FILE 不排除FILE指定模式匹配的文件
100 
101 --version 打印版本信息
102 
103 --address 绑定到特定的地址
104 
105 --config=FILE 指定其他的配置文件，不使用默认的rsyncd.conf文件
106 
107 --port=PORT 指定其他的rsync服务端口
108 
109 --blocking-io 对远程shell使用阻塞IO
110 
111 -stats 给出某些文件的传输状态
112 
113 --progress 在传输时现实传输过程
114 
115 --log-format=formAT 指定日志文件格式
116 
117 --password-file=FILE 从FILE中得到密码
118 
119 --bwlimit=KBPS 限制I/O带宽，KBytes per second
120 
121 -h, --help 显示帮助信息
rsync详细参数
```

参考地址：

[https://blog.51cto.com/liubao0312/1677586](https://blog.51cto.com/liubao0312/1677586)

[https://blog.csdn.net/ljx1528/article/details/105348259](https://blog.csdn.net/ljx1528/article/details/105348259)

[https://www.cnblogs.com/lei0213/p/8598072.html](https://www.cnblogs.com/lei0213/p/8598072.html)
