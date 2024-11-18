---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2023-05-31 14:13:57
description: 原理在现代的容器化环境中，节点资源的管理是一个重要的任务。特别是对于内存资源的管理，它直接影响着容器应用的性能和可用性。在中，我们可以利用自动调度和控制的机制来实现对节点内存的有效管理。本文将介绍一种。。。。。。。
image: ../../title_pic/17.jpg
slug: '202305311413'
tags:
- kubernetes
- docker
- 容器
title: 当节点内存管理遇上 Kubernetes：自动调度与控制
---

<!--more-->

##  原理
在现代的容器化环境中，节点资源的管理是一个重要的任务。特别是对于内存资源的管理，它直接影响着容器应用的性能和可用性。在 Kubernetes 中，我们可以利用自动调度和控制的机制来实现对节点内存的有效管理。本文将介绍一种基于 Bash 脚本的节点内存管理方案，并探讨其原理、优势、缺点以及部署和应用趋势。

##  背景
注意到一个节点的内存使用率非常高，一些 Pods 在这个节点上无法正常运行并不断重启。经过仔细研究，发现是因为这个节点的内存资源不足，导致一些高内存需求的 Pods 无法正常运行。您决定实施一种解决方案，以确保这些高内存需求的 Pods 不会被调度到这个节点上，直到您能够通过扩容或升级硬件等方式来解决这个问题。
![在这里插入图片描述](../../image/a7bd959cd55144b5a7405929759ff709.png)![在这里插入图片描述](../../image/94066dc9b42e423ea4bd5f8d4a3b92b8.png)


## 方案
为了实现这个解决方案，您决定使用 Kubernetes 中的污点（Taint）和容忍度（Toleration）机制。您将首先添加一个污点到这个节点，以标识它当前无法容纳高内存需求的 Pods。然后，您将在这些 Pods 的 YAML 文件中添加容忍度字段，以允许它们在具有更充足内存资源的其他节点上运行。最后，您将设置 SchedulingDisabled 标志，以确保后续的 Pods 不会被调度到这个节点上，直到您解决了该节点的内存问题。

## 脚本
```bash
#!/bin/bash

# 功能：控制节点内存
# 如果节点内存占用率超过 90%，则禁止在该节点上调度 Pod
# 如果节点内存占用率低于平均值且平均值小于 90%，则允许在该节点上调度 Pod

# 使用 kubectl top 命令获取节点的内存占用率，并忽略掉一些特定的节点
data=$(kubectl top node | grep -v "MEMORY" | grep -v "cn-shenzhen" | sed "s/%//g")
# 计算所有节点的内存占用率的平均值
avg=$(echo "$data" | awk '{ sum += $NF } END { print sum / NR }' | awk -F. '{ print $1 }')
# 逐行读取每个节点的信息（节点名称和内存占用率）
echo "$data" | awk '{ print $1, $NF }' | while read line
do
  # 获取节点名称和内存占用率
  n=$(echo $line | awk '{ print $1 }')
  m=$(echo $line | awk '{ print $2 }')
  # 如果内存占用率超过 90%，并且该节点没有被设置为不可调度状态，则禁止在该节点上调度 Pod
  if [ "$m" -ge "90" ];then
    if kubectl get node | grep $n | grep -q "SchedulingDisabled";then
      continue
    else
      kubectl cordon $n
    fi
  # 如果内存占用率低于平均值且平均值小于 90%，并且该节点已被设置为不可调度状态，则允许在该节点上调度 Pod
  elif [ "$m" -lt "$avg" ] && [ "$avg" -lt "90" ];then
    if kubectl get node | grep $n | grep -q "SchedulingDisabled";then
      kubectl uncordon $n
    fi
  fi
done

```
![在这里插入图片描述](../../image/5bcdd0b8e7a349f39dc4866302380bbf.png)
![在这里插入图片描述](../../image/0b169f11732e485a8b0e1d7c33ceb585.png)

## 升级版(动态)
它实现了以下功能：

