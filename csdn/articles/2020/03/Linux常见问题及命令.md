+++
author = "南宫乘风"
title = "Linux常见问题及命令"
date = "2020-03-25 17:09:05"
tags=[]
categories=['Linux系统入门']
image = "post/4kdongman/16.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/105099552](https://blog.csdn.net/heian_99/article/details/105099552)

# <a id="Linux_0"></a>Linux常见问题及命令总结

## <a id="1Linux_2"></a>1.查询Linux系统相关的

### <a id="linux_4"></a>查看linux内核版本

```
cat /etc/version  

```

### <a id="_10"></a>查看内核版本号

```
uname -r

```

### <a id="_16"></a>查看内核/操作系统的信息

```
uname -a

```

### <a id="_22"></a>查看系统版本号

```
lsb_release -a

```

### <a id="cache_28"></a>手动释放cache缓存

```
echo 3 &gt; /proc/sys/vm/drop_caches 

```

## <a id="2_34"></a>2.操作文件相关的

### <a id="_36"></a>查找目录下文件内字符串

```
grep -rn "welcome" *;//查找当前目录下"welcome"字符串, *表示当前目录下所有文件,也可以是文件名

```

### <a id="_43"></a>查找指定文件内字符串

```
grep -rn /usr/local/ -e "20003";//查找在/usr/local目录下文件中包含20003关键字的文件

```

### <a id="index_53"></a>搜索所有以index开头的文件

```
find /home/tom -name 'index*'   # 搜索所有以index开头的文件

```

### <a id="home10000K_62"></a>在/home目录下搜索所有大小超过10000K的文件

```
find /home -size +10000k        # 在/home目录下搜索所有大小超过10000K的文件


```

### <a id="homesoftware__69"></a>在/home/software 下查找名字

```
find /home/software/ -type f -name "splunk.tgz"; //在/home/software 下查找名字为"splunk.tgz"的文件


```

### <a id="redistargz_76"></a>解压redis.tar.gz的文件

```
tar -zxvf redis.tar.gz;//解压redis.tar.gz的文件


```

### <a id="C_83"></a>解压到指定目录（-C）

```
tar -zxvf jdk-8u72-linux-x64.tar.gz -C /usr/local;//将jdk-8u72-linux-x64.tar.gz 解压到/usr/local目录中


```

### <a id="d_90"></a>解压到指定目录（-d）

```
unzip gradle-3.3-bin.zip -d /usr/local/; 将gradle-3.3-bin.zip解压到/usr/local目录


```

### <a id="zip_97"></a>zip压缩文件

```
zip  -r test.zip  test;将test文件夹打包成test.zip


```

### <a id="_104"></a>查看尾部内容

```
tail -f access.log;//查看文件尾部内容


```

### <a id="_111"></a>进程后台运行

```
nohup java -jar jenkins.war &amp;;//进程后台程序


```

### <a id="_118"></a>将文件权限分配用户

```
chown -R cdn:cdn common/;//将common文件夹权限分给cdn


```

### <a id="2017622_125"></a>查询2017年6月22日日志

```
sed -n '/22\/Jun\/2017/'p  access.log&gt;&gt;20170622.log;//查询2017年6月22日日志


```

### <a id="_132"></a>截取某段时间的日志

```
sed -n '/2017-06-15 00:00:00/,/2017-06-15 24:00:00/p' catalina.out &gt;&gt; 20170615.log;//截取某个时间段的日志


```

```
sed -n '/2017-07-05 09:[0-9][0-9]:[0-9][0-9]/,/2017-07-05 16:[0-9][0-9]:[0-9][0-9]/p'  catalina.out


```

### <a id="_144"></a>创建文件软链接

```
ln -s /usr/mengqc/mub1 /usr/liu/abc; 将/usr/mengqc/mub1代表的路径将存放在名为/usr/liu/abc的文件中。


```

### <a id="_151"></a>删除软链接

