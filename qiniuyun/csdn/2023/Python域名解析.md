---
author: 南宫乘风
categories:
- 企业级-Shell脚本案例
date: 2023-03-21 10:45:13
description: 、背景阿里云是一个全球领先的云计算服务提供商，其域名解析服务可以帮助用户将域名映射到地址，从而使得网站可以被访问。、需求日常使用阿里云域名解析服务需要登录阿里云账号进行操作，但是这样手工操作费时费力。。。。。。。。
image: ../../title_pic/16.jpg
slug: '202303211045'
tags:
- python
title: Python域名解析
---

<!--more-->

# 1、背景

阿里云是一个全球领先的云计算服务提供商，其域名解析服务可以帮助用户将域名映射到IP地址，从而使得网站可以被访问。

# 2、需求

日常使用阿里云域名解析服务需要登录阿里云账号进行操作，但是这样手工操作费时费力。因此，我们需要使用Python编写程序来实现域名解析功能，以便快速方便地完成域名解析任务。具体实现过程为：通过调用阿里云API接口获取用户授权，然后使用Python的DNS解析库对域名进行解析，并将解析结果存储到本地或者发送到指定邮箱。这样就可以省去手动登录阿里云的步骤，大大提高了工作效率。

# 3、Python2自动域名解析

Python环境：Python 2.7.5

阿里云的SDK：

aliyun-python-sdk-alidns \(2.6.20\)

aliyun-python-sdk-core \(2.13.30\)

自动域名解析是一种高效的方式，可以帮助我们快速地将域名映射到对应的IP地址。在CentOS机器上，由于Python环境版本较老，因此需要注意对代码进行适配，以确保程序正常运行。

在Python 2环境下，一些语法和库函数可能已经过时或不再支持，因此在编写代码时应该仔细检查，并根据需要进行相应的修改和替代。这样才能够确保程序的稳定运行和正确性。

因为Centos机器默认安装Python2.0的环境，我们就是用2.0的语法进行书写

```python
#!/usr/bin/env python
#coding=utf-8

# 导入模块
import os      # 用于和操作系统交互
import sys     # 用于获取命令行参数
import time    # 用于处理时间相关的操作
import json    # 用于解析和生成 JSON 格式的数据

# 导入阿里云 SDK 相关模块
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest

# 创建一个 AcsClient 实例，用于调用阿里云 API
client = AcsClient('xxxx', 'xxxx', 'cn-xxxx')

# 获取命令行参数，并判断是否满足要求
v = sys.argv
if len(v) < 2:
    print("域名或记录值不存在")
else:
    m = v[1]
    value = v[2]
    domain = m.split(".xxx.com")[0]  # 提取二级域名

# 创建一个阿里云 API 调用请求对象
request = AddDomainRecordRequest()
request.set_accept_format('json')

# 设置该请求需要传递的参数
request.set_DomainName("xxx.com")  # 将 xxx.com 替换为你自己的一级域名
request.set_RR(domain)            # 设置二级域名
if len(value) <= 15:
    request.set_Type("A")         # 如果记录值不超过 15 个字符，则为 A 记录
else:
    request.set_Type("CNAME")     # 否则为 CNAME 记录
request.set_Value(value)          # 设置记录值

# 发送 API 请求，并处理异常
try:
    response = client.do_action_with_exception(request)
    print(response)
except Exception as e:
    print(e)
```

使用方法

```bash
./addDNS-xxx.py  fyhm.xxxx.net  需要解析IP

 for i in `cat dns.list`;do ./addDNS-xx.py $i IP;done
```

![](../../image/99943cf1cc05427e87591b1b83173911.png)

已经存在

![](../../image/9b7d68c35a0245808cd8562af896d9e6.png)

# 4、shell界面化

![](../../image/00f7badb302f48bdbf38f1ac80d8bc93.png)

![](../../image/e0e1be1532d44677a8cdf3cd0f87a8a2.png)

