---
author: 南宫乘风
categories:
- Ansible
date: 2024-01-26 10:29:52
description: 批量主机机器到、背景在现代环境中，随着机器数量的增加和复杂性的提高，手动管理和配置机器变得越来越困难和耗时。为了提高效率并确保一致性，自动化工具成为了不可或缺的一部分。是一个功能强大的堡垒机和服务器管。。。。。。。
image: ../../title_pic/15.jpg
slug: '202401261029'
tags:
- 自动化
- linux
- 运维
title: 自动化批量导入机器到Jumpserver：提高效率与一致性的关键步骤
---

<!--more-->

# Ansible批量主机机器到Jumpserver

## 1、背景

在现代 IT 环境中，随着机器数量的增加和复杂性的提高，手动管理和配置机器变得越来越困难和耗时。为了提高效率并确保一致性，自动化工具成为了不可或缺的一部分。Jumpserver 是一个功能强大的堡垒机和服务器管理平台，可以帮助管理员更好地管理和控制远程机器。

最近，我们面临着一个挑战：**需要将一批新的机器（约 K 台）导入到 Jumpserver 中，并按照预定义的分组进行组织**。手动逐个导入这些机器将是一项繁琐且容易出错的任务。为了解决这个问题，**我们决定使用自动化脚本来批量导入机器到 Jumpserver，并根据分组进行组织**。

## 2、环境准备

Ansible

```bash
root@wq-1:~/file# ansible --version
ansible 2.10.8
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]
```

Jumpserver 版本（3.8.1）

‍

## 3、操作流程