```
rm -rf /usr/softlink ;删除软链接 注意后面不用加／


```

### <a id="_158"></a>创建目录引向某个文件

```
ln –s  /var/www/test   /var/test ; 创建/var/test 引向/var/www/test 文件夹 


```

## <a id="3_165"></a>3.查询进程相关的

```
netstat -lp|grep memcached; //查看启动的memcache服务

netstat -nltp|grep 8080;//查询8080端口是否监听

ps -aux;//查看所有的进程

ps -ef|grep java; //查看java的进程号

history 1000|grep pip;//列出最近使用pip 命令的1000条记录

ps -ef|grep jetty|grep -v grep|awk '{print $2}';//查看jetty进程号

ps -ef|grep -v grep|grep jetty-avene|grep jetty|grep -v python|awk '{print $2}';//查询jetty项目名称为jetty－avene的进程号

ps -ef|grep -v grep|grep jetty-avene|grep jetty|grep -v python|awk '{print $2}'



```

## <a id="4_187"></a>4.安装软件相关的

```
rpm --install couchbase-server-enterprise-3.0.3-centos6.x86_64.rpm;//解压rpm文件

rpm -qa;//查看所有安装的软件包

rpm -qa|grep kernel;//查询系统所有内核

yum remove kernel-headers-3.10.0-327.el7.x86_64;//删除内核kernel-headers-3.10.0-327.el7.x86_64

rpm -l pkgname.rpm；//安装rpm包

rpm -e pkgname;//删除rmp包


从源码安装
./configure
make
make install


```

## <a id="5centos6_210"></a>5.防火墙相关的(centos6)

```
chkconfig --list;//列出系统所有服务启动情况

service iptables status;//查看防火墙状态

service iptables start;//打开防火墙

service iptables stop;//关闭防火墙


为防火墙添加访问端口和ip，在vi /etc/sysconfig/iptables目录下编辑:

iptables -A INPUT -p tcp --dport 10006 -j ACCEPT; //允许端口10006访问

iptables -A INPUT -s 192.168.50.87 -p tcp -j ACCEPT；//允许192.168.50.87地址能访问


```

## <a id="6_230"></a>6.操作磁盘相关的

```
df -h;//查看磁盘的使用情况

du -h;//查看目录的大小

du –sh *；//查看某个目录下所有文件及文件的大小：

du -sh *|sort -nr;//定位那个目录最大

du –sh * |sort –n;//按照文件大小排序

fdisk -l;//可以查看到当前的所有分区，比如boot分区，该分区存档linux的grub以及内核源码

vim /etc/fstab ;//修改fstab内容


```

## <a id="7_249"></a>7.网络相关的

```
nslookup www.baidu.com;//查询域名对应的ip地址

dig www.baidu.com;//查询域名对应的ip地址

lsof -i:4080;//查看4080端口是否被占用

curl ifconfig.me;//查出外网的ip地址

netstat -tnlp|grep redis;

ifconfig -a;      //列出所有网络端口和IP地址

iftop            //监控网络带宽

ifconfig eth0    //列出指定以太网端口对应的IP地址和详细信息

ethtool eth0     //查看以太网状态

ping host   

whois domain     //获取指定域名的信息

dig domain       //获取指定域名的DNS信息

dig -x host      //根据主机地址反向查找

host goole.com   //根据域名查找DNS IP地址

wget file        //下载文件

netstat -tupl    //列出系统的活跃连接


```

## <a id="8_286"></a>8.文件传输相关的

```
scp file.txt server2:/tmp                 //安全拷贝file.txt到远程主机的/tmp目录下

scp noodle@server2:/www/*.html /www/tmp   //拷贝远程主机的/www/目录下的所有HTML文件到本地的/www/tmp目录

scp -r noodle@server2:/www /www/tmp       //递归拷贝远程主机/www目录下的所有文件和文件夹到本地/www/tmp目录

scp -P 2244 client.xml datasources.xml server.xml 

root@139.136.218.194:/data/appdatas/cat;//远程机器访问端口为2244

# rsync
rsync -a /home/apps /backup/              # 源目录和目标目录同步
rsync -avz /home/apps noodle@192.168.10.1:/backup   //本地目录和远程主机目录同步，启用压缩

//模拟请求
curl -i -X POST -H 'Content-type':'application/json' -d '{"customerId":3,"recNum":"18862285367"}' http://10.105.31.109:10000/sms/sendCoupenCodeSms


```