```bash
#!/bin/bash

#日志级别 debug-1, info-2, warn-3, error-4, always-5
LOG_LEVEL=1

#日志名称
job_name=dns_name

#脚本目录
script_dir=/opt

#日志文件
LOG_FILE=./${job_name}.log

#调试日志
function log_debug() {
    content="[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $@"
    [ $LOG_LEVEL -le 1 ] && echo $content >>$LOG_FILE && echo -e "\033[32m" ${content} "\033[0m"
}
#信息日志
function log_info() {
    content="[INFO] $(date '+%Y-%m-%d %H:%M:%S') $@"
    [ $LOG_LEVEL -le 2 ] && echo $content >>$LOG_FILE && echo -e "\033[32m" ${content} "\033[0m"
}
#警告日志
function log_warn() {
    content="[WARN] $(date '+%Y-%m-%d %H:%M:%S') $@"
    [ $LOG_LEVEL -le 3 ] && echo $content >>$LOG_FILE && echo -e "\033[33m" ${content} "\033[0m"
}
#错误日志
function log_err() {
    content="[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $@"
    [ $LOG_LEVEL -le 4 ] && echo $content >>$LOG_FILE && echo -e "\033[31m" ${content} "\033[0m"
}
#一直都会打印的日志
function log_always() {
    content="[ALWAYS] $(date '+%Y-%m-%d %H:%M:%S') $@"
    [ $LOG_LEVEL -le 5 ] && echo $content >>$LOG_FILE && echo -e "\033[32m" ${content} "\033[0m"
}

# 定义函数：增加解析记录
function add_dns_record() {
    local domain=$1
    local ip=$2
    local script=$3

    # 校验域名是否符合要求
    if [[ $domain =~ $4 ]]; then
        log_info "$domain 效验通过 正常"
    else
        log_err "不包含 $4，请检查域名是否符合"
        exit 1
    fi

    # 增加解析记录
    log_info "开始增加 $domain 解析"
    $script $domain $ip >/dev/null 2>&1
    if [ $? != "0" ]; then
        log_err "$domain 解析已经存在，请检查"
        exit 1
    fi
    log_info "$domain 添加解析完毕"
}

# 定义函数：生产域名
function prod_fujfu() {
    # TODO: 在这里实现生产域名的操作
    log_info "您选择了 prod_fujfu"
    read -p "请输您的域名:  " choice2
    add_dns_record $choice2 xxxxxxxx $script_dir/addDNS.py "xxxx.com"
}

# 定义函数：测试域名
function uat_fujfu() {
    # TODO: 在这里实现测试域名的操作
    log_info "您选择了 uat_fujfu"
    read -p "请输您的域名:  " choice2
    add_dns_record $choice2 xxx.xxx.xxx.xxx $script_dir/addDNS.py "xxxx.com"

}

# 定义函数：uat 域名
function prod_xxxx() {
    # TODO: 在这里实现生产域名的操作
    log_info "您选择了 prod_xxxx"
    read -p "请输您的域名:  " choice2
    add_dns_record $choice2 xxx.xxx.xxx.xxx $script_dir/addDNS-xxxx.py "xxxx.net"

}

# 定义函数：dev域名
function uat_xxxx() {
    # TODO: 在这里实现dev域名的操作
    log_info "您选择了 uat_xxxx"
    read -p "请输您的域名:  " choice2
    add_dns_record $choice2 xxx.xxx.xxx.xxx $script_dir/addDNS-xxxx.py "xxxx.net"

}

# 定义函数：uat 域名
function prod_mumugz() {
    # TODO: 在这里实现生产域名的操作
    log_info "您选择了 prod_mumugz"
    read -p "请输您的域名:  " choice2
    add_dns_record $choice2 xxx.xxx.xxx.xxx $script_dir/addDNS-mumugz.py "xxxx.com"

}

# 定义函数：dev域名
function uat_mumugz() {
    # TODO: 在这里实现dev域名的操作
    log_info "您选择了 uat_mumugz"
    read -p "请输您的域名:  " choice2
    add_dns_record $choice2 xxx.xxx.xxx.xxx $script_dir/addDNS-mumugz.py "xxxx.com"

}

# 定义主函数
function main() {
    # 显示菜单
    echo "请选择一个选项："
    echo "1. 生产 xxxx.com"
    echo "2. 测试 xxxx.com"
    echo "3. 生产 xxxx.net"
    echo "4. 测试 xxxx.net"
    echo "5. 生产 xxxx.com"
    echo "6. 测试 xxxx.com"
    # 读取用户输入
    read -p "请输您的选择:  " choice

    # 根据用户输入选择对应的操作
    case $choice in
    1) prod_fujfu ;;
    2) uat_fujfu ;;
    3) prod_xxxx ;;
    4) uat_xxxx ;;
    5) prod_mumugz ;;
    6) uat_mumugz ;;
    *) echo "无效的选项，请重新输入" ;;
    esac

}

# 调用主函数
main
```

![](../../image/cb86f836b886494aae2869483bea6df6.png)