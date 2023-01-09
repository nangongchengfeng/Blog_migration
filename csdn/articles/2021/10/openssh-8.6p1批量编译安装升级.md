+++
author = "南宫乘风"
title = "openssh-8.6p1批量编译安装升级"
date = "2021-10-30 14:55:04"
tags=['ssh', '运维']
categories=[' 企业级-Shell脚本案例', 'Ansible']
image = "post/4kdongman/14.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/121050983](https://blog.csdn.net/heian_99/article/details/121050983)

近期因为业务系统等保，发现ssh有好多的漏洞，需要更新升级。

负责的服务器有点多，不能单个手动编译，所以采用 ansible + 脚本方式批量编译安装

相关下载软件地址：[https://download.csdn.net/download/heian_99/35589407](https://download.csdn.net/download/heian_99/35589407)

![746d38181ced4e5980256ade89206e05.png](https://img-blog.csdnimg.cn/746d38181ced4e5980256ade89206e05.png)

 ![e8edeb1bb61648f8a0159b451ca2c432.png](https://img-blog.csdnimg.cn/e8edeb1bb61648f8a0159b451ca2c432.png)

**本次升级主要解决上次升级造成的隐患，并添加12222端口，**

**隐患：**
- （1）sshd无法开机自启 主机重启后，sshd无法起来，需要他们手动重启- （2）ssh的配置文件目录不对 ，没办法统一管理- （3）sshd无法开机自启，导致rc-local.service 无法自启,
**再次升级基础上**

（1）添加ssh_banner_change 隐藏版本信息

（2）编译是修改版本号，禁止telnet显示版本号

（3）禁止root的密码登录

端口添加

（注：集群有些业务是需要22端口，暂时不能直接去掉22端口）

![446865ea023a4fbb99197bf531cb9550.png](https://img-blog.csdnimg.cn/446865ea023a4fbb99197bf531cb9550.png)

 隐藏效果

![7db72f16e34e4651ab0b358acac69eca.png](https://img-blog.csdnimg.cn/7db72f16e34e4651ab0b358acac69eca.png)

![ac10c0495e464bfd97081ebc3f87be59.png](https://img-blog.csdnimg.cn/ac10c0495e464bfd97081ebc3f87be59.png)

**sshup.sh**

```
#!/bin/bash
# 作者：南宫乘风
# 作用：升级ssh 到 OpenSSH_8.6p1 版本，并添加12222端口

#日期和升级过程中步骤
log="/opt/backup/update_log"
datetime=$(date '+%Y-%m-%d %H:%M:%S')
hostname=`hostname`
echo "==========主机名：${hostname} 开始升级==============" &gt;&gt;${log}
yum -y install openssl-devel zlib-devel gcc gcc-c++ pam-devel perl
#步骤 ：备份  解压 编译 重启

#备份，主要是/etc/ssh 目录 和 先关升级的包
backup=/opt/backup/update_2021_11_01
mkdir -p ${backup}
echo "${backup} 创建成功" &gt;&gt;${log}
#备份文件 主要是移除
echo "=======time: ${datetime}=======开始备份文件==============" &gt;&gt;${log}
mv /etc/ssh ${backup}
mv /usr/sbin/sshd ${backup}
mv /usr/bin/ssh ${backup}/ssh_bak
mv /usr/bin/ssh-keygen ${backup}
datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "${datetime}    /etc/ssh 备份成功" &gt;&gt;${log}
echo "${datetime}    /usr/sbin/sshd 备份成功" &gt;&gt;${log}
echo "${datetime}    /usr/bin/ssh 备份成功" &gt;&gt;${log}
echo "${datetime}    /usr/bin/ssh-keygen 备份成功" &gt;&gt;${log}
FILE=/lib/systemd/system/sshd.service
if [ -f "$FILE" ]; then
	rm -rf /lib/systemd/system/sshd.service
	echo "sshd.service  已清除" &gt;&gt;${log}
fi
datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======备份程序编译文件==============" &gt;&gt;${log}
mv /usr/local/src/openssh* ${backup}
mv /usr/local/src/openssl* ${backup}
mv /usr/local/src/zlib* ${backup}

datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======开始解压文件==============" &gt;&gt;${log}
#解压
cd /opt/backup/ssh_tar
tar xf openssh-8.6p1.tar.gz -C /usr/local/src/
tar xf openssl-1.1.1i.tar.gz -C /usr/local/src/
tar xf zlib-1.2.11.tar.gz -C /usr/local/src/

datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======开始编译zlib==============" &gt;&gt;${log}
#移除
mv /usr/local/zlib ${backup}
cd /usr/local/src/zlib-1.2.11/
./configure --prefix=/usr/local/zlib &amp;&amp; make -j 4 &amp;&amp; make install

datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======开始编译openssl==============" &gt;&gt;${log}
#openssl
mv /usr/local/ssl ${backup}
cd /usr/local/src/openssl-1.1.1i/
./config --prefix=/usr/local/ssl -d shared
make -j 4 &amp;&amp; make install
echo '/usr/local/ssl/lib' &gt;&gt;/etc/ld.so.conf
ldconfig -v
datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======开始编译openssh==============" &gt;&gt;${log}
#openssh
mv /usr/local/openssh ${backup}
cd /usr/local/src/openssh-8.6p1/
sed -i 's/OpenSSH_8.6/Prohibit_detection/g'  /usr/local/src/openssh-8.6p1/version.h
./configure --prefix=/usr/local/openssh --sysconfdir=/etc/ssh --with-pam --with-ssl-dir=/usr/local/ssl --with-zlib=/usr/local/zlib
make -j 4 &amp;&amp; make install
echo 'Version is empty'&gt;&gt; /etc/ssh_banner_change
echo 'Banner /etc/ssh_banner_change' &gt;&gt; /etc/ssh/sshd_config

echo 'Port 22' &gt;&gt;/etc/ssh/sshd_config
echo 'Port 12222' &gt;&gt;/etc/ssh/sshd_config

echo 'PermitRootLogin without-password' &gt;&gt;/etc/ssh/sshd_config
echo 'PubkeyAuthentication yes' &gt;&gt;/etc/ssh/sshd_config
echo 'PasswordAuthentication yes' &gt;&gt;/etc/ssh/sshd_config
echo 'UsePAM yes' &gt;&gt;/etc/ssh/sshd_config
echo 'KexAlgorithms curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group14-sha1' &gt;&gt;/etc/ssh/sshd_config

datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======开始写入pam_sshd==============" &gt;&gt;${log}
cp /etc/pam.d/sshd ${backup}/pam_sshd
if [ ! -e /etc/pam.d/sshd ]; then
	cat &gt;/etc/pam.d/sshd &lt;&lt;EOF
#%PAM-1.0
auth       required     pam_sepermit.so
auth       substack     password-auth
auth       include      postlogin
# Used with polkit to reauthorize users in remote sessions
-auth      optional     pam_reauthorize.so prepare
account    required     pam_nologin.so
account    include      password-auth
password   include      password-auth
# pam_selinux.so close should be the first session rule
session    required     pam_selinux.so close
session    required     pam_loginuid.so
# pam_selinux.so open should only be followed by sessions to be executed in the user context
session    required     pam_selinux.so open env_params
session    required     pam_namespace.so
session    optional     pam_keyinit.so force revoke
session    include      password-auth
session    include      postlogin
# Used with polkit to reauthorize users in remote sessions
-session   optional     pam_reauthorize.so prepare
EOF
	chmod 644 /etc/pam.d/sshd
else
	cp -pf /etc/pam.d/{login,sshd}
fi

datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======开始覆盖sshd，ssh，ssh-keygen==============" &gt;&gt;${log}
cp -rf /usr/local/openssh/sbin/sshd /usr/sbin/sshd
cp -rf /usr/local/openssh/bin/ssh /usr/bin/ssh
cp -rf /usr/local/openssh/bin/ssh-keygen /usr/bin/ssh-keygen
chmod 755 /usr/sbin/sshd
chmod 755 /usr/bin/ssh
chmod 755 /usr/bin/ssh-keygen
datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======设置开机自启sshd==============" &gt;&gt;${log}
\cp  /usr/local/src/openssh-8.6p1/contrib/redhat/sshd.init /etc/init.d/sshd
chmod u+x /etc/init.d/sshd
systemctl daemon-reload
/etc/init.d/sshd restart
chkconfig --add sshd
chkconfig sshd on
chkconfig --list sshd
datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======sshd升级成功==============" &gt;&gt;${log}
echo -e "本次升级使用: $SECONDS seconds"
datetime=$(date '+%Y-%m-%d %H:%M:%S')
echo "=======time: ${datetime}=======本次升级使用: ${SECONDS} seconds ==============" &gt;&gt;${log}

```

 配合ansible 批量升级

```
[heian@zabbix ssh]$ cat ssh-update.yml 
- hosts: test
  remote_user: heian
  gather_facts: false
  become: yes
  become_user: root
  become_method: sudo
  vars:
   - ssh_tar: /opt/backup/ssh_tar
  tasks:
  - name: 创建ssh_tar目录
    file:
      path: "{<!-- -->{ssh_tar}}"
      state: directory
      mode: '0755'
  - name: 分发编译包
    copy:
      src: "{<!-- -->{ item }}"
      dest: "{<!-- -->{ ssh_tar }}"
      mode: 0755
    with_items:
      - /home/heian/ssh/openssh-8.6p1.tar.gz
      - /home/heian/ssh/openssl-1.1.1i.tar.gz
      - /home/heian/ssh/zlib-1.2.11.tar.gz
      - /home/heian/ssh/sshup.sh
  - name: 执行sshd升级脚本
    shell: sh /opt/backup/ssh_tar/sshup.sh
  - name: 查看升级结果
    shell: cat /opt/backup/update_log
    register: ssh_log
  - name: Debug number
    debug:
      msg: " IP : {<!-- -->{ inventory_hostname }}  升级结果 : {<!-- -->{ ssh_log.stdout  }} "

```

![d2c97494a4c94825b2e328e09ebce52f.png](https://img-blog.csdnimg.cn/d2c97494a4c94825b2e328e09ebce52f.png)



 参考文档：[CentOS7.x升级openssh8.4p1详解 - chillax1314 - 博客园](https://www.cnblogs.com/chillax1314/p/13858655.html)
