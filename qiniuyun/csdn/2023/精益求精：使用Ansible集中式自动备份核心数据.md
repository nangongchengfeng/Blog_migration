---
author: 南宫乘风
categories:
- Ansible
date: 2023-10-20 15:59:21
description: 、引言在当今数字化时代，数据是企业和组织的核心资产。为了确保数据的安全性和可恢复性，备份是至关重要的。然而，手动备份数据可能会繁琐且容易出错，特别是在面对大规模和分布式的数据存储情况下。幸运的是，作为。。。。。。。
image: ../../title_pic/31.jpg
slug: '202310201559'
tags:
- ansible
title: 精益求精：使用Ansible集中式自动备份核心数据
---

<!--more-->

## 1、引言
在当今数字化时代，数据是企业和组织的核心资产。为了确保数据的安全性和可恢复性，备份是至关重
要的。然而，手动备份数据可能会繁琐且容易出错，特别是在面对大规模和分布式的数据存储情况下。幸运的是，Ansible作为一种自动化工具，能够帮助我们轻松实现核心数据的集中式自动备份。本文将深入探讨如何使用Ansible来自动备份核心数据，确保数据安全无忧。

## 2、背景
公司有一些核心数据需要备份，比如，gitlab，wiki，MySQL，MongoDB等等数据库。

为了防止数据丢失或损坏，我们需要定期备份GitLab数据。备份的内容通常包括Git存储库、配置文件、数据库等

**之前方案：**

> 在每台相关的机器上备份，任务分散，数据不容易管理，存储

**现在方案：**

> 采用一台机器，设置定时任务，把备份数据归档到同一地方存储，统一管理

![在这里插入图片描述](../../image/51cc1cab1ec347d096c9dac34894d395.png)
使用Ansible自动备份GitLab具有以下优点：

>  - 提高效率：使用Ansible可以自动备份，无需手动执行备份操作。
>   
>  - 提高可靠性：通过Ansible自动化备份可以减少人为错误，提高备份的可靠性。
>    
>   - 充分利用资源：Ansible可以在多个主机上并行执行任务，充分利用资源提高效率。

## 3、方案实现
1. 编写Ansible Playbook：在Playbook中定义需要备份的文件和路径，以及备份的文件存储位置。

2. 执行Ansible Playbook：通过执行Playbook来自动备份GitLab。

3. 验证备份：检查备份文件是否已正确存储，并确保文件可用于恢复。
### 1、基础环境
```bash
backupGitlab.yml  group_vars  hosts
[root@ansible-yunwei backupData]# tree .
.
├── backupGitlab.yml
├── group_vars
│?? └── all
└── hosts

```
![在这里插入图片描述](../../image/ffe77a74854f4a5db522f20fbe705e61.png)
创建hosts主机
```bash
[gitlab]
192.168.xx.xx ansible_ssh_user=root ansible_ssh_pass="xxxx.xx"

[confluence]
192.168.xx.xx ansible_ssh_user=root ansible_ssh_pass="xxxx.xx"

[uatmysql]
192.168.xx.xx ansible_ssh_user=root ansible_ssh_pass="xxx.xx"

[uatmongo8449]
192.168.xx.xx ansible_ssh_user=root ansible_ssh_pass="xxxx.xx"

[uatmongo9942]
192.168.xxx.xx ansible_ssh_user=root ansible_ssh_pass="xxxxx.xx"


```
定义变量环境
```bash
# gitlab备份存放目录
gitlabBackupDir: /data/backup/gitlab

# confluence备份存放目录
confluenceBackupDir: /data/backup/confluence

# uat环境mysql备份存放目录
uatMysqlBackupDir: /data/backup/uatmysql

# uat环境mongo(192.168.84.xx)备份存放目录
uatMongo8449BackupDir: /data/backup/uatmongo8449

# uat环境mongo(192.168.99.xx)备份存放目录
uatMongo9942BackupDir: /data/backup/uatmongo9942

# 备份结果记录文件
statusFile: /data/backup/backupStatus

```
### 2、编写Ansible Playbook
1. 获取当前日期，创建备份目录。
2. 生成GitLab备份文件并拉取至本地备份目录。
3. 拉取GitLab配置文件并存储在备份目录中。
4. 删除原始备份文件及旧备份文件。
5. 记录备份完成状态

