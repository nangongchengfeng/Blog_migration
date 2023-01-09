+++
author = "南宫乘风"
title = "Redhat机器巡检脚本"
date = "2021-02-25 14:11:07"
tags=['操作系统', 'linux', 'cpu', '网络']
categories=[' 企业级-Shell脚本案例']
image = "post/4kdongman/11.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/114080095](https://blog.csdn.net/heian_99/article/details/114080095)

此脚本适合Redhat系列

centos系列，内存缓存计数位置不同，可能不准确

 

```
#!/bin/bash
##系统信息##
sys_check(){
os_type=`uname`
echo "操作系统类型是:$os_type"
os_banben=`cat /etc/redhat-release`
echo "操作系统版本号是:$os_banben"
os_neihe=`uname -r`
echo "操作系统的内核是:$os_neihe"
os_time=`date +%F_%T`
echo "操作系统当前时间是:$os_time"
os_uptime=`uptime | awk '{print $3}'|awk -F , '{print $1}'`
echo "操作系统最后重启时间为:$os_uptime"
os_hostname=`hostname`
echo "操作系统主机名称为:$os_hostname"
}
##网络信息##
net_check(){
net_ip=`/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d "addr:"`
echo "操作系统的ip是:$net_ip"
ping -c1 www.baidu.com &gt;/dev/null
if [ $? -eq 0 ];then
        echo "外网可以连通"
else
        echo "外网连不通，请检查"
fi
}
cpu_check(){
physical_id=`cat /proc/cpuinfo | grep "physical id"|sort|uniq|wc -l`
echo "操作系统cpu物理个数是:$physical_id"
cpu_core=`cat /proc/cpuinfo | grep "cpu cores"|sort|uniq|awk -F ':' '{print $2}'`
echo "操作系统的cpu核心数是:$cpu_core"
cpu_type=`cat /proc/cpuinfo | grep "model name"|sort|uniq|awk -F ':' '{print $2}'`
echo "操作系统的cpu型号是:$cpu_type"
free_total=`free -m | grep Mem|awk '{printf $2}'`
echo "操作系统的内存总大小为:$free_total M"
free_used=`free -m | grep Mem|awk '{printf $3}'`
echo "操作系统已使用内存为:$free_used M"
free_shengyu=`free -m | grep Mem|awk '{printf $4}'`
echo "操作系统剩余内存为:$free_shengyu M"
used_baifen=`echo "scale=2;$free_used/$free_total*100"|bc`
echo "已使用内存百分比是:$used_baifen"%
shengyu_baifen=`echo "scale=2;$free_shengyu/$free_total*100"|bc`
echo "未使用内存百分比是:$shengyu_baifen"%
}
disk_check(){
disk_size=`lsblk | grep -w sda |awk '{print $4}'`
echo "磁盘总量为:$disk_size"
a=($(df -m | grep -v "tmpfs" | egrep -A 1 "mapper|sd" | awk 'NF&gt;1{print $(NF-2)}'))
sum=0
for i in ${a[*]}
do
        let sum=sum+$i
done
shengfree=$[$sum/1024]
echo "剩余磁盘总量为:$shengfree" G
}
sys_check
net_check
cpu_check
disk_check
```

 
