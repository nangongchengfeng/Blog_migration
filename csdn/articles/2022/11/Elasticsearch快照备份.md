+++
author = "南宫乘风"
title = "Elasticsearch快照备份"
date = "2022-11-13 09:22:40"
tags=['elasticsearch', '搜索引擎', '大数据']
categories=['项目实战']
image = "post/4kdongman/18.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/127828348](https://blog.csdn.net/heian_99/article/details/127828348)

**目录**

[1、Repositories](#1%E3%80%81Repositories)

[1、配置路径](#1%E3%80%81%E9%85%8D%E7%BD%AE%E8%B7%AF%E5%BE%84)

[2、注册快照存储库](#2%E3%80%81%E6%B3%A8%E5%86%8C%E5%BF%AB%E7%85%A7%E5%AD%98%E5%82%A8%E5%BA%93)

[2、查看注册的库](#2%E3%80%81%E6%9F%A5%E7%9C%8B%E6%B3%A8%E5%86%8C%E7%9A%84%E5%BA%93)

[3、创建快照](#3%E3%80%81%E5%88%9B%E5%BB%BA%E5%BF%AB%E7%85%A7)

[1、为全部索引创建快照](#1%E3%80%81%E4%B8%BA%E5%85%A8%E9%83%A8%E7%B4%A2%E5%BC%95%E5%88%9B%E5%BB%BA%E5%BF%AB%E7%85%A7)

[2、为指定索引创建快照](#2%E3%80%81%E4%B8%BA%E6%8C%87%E5%AE%9A%E7%B4%A2%E5%BC%95%E5%88%9B%E5%BB%BA%E5%BF%AB%E7%85%A7)

[4、查看备份完成的列表](#4%E3%80%81%E6%9F%A5%E7%9C%8B%E5%A4%87%E4%BB%BD%E5%AE%8C%E6%88%90%E7%9A%84%E5%88%97%E8%A1%A8)

[5、删除快照](#5%E3%80%81%E5%88%A0%E9%99%A4%E5%BF%AB%E7%85%A7)

[6、从快照恢复](#6%E3%80%81%E4%BB%8E%E5%BF%AB%E7%85%A7%E6%81%A2%E5%A4%8D)

[1、恢复指定索引](#1%E3%80%81%E6%81%A2%E5%A4%8D%E6%8C%87%E5%AE%9A%E7%B4%A2%E5%BC%95)

[2、恢复所有索引（除.开头的系统索引）](#2%E3%80%81%E6%81%A2%E5%A4%8D%E6%89%80%E6%9C%89%E7%B4%A2%E5%BC%95%EF%BC%88%E9%99%A4.%E5%BC%80%E5%A4%B4%E7%9A%84%E7%B3%BB%E7%BB%9F%E7%B4%A2%E5%BC%95%EF%BC%89)

[3、恢复所有索引（包含.开头的系统索引）](#3%E3%80%81%E6%81%A2%E5%A4%8D%E6%89%80%E6%9C%89%E7%B4%A2%E5%BC%95%EF%BC%88%E5%8C%85%E5%90%AB.%E5%BC%80%E5%A4%B4%E7%9A%84%E7%B3%BB%E7%BB%9F%E7%B4%A2%E5%BC%95%EF%BC%89)

[4、将快照恢复到Indexing Service实例中。](#4%E3%80%81%E5%B0%86%E5%BF%AB%E7%85%A7%E6%81%A2%E5%A4%8D%E5%88%B0Indexing%20Service%E5%AE%9E%E4%BE%8B%E4%B8%AD%E3%80%82)

[7、查看快照恢复信息](#7%E3%80%81%E6%9F%A5%E7%9C%8B%E5%BF%AB%E7%85%A7%E6%81%A2%E5%A4%8D%E4%BF%A1%E6%81%AF)

[1、查看快照中指定索引的恢复状态](#1%E3%80%81%E6%9F%A5%E7%9C%8B%E5%BF%AB%E7%85%A7%E4%B8%AD%E6%8C%87%E5%AE%9A%E7%B4%A2%E5%BC%95%E7%9A%84%E6%81%A2%E5%A4%8D%E7%8A%B6%E6%80%81)

[2、查看集群中的所有索引的恢复信息](#2%E3%80%81%E6%9F%A5%E7%9C%8B%E9%9B%86%E7%BE%A4%E4%B8%AD%E7%9A%84%E6%89%80%E6%9C%89%E7%B4%A2%E5%BC%95%E7%9A%84%E6%81%A2%E5%A4%8D%E4%BF%A1%E6%81%AF)

[8、删除正在进行快照恢复的索引](#8%E3%80%81%E5%88%A0%E9%99%A4%E6%AD%A3%E5%9C%A8%E8%BF%9B%E8%A1%8C%E5%BF%AB%E7%85%A7%E6%81%A2%E5%A4%8D%E7%9A%84%E7%B4%A2%E5%BC%95)

[2、备份脚本](#2%E3%80%81%E5%A4%87%E4%BB%BD%E8%84%9A%E6%9C%AC)

[1、Elasticsearch索引备份](#1%E3%80%81Elasticsearch%E7%B4%A2%E5%BC%95%E5%A4%87%E4%BB%BD)

[2、Elasticsearch索引清理](#2%E3%80%81Elasticsearch%E7%B4%A2%E5%BC%95%E6%B8%85%E7%90%86)



快照是增量的，可以包含在多个ES版本中创建的索引。如果在一个快照中的任何索引时在不兼容的ES版本中创建的，你将不能恢复该快照。

在升级前备份数据的时候，如果快照中的索引是在与你升级版本不兼容的ES版本中创建的，那么这些快照将不能被恢复。

如果你的情况是需要恢复一个与你当前运行的集群版本不兼容的索引快照，你可以先恢复到最新的兼容版本中，然后在当前版本中使用 reindex-from-remote 重建索引。远程Reindexing只能在源索引source为enabled的情况下进行。获取并重建数据索引的时间可能比简单恢复快照要长的多。如果你的数据量较大，建议先用一部分数据测试远程reindex，以便了解需要花费的时间

# 1、Repositories

必须先注册一个快照仓库，然后才能进行快照和恢复操作。建议为每个主版本创建一个新快照仓库。有效的仓库设置取决于仓库类型。

如果多个集群注册同一个快照仓库，只有一个集群可以对仓库进行写访问，其他所有集群应该设置该仓库为 readonly 模式。

跨主版本时快照格式可能会改变，所以不同版本的集群写同一个快照仓库，某个版本写的快照可能对其他版本不可见，仓库快照也存在问题。ES不支持仓库对所有集群设置为readonly，其中一个集群和不同主版本的多个集群一起工作。

**关于备份可以分为备份数据，备份集群配置，备份安全配置**

**关于还原可以分为还原数据，还原安全配置**

## 1、配置路径

大致分为以下几步（如果您的集群启用了安全功能，则在备份数据时必须授权快照API调用）

修改elasticsearch.yml添加快照存储位置配置

```
cat elasticsearch.yml
node.name: node-1
discovery.seed_hosts: ["172.18.199.93"]
cluster.initial_master_nodes: node-1
network.host: 0.0.0.0
path.data: /data02/elasticsearch/data
path.logs: /data02/elasticsearch/logs
xpack.security.enabled: true
xpack.license.self_generated.type: basic
xpack.security.transport.ssl.enabled: true
​
xpack.sql.enabled: false
http.cors.enabled: true
http.cors.allow-credentials: true
http.cors.allow-origin: "/.*/"
http.cors.allow-headers: WWW-Authenticate,X-Requested-With,X-Auth-Token,Content-Type,Content-Length,Authorization
​
# 避免发生OOM，发生OOM对集群影响很大的,揉合 request 和 fielddata 断路器保证两者组合起来不会使用超过堆内存的 70%。
indices.breaker.total.limit: 80%
# 有了这个设置，最久未使用（LRU）的 fielddata 会被回收为新数据腾出空间   
indices.fielddata.cache.size: 10%
#
# # fielddata 断路器默认设置堆的  作为 fielddata 大小的上限。
indices.breaker.fielddata.limit: 60%
#
# #request 断路器估算需要完成其他请求部分的结构大小，例如创建一个聚合桶，默认限制是堆内存的 40%。
indices.breaker.request.limit: 40%
#
# #最久未使用（LRU）的 fielddata 会被回收为新数据腾出空间 必须要添加的配置
indices.breaker.total.use_real_memory: false
####副本数设置唯一
#索引调优
#
indices.memory.index_buffer_size: 20%
indices.memory.min_index_buffer_size: 96mb
​
# Search pool
thread_pool.search.size: 5
​
​
discovery.zen.fd.ping_timeout: 120s
discovery.zen.fd.ping_retries: 6
discovery.zen.fd.ping_interval: 30s
​
#仓库
path.repo: ["/data/es_snapshot"]
```

```
chown -R es:es  /data/es_snapshot
```

## 2、注册快照存储库

快照可以存储在本地或远程存储库中。远程存储库可以驻留在 Amazon S3、HDFS、Microsoft Azure、Google Cloud Storage 和存储库插件支持的其他平台上。

除了location 参数外，还可以通过`max_snapshot_bytes_per_sec`和`max_restore_bytes_per_sec` 来限制备份和恢复时的速度

**查看快照仓库。**

```
GET _snapshot
```

```
curl  -XPUT 'http://192.168.18.15:9200/_snapshot/backup（仓库名称）' -d '{
  "type": "fs",
  "settings": {
  "location": "/data/es_snapshot",
  "compress": true  #压缩
  }
  }'
```

或者在Kibana console中输入如下的命令进行注册也可以

```
PUT _snapshot/backup
    {
      "type": "fs",
      "settings": {
      "location": "/data/es_snapshot",
      "compress": true
      }

```

## 2、查看注册的库

GET _snapshot/

```
GET _snapshot/
```

![dae0fd647c7e49e2bfd6037f03b65059.png](https://img-blog.csdnimg.cn/dae0fd647c7e49e2bfd6037f03b65059.png)

## 3、创建快照

自建Elasticsearch中创建一个快照，用来备份您需要迁移的索引数据。创建快照时，默认会备份所有打开的索引。如果您不想备份系统索引，例如以**.kibana**、**.security**、**.monitoring**等开头的索引，可在创建快照时指定需要备份的索引

**注意**： 建议您不要备份系统索引，因为系统索引会占用较大空间。

### 1、为全部索引创建快照

```
PUT _snapshot/my_backup/snapshot_1
```

以上命令会为所有打开的索引创建名称为**snapshot_1**的快照，并保存到**my_backup**仓库中。该命令会立刻返回，并在后台执行备份任务。如果您希望任务执行完成后再返回，可通过添加**wait_for_completion**实现。该参数会阻塞调用直到备份完成，如果是大型快照，需要很长时间才能返回。

```
PUT _snapshot/my_backup/snapshot_1?wait_for_completion=true
```

**说明**
-  一个仓库可以包含多个快照，每个快照中可以包含所有、部分或单个索引的备份数据。 -  第一次创建快照时，系统会备份所有的数据，后续所有的快照仅备份已存快照和新快照之间的增量数据。随着快照的不断进行，备份也在增量的添加和删除。这意味着后续备份会相当快速，因为它们只传输很小的数据量。 
### 2、为指定索引创建快照

系统默认会备份所有打开的索引。如果您在使用Kibana，并且考虑到磁盘空间大小因素，不需要把所有诊断相关的`.kibana`索引都备份起来，那么可以在创建快照时，指定需要备份的索引。

```
PUT _snapshot/my_backup/snapshot_2
{
    "indices": "index_1,index_2"
}
```

## 4、查看备份完成的列表

```
查看所有快照信息
GET _snapshot/my_backup/_all

根据快照名查看指定快照的信息
GET _snapshot/my_backup/snapshot_3

使用_status API查看指定快照的信息
GET _snapshot/my_backup/snapshot_3/_status


```

![6c3091182b7c46988fb1eb3893f19fcd.png](https://img-blog.csdnimg.cn/6c3091182b7c46988fb1eb3893f19fcd.png)

 

## 5、删除快照

删除指定的快照。如果该快照正在进行，执行以下命令，系统会中断快照进程并删除仓库中创建到一半的快照。

```
DELETE _snapshot/my_backup/snapshot_3
```

**注意** 删除快照请使用DELETE API，而不能使用其他机制删除（例如手动删除可能会造成备份严重损坏）。因为快照是增量的，很多快照可能依赖于之前的备份数据。DELETE API能够过滤出还在被其他快照使用的数据，只删除不再被使用的备份数据。

## 6、从快照恢复

**注意**
-  建议不要恢复`.`开头的系统索引，此操作可能会导致Kibana访问失败。 -  如果集群中存在与待恢复索引同名的索引，需要提前删除或者关闭该同名索引后再恢复，否则恢复失败。 -  如果需要跨地域恢复集群快照，需要先将原地域OSS中的快照数据迁移到目标地域的OSS中，再恢复到目标地域的Elasticsearch集群中。OSS间迁移的具体操作，请参见[阿里云OSS之间迁移教程](https://help.aliyun.com/document_detail/95040.htm#concept-yr2-3cf-qfb)。 
### 1、恢复指定索引

如果您需要在不替换现有数据的前提下，恢复旧版本的数据来验证内容，或者进行其他处理，可恢复指定的索引，并重命名该索引。

```
POST /_snapshot/my_backup/snapshot_1/_restore
{
 "indices": "index_1", 
 "rename_pattern": "index_(.+)", 
 "rename_replacement": "restored_index_$1" 
}
```

|参数|说明
|------
|**indices**|只恢复**index_1**索引，忽略快照中的其他索引。
|**rename_pattern**|查找正在恢复的索引，该索引名称需要与提供的模板匹配。
|**rename_replacement**|重命名查找到的索引。

### 2、恢复所有索引（除`.`开头的系统索引）

```
POST _snapshot/my_backup/snapshot_1/_restore 
{"indices":"*,-.monitoring*,-.security*,-.kibana*","ignore_unavailable":"true"}
```

### 3、恢复所有索引（包含`.`开头的系统索引）

```
POST _snapshot/my_backup/snapshot_1/_restore
```
-  假设**snapshot_1**中包含5个索引，那么这5个索引都会被恢复到集群中。 -  _restore API会立刻返回，恢复进程会在后台进行。如果您希望调用阻塞直到恢复完成，可以添加**wait_for_completion**参数。 
```
POST _snapshot/my_backup/snapshot_1/_restore?wait_for_completion=true
```

### 4、将快照恢复到Indexing Service实例中。

例如将**my_backup**仓库中，**snapshot_1**快照中的**index_1**索引数据恢复到Indexing Service实例中，示例如下。

** 说明** 实际使用时，您需要将对应信息替换为您实际的信息。

```
POST /_snapshot/my_backup/snapshot_1/_restore
{
  "indices": "index_1",
  "ignore_index_settings": [
    "index.apack.cube.following_index"
  ]
}
```

## 7、查看快照恢复信息

您可以通过_recovery API来监控快照恢复的状态、进度等信息。

### 1、查看快照中指定索引的恢复状态

```
GET restored_index_3/_recovery
```

### 2、查看集群中的所有索引的恢复信息

**说明** 获取的恢复信息可能包含跟您的恢复进程无关的其他分片的恢复信息。

```
GET /_recovery/
```

```
{
   "restored_index_3" : {
     "shards" : [ {
       "id" : 0,
       "type" : "snapshot",
       "stage" : "index",
       "primary" : true,
       "start_time" : "2014-02-24T12:15:59.716",
       "stop_time" : 0,
       "total_time_in_millis" : 175576,
       "source" : {
         "repository" : "my_backup",
         "snapshot" : "snapshot_3",
         "index" : "restored_index_3"
       },
       "target" : {
         "id" : "ryqJ5lO5S4-lSFbGnt****",
         "hostname" : "my.fqdn",
         "ip" : "10.0.**.**",
         "name" : "my_es_node"
       },
       "index" : {
         "files" : {
           "total" : 73,
           "reused" : 0,
           "recovered" : 69,
           "percent" : "94.5%"
         },
         "bytes" : {
           "total" : 79063092,
           "reused" : 0,
           "recovered" : 68891939,
           "percent" : "87.1%"
         },
         "total_time_in_millis" : 0
       },
       "translog" : {
         "recovered" : 0,
         "total_time_in_millis" : 0
       },
       "start" : {
         "check_index_time" : 0,
         "total_time_in_millis" : 0
       }
     } ]
   }
}
```

 输出结果会展示所有恢复中的索引，并列出这些索引中的所有分片。同时每个分片中会展示启动和停止时间、持续时间、恢复百分比、传输字节数等统计值。部分参数说明如下。

|参数|说明
|------
|**type**|恢复的类型。**snapshot**表示这个分片是在从一个快照恢复。
|**source**|待恢复的快照和仓库。
|**percent**|恢复的进度。**94.5%**表示对应分片已经恢复了94.5%的数据。

## 8、删除正在进行快照恢复的索引

通过**DELETE**命令删除正在恢复的索引，取消恢复操作。

​

```
DELETE /restored_index_3
```

# 2、备份脚本



​

## 1、Elasticsearch索引备份

```
#Elasticsearch索引备份
1 3 * * * /bin/bash -x /opt/shell-code/es_backup.sh  &gt; /opt/shell-code/logs/es_backup.log
```

```
#!/bin/bash
#/**********************************************************
# * Author        : 南宫乘风
# * Email         : 1794748404@qq.com
# * Last modified : 2022-11-03 23:43
# * Filename      : 01_ping_check_isalive.sh
# * Description   :
# * *******************************************************/
#/bin/bash

###################################

#日志级别 debug-1, info-2, warn-3, error-4, always-5
LOG_LEVEL=3
user=$(whoami)
#日志文件
LOG_FILE=./Elasticsearch.log

#调试日志
function log_debug() {
  content="[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $0  $user msg : $@"
  [ $LOG_LEVEL -le 1 ] &amp;&amp; echo $content &gt;&gt;$LOG_FILE
}
#信息日志
function log_info() {
  content="[INFO] $(date '+%Y-%m-%d %H:%M:%S') $0  $user msg : $@"
  [ $LOG_LEVEL -le 2 ] &amp;&amp; echo $content &gt;&gt;$LOG_FILE
}
#警告日志
function log_warn() {
  content="[WARN] $(date '+%Y-%m-%d %H:%M:%S') $0  $user msg : $@"
  [ $LOG_LEVEL -le 3 ] &amp;&amp; echo $content &gt;&gt;$LOG_FILE
}
#错误日志
function log_err() {
  content="[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $0  $user msg : $@"
  [ $LOG_LEVEL -le 4 ] &amp;&amp; echo $content &gt;&gt;$LOG_FILE
}
#一直都会打印的日志
function log_always() {
  content="[ALWAYS] $(date '+%Y-%m-%d %H:%M:%S') $0  $user msg : $@"
  [ $LOG_LEVEL -le 5 ] &amp;&amp; echo $content &gt;&gt;$LOG_FILE
}

# 执行快照备份
#times="2022.09.08 2022.09.09 2022.09.10 2022.09.11 2022.09.12 2022.09.13 2022.09.14 2022.09.15 2022.09.16 2022.09.17 2022.09.18 2022.09.19 2022.09.20 2022.09.21 2022.09.22 2022.09.23 2022.09.24 2022.09.25 2022.09.26 2022.09.27 2022.09.28 2022.09.29 2022.09.30 2022.10.01 2022.10.02 2022.10.03 2022.10.04 2022.10.05 2022.10.06 2022.10.07 2022.10.08 2022.10.09 2022.10.10 2022.10.11 2022.10.12 2022.10.13 2022.10.14 2022.10.15 2022.10.16 2022.10.17 2022.10.18 2022.10.19 2022.10.20 2022.10.21 2022.10.22 2022.10.23 2022.10.24 2022.10.25 2022.10.26 2022.10.27 2022.10.28 2022.10.29 2022.10.30 2022.10.31 2022.11.01 2022.11.02 2022.11.03 2022.11.04 2022.11.05 2022.11.06 2022.11.07 2022.11.08 2022.11.09 "
time=$(date +"%Y.%m.%d" -d "-1day")
host='http://elasticsearch-log.prod.server.fjf:9200'
username='elastic'
password='4reQiUCLB7meNU8VoUsm'
#仓库名称
STORE_NAME="backup"
#curl的绝对路径
CURL_CMD="/usr/bin/curl"

#告警信息
webhook='https://oapi.dingtalk.com/robot/send?access_token=810921774dac36151d8939b6ea68c90df667f50e1313xxxxxxxxxxxx'
cluster='ES备份告警'
function SendMsgToDingding() {
  curl $webhook -H 'Content-Type: application/json' -d "
  {
    'msgtype': 'text',
    'text': {
      'content': '集群名称：$cluster\n告警信息： $1 已经备份完成 \n'
    },
    'at': {
      'isAtAll': true
    }
  }"
}

list_groups="labor-prod-${time},app-prod-${time},fk-prod-${time}"
curl -s -u elastic:4reQixxxxxVoUsm -sXPUT http://exxxxxxxxxxxxxxxxxxxerver.fjf:9200/_snapshot/backup/log_es_${time}?wait_for_completion=true -H 'Content-Type: application/json' -d'{ "indices": "'${list_groups}'" }'

if [[ $? -eq 0 ]]; then
  SendMsgToDingding $list_groups
  log_always " $list_groups  已经备份成功"
else
  log_err "$list_groups  备份失败，请查看"
fi
```

## 2、Elasticsearch索引清理

```
# Elasticsearch索引清理
1 3 * * * bash /opt/shell-code/es_index.sh 2&gt;&amp;1 &gt; /usr/local/script/es_index.log
```

```
#author        : 南宫乘风
# * Email         : 1794748404@qq.com
# * Last modified : 2022-11-03 23:43
# * Filename      : 01_ping_check_isalive.sh
# * Description   : 
# * *******************************************************/
#/bin/bash

###################################

#!/bin/bash

host='elasticxxxxxxxxxxxxxxxx.fjf'
username='elastic'
password='4reQiUxxxxxxxxxxxxxx'

########################################### 如下用于清理旧的索引数据 ##########################################
# 清除旧索引
function purgeOldIndexes() {
	for i in $INDEXES;
	do
  		for index in `curl -u $username:$password -s http://$host:9200/_cat/indices |grep -P "$i" |awk '{print $3}' |sort  -r | tail -n +${NUM}`
  		do
    			echo ${index}
    			curl -u $username:$password -s -XDELETE http://$host:9200/${index}
  		done
	done
}

# 不同索引的日志保留时长要求不同，
NUM=11
INDEXES="monitoring-es
syslog
zipkin-prod:dependency
zipkin-prod:span
"
purgeOldIndexes

sleep 10

NUM=31
INDEXES="logstash-fk-prod
logstash-_doc
logstash-prod
"
purgeOldIndexes





sleep 10

NUM=60
INDEXES="app-prod
fk-prod
"
purgeOldIndexes

sleep 10

NUM=91
INDEXES="labor-prod"
purgeOldIndexes

```

 文档：[通过OSS将自建Elasticsearch数据迁移至阿里云](https://help.aliyun.com/document_detail/170022.html#section-ftm-9c8-55t)

[自动备份与恢复](https://help.aliyun.com/document_detail/85017.html)

[手动备份与恢复](https://help.aliyun.com/document_detail/65675.html)

[备份你的集群](https://www.elastic.co/guide/cn/elasticsearch/guide/current/backing-up-your-cluster.html)

[Elasticsearch的Snapshot and Restore（快照备份与恢复）](https://developer.aliyun.com/article/790820)


-  [Snapshot And Restore](https://www.elastic.co/guide/en/elasticsearch/reference/5.5/modules-snapshots.html) -  [自动备份与恢复](https://help.aliyun.com/document_detail/85017.htm#task-2439001) 