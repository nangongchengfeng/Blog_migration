---
author: 南宫乘风
categories:
- ansible
date: 2020-01-22 14:44:40
description: 一、自动化部署集群介绍是一种自动化工具。它可以配置系统，部署软件以及协调更高级的任务，例如持续部署，滚动更新。适用于管理企业基础设施，从具有少数主机的小规模到数千个实例的企业环境。也是一种简单的自动化。。。。。。。
image: http://image.ownit.top/4kdongman/41.jpg
tags:
- 自动化
title: Ansible自动化部署详细教程
---

<!--more-->

# 一、Ansible自动化部署K8S集群

## 1.1 Ansible介绍

Ansible是一种IT自动化工具。它可以配置系统，部署软件以及协调更高级的IT任务，例如持续部署，滚动更新。Ansible适用于管理企业IT基础设施，从具有少数主机的小规模到数千个实例的企业环境。Ansible也是一种简单的自动化语言，可以完美地描述IT应用程序基础结构。

具备以下三个特点：

- 简单：减少学习成本

- 强大：协调应用程序生命周期

- 无代理：可预测，可靠和安全

使用文档： <https://docs.ansible.com/>

安装Ansible：

```bash
yum install ansible -y
```

![](http://image.ownit.top/csdn/20200122122434796.png)

- Inventory：Ansible管理的主机信息，包括IP地址、SSH端口、账号、密码等

- Modules：任务均有模块完成，也可以自定义模块，例如经常用的脚本。

- Plugins：使用插件增加Ansible核心功能，自身提供了很多插件，也可以自定义插件。例如connection插件，用于连接目标主机。

- Playbooks：“剧本”，模块化定义一系列任务，供外部统一调用。Ansible核心功能。

## 1.2 主机清单

 

<table border="1" cellpadding="1" cellspacing="1" style="width:500px;"><tbody><tr><td>服务</td><td>主机名称</td><td>IP地址</td></tr><tr><td>服务端</td><td>master</td><td>192.168.116.129</td></tr><tr><td>客户端</td><td>node1</td><td>192.168.116.130</td></tr><tr><td>客户端</td><td>node2</td><td>192.168.116.131</td></tr></tbody></table>
 

## 1.3 命令行使用

ad-hoc命令可以输入内容，快速执行某个操作，但不希望留存记录。

ad-hoc命令是理解Ansible和在学习playbooks之前需要掌握的基础知识。

一般来说，Ansible的真正能力在于剧本。

### 1、连接远程主机认证

配置主机清单目录：/etc/ansible

配置hosts ：vim /etc/ansible/hosts 

![](http://image.ownit.top/csdn/20200122124117518.png)

 

SSH密码认证：【主机清单配置】

```bash
[webservers]
192.168.116.130:22 ansible_ssh_user=root ansible_ssh_pass=’root’
192.168.116.131:22 ansible_ssh_user=root ansible_ssh_pass=’root’
```

![](http://image.ownit.top/csdn/20200122130324380.png)

SSH密钥对认证：

```
ssh-keygen
```

![](http://image.ownit.top/csdn/20200122130550452.png)

```bash
ssh-copy-id root@192.168.116.130
```

```
[webservers]
192.168.116.130:22 ansible_ssh_user=root ansible_ssh_key=/root/.ssh/id_rsa 
192.168.116.131:22 ansible_ssh_user=root
```

 

也可以ansible.cfg在配置文件中指定：

```
[defaults]
private_key_file = /root/.ssh/id_rsa  # 默认路径
```

测速是否连通

![](http://image.ownit.top/csdn/20200122125238374.png)

![](http://image.ownit.top/csdn/20200122125502470.png)

```
ansible webservers -m ping -uroot -k
```

![](http://image.ownit.top/csdn/20200122125414493.png)

### 2、常用选项

| 选项 | 描述 |
| --- | --- |
| \-C, --check | 运行检查，不执行任何操作 |
| \-e EXTRA\_VARS,--extra-vars=EXTRA\_VARS | 设置附加变量 key=value |
| \-u REMOTE\_USER, --user=REMOTE\_USER | SSH连接用户，默认None |
| \-k, --ask-pass | SSH连接用户密码 |
| \-b, --become | 提权，默认root |
| \-K, --ask-become-pass | 提权密码 |

###   
3、命令行使用

```bash
ansible all -m ping
ansible all -m shell -a "ls /root" -u root -k 
ansible webservers -m copy –a "src=/etc/hosts dest=/tmp/hosts"
```

## 1.4 常用模块

ansible-doc –l 查看所有模块

ansible-doc –s copy 查看模块文档

模块文档：<https://docs.ansible.com/ansible/latest/modules/modules_by_category.html>

### 1、shell

```bash
- name: 将命令结果输出到指定文件
  shell: somescript.sh >> somelog.txt
- name: 切换目录执行命令
  shell:
    cmd: ls -l | grep log
    chdir: somedir/
- name: 编写脚本
  shell: |
      if [ 0 -eq 0 ]; then
         echo yes > /tmp/result
      else
         echo no > /tmp/result
      fi
  args:
    executable: /bin/bash
```

```bash
 ansible webservers -m shell -a "ls /root;df -h"
```

### ![](http://image.ownit.top/csdn/20200122131951893.png)

### 2、copy

将文件复制到远程主机。

```bash
- name: 拷贝文件
  copy:
    src: /srv/myfiles/foo.conf
    dest: /etc/foo.conf
    owner: foo
    group: foo
    mode: u=rw,g=r,o=r
    # mode: u+rw,g-wx,o-rwx
    # mode: '0644'
    backup: yes
```

### 3、file

管理文件和文件属性。

```bash
- name: 创建目录
  file:
    path: /etc/some_directory
    state: directory
    mode: '0755'
- name: 删除文件
  file:
    path: /etc/foo.txt
    state: absent
- name: 递归删除目录
  file:
    path: /etc/foo
    state: absent
```

present，latest：表示安装

absent：表示卸载

### 4、yum

软件包管理。

```bash
- name: 安装最新版apache
  yum:
    name: httpd
    state: latest
- name: 安装列表中所有包
  yum:
    name:
      - nginx
      - postgresql
      - postgresql-server
    state: present
- name: 卸载apache包
  yum:
    name: httpd
    state: absent 
- name: 更新所有包
  yum:
    name: '*'
    state: latest
- name: 安装nginx来自远程repo
  yum:
    name: http://nginx.org/packages/rhel/7/x86_64/RPMS/nginx-1.14.0-1.el7_4.ngx.x86_64.rpm
    # name: /usr/local/src/nginx-release-centos-6-0.el6.ngx.noarch.rpm
    state: present
```

### 5、service/systemd

管理服务。

```bash
- name: 服务管理
  service:
    name: etcd
    state: started
    #state: stopped
    #state: restarted
    #state: reloaded
- name: 设置开机启动
  service:
    name: httpd
    enabled: yes
```

```bash
- name: 服务管理  
  systemd: 
	name=etcd 
	state=restarted 
	enabled=yes 
	daemon_reload=yes
```

### 6、unarchive

```
- name: 解压
  unarchive: 
    src=test.tar.gz 
    dest=/tmp
```

### 7、debug

执行过程中打印语句。

```bash
- debug:
    msg: System {{ inventory_hostname }} has uuid {{ ansible_product_uuid }}

- name: 显示主机已知的所有变量
  debug:
    var: hostvars[inventory_hostname]
    verbosity: 4
```

## 1.5 Playbook

Playbooks是Ansible的配置，部署和编排语言。他们可以描述您希望在远程机器做哪些事或者描述IT流程中一系列步骤。使用易读的YAML格式组织Playbook文件。

如果Ansible模块是您工作中的工具，那么Playbook就是您的使用说明书，而您的主机资产文件就是您的原材料。

与adhoc任务执行模式相比，Playbooks使用ansible是一种完全不同的方式，并且功能特别强大。

<https://docs.ansible.com/ansible/latest/user_guide/playbooks.html>

```bash
---
- hosts: webservers
  vars:
    http_port: 80
    server_name: www.ctnrs.com
  remote_user: root
  gather_facts: false
  tasks:
  - name: 安装nginx最新版
    yum: pkg=nginx state=latest
  - name: 写入nginx配置文件
    template: src=/srv/httpd.j2 dest=/etc/nginx/nginx.conf
    notify:
    - restart nginx
  - name: 确保nginx正在运行
    service: name=httpd state=started
  handlers:
    - name: restart nginx
      service: name=nginx state=reloaded
```

### 1、主机和用户

```bash
- hosts: webservers
  remote_user: lizhenliang
  become: yes
  become_user: root
```

```
ansible-playbook nginx.yaml -u lizhenliang -k -b -K
```

### 2、定义变量

变量是应用于多个主机的便捷方式； 实际在主机执行之前，变量会对每个主机添加，然后在执行中引用

- **命令行传递**

  \-e VAR=VALUE

- **主机变量与组变量**

在Inventory中定义变量。

```bash
[webservers]
192.168.1.100 ansible_ssh_user=root hostname=web1
192.168.1.100 ansible_ssh_user=root hostname=web2
​
[webservers:vars]
ansible_ssh_user=root hostname=web1
```

- **单文件存储**

Ansible中的首选做法是不将变量存储在Inventory中。

除了将变量直接存储在Inventory文件之外，主机和组变量还可以存储在相对于Inventory文件的单个文件中。

组变量：

group\_vars 存放的是组变量

group\_vars/all.yml 表示所有主机有效，等同于\[all:vars\]

grous\_vars/etcd.yml 表示etcd组主机有效，等同于\[etcd:vars\]

 

  - **在Playbook中定义**

```bash
- hosts: webservers
  vars:
    http_port: 80
    server_name: www.ctnrs.com
```

  - **Register变量**

```bash
- shell: /usr/bin/uptime
  register: result
- debug:
    var: result
```

### 3、任务列表

 

每个play包含一系列任务。这些任务按照顺序执行，在play中，所有主机都会执行相同的任务指令。play目的是将选择的主机映射到任务。

```bash
 tasks:
  - name: 安装nginx最新版
    yum: pkg=nginx state=latest
```

### 4、语法检查与调试

语法检查：ansible-playbook \--check /path/to/playbook.yaml

测试运行，不实际操作：ansible-playbook \-C /path/to/playbook.yaml

debug模块在执行期间打印语句，对于调试变量或表达式，而不必停止play。与'when：'指令一起调试更佳。

```bash
 - debug: msg={{group_names}}
  - name: 主机名
    debug:
      msg: "{{inventory_hostname}}"
```

### 5、任务控制

如果你有一个大的剧本，那么能够在不运行整个剧本的情况下运行特定部分可能会很有用。

```bash
  tasks:
  - name: 安装nginx最新版
    yum: pkg=nginx state=latest
    tags: install
  - name: 写入nginx配置文件
    template: src=/srv/httpd.j2 dest=/etc/nginx/nginx.conf
    tags: config
```

使用：

```bash
ansible-playbook example.yml --tags "install"
ansible-playbook example.yml --tags "install,config"
ansible-playbook example.yml --skip-tags "install"
```

### 6、流程控制

条件：

```bash
tasks:
- name: 只在192.168.1.100运行任务
  debug: msg="{{ansible_default_ipv4.address}}"
  when: ansible_default_ipv4.address == '192.168.1.100'
```

循环：

```bash
tasks:
- name： 批量创建用户
  user: name={{ item }} state=present groups=wheel
  with_items:
     - testuser1
     - testuser2
```

```bash
- name: 解压
  copy: src={{ item }} dest=/tmp
  with_fileglob:
    - "*.txt"
```

常用循环语句：

| 语句 | 描述 |
| --- | --- |
| with\_items | 标准循环 |
| with\_fileglob | 遍历目录文件 |
| with\_dict | 遍历字典 |

### 7、模板

```bash
vars:
    domain: "www.ctnrs.com"
 tasks:
  - name: 写入nginx配置文件
    template: src=/srv/server.j2 dest=/etc/nginx/conf.d/server.conf
```

```bash
# server.j2
{% set domain_name = domain %}
server {
   listen 80;
   server_name {{ domain_name }};
   location / {
        root /usr/share/html;
   }
}
```

在jinja里使用ansible变量直接 \{<!-- -->\{ \}\}引用。使用ansible变量赋值jinja变量不用\{<!-- -->\{ \}\}引用。

**定义变量**：

\{\% set local\_ip = inventory\_hostname \%\}

**条件和循环**：

```bash
{% set list=['one', 'two', 'three'] %}
{% for i in list %}
    {% if i == 'two' %}
        -> two
    {% elif loop.index == 3 %}
        -> 3
    {% else %}
        {{i}}
    {% endif %}
{% endfor %}
```

例如：生成连接etcd字符串

```bash
{% for host in groups['etcd'] %}
    https://{{ hostvars[host].inventory_hostname }}:2379
    {% if not loop.last %},{% endif %}
{% endfor %} 
```

里面也可以用ansible的变量。

## 1.6 Roles

Roles是基于已知文件结构自动加载某些变量文件，任务和处理程序的方法。按角色对内容进行分组，适合构建复杂的部署环境。

### 1、定义Roles

Roles目录结构：

```bash
site.yml
webservers.yml
fooservers.yml
roles/
   common/
     tasks/
     handlers/
     files/
     templates/
     vars/
     defaults/
     meta/
   webservers/
     tasks/
     defaults/
     meta/
```

- `tasks` \-包含角色要执行的任务的主要列表。

- `handlers` \-包含处理程序，此角色甚至在此角色之外的任何地方都可以使用这些处理程序。

- `defaults`\-角色的默认变量

- `vars`\-角色的其他变量

- `files` \-包含可以通过此角色部署的文件。

- `templates` \-包含可以通过此角色部署的模板。

- `meta`\-为此角色定义一些元数据。请参阅下面的更多细节。

 

通常的做法是从`tasks/main.yml`文件中包含特定于平台的任务：

```bash
# roles/webservers/tasks/main.yml
- name: added in 2.4, previously you used 'include'
  import_tasks: redhat.yml
  when: ansible_facts['os_family']|lower == 'redhat'
- import_tasks: debian.yml
  when: ansible_facts['os_family']|lower == 'debian'
​
# roles/webservers/tasks/redhat.yml
- yum:
    name: "httpd"
    state: present
​
# roles/webservers/tasks/debian.yml
- apt:
    name: "apache2"
    state: present
```

### 2、使用角色

```bash
# site.yml
- hosts: webservers
  roles:
    - common
    - webservers
```

定义多个：

```bash
- name: 0
  gather_facts: false
  hosts: all 
  roles:
    - common
​
- name: 1
  gather_facts: false
  hosts: all 
  roles:
    - webservers
```

### 3、角色控制

```bash
- name: 0.系统初始化
  gather_facts: false
  hosts: all 
  roles:
    - common
  tags: common 
```