```bash
[root@ansible-yunwei backupData]# cat backupGitlab.yml 
- name: 备份gitlab
  hosts: gitlab
  remote_user: root
  tasks:
  - name: 获取当日日期
    local_action: shell date +%Y%m%d
    args:
      warn: no
    register: date
  
  - name: 本机创建备份目录
    local_action: file path={{gitlabBackupDir}}/{{date.stdout}} state=directory owner=root group=root mode=0700
  
  - name: 生成gitlab备份
    shell: gitlab-backup create STRATEGY=copy
    args:
      warn: no
  
  - name: 获取文件名
    find: paths=/var/opt/gitlab/backups/ recurse=no patterns='*.tar'
    register: backupFile
  
  - name: 拉取备份文件
    fetch: src={{item.path}} dest={{gitlabBackupDir}}/{{date.stdout}}/ flat=True
    with_items:
      - '{{backupFile.files}}'
  
  - name: 拉取配置文件
    fetch: src={{item}} dest={{gitlabBackupDir}}/{{date.stdout}}/ flat=True
    with_items:
      - /etc/gitlab/gitlab.rb
      - /etc/gitlab/gitlab-secrets.json
  
  - name: 删除原始文件
    file: path={{item.path}} state=absent
    with_items:
      - '{{backupFile.files}}'
  
  - name: 查找旧的备份
    local_action: find paths={{gitlabBackupDir}}/ recurse=no patterns='*' age=3d age_stamp=mtime file_type=directory
    register: backupDir
  
  - name: 删除旧的备份
    local_action: file path={{item.path}} state=absent
    with_items:
      - '{{backupDir.files}}'
  
  - name: 记录备份完成状态
    local_action: shell if [ ! "`ls -A {{gitlabBackupDir}}/{{date.stdout}}`" = "" ]; then echo '{{date.stdout}}:successful:gitlab' >> {{statusFile}} ; else echo '{{date.stdout}}:failed:gitlab' >> {{statusFile}} ; fi
    args:
      warn: no

```
### 3、执行ansible-playbook

```bash
/usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupGitlab.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log
```

### 4、设置定时任务
```bash
1  0 * * * /usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupGitlab.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log
```
### 5、执行结果
![在这里插入图片描述](../../image/a492bb8bd13d44f4bb8e45bc7ed82d73.png)

## 4、备份其余类型
**backupConfluence.yml**
```bash
- name: 备份confluence
  hosts: confluence
  remote_user: root
  tasks:
  - name: 获取当日日期
    local_action: shell date +%Y%m%d
    args:
      warn: no
    register: date

  - name: 获取用于模式匹配的当日日期
    local_action: shell date +%Y_%m_%d
    args:
      warn: no
    register: datePattern
  
  - name: 本机创建备份目录
    local_action: file path={{confluenceBackupDir}}/{{date.stdout}} state=directory owner=root group=root mode=0700
  
  - name: 获取文件名
    find: paths=/var/atlassian/application-data/confluence/backups/ recurse=no patterns='backup-{{datePattern.stdout}}.zip'
    register: backupFile
  
  - name: 拉取备份文件
    fetch: src={{item.path}} dest={{confluenceBackupDir}}/{{date.stdout}}/ flat=True
    with_items:
      - '{{backupFile.files}}'
  
  - name: 查找旧的备份
    local_action: find paths={{confluenceBackupDir}}/ recurse=no patterns='*' age=3d age_stamp=mtime file_type=directory
    register: backupDir
  
  - name: 删除旧的备份
    local_action: file path={{item.path}} state=absent
    with_items:
      - '{{backupDir.files}}'
  
  - name: 记录备份完成状态
    local_action: shell if [ ! "`ls -A {{confluenceBackupDir}}/{{date.stdout}}`" = "" ]; then echo '{{date.stdout}}:successful:confluence' >> {{statusFile}} ; else echo '{{date.stdout}}:failed:confluence' >> {{statusFile}} ; fi
    args:
      warn: no

```


