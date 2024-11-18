---
author: 南宫乘风
categories:
- 项目实战
date: 2024-04-08 16:16:38
description: 和快照概述的重要性：支持的灵活的文档模型，使其成为处理大量分散数据的理想选择，特别是在需要快速迭代和频繁更改数据结构的应用中。逻辑卷管理快照技术基本概念：允许在不停止数据库服务的情况下，创建数据在某一。。。。。。。
image: ../../title_pic/66.jpg
slug: '202404081616'
tags:
- mongodb
- 数据库
title: MongoDB快照（LVM）业务场景应用实战
---

<!--more-->

## MongoDB和LVM快照概述

**MongoDB的重要性**：MongoDB支持的灵活的文档模型，使其成为处理大量分散数据的理想选择，特别是在需要快速迭代和频繁更改数据结构的应用中。

**LVM（逻辑卷管理）快照技术基本概念**：LVM允许在不停止数据库服务的情况下，创建数据在某一时间点的快照。这意味着可以在不影响数据库性能和用户体验的情况下进行备份。

## 应用方面

1、备份（恢复）的重要性：

备份MongoDB数据对于确保数据安全和业务连续性至关重要。无论是因为硬件故障、软件故障、还是人为错误，数据丢失的后果都可能是灾难性的。定期备份可以最小化这些风险，确保在出现问题时可以快速恢复。

2、测试和开发环境的创建

在测试和开发过程中，需要创建一个与生产环境相同的数据库副本。通过使用快照，可以在测试和开发环境中快速创建一个具有相同数据和结构的数据库副本，以便进行有效的测试和开发工作。

3、数据分析和报告生成

某些情况下，需要对数据库进行离线分析和报告生成。通过使用快照，在不影响生产环境的情况下，可以在备份中创建一个副本，用于数据分析和报告生成，而不会对生产环境的性能产生负面影响。

## LVM快照的优势

使用LVM快照作为MongoDB备份策略的优点包括：

* **快速备份**：能够迅速捕捉到数据的瞬时状态，减少备份时间。
* **最小化停机时间**：备份过程中不需要停止服务，这对于需要24/7运行的业务至关重要。
* **有效地恢复数据**：可以精确到备份时的状态恢复数据，提高恢复效率。

## 环境准备

进行MongoDB备份前的环境准备包括：

* 确保已安装LVM并正确配置存储。

```yml
sudo yum install lvm2

首先，识别可用的磁盘或分区（例如，/dev/sdb）并创建物理卷：
sudo pvcreate /dev/sdb
展示效果：该命令应返回“Physical volume "/dev/sdb" successfully created”的信息。

接着，创建一个卷组，加入刚创建的物理卷：

sudo vgcreate vg0 /dev/sdb
展示效果：返回“Volume group "vg0" successfully created”表明卷组创建成功。

步骤三：创建逻辑卷

最后，在卷组内创建逻辑卷用于MongoDB数据存储：

sudo lvcreate -L 10G -n mongo_data vg0
展示效果：应返回“Logical volume "mongo_data" created”的消息。
```

* MongoDB数据库运行在支持LVM的存储卷上。

```yml
配置MongoDB以使用逻辑卷

修改MongoDB的配置文件（通常为/etc/mongod.conf），指定数据存储路径到刚创建的逻辑卷上的某个目录：

storage:
  dbPath: "/mnt/mongo_data"

然后，将MongoDB数据目录移动到新的位置，并修改目录权限：

sudo mkdir /mnt/mongo_data
sudo mount /dev/vg0/mongo_data /mnt/mongo_data
sudo rsync -av /var/lib/mongo/ /mnt/mongo_data
sudo chown -R mongodb:mongodb /mnt/mongo_data
```

* 验证系统的性能和存储空间，确保快照操作不会导致性能瓶颈或空间耗尽。

```yml
htop
htop将显示CPU和内存的实时使用情况，用户需要确保在创建快照期间，这些资源的使用不会达到饱和
```

### 步骤详解

1. 确认MongoDB数据库的存储卷

首先，使用`lvdisplay`命令来查找MongoDB数据存储在哪个逻辑卷上：

```
lvdisplay
```

这个命令会列出系统中所有的逻辑卷。你需要找到与MongoDB数据相关联的逻辑卷信息，比如卷名（Volume Name）、卷组名（VG Name）等。

2. 创建快照卷

**注意：在执行的时候需要关闭数据库，以防止有数据继续写入（**​`systemctl stop mongod`​ **）**


