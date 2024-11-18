---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2021-02-27 18:39:16
description: 无聊，近期痴迷编程，没事就写写和代码练练手。这次写了个自动安装的代码菜单功能比较，相对比较省事。多台主机安装方便。仅供参考，大佬勿喷颜色控制判断软件是否安装没有安装已经安装安装组件已经安装配置请输的未。。。。。。。
image: ../../title_pic/30.jpg
slug: '202102271839'
tags:
- linux
- centos
- 运维
- salt
title: SaltStack脚本安装
---

<!--more-->

无聊，近期痴迷编程，没事就写写shell和Python代码练练手。

这次写了个自动安装saltstack的shell代码菜单

![](../../image/20210227183529467.png)

功能比较low，相对比较省事。多台主机安装方便。仅供参考，大佬勿喷

![](../../image/20210227183642189.png)

 

```bash
 #!/bin/bash


#颜色控制
red='\033[1;31m'
black='\033[0m'
Orange='\033[35m'
background='\033[0m'
minion_file='/etc/salt/minion'
datetime=`date +"%F %T"`

#判断软件是否安装
function if_installed(){
    salt_name=$1
    salt_status=`rpm -qa | grep $salt_name`
    if [  ! -n "$salt_status" ];then
        echo "$salt_name没有安装"
        return 2
    else
        echo "$salt_name已经安装"
        echo $salt_status
    fi
    
}

#安装master组件
function install_master(){
    salt_name=$1
    if_installed $salt_name
    if [ $? -eq 2 ];then
        yum install -y https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm
        sed -i "s/repo.saltstack.com/mirrors.aliyun.com\/saltstack/g" /etc/yum.repos.d/salt-latest.repo
        yum install -y $salt_name
        systemctl enable $salt_name
        systemctl start $salt_name	
        echo "s$salt_name已经安装"
    fi 
}


#4)salt-minion配置
function salt-minion(){
    read -p "请输salt-master的IP:" master_ip
	if [ ! -n "$master_ip" ];then
		echo "未获取salt-master的IP，无法配置salt-minion"
	else
		if [ -f "$minion_file" ]; then
            num1=`grep -vE '^#|^$' $minion_file | grep master |wc -l `
            old_ip=`grep -vE '^#|^$' $minion_file | grep master | awk -F ":"  '{print $2}'`
            if [ $num1 -eq 0 ];then
                sed -i "17i master: $master_ip" $minion_file
                echo "salt-minion配置salt-master的IP为：$master_ip"
            else
                sed  -i "s/$old_ip/$master_ip/"  $minion_file
                echo "salt-minion配置salt-master的IP为：$master_ip"
            fi
        
        else
            echo "$minion_file文件不存在"
        fi
	fi
}


#删除软件
function salt_remove(){
    salt_name=$1
    salt_status=`rpm -qa | grep $salt_name`
    if [  ! -n "$salt_status" ];then
        echo "$salt_name没有安装"
    else
        rpm -qa | grep $salt_name | xargs rpm -e
        if [ $? -eq 0 ];then
            echo "$salt_name已经卸载"
        fi
    fi
}

#重启服务
function salt_restart(){
    salt_name=$1
    if_installed $salt_name
    if [ $? -eq 2 ];then
        echo ""
    else
        systemctl restart $salt_name
        echo "$salt_name已经重启"
    fi
}



#菜单
function menu()
{
echo -e "         $datetime"
cat <<EOF
--------------------------------------------
`echo -e "        $black SaltStack菜单主页$background"`
`echo -e "$Orange  1)安装slat-master $background"`    `echo -e "$Orange   2)安装salt-minion$background"`
`echo -e "$Orange  3)是否软件安装查询$background"`     `echo -e "$Orange   4)salt-minion配置$background"`
`echo -e "$Orange  5)卸载slat-master$background"`      `echo -e "$Orange  6)卸载slat-minion$background"`
`echo -e "$Orange  7)重启slat-master$background"`      `echo -e "$Orange  8)重启slat-minion$background"`
`echo -e "$Orange  Q)退出$background"`                
--------------------------------------------
EOF
read -p "请输入对应序列号：" num1
case $num1 in
    1)
    install_master salt-master
    menu
    ;;
    2)
    install_master salt-minion
    menu
    ;;
    3)
    if_installed salt-master
    if_installed salt-minion
    menu
    ;;
    4)
    salt-minion
    menu
    ;;
    5)
    salt_remove salt-master
    menu
    ;;
    6)
    salt_remove salt-minion
    menu
    ;;
    7)
    salt_restart salt-master
    menu
    ;;
    8)
    salt_restart salt-minion
    menu
    ;;
    Q|q)
    exit 0
    ;;
    *)
    echo -e "\033[31m err：请输入正确的编号\033[0m"
    menu
esac
}

menu
```