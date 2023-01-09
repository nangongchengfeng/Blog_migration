+++
author = "南宫乘风"
title = "Ansible小实例"
date = "2021-05-05 00:07:08"
tags=['linux', 'centos', 'ssh', 'ansible']
categories=['Ansible']
image = "post/4kdongman/97.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/116401940](https://blog.csdn.net/heian_99/article/details/116401940)

## 1、向各主机分发秘钥

方法一

```
---
- name: 配置ssh免秘钥连接
  hosts: new
  gather_facts: false
  connection: local #本地连接
  tasks:
    - name: configure ssh connection
      shell: |
        ssh-keyscan {<!-- -->{inventory_hostname}} &gt;&gt;~/.ssh/known_hosts
        sshpass -p'密码' ssh-copy-id root@{<!-- -->{inventory_hostname}}

```

方法二 

```
---
- name: configure ssh connection
  hosts: new
  gather_facts: false
  tasks:
    - authorized_key:
        key: "{<!-- -->{lookup('file','~/.ssh/id_rsa.pub')}}"
        state: present
        user: root
```

执行该playbook，主机加上了`-k`选项，它会提示用户输入ssh连接密码。如果所有目标主机的密码都相同，则只需输入一次即可：

```
$ ansible-playbook -k anth_key.yml
SSH password: 

PLAY [configure ssh connection] ***********

TASK [authorized_key] *********************
changed: [192.168.200.34]
changed: [192.168.200.35]
......
```

## 2、循环创建文件

方法一

```
---
- name: play1
  hosts: localhost
  gather_facts: false
  tasks: 
    - name: create /tmp/test1
      file: 
        path: /tmp/test1
        state: directory

    - name: create /tmp/test2
      file: 
        path: /tmp/test2
        state: directory
```

方法二

```
---
- name: play1
  hosts: localhost
  gather_facts: false
  tasks: 
    - name: create directories
      file: 
        path: "{<!-- -->{item}}"
        state: directory
      loop:
        - /tmp/test1
        - /tmp/test2
```

## 3、设置多个主机名

```
---
- name: set hostname
  hosts: new
  gather_facts: false
  vars:
    hostnames:
      - host: 192.168.200.34
        name: new1
      - host: 192.168.200.35
        name: new2
  tasks: 
    - name: set hostname
      hostname: 
        name: "{<!-- -->{item.name}}"
      when: item.host == inventory_hostname
      loop: "{<!-- -->{hostnames}}"
```

 

## 4、主机之间相互添加DNS

```
---
- name: add DNS for each
  hosts: new
  gather_facts: true
  tasks: 
    - name: add DNS
      lineinfile: 
        path: "/etc/hosts"
        line: "{<!-- -->{item}} {<!-- -->{hostvars[item].ansible_hostname}}"
      when: item != inventory_hostname
      loop: "{<!-- -->{ play_hosts }}"
```

 

## 5、添加yum源

```
---
- name: config yum repo and install software
  hosts: new
  gather_facts: false
  tasks: 
    - name: backup origin yum repos
      shell: 
        cmd: "mkdir bak; mv *.repo bak"
        chdir: /etc/yum.repos.d
        creates: /etc/yum.repos.d/bak

    - name: add os repo and epel repo
      yum_repository: 
        name: "{<!-- -->{item.name}}"
        description: "{<!-- -->{item.name}} repo"
        baseurl: "{<!-- -->{item.baseurl}}"
        file: "{<!-- -->{item.name}}"
        enabled: 1
        gpgcheck: 0
        reposdir: /etc/yum.repos.d
      loop:
        - name: os
          baseurl: "https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/os/$basearch"
        - name: epel
          baseurl: "https://mirrors.tuna.tsinghua.edu.cn/epel/$releasever/$basearch"

    - name: install pkgs
      yum: 
        name: lrzsz,vim,dos2unix,wget,curl
        state: present
```

## 6、时间同步

```
---
- name: sync time
  hosts: new
  gather_facts: false
  tasks: 
    - name: install and sync time
      block: 
        - name: install ntpdate
          yum: 
            name: ntpdate
            state: present

        - name: ntpdate to sync time
          shell: |
            ntpdate ntp1.aliyun.com
            hwclock -w
    - name: date_show
      shell: |
        date +%F-%T

```

## 7、关闭selinux

```
---
- name: disable selinux
  hosts: new
  gather_facts: false
  tasks: 
    - block: 
        - name: disable on the fly
          shell: setenforce 0

        - name: disable forever in config
          lineinfile: 
            path: /etc/selinux/config
            line: "SELINUX=disabled"
            regexp: '^SELINUX='
      ignore_errors: true
```

