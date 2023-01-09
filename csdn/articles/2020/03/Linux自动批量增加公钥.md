+++
author = "南宫乘风"
title = "Linux自动批量增加公钥"
date = "2020-03-30 13:41:03"
tags=['秘钥', 'Linux', 'Centos', '批量', 'ssh']
categories=['Linux Shell', ' 企业级-Shell脚本案例']
image = "post/4kdongman/92.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/105197561](https://blog.csdn.net/heian_99/article/details/105197561)

### 自动增加公钥

需求：

提示要输入对方的ip和root密码，然后可以自动把本机的公钥增加到对方机器上，从而实现密钥认证。

1.在使用之前，先安装epel源，yum install expect -y

2.写分发脚本，后缀为exp

```
#!/usr/bin/expect#!/bin/bash
#name:南宫乘风
#email：heian99@163.com
#自动添加公钥到指定的服务器
set host_ip [lindex $argv 0]
spawn ssh-copy-id -i /root/.ssh/id_rsa.pub $host_ip
expect {
        -timeout 60
        "(yes/no)?" { send "yes\n";exp_continue}
        "password:" { send "root\n"} #填写服务器的同一密码
        timeout {puts "Connect timeout!";return}
}
expect eof
exit -onexit {
        send_user "Job has finished!"
}
```

注：set的作用是设置变量，spawn设置执行命令时，可以引用变量；变量的第一个参数为0

编写ip.txt,存放ip地址

![20200330133725664.png](https://img-blog.csdnimg.cn/20200330133725664.png)

3.执行以下命令开始分发

```
for ip in `cat /root/ip.txt`;do expect /root/ssh.exp $ip ;done
```

![20200330134021584.png](https://img-blog.csdnimg.cn/20200330134021584.png)

如果密码不一样，也可以定义到ip.txt的文本里面，通过awk获取到。

然后传值给expect。可以实现不同ip和密码的自动批量秘钥传输。