**jumpserverAPI 文档** ⚓︎   [https://docs.jumpserver.org/zh/master/dev/rest_api/](https://docs.jumpserver.org/zh/master/dev/rest_api/)

‍

### 1、获取 Jumpserver 的 token

需要替换 网站地址 和 用户 账号 和 密码。

> （注意）：Jumpserver 的版本不一样，接口文档的参数也会变得，请依照自己的版本接口调试。

```bash
curl -X POST https://jms.网站.top/api/v1/authentication/auth/      -H 'Content-Type: application/json'      -d '{"username": "admin", "password": "xxxx"}'
```

![在这里插入图片描述](../../image/77b9cdeb4a2a42b39ab4a800814ef0bd.png)
​

### 2、创建所有机器的模板账号

所有的机器可以统一使用同一 账号来管理。账号可以使用 ，密码或秘钥。根据自己情况来操作，我们这边需要这个模板账号的 id 进行绑定，这样就可以在 Jumpserver 中远程访问机器。

步骤 1
![在这里插入图片描述](../../image/6491cb1d45ca474d8319951ee37cc888.png)


​

步骤 2
![在这里插入图片描述](../../image/17fa23d2e8014346b22b2edc6962db11.png)

​​

步骤 3
![在这里插入图片描述](../../image/eb1923da1e3e4edd893e4b5772d5ecce.png)

​​

我们需要这个 id 号。

### 3、自动创建分组和机器脚本

**add_jms_hosts.sh （会参入三个参数    分组名称   IP 地址    主机名称） 注意：这个脚本必选 配合 jq  。请先安装完成使用**

```bash
yum install -y jq
```

主机名称作为 id 来的，所以值必选唯一，请注意

```bash

#!/bin/bash

# JumpServer API 相关信息
JUMPSERVER_URL="http://10.1.10.3/api/v1"
JUMPSERVER_TOKEN="8j85rhlicQ8Mjxxxxx"

# 传入的参数
GROUP_NAME="$1"
IP="$2"
HOST_NAME="$3"

# 检查分组是否存在，不存在则创建
check_and_create_group() {
    echo "检查分组是否存在..."
    group_id=$(curl -s -H "Authorization: Bearer $JUMPSERVER_TOKEN" "$JUMPSERVER_URL/assets/nodes/" | jq -r --arg GROUP_NAME "$GROUP_NAME" '.[] | select(.name==$GROUP_NAME) | .id')
  
    if [ -z "$group_id" ]; then
        echo "分组不存在，创建分组..."
        group_id=$(curl -s -X POST -H "Authorization: Bearer $JUMPSERVER_TOKEN" -H "Content-Type: application/json" -d '{"value": "'$GROUP_NAME'"}' "$JUMPSERVER_URL/assets/nodes/" | jq -r '.id')
        echo "创建后的分组ID: $group_id"
    else
        echo "找到的分组ID: $group_id"
    fi
}

# 创建或更新资产
create_or_update_asset() {
    echo "创建或更新资产 $HOST_NAME ..."
    asset_data='{
        "name": "'$HOST_NAME'",
        "address": "'$IP'",
        "platform": "1",
        "protocols": [{"name": "ssh", "port": 22}],
        "is_active": true,
        "nodes": ["'$group_id'"],
        "accounts": [{"template": "f728c07f-003e-415e-a6be-d02e6fbf7f28"}]
    }'
	 #此处的id，为模板账号 id
    response=$(curl -s -X POST -H "Authorization: Bearer $JUMPSERVER_TOKEN" -H "Content-Type: application/json" -d "$asset_data" "$JUMPSERVER_URL/assets/hosts/")
    echo "资产创建或更新响应: $response"
}

check_and_create_group
create_or_update_asset
```

执行 demo

```bash
root@wq-1:~/file# ./add_jms_hosts.sh ownit 192.168.16.16 ownit-16
检查分组是否存在...
分组不存在，创建分组...
创建后的分组ID: b939d606-e334-494f-8a87-b1b464a941ce
创建或更新资产 ownit-16 ...
资产创建或更新响应: {"id":"ec503228-77e8-4d44-9c5a-a322f45ad4ec","name":"ownit-16","address":"192.168.16.16","comment":"","domain":null,"platform":{"id":1,"name":"Linux"},"nodes":[{"id":"b939d606-e334-494f-8a87-b1b464a941ce","name":"ownit"}],"labels":[],"protocols":[{"name":"ssh","port":22}],"nodes_display":["/Default/ownit"],"category":{"value":"host","label":"主机"},"type":{"value":"linux","label":"Linux"},"connectivity":{"value":"-","label":"未知"},"auto_config":{"su_enabled":true,"domain_enabled":true,"ansible_enabled":true,"id":1,"ansible_config":{"ansible_connection":"smart"},"ping_enabled":true,"ping_method":"posix_ping","ping_params":{},"gather_facts_enabled":true,"gather_facts_method":"gather_facts_posix","gather_facts_params":{},"change_secret_enabled":true,"change_secret_method":"change_secret_posix","change_secret_params":{},"push_account_enabled":true,"push_account_method":"push_account_posix","push_account_params":{"sudo":"/bin/whoami","shell":"/bin/bash","home":"","groups":""},"verify_account_enabled":true,"verify_account_method":"verify_account_posix","verify_account_params":{},"gather_accounts_enabled":true,"gather_accounts_method":"gather_accounts_posix","gather_accounts_params":{},"remove_account_enabled":true,"remove_account_method":"remove_account_posix","remove_account_params":{},"platform":1},"created_by":"Administrator","gathered_info":{},"org_id":"00000000-0000-0000-0000-000000000002","org_name":"Default","spec_info":{},"is_active":true,"date_verified":null,"date_created":"2024/01/26 09:50:54 +0800"}
```

![在这里插入图片描述](../../image/54f7de80ec574d6aa766a204ebab33c7.png)


### 4、Ansible 批量跑脚本

上面的脚本已经实现，现在就批量跑数据。（注意，使用 Ansible 跑，但是有个问题，有些不成功） **最后使用 shell 脚本来处理 的**

‍

Ansible 的 hosts 定义

```bash
root@wq-1:~/ansible# cat hosts 
[all:vars]
ansible_ssh_user=root
ansible_ssh_pass=dgadxxx

[wq]
10.1.11.[1:90]
[li]
10.1.17.[1:46]
```

Ansible 的剧本文件（注意 hosts 的定义，我是按分组单个执行）

```bash
 {{ group_names[0] }} {{ inventory_hostname }}  这两个是Ansible的内置变量

ansible own  -m setup 可以使用 这个查询那个有内置变量
[root@bt ~]# ansible own  -m setup  | head -n  50
192.168.102.20 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.102.20", 
            "172.17.0.1", 
            "172.23.0.1", 
            "172.18.0.1", 
            "172.22.0.1", 
            "172.25.1.10", 
            "172.19.0.1"
        ], 
        "ansible_all_ipv6_addresses": [
            "fe80::a095:f2ff:fe80:413b", 
            "fe80::42:b1ff:fe02:9e5f", 
            "fe80::42:20ff:fe5e:7cfd", 
            "fe80::6c19:a7ff:fe5e:a4f", 
            "fe80::ac72:32ff:feaa:3ef", 
            "fe80::c0a1:c1ff:fea2:63b9"
        ], 
        "ansible_apparmor": {
            "status": "disabled"
        }, 


```

```bash
root@wq-1:~/ansible# cat add_jms_host.yml 
- hosts: wq
  remote_user: root
  gather_facts: no
  tasks:
    - name: 复制 jq 到远程主机
      copy:
        src: /usr/bin/jq
        dest: /usr/bin/jq
        mode: '0755'

    - name: 获取系统的主机名称
      shell: hostname
      register: result

    - name: 打印变量
      debug:
        msg:
          - "Group Name: {{ group_names[0] }}"
          - "Ansible Host: {{ inventory_hostname  }}"
          - "Inventory Hostname: {{ result.stdout }}"

    - name: "执行添加到 JumpServer 的脚本"
      script: /root/file/add_jms_hosts.sh {{ group_names[0] }} {{ inventory_hostname }} {{ result.stdout }}
      args:
        executable: /bin/bash
```

执行的 demo

```bash
 ansible-playbook add_jms_host.yml -i ./hosts
```

上执行完毕，但是有问题，我 90 台机器，但实际添加的只有 30 台，其余是执行正常的，但是没有添加。

或者使用下面的

‍

```bash
- hosts: wq
  remote_user: root
  gather_facts: no
  tasks:
    - name: 复制 jq 到远程主机
      copy:
        src: /usr/bin/jq
        dest: /usr/bin/jq
        mode: '0755'

    - name: 复制 add_jms_hosts.sh 到远程主机
      copy:
        src: /root/file/add_jms_hosts.sh
        dest: /root/add_jms_hosts.sh
        mode: '0755'

    - name: 获取系统的主机名称
      shell: hostname
      register: result

    - name: 打印变量
      debug:
        msg:
          - "Group Name: {{ group_names[0] }}"
          - "Ansible Host: {{ inventory_hostname  }}"
          - "Inventory Hostname: {{ result.stdout }}"

    - name: 执行添加到 JumpServer 的脚本
      command: /bin/bash /root/add_jms_hosts.sh {{ group_names[0] }} {{ inventory_hostname }} {{ result.stdout }}

```

‍

### 5、shell 执行批量数据

如果上面的执行还是不行，那就使用 下方的方式 100 % 可以。

我先使用 ansible 跑出 分组  ip 和 主机名称

‍

```bash
- hosts: li
  remote_user: root
  gather_facts: no
  tasks:
    - name: 获取系统的主机名称
      shell: hostname
      register: result

    - name: 打印变量
      debug:
        msg:
          - "{{ group_names[0] }}  {{ inventory_hostname  }}  {{ result.stdout }} "
```

执行

```bash
ansible-playbook test.yml -i ./hosts  >> 1.txt

cat 1.txt | grep wq > /root/file/host  （编辑host 删除 第一行 非 ip的）

sed 's/. *&quot;(.* \)".*/\1/'  host  > 1.txt   (出去 双引号)



过滤后的数据格式 



root@wq-1:~/file# cat 1.txt 
li  10.1.17.1  li-1 
li  10.1.17.2  li-2 
li  10.1.17.3  li-3 
li  10.1.17.4  li-4 
li  10.1.17.5  li-5 
li  10.1.17.6  li-6 
li  10.1.17.7  li-7 
li  10.1.17.8  li-8 
li  10.1.17.9  li-9 
```

```bash
root@wq-1:~/file# cat star_add.sh 
#!/bin/bash

while IFS= read -r line; do
  group=$(echo "$line" | awk '{print $1}')
  ip=$(echo "$line" | awk '{print $2}')
  name=$(echo "$line" | awk '{print $3}')
  echo "Group: $group, IP: $ip, Name: $name"
  # 在这里执行您的操作，例如调用其他脚本并传递这三个变量
  ./add_jms_hosts.sh "$group" "$ip" "$name"
done < 1.txt
```

bash star_add.sh  注册到 jumpserver 上

![在这里插入图片描述](../../image/7388d5887ab647e2969608aa5bd116a3.png)
​

‍

## 4、总结

我们的解决方案是编写一个脚本，该脚本可以读取包含机器信息的文本文件，并使用 Jumpserver 提供的 API 进行自动导入。脚本首先通过逐行读取文本文件来获取每台机器的相关信息，例如 IP 地址、主机名和分组。然后，它使用 Jumpserver 的 API 调用来创建新的机器对象，并将其分配到相应的分组中。

通过使用这个自动化脚本，我们可以大大减少手动操作的工作量，并确保导入的机器被正确地组织到 Jumpserver 中的相应分组中。这不仅提高了操作效率，还降低了出错的风险，并提供了一致性和可追溯性。

总结起来，通过编写自动化脚本来批量导入机器到 Jumpserver，并根据预定义的分组进行组织，我们能够提高工作效率、降低错误率，并确保一致性和可追溯性。这个解决方案为我们节省了宝贵的时间和精力，使我们能够更好地管理和控制远程机器。