## 8、配置防火墙

方法一

```
---
- name: set firewall
  hosts: new
  gather_facts: false
  tasks: 
    - name: set iptables rule
      shell: |
        # 备份已有规则
        iptables-save &gt; /tmp/iptables.bak$(date +"%F-%T")
        # 给它三板斧
        iptables -X
        iptables -F
        iptables -Z

        # 放行lo网卡和允许ping
        iptables -A INPUT -i lo -j ACCEPT
        iptables -A INPUT -p icmp -j ACCEPT

        # 放行关联和已建立连接的包，放行22、443、80端口
        iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
        iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
        iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
        iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT

        # 配置filter表的三链默认规则，INPUT链丢弃所有包
        iptables -P INPUT DROP
        iptables -P FORWARD DROP
        iptables -P OUTPUT ACCEPT
```

方法二

```
---
- name: set firewall
  hosts: new
  gather_facts: false
  vars: 
    allowed_tcp_ports: [22,80,443]
    default_policies:
      INPUT: DROP
      FORWARD: DROP
      OUTPUT: ACCEPT
    user_iptables_rule: 
      - iptables -A INPUT -p tcp -m tcp --dport 8000 -j ACCEPT
      - iptables -A INPUT -p tcp -m tcp --dport 8080 -j ACCEPT

  tasks: 
    - block: 
      - name: backup and empty rules
        shell: |
          # 备份已有规则，并清空规则等
          iptables-save &gt; /tmp/iptables.bak$(date +"%F-%T")
          iptables -X
          iptables -F
          iptables -Z

      - name: green light for lo interface and icmp protocol
        shell: |
          # 放行lo接口、ping和已建立连接的包
          iptables -A INPUT -i lo -j ACCEPT
          iptables -A INPUT -p icmp -j ACCEPT
          iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

      # 放行用户指定的tcp端口列表
      - name: allow for given tcp port
        shell: iptables -A INPUT -p tcp -m tcp --dport {<!-- -->{item}} -j ACCEPT
        loop: "{<!-- -->{ allowed_tcp_ports | default([]) }}"

      # 执行用户自定义的iptables命令
      - name: execute user iptables command
        shell: "{<!-- -->{item}}"
        loop: "{<!-- -->{user_iptables_rule | default([]) }}"

      # 设置filter表三链的默认规则
      - name: default policies for filter table
        shell: iptables -P {<!-- -->{item.key}} {<!-- -->{item.value}}
        loop: "{<!-- -->{ query('dict', default_policies | default({})) }}"
```

## 9、远程修改sshd配置文件并重启

采用lineinfile模块去修改配置文件，要修改的内容只有两项： 1.将PermitRootLogin指令设置为no，禁止root用户直接登录 2.将PasswordAuthentication指令设置为no，不允许使用密码认证的方式登录

```
---
- name: modify sshd_config
  hosts: new
  gather_facts: false
  tasks:
    # 1. 备份/etc/ssh/sshd_config文件
    - name: backup sshd config
      shell: 
        /usr/bin/cp -f {<!-- -->{path}} {<!-- -->{path}}.bak
      vars: 
        - path: /etc/ssh/sshd_config

    # 2. 设置PermitRootLogin no
    - name: disable root login
      lineinfile: 
        path: "/etc/ssh/sshd_config"
        line: "PermitRootLogin no"
        insertafter: "^#PermitRootLogin"
        regexp: "^PermitRootLogin"
      notify: "restart sshd"

    # 3. 设置PasswordAuthentication no
    - name: disable password auth
      lineinfile: 
        path: "/etc/ssh/sshd_config"
        line: "PasswordAuthentication no"
        regexp: "^PasswordAuthentication yes"
      notify: "restart sshd"

  handlers: 
    - name: "restart sshd"
      service: 
        name: sshd
        state: restarted
```

 

通过一个入口文件引入所有这些任务文件将它们组织起来。假设入口文件名为main.yaml，其内容为：

```
---
- import_playbook: "init_server/sshkey.yaml"
- import_playbook: "init_server/hostname.yaml"
- import_playbook: "init_server/add_dns.yaml"
- import_playbook: "init_server/add_repos.yaml"
- import_playbook: "init_server/synctime.yaml"
- import_playbook: "init_server/disable_selinux.yaml"
- import_playbook: "init_server/iptables.yaml"
- import_playbook: "init_server/sshd_config.yaml"
```

 

 
