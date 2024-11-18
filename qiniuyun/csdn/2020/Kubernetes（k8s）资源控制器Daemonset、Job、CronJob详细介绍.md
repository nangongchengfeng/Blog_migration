---
author: 南宫乘风
categories:
- Kubernetes
date: 2020-02-05 21:34:32
description: 什么是确保全部或者一些上运行一个的副本。当有加入集群时，也会为他们新增一个。当有从集群移除时，这些也会被回收。删除将会删除它创建的所有使用的一些典型用法：运行集群存储，例如在每个上运行、在每个上运行日。。。。。。。
image: ../../title_pic/74.jpg
slug: '202002052134'
tags:
- Kubernetes
- k8s
- Daemonset
- Job
- CronJob
title: Kubernetes（k8s）资源控制器Daemonset、Job、CronJob详细介绍
---

<!--more-->

# 什么是 DaemonSet 

DaemonSet 确保全部（或者一些）Node 上运行一个 Pod 的副本。当有 Node 加入集群时，也会为他们新增一 个 Pod 。当有 Node 从集群移除时，这些 Pod 也会被回收。删除 DaemonSet 将会删除它创建的所有 Pod

**使用 DaemonSet 的一些典型用法：**

- 运行集群存储 daemon，例如在每个 Node 上运行 glusterd 、 ceph
- 在每个 Node 上运行日志收集 daemon，例如 fluentd 、 logstash
- 在每个 Node 上运行监控 daemon，例如 Prometheus Node Exporter、 collectd 、Datadog 代理、 New Relic 代理，或 Ganglia gmond

 

```bash
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: deamonset-example
  labels:
    app: daemonset
spec:
  selector:
    matchLabels:
      name: deamonset-example
  template:
    metadata:
      labels:
        name: deamonset-example
    spec:
      containers:
      - name: daemonset-example
        image: wangyanglinux/myapp:v1
```

![](../../image/20200205205134703.png)

![](../../image/20200205205314918.png)

# Job 

**Job 负责批处理任务，即仅执行一次的任务，它保证批处理任务的一个或多个 Pod 成功结束 **

**特殊说明 **

- spec.template格式同Pod
- RestartPolicy仅支持Never或OnFailure
- 单个Pod时，默认Pod成功运行后Job即结束
- .spec.completions 标志Job结束需要成功运行的Pod个数，默认为1
- .spec.parallelism 标志并行运行的Pod的个数，默认为1
- spec.activeDeadlineSeconds 标志失败Pod的重试大时间，超过这个时间不会继续重试  
 

**Example**

```bash
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    metadata:
      name: pi
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

![](../../image/20200205210847466.png)

![](../../image/20200205211406490.png)

# CronJob Spec 

- spec.template格式同Pod
- RestartPolicy仅支持Never或OnFailure
- 单个Pod时，默认Pod成功运行后Job即结束
- .spec.completions 标志Job结束需要成功运行的Pod个数，默认为1 .
- spec.parallelism 标志并行运行的Pod的个数，默认为1
- spec.activeDeadlineSeconds 标志失败Pod的重试大时间，超过这个时间不会继续重试  
 

# CronJob 

**Cron Job 管理基于时间的 Job，即：**

- 在给定时间点只运行一次
- 周期性地在给定时间点运行  
 

使用条件：当前使用的 Kubernetes 集群，版本 >= 1.8（对 CronJob）  
典型的用法如下所示：

- 在给定的时间点调度 Job 运行
- 创建周期性运行的 Job，例如：数据库备份、发送邮件  
 

# CronJob Spec 

- .spec.schedule ：调度，必需字段，指定任务运行周期，格式同 Cron
- .spec.jobTemplate ：Job 模板，必需字段，指定需要运行的任务，格式同 Job
- .spec.startingDeadlineSeconds  ：启动 Job 的期限（秒级别），该字段是可选的。如果因为任何原因而错过了被调度的时间，那么错过执行时间的 Job 将被认为是失败的。如果没有指定，则没有期限
- .spec.concurrencyPolicy ：并发策略，该字段也是可选的。它指定了如何处理被 Cron Job 创建的 Job 的并发执行。只允许指定下面策略中的一种：

1.  Allow （默认）：允许并发运行 Job
2.  Forbid  ：禁止并发运行，如果前一个还没有完成，则直接跳过下一个
3.  Replace ：取消当前正在运行的 Job，用一个新的来替换

注意，当前策略只能应用于同一个 Cron Job 创建的 Job。如果存在多个 Cron Job，它们创建的 Job 之间总  
是允许并发运行。

- .spec.suspend  ：挂起，该字段也是可选的。如果设置为  true   ，后续所有执行都会被挂起。它对已经开始执行的 Job 不起作用。默认值为  false   。
- .spec.successfulJobsHistoryLimit  和  .spec.failedJobsHistoryLimit   ：历史限制，是可选的字段。它们指定了可以保留多少完成和失败的 Job。默认情况下，它们分别设置为  3  和   1 。设置限制的值为   0  ，相关类型的 Job 完成后将不会被保留。

### Example

```bash
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            args:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

###  ![](../../image/20200205212840212.png)

```bash
$ kubectl get cronjob
NAME      SCHEDULE      SUSPEND   ACTIVE    LAST-SCHEDULE
hello     */1 * * * *   False     0         <none>
$ kubectl get jobs
NAME               DESIRED   SUCCESSFUL   AGE
hello-1202039034   1         1            49s
$ pods=$(kubectl get pods --selector=job-name=hello-1202039034 --output=jsonpath=
{.items..metadata.name})
$ kubectl logs $pods
Mon Aug 29 21:34:09 UTC 2016
Hello from the Kubernetes cluster
# 注意，删除 cronjob 的时候不会自动删除 job，这些 job 可以用 kubectl delete job 来删除
$ kubectl delete cronjob hello
cronjob "hello" deleted
```

**CrondJob 本身的一些限制   
创建 Job 操作应该是 幂等的**