接着，根据确认的MongoDB数据卷，使用`lvcreate`命令创建一个新的快照卷。例如，如果MongoDB数据存储在名为`mongo_data`的逻辑卷上，位于卷组`vg0`中，可以执行：

```
sudo lvcreate --size 1G --snapshot --name mongo_backup /dev/vg0/mongo_data
```

这个命令创建了一个名为`mongo_backup`的快照卷，大小为1GB。

3. 挂载快照卷并备份

创建快照卷后，需要将其挂载到系统的一个目录上，以便访问和备份数据。首先，创建一个挂载点，然后挂载快照卷：

```
sudo mkdir /mnt/mongo_backup
sudo mount /dev/vg0/mongo_backup /mnt/mongo_backup
```

挂载完成后，使用标准备份工具（如`tar`或`rsync`）备份数据。例如，使用`tar`创建一个压缩的备份文件：

```
sudo tar czf /path/to/backup/mongo_backup.tar.gz /mnt/mongo_backup
```

4. 卸载快照卷并删除

备份完成后，不要忘记卸载快照卷并删除它，以释放空间：

```
sudo umount /mnt/mongo_backup
sudo lvremove /dev/vg0/mongo_backup
```

在删除快照卷时，系统会询问你是否确定删除，输入`y`确认。


### 快照恢复流程


1. 准备恢复环境

在恢复数据之前，确保目标位置有足够的空间接收从快照中恢复的数据。可以使用`df -h`命令检查磁盘空间，并根据需要清理或添加存储空间。

2. 使用快照数据恢复

在进行数据恢复之前，确保MongoDB服务已停止，以避免数据恢复过程中的冲突。使用以下命令停止MongoDB服务：

```
sudo systemctl stop mongod
```

然后，将快照数据恢复到MongoDB的数据目录中。首先，确认快照挂载点和MongoDB的数据目录路径。假设快照挂载在`/mnt/mongo_backup`，MongoDB数据目录为`/var/lib/mongo`，可以使用`rsync`进行数据恢复：

```
sudo rsync -av /mnt/mongo_backup/ /var/lib/mongo/
```

确保使用结束斜杠`/`来指示同步目录内容而非目录本身。

3. 启动MongoDB服务

数据恢复完成后，重启MongoDB服务，并验证数据的一致性和完整性：

```
sudo systemctl start mongod
```

重启服务后，检查MongoDB的日志文件，确保没有启动错误，并进行必要的数据一致性检查。使用MongoDB客户端或应用程序验证数据完整性和访问性。

MongoDB，作为一个高性能、开源、无模式的文档数据库，因其高可伸缩性和灵活性而受到广泛欢迎。然而，正如任何技术专家所知，无论数据库的强大与否，数据备份和恢复计划的重要性都不可忽视。本文将探讨如何利用逻辑卷管理（LVM）快照技术来备份MongoDB数据库，确保数据的安全和业务的连续性。

## 业务实战

（数据分析和报告生成：某些情况下，需要对数据库进行离线分析和报告生成。通过使用快照，在不影响生产环境的情况下，可以在备份中创建一个副本，用于数据分析和报告生成，而不会对生产环境的性能产生负面影响）。

财务报表的准确性对于公司的及时决策至关重要。当前，报表直接在业务数据库上运行，不仅耗时长，而且在月初出报时常常失败，这对财务部门和公司决策产生了影响。随着公司业务规模的持续增长，现有的报表运行方式已不再适用。

我们的业务数据每日凌晨从多个业务数据库同步到数据仓库中。数据同步的耗时长意味着，同步完成时的数据已不再是某一时刻的精准快照（因为业务数据库在不断更新）。

**需求**：我们需要一个能将数据从MongoDB业务数据库精准同步到阿里云MaxCompute数据仓库的简单且可靠方案。简单性至关重要，因为它能提高系统的可靠性。理想的解决方案中应避免使用复杂的自编脚本来处理主从同步的细节，例如确定binlog的位置或时间点等技术栈，而是应尽可能使用封装良好的技术解决方案。数据的精确性非常关键，任何错误都可能导致不可逆的后果。

**思路**：利用操作系统提供的LVM快照技术，可以在某一时刻将基于MongoDB的业务数据库数据精准同步到另一个MongoDB数据库中。这样，MaxCompute就可以从后者获取数据，进行同步任务。

**实践**：以核心系统的MongoDB数据库为例，我们将展示如何将数据精准同步到数据仓库中，从而为财务报表的生成提供可靠的数据基础。
![在这里插入图片描述](../../image/2d1526f752b44783a08178c6e1e15260.png)
### 实践步骤