使用 kubectl top 命令获取节点的内存占用率，并忽略掉特定节点（例如 "MEMORY" 和 "cn-shenzhen"）的数据。
计算所有节点的内存占用率的平均值。
遍历每个节点的内存占用率，并根据阈值动态调整节点的调度状态。
如果某个节点的内存占用率超过 90%，并且该节点没有被设置为不可调度状态，则禁止在该节点上调度 Pod（使用 kubectl cordon 命令）。
如果某个节点的内存占用率低于下限阈值，并且该节点已被设置为不可调度状态，则允许在该节点上调度 Pod（使用 kubectl uncordon 命令）。
这样，脚本会根据节点的内存占用率动态调整节点的调度状态，以确保每台机器资源使用率基本一样，并在内存占用率达到 90% 时禁止调度 Pod。
```bash
#/**********************************************************
# * Author        : 南宫乘风
# * Email         : 1794748404@qq.com
# * Last modified : 2023-07-31 16:21
# * Filename      : k8s_auto_mem.sh
# * Description   : 根据节点的内存占用率动态调整节点的调度状态，以确保每台机器资源使用率基本一样，并在内存占用率达到 90% 时禁止调度 Pod。
# * *******************************************************/
#/bin/bash


# 日志函数，接收时间、日志级别和日志内容作为参数
log() {
  local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
  local level=$1
  local message=$2
  echo "[$timestamp] [$level] $message"
}

log "info" "开始执行脚本"

# 使用 kubectl top 命令获取节点的内存占用率，并忽略掉一些特定的节点
data=$(kubectl top node | grep -v "MEMORY" | grep -v "cn-shenzhen" | sed "s/%//g")

# 计算所有节点的内存占用率的平均值
avg=$(echo "$data" | awk '{ sum += $NF } END { print sum / NR }' | awk -F. '{ print $1 }')

# 逐行读取每个节点的信息（节点名称和内存占用率）
echo "$data" | awk '{ print $1, $NF }' | while read line
do
  # 获取节点名称和内存占用率
  n=$(echo $line | awk '{ print $1 }')
  m=$(echo $line | awk '{ print $2 }')

  # 输出节点名称和内存占用率日志
  log "info" "节点 $n 的内存占用率为 $m%"
  
  # 如果内存占用率超过90%，并且该节点没有被设置为不可调度状态，则禁止在该节点上调度 Pod
  if [ "$m" -ge 90 ];then
    if kubectl get node $n | grep -q "SchedulingDisabled";then
      log "info" "节点 $n 内存占用率超过90%，已经禁止调度 Pod"
    else
      log "info" "节点 $n 内存占用率超过90%，禁止调度 Pod"
      kubectl cordon $n
    fi
  else
    # 根据平均阈值动态调整阈值范围（比如将平均阈值的上限和下限设置为平均值的上下10%）
    threshold=$(echo "$avg * 0.1" | bc)
    upper_threshold=$(printf "%.0f" $(echo "$avg + $threshold" | bc))
    lower_threshold=$(printf "%.0f" $(echo "$avg - $threshold" | bc))

    # 如果内存占用率超过上限阈值，并且该节点没有被设置为不可调度状态，则禁止在该节点上调度 Pod
    if [ "$m" -ge "$upper_threshold" ];then
      if kubectl get node $n | grep -q "SchedulingDisabled";then
        log "info" "节点 $n 内存占用率过高，已经禁止调度 Pod"
      else
        log "info" "节点 $n 内存占用率过高，禁止调度 Pod"
        kubectl cordon $n
      fi
    # 如果内存占用率低于下限阈值，并且该节点已被设置为不可调度状态，则允许在该节点上调度 Pod
    elif [ "$m" -lt "$lower_threshold" ];then
      if kubectl get node $n | grep -q "SchedulingDisabled";then
        log "info" "节点 $n 内存占用率较低，允许调度 Pod"
        kubectl uncordon $n
      fi
    fi
  fi
done

log "info" "脚本执行完成"

```


## 原理
该脚本的原理是通过获取节点的内存占用率，并根据预设的阈值进行判断和操作。具体流程如下：

1. 使用 kubectl top 命令获取节点的内存占用率，并忽略掉特定的节点。
2. 计算所有节点的内存占用率的平均值。
3. 逐行读取每个节点的信息，包括节点名称和内存占用率。
4. 如果节点内存占用率超过设定的阈值（例如 90%），并且该节点没有被设置为不可调度状态，则禁止在该节点上调度 Pod。
5. 如果节点内存占用率低于平均值且平均值小于阈值，并且该节点已被设置为不可调度状态，则允许在该节点上调度 Pod。

通过这样的原理，我们可以在集群中实现对节点内存的动态管理，确保节点资源的合理利用和容器应用的稳定运行。

## 优势
**自动化管理：** 该脚本实现了自动化的节点内存管理，无需手动干预，减轻了运维人员的负担。
**实时监测**：通过定期执行脚本，可以实时监测节点的内存占用情况，及时做出调整，提高了容器应用的性能和可用性。
**智能决策**：根据设定的阈值和平均值，脚本能够智能地决策是否禁止或允许在节点上调度 Pod，确保资源的合理分配。
## 缺点

**依赖性：** 该脚本依赖于 Kubernetes 命令行工具 kubectl 和集群的配置，因此需要保证环境的正确配置和可用性。
**单一维度：** 该脚本仅基于节点的内存占用率进行管理，没有考虑其他资源（如 CPU、存储）的情况，因此在综合资源管理方面还有待完善。