** backupUatMongo8449.yml**
```bash
- name: 备份uat环境mongo数据库(192.168.xx.xx)
  hosts: uatmongo8449
  remote_user: root
  tasks:
  - name: 获取当日日期
    local_action: shell date +%Y%m%d
    args:
      warn: no
    register: date
  
  - name: 本机创建备份目录
    local_action: file path={{uatMongo8449BackupDir}}/{{date.stdout}} state=directory owner=root group=root mode=0700
  
  - name: 生成备份
    shell: mongodump --host '192.168.xx.xx' --port '27017' -u 'root' -p 'xxx' --authenticationDatabase 'admin' --gzip -o /tmp/uatmongo8449-{{date.stdout}}
    args:
      warn: no

  - name: 进行打包
    archive: path=/tmp/uatmongo8449-{{date.stdout}} dest=/tmp/uatmongo8449-{{date.stdout}}.tar format=tar remove=True
  
  - name: 拉取备份文件
    fetch: src=/tmp/uatmongo8449-{{date.stdout}}.tar dest={{uatMongo8449BackupDir}}/{{date.stdout}}/ flat=True
  
  - name: 删除原始文件
    file: path={{item}} state=absent
    with_items:
      - '/tmp/uatmongo8449-{{date.stdout}}.tar'
      - '/tmp/uatmongo8449-{{date.stdout}}'
  
  - name: 查找旧的备份
    local_action: find paths={{uatMongo8449BackupDir}}/ recurse=no patterns='*' age=3d age_stamp=mtime file_type=directory
    register: backupDir
  
  - name: 删除旧的备份
    local_action: file path={{item.path}} state=absent
    with_items:
      - '{{backupDir.files}}'
  
  - name: 记录备份完成状态
    local_action: shell if [ ! "`ls -A {{uatMongo8449BackupDir}}/{{date.stdout}}`" = "" ]; then echo '{{date.stdout}}:successful:uatMongo8449' >> {{statusFile}} ; else echo '{{date.stdout}}:failed:uatMongo8449' >> {{statusFile}} ; fi
    args:
      warn: no

```


** backupUatMysql.yml**
```bash
- name: 备份uat环境mysql数据库
  hosts: uatmysql
  remote_user: root
  tasks:
  - name: 获取当日日期
    local_action: shell date +%Y%m%d
    args:
      warn: no
    register: date
  
  - name: 本机创建备份目录
    local_action: file path={{uatMysqlBackupDir}}/{{date.stdout}} state=directory owner=root group=root mode=0700
  
  - name: 生成备份
    shell: mysqldump -h'192.168.1xx.xxx' -u'root' -p'xxxx' --single-transaction --flush-logs --master-data=2 --events --routines --triggers --hex-blob --all-databases | gzip > /tmp/uatmysql-{{date.stdout}}.sql.gz
    args:
      warn: no

  - name: 拉取备份文件
    fetch: src=/tmp/uatmysql-{{date.stdout}}.sql.gz dest={{uatMysqlBackupDir}}/{{date.stdout}}/ flat=True
  
  - name: 删除原始文件
    file: path=/tmp/uatmysql-{{date.stdout}}.sql.gz state=absent
  
  - name: 查找旧的备份
    local_action: find paths={{uatMysqlBackupDir}}/ recurse=no patterns='*' age=3d age_stamp=mtime file_type=directory
    register: backupDir
  
  - name: 删除旧的备份
    local_action: file path={{item.path}} state=absent
    with_items:
      - '{{backupDir.files}}'
  
  - name: 记录备份完成状态
    local_action: shell if [ ! "`ls -A {{uatMysqlBackupDir}}/{{date.stdout}}`" = "" ]; then echo '{{date.stdout}}:successful:uatMysql' >> {{statusFile}} ; else echo '{{date.stdout}}:failed:uatMysql' >> {{statusFile}} ; fi
    args:
      warn: no

```


```bash
[root@kvm-master backupData]# crontab -l
# 备份数据：Gitlab、Confluence、uat环境mysql(192.168.1xx.xx)、uat环境mongo(192.168.xx.xx) (每天执行一次)
1  0 * * * /usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupGitlab.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log
10 0 * * * /usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupConfluence.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log
20 0 * * * /usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupUatMysql.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log
30 0 * * * /usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupUatMongo8449.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log
40 0 * * * /usr/local/python36/bin/ansible-playbook /opt/ansible/backupData/backupUatMongo9942.yml -i /opt/ansible/backupData/hosts 2>&1 >> /data/backup/backup.log


```
## 5、总结
通过上述自动化备份策略，我们可以有效地保护Gitlab数据的安全性和完整性。在实际应用过程中，这种备份策略还可以根据需要进行定制和扩展，以满足不同场景下的需求。希望这篇博客对大家有所帮助！