## <a id="9_308"></a>9.硬件相关的

```
dmesg                   //监测硬件和启动消息 

cat /proc/cpuinfo       //CPU信息 

cat /proc/meminfo       //硬件内存信息 

free -m                 //已使用的和可用内存，-m表示单位为M 

lspci -tv               //显示PCI设备信息 

lsusb -tv               //显示USB设备信息 

hdparm -l /dev/sda      //显示sda硬盘信息 

hdparm -tT /dev/sda     //对sda硬盘进行读取速度测试 

hdparm -s /dev/sda      //测试sda硬盘上不可读的块


```

## <a id="10_331"></a>10.统计相关的

```
top                       //显示并不断更新最耗CPU的进程 
mpstat 1                  //显示CPU统计信息 
vmstat 2                  //显示虚拟内存统计信息 
iostat 2                  //显示IO统计信息（2s采样间隔） 
tcpdump -i eth1           //捕获eth1网络接口上的所有数据包 
tcpdump -i eth0 'port 80' //监控80端口的网络流量 
lsof                      //列出所有活跃进程打开的文件 
lsof -u testuser          //列出所有testuser用户打开的文件

wc -l filename;//统计行数
wc -c filename;//统计字节数
wc -m filename;//统计字符数
wc -w filename;//统计单词数
ls -l|wc -l 用来统计当前目录下的文件数


```

## <a id="11nginx_351"></a>11.nginx统计相关的

```
1.根据访问IP统计UV

awk '{print $1}'  access.log|sort | uniq -c |wc -l

2.统计访问URL统计PV

awk '{print $7}' access.log|wc -l

3.查询访问最频繁的URL

awk '{print $7}' access.log|sort | uniq -c |sort -n -k 1 -r|more

4.查询访问最频繁的IP

awk '{print $1}' access.log|sort | uniq -c |sort -n -k 1 -r|more

5.根据时间段统计查看日志

 cat  access.log| sed -n '/14\/Mar\/2015:21/,/14\/Mar\/2015:22/p'|more


```

## <a id="12nmap_376"></a>12.nmap相关的

```
nmap 192.168.102.10; 侦测ip地址

nmap weixin.hao.cn;侦测域名

nmap -sU -sS -F weixin.hao.cn;//-F 快速扫描模式，扫描最可能开放的前100个端口

nmap -sV 192.168.102.10;

nmap -A 192.168.102.10;执行全网扫描

nmap -O weixin.hao.cn;//侦测操作系统的信息

nmap -sP 192.168.102.*;//找出网络中的在线主机

nmap -V;//查询nmap版本

nmap -p 8080 weixin.hao.cn;//扫描特定端口


```

## <a id="13_399"></a>13.用户相关的

```
adduser newname // 新建用户newname

passwd  newname //设置用户名和密码

userdel newname //删除用户

deluser –remove-home newname //删除home目录的数据

sudo addgroup siatstudent  //创建组

groupadd testgroup

groupmod -n test2group testgroup //修改组

delgroup happy  //删除分组

groups  #查看当前登陆用户所在的组

groups testnewuser #查看testnewuser 所在的组

cat /etc/group  #查看所有组


```

## <a id="14Linux_426"></a>14.Linux内存清理命令

```
free -m;//清理内存前 查看内存使用情况

echo 1 &gt; /proc/sys/vm/drop_caches;//开始清理

free -m;//清理之后查看内存使用情况

dmidecode | grep -A16 "Memory Device$";//查看内存条数


```
