---
author: 南宫乘风
categories:
- Kubernetes
date: 2021-03-06 22:16:21
description: 一、什么是？基于企业内个人用户属于角色来访问计算和网络的常规访问控制方法。简单理解为权限与角色关联，用户通过成为角色的成员来得到角色的权限。的使用组驱动认证决策，准许管理员通过动态配置策略。为了启用，。。。。。。。
image: http://image.ownit.top/4kdongman/100.jpg
tags:
- 技术记录
title: Kubernetes认证之RBAC
---

<!--more-->

### 一、什么是RBAC？

>     Role-based access control\(RBAC\)基于企业内个人用户属于角色来访问计算和网络的常规访问控制方法。  
>     简单理解为权限与角色关联，用户通过成为角色的成员来得到角色的权限。K8S的RBAC使用rbac.authorization.k8s.io/v1 API组驱动认证决策，准许管理员通过API动态配置策略。为了启用RBAC，需要在apiserver启动参数添加--authorization-mode=RBAC。目前支持RBAC,ABAC\(基于属性的访问控制\)，Node（默认node和apiserver就是采用这种模式）,Webhook。

### 二、RBAC分类介绍（API 对象）

2.1、RBAC有4种顶级资源

- Role
- ClusterRole
- RoleBinding
- ClusterRoleBinding

2.2、资源介绍

**Role**：角色，包含一组权限的规则。没有拒绝规则，只是附加允许。Namespace隔离，只作用于命名空间内！

**ClusterRole**：集群角色，和Role一样。和Role的区别，Role是只作用于命名空间内，ClusterRole作用于整个集群！

**RoleBinding**：作用于命令空间内，将ClusterRole或者Role绑定到User、Group、ServiceAccount！

**ClusterRoleBinding**：作用于整个集群。

**中文官方文档**：<https://kubernetes.io/zh/docs/reference/access-authn-authz/rbac/>

### 三、示例

3.1、Role 示例

Role 总是用来在某个名字空间内设置访问权限；在你创建 Role 时，你必须指定该 Role 所属的名字空间

```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" 标明 core API 组
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

3.2、ClusterRole 示例

ClusterRole 有若干用法。你可以用它来：

 1.     定义对某名字空间域对象的访问权限，并将在各个名字空间内完成授权；
 2.     为名字空间作用域的对象设置访问权限，并跨所有名字空间执行授权；
 3.     为集群作用域的资源定义访问权限。

```bash
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" 被忽略，因为 ClusterRoles 不受名字空间限制
  name: secret-reader
rules:
- apiGroups: [""]
  # 在 HTTP 层面，用来访问 Secret 对象的资源的名称为 "secrets"
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

3.3、RoleBinding 示例

下面的例子中的 RoleBinding 将 "pod-reader" Role 授予在 "default" 名字空间中的用户 "jane"。 这样，用户 "jane" 就具有了读取 "default" 名字空间中 pods 的权限。

```bash
apiVersion: rbac.authorization.k8s.io/v1
# 此角色绑定允许 "jane" 读取 "default" 名字空间中的 Pods
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
# 你可以指定不止一个“subject（主体）”
- kind: User # 这里可以是User,Group,ServiceAccount
  name: jane # "name" 是不区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" 指定与某 Role 或 ClusterRole 的绑定关系
  kind: Role # 此字段必须是 Role 或 ClusterRole
  name: pod-reader     # 此字段必须与你要绑定的 Role 或 ClusterRole 的名称匹配
  apiGroup: rbac.authorization.k8s.io
```

3.3.1、RoleBinding 引用 ClusterRole

RoleBinding 也可以引用 ClusterRole，以将对应 ClusterRole 中定义的访问权限授予 RoleBinding 所在名字空间的资源。这种引用使得你可以跨整个集群定义一组通用的角色， 之后在多个名字空间中复用！

下面的例子中的 RoleBinding，将"secret-reader" ClusterRole授予在"development" namespace中的用户"dave"。这样，用户 "dave" 就具有了读取 "development" 名字空间中 pods 的权限。

```bash
apiVersion: rbac.authorization.k8s.io/v1
# 此角色绑定使得用户 "dave" 能够读取 "default" 名字空间中的 Secrets
# 你需要一个名为 "secret-reader" 的 ClusterRole
kind: RoleBinding
metadata:
  name: read-secrets
  # RoleBinding 的名字空间决定了访问权限的授予范围。
  # 这里仅授权在 "development" 名字空间内的访问权限。
  namespace: development
subjects:
- kind: User
  name: dave # 'name' 是不区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

3.4、ClusterRoleBinding 示例

要跨整个集群完成访问权限的授予，你可以使用一个 ClusterRoleBinding。 下面的 ClusterRoleBinding 允许 "manager" 组内的所有用户访问任何名字空间中的 Secrets。

```bash
apiVersion: rbac.authorization.k8s.io/v1
# 此集群角色绑定允许 “manager” 组中的任何人访问任何名字空间中的 secrets
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: manager # 'name' 是不区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

**注意：**

​ 创建了绑定之后，你不能再修改绑定对象所引用的 Role 或 ClusterRole。 试图改变绑定对象的 `roleRef` 将导致合法性检查错误。 如果你想要改变现有绑定对象中 `roleRef` 字段的内容，必须删除重新创建绑定对象。

**这种限制有两个主要原因：**

1.  针对不同角色的绑定是完全不一样的绑定。要求通过删除/重建绑定来更改 `roleRef`, 这样可以确保要赋予绑定的所有主体会被授予新的角色（而不是在允许修改 `roleRef` 的情况下导致所有现有主体胃镜验证即被授予新角色对应的权限）。
2.  将 `roleRef` 设置为不可以改变，这使得可以为用户授予对现有绑定对象的 `update` 权限， 这样可以让他们管理主体列表，同时不能更改被授予这些主体的角色。

命令 `kubectl auth reconcile` 可以创建或者更新包含 RBAC 对象的清单文件， 并且在必要的情况下删除和重新创建绑定对象，以改变所引用的角色

3.5、聚合的 ClusterRole

下面是一个聚合 ClusterRole 的示例：

```bash
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: [] # 控制面自动填充这里的规则

-------
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-endpoints
  labels:
    rbac.example.com/aggregate-to-monitoring: "true"
# 当你创建 "monitoring-endpoints" ClusterRole 时，
# 下面的规则会被添加到 "monitoring" ClusterRole 中
rules:
- apiGroups: [""]
  resources: ["services", "endpoints", "pods"]
  verbs: ["get", "list", "watch"]
```

下面的 ClusterRoles 让默认角色 "admin" 和 "edit" 拥有管理自定义资源 "CronTabs" 的权限， "view" 角色对 CronTab 资源拥有读操作权限。 你可以假定 CronTab 对象在 API 服务器所看到的 URL 中被命名为 `"crontabs"`。

```bash
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: aggregate-cron-tabs-edit
  labels:
    # 添加以下权限到默认角色 "admin" 和 "edit" 中
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
rules:
- apiGroups: ["stable.example.com"]
  resources: ["crontabs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: aggregate-cron-tabs-view
  labels:
    # 添加以下权限到 "view" 默认角色中
    rbac.authorization.k8s.io/aggregate-to-view: "true"
rules:
- apiGroups: ["stable.example.com"]
  resources: ["crontabs"]
  verbs: ["get", "list", "watch"]
```