#### 1. 准备工作

首先，确保已经在服务器上安装并配置了MongoDB，并且有足够的磁盘空间用于创建快照。

#### 2. 自动化脚本

为了实现这一过程的自动化，我们编写了一个MongoDB脚本和一个Shell脚本。MongoDB脚本用于锁定数据库，触发快照的创建，然后解锁数据库。Shell脚本负责实际创建LVM快照。

##### MongoDB 脚本 (`snapshot.js`)

这个JavaScript脚本是为了在MongoDB数据库中创建一个数据快照，同时确保数据一致性，而设计的。这是通过在不完全停止数据库服务的情况下“锁定”数据库来实现的。

```yml
conn = new Mongo();
db = conn.getDB("admin");
db.auth('root','xxx');
db = db.getSiblingDB('数据库名称');

session = db.getMongo().startSession();
session.startTransaction();
db.fsyncLock();
run('/opt/mongodb_snap.sh');
db.fsyncUnlock();
session.commitTransaction();
session.endSession();
conn.close();
```

1. **建立连接和认证**：

    * `conn = new Mongo();` 创建一个新的MongoDB连接。
    * `db = conn.getDB("admin");` 选择`admin`数据库进行操作。
    * `db.auth('root','xxx');` 使用root账号和对应密码进行认证。
    * `db = db.getSiblingDB('fubaodai');` 切换到目标数据库`fubaodai`，这是实际要快照的数据库。
2. **事务和锁定**：

    * `session = db.getMongo().startSession();` 启动一个新的会话。
    * `session.startTransaction();` 在该会话中开始一个新的事务。
    * `db.fsyncLock();` 锁定数据库，以准备进行快照。这个操作会阻止写操作，但读操作仍然可以继续，从而保证了数据的一致性而不完全停止服务。
3. **执行快照脚本**：

    * `run('/opt/mongodb_snap.sh');` 执行Shell脚本`/opt/mongodb_snap.sh`来创建一个LVM快照。注意，`run`函数在这个上下文中并不是MongoDB Shell的内置函数，这里假设它是为了说明目的而使用的。在实际MongoDB Shell脚本中，你可能需要通过其他方式触发快照脚本，比如通过MongoDB的系统命令执行或外部程序调度。
4. **解锁和结束**：

    * `db.fsyncUnlock();` 解锁数据库，恢复正常的读写操作。
    * `session.commitTransaction();` 提交事务，虽然这里的事务主要用于fsync锁定和解锁操作。
    * `session.endSession();` 结束会话。
    * `conn.close();` 关闭与MongoDB的连接。

通过上述步骤，这个脚本使得数据库能够在确保数据一致性的同时，进行LVM快照创建，而不需要停机或重启服务。这对于需要24/7运行的生产环境尤为重要。


##### Shell 脚本 (`mongodb_snap.sh`)

```yml
#!/bin/bash
name=mongodb-$(date +%Y%m%d%H%M%S)
/usr/sbin/lvcreate -s -L 100G -n $name /dev/mapper/data-mongodb
```

这些脚本通过Cron任务在每天零点自动执行，以确保数据同步的准确性和及时性。

要通过`cron`在凌晨自动执行`mongo --nodb mongodb_snap.js`命令，你需要按照以下步骤操作：

在终端中运行`crontab -e`命令。这将打开一个文本编辑器，允许你编辑当前用户的`cron`作业。

```yml
0 1 * * * /usr/bin/mongo --nodb /path/to/mongodb_snap.js
```

在每天的1:00 AM，执行`/usr/bin/mongo --nodb /path/to/mongodb_snap.js`命令。请确保根据你的环境替换`/usr/bin/mongo`和`/path/to/mongodb_snap.js`为`mongo`命令和`mongodb_snap.js`脚本的实际路径。

#### 3. 数据同步

完成LVM快照后，我们可以将快照数据同步到另一个MongoDB数据库实例，该实例将作为数据仓库同步任务的数据源。这保证了数据仓库中的数据既准确又是最新的。

## 总结

MongoDB数据库的备份和恢复是确保数据安全和业务连续性的重要环节。通过使用LVM快照作为备份策略，我们能够快速备份MongoDB数据，最小化停机时间，并以高效的方式恢复数据。这种备份方式的优点在于它提供了高级别的数据保护和可靠性，使得企业能够在数据风险和灾难发生时保持高度的安全性和稳定性。
