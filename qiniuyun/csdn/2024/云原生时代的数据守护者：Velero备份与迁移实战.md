---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2024-08-16 15:19:11
description: 本文将基于一个典型的云原生环境，介绍如何使用 Velero 进行 Kubernetes 集群的备份与迁移支持的版本列表Velero 组件一共分两部分，分别是服务端和客户端。服务端：运行在你
  Kubernetes 的集群中客户端：是一些运行在本地的命令行的工具，需要已配置好 kubectl 及集群 kubeconfig 的机器上。
image: ../../title_pic/60.jpg
slug: '202408161519'
tags:
- 云原生,kubernetes,备份
title: 云原生时代的数据守护者：Velero 备份与迁移实战
---
<!--more-->
## 项目背景
在云计算和容器技术飞速发展的今天，Kubernetes 已经成为容器编排和管理的事实标准。然而，随着业务的不断扩展，如何在云原生环境下保护和迁移 Kubernetes 集群资源，成为了摆在运维人员面前的一大挑战。Velero，作为一款云原生的灾难恢复和迁移工具，以其强大的功能和灵活的使用方式，为 Kubernetes 集群的数据安全提供了坚实的保障。
## 环境介绍
本文将基于一个典型的云原生环境，介绍如何使用 Velero 进行 Kubernetes 集群的备份与迁移

- Kubernetes：v1.23.1
- Velero：1.11


开源地址：[https://github.com/vmware-tanzu/velero](https://github.com/vmware-tanzu/velero)
官方文档：[https://velero.io/docs/v1.11/](https://velero.io/docs/v1.11/)

支持的版本列表
![在这里插入图片描述](../../image/d1a724a24df14242a6487bbcb95c66cf.png)

## 组件介绍
### Velero组件
Velero 组件一共分两部分，分别是服务端和客户端。

- 服务端：运行在你 Kubernetes 的集群中
- 客户端：是一些运行在本地的命令行的工具，需要已配置好 kubectl 及集群 kubeconfig 的机器上

### velero备份流程

1. **Velero 客户端**
   发送 API 请求至 Kubernetes API Server，创建备份任务。
2. **Kubernetes API Server**
   接收并处理 Velero 客户端的请求，创建备份任务，同时通过 Watch 机制通知相关的控制器。
3. **Backup 控制器**
   通过 Watch 机制监听 API Server，获取备份任务后，向 API Server 请求需要备份的数据。
4. **对象存储服务器**
   Backup 控制器将从 API Server 获取的数据备份至指定的对象存储服务器。

![在这里插入图片描述](../../image/1cd67cf7e3564c0ea92111e3e7d1d709.png)

![在这里插入图片描述](../../image/3a948d1e7b43433d883df35f01d6f75f.png)
### Velero 后端存储
Velero 支持两种用于配置后端存储的自定义资源定义 (CRD)，分别是 `BackupStorageLocation` 和 `VolumeSnapshotLocation`。

**BackupStorageLocation**
`BackupStorageLocation` 主要用于定义 Kubernetes 集群资源的备份存储位置，针对的是集群对象数据，而非持久化卷 (PVC) 的数据。该存储通常是 S3 兼容的对象存储，如 MinIO、阿里云 OSS 等。

**VolumeSnapshotLocation**
`VolumeSnapshotLocation` 主要用于对持久化卷 (PV) 进行快照备份，这要求云提供商提供相应的插件。阿里云已经提供了该插件，用户可以通过 CSI (容器存储接口) 等存储机制来进行 PV 的快照备份。此外，用户还可以使用专门的备份工具 **Restic**，将 PV 的数据备份到阿里云 OSS（安装 Velero 时可以选择自定义该选项）。 

> Restic 是一款 GO 语言开发的数据加密备份工具，顾名思义，可以将本地数据加密后传输到指定的仓库。支持的仓库有 Local、SFTP、Aws S3、Minio、OpenStack Swift、Backblaze B2、Azure BS、Google Cloud storage、Rest Server。

## velero客户端
在 [Github Release 页面](https://github.com/vmware-tanzu/velero/releases)下载指定的 velero 二进制客户端安装包，比如这里我们下载我们k8s集群对应的版本为 `v1.11.1`
![在这里插入图片描述](../../image/c4db5520afea4d5887b30ce0493a490d.png)

版本列表：https://github.com/vmware-tanzu/velero/releases

### 安装velero客户端

```bash
$ wget https://github.com/vmware-tanzu/velero/releases/download/v1.11.1/velero-v1.11.1-linux-amd64.tar.gz
$ tar zxf velero-v1.11.1-linux-amd64.tar.gz
$ mv velero-v1.11.1-linux-amd64/velero /usr/bin/
$ velero -h
# 启用命令补全
$ source <(velero completion bash)
$ velero completion bash > /etc/bash_completion.d/velero
```
### 安装minio
 Velero支持很多种存储插件，可查看：[Velero Docs - Providers](https://velero.io/docs/v1.13/supported-providers/)获取插件信息，我们这里使用minio作为S3兼容的对象存储提供程序。您也可以在任意地方部署Minio对象存储，只需要保证K8S集群可以访问到即可。 
 `minio.yaml`

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: velero

---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: velero
  name: minio
  labels:
    component: minio
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      component: minio
  template:
    metadata:
      labels:
        component: minio
    spec:
      volumes:
      - name: storage
        emptyDir: {}
      - name: config
        emptyDir: {}
      containers:
      - name: minio
        image: minio/minio:latest
        imagePullPolicy: IfNotPresent
        args:
        - server
        - /storage
        - --config-dir=/config
        - --console-address=:9001
        env:
        - name: MINIO_ACCESS_KEY
          value: "minio"
        - name: MINIO_SECRET_KEY
          value: "minio123"
        ports:
        - containerPort: 9000
        volumeMounts:
        - name: storage
          mountPath: "/storage"
        - name: config
          mountPath: "/config"

---
apiVersion: v1
kind: Service
metadata:
  namespace: velero
  name: minio
  labels:
    component: minio
spec:
  # ClusterIP is recommended for production environments.
  # Change to NodePort if needed per documentation,
  # but only if you run Minio in a test/trial environment, for example with Minikube.
  type: NodePort
  ports:
    - name: api
      port: 9000
      targetPort: 9000
      nodePort: 32000
    - name: console
      port: 9001
      targetPort: 9001
      nodePort: 32001
  selector:
    component: minio

---
apiVersion: batch/v1
kind: Job
metadata:
  namespace: velero
  name: minio-setup
  labels:
    component: minio
spec:
  template:
    metadata:
      name: minio-setup
    spec:
      restartPolicy: OnFailure
      volumes:
      - name: config
        emptyDir: {}
      containers:
      - name: mc
        image: minio/mc:latest
        imagePullPolicy: IfNotPresent
        command:
        - /bin/sh
        - -c
        - "mc --config-dir=/config config host add velero http://minio:9000 minio minio123 && mc --config-dir=/config mb -p velero/velero"
        volumeMounts:
        - name: config
          mountPath: "/config"

```
### 创建minio应用

```bash
# 创建velero命名空间
$ kubectl create namespace velero
# 创建minio资源
$  kubectl apply -f  minio.yaml
 
# 查看部署状态
[root@bt velero]# kubectl get sts,pod,svc -n velero
NAME                          READY   STATUS      RESTARTS   AGE
pod/minio-78f994f86c-4t9lw    1/1     Running     0          27h
pod/minio-setup-d7vbl         0/1     Completed   4          27h
pod/node-agent-6z5mn          1/1     Running     0          27h
pod/node-agent-8kjcm          1/1     Running     0          27h
pod/node-agent-k8zbk          1/1     Running     0          27h
pod/velero-85dd87c457-mz5jm   1/1     Running     0          27h

NAME            TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)                         AGE
service/minio   NodePort   172.21.25.69   <none>        9000:32000/TCP,9001:32001/TCP   27h

# 开放NodePort端口
$ kubectl patch svc minio -n velero -p '{"spec": {"type": "NodePort"}}'
$ kubectl patch svc minio -n velero --type='json' -p='[{"op": "replace", "path": "/spec/ports/0/nodePort", "value":9000},{"op": "replace", "path": "/spec/ports/1/nodePort", "value":9001}]'
 
[root@bt velero]#  kubectl get svc -n velero  
NAME    TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)                         AGE
minio   NodePort   172.21.25.69   <none>        9000:32000/TCP,9001:32001/TCP   27h

```

通过浏览器访问服务器IP:30282，并使用账号minio密码minio123登入验证。
![在这里插入图片描述](../../image/cfd824198d614b679305e903cc1918b2.png)

## velero 服务端
我们可以使用 velero 客户端来安装服务端，也可以使用 Helm Chart 来进行安装，比如这里我们用客户端来安装，velero 命令默认读取 kubectl 配置的集群上下文，所以前提是 velero 客户端所在的节点有可访问集群的 kubeconfig 配置。
### 创建密钥
首先准备密钥文件，在当前目录建立一个空白文本文件，内容如下所示：

```bash
$ cat > credentials-velero <<EOF
[default]
aws_access_key_id = minio
aws_secret_access_key = minio123
EOF
```
###  安装velero到k8s集群

替换为之前步骤中 minio 的对应 access key id 和 secret access key如果 minio 安装在 kubernetes 集群内时按照如下命令安装 velero 服务端:

```bash
$ velero install \
  --provider aws \
  --image velero/velero:v1.11.1 \
  --plugins velero/velero-plugin-for-aws:v1.7.1 \
  --bucket velero \
  --secret-file ./credentials-velero \
  --use-node-agent \
  --use-volume-snapshots=false \
  --namespace velero \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio:9000 \
  --wait
# 执行install命令后会创建一系列清单，包括CustomResourceDefinition、Namespace、Deployment等。
# velero install .... --dry-run -o yaml > velero_deploy.yaml 如果为私仓，可以通过--dry-run 导出 YAML 文件调整在应用。

# 可使用如下命令查看运行日志
$ kubectl logs deployment/velero -n velero
 
# 查看velero创建的api对象
$ kubectl api-versions | grep velero
velero.io/v1
 
# 查看备份位置
$ velero backup-location get
NAME      PROVIDER   BUCKET/PREFIX   PHASE       LAST VALIDATED                  ACCESS MODE   DEFAULT
default   aws        velero          Available   2024-08-16 14:42:38 +0800 CST   ReadWrite     true


#卸载命令
# velero uninstall --namespace velero
You are about to uninstall Velero.
Are you sure you want to continue (Y/N)? y
Waiting for velero namespace "velero" to be deleted
............................................................................................................................................................................................
Velero namespace "velero" deleted
Velero uninstalled ⛵

```

`选项说明：`
1. `--kubeconfig`(可选)：指定`kubeconfig`认证文件，默认使用`.kube/config`；
2. `--provider`：定义插件提供方；
3. `--image`：定义运行velero的镜像，默认与velero客户端一致；
4. `--plugins`：指定使用aws s3兼容的插件镜像；
5. `--bucket`：指定对象存储Bucket桶名称；
6. `--secret-file`：指定对象存储认证文件；
7. `--use-node-agent`：创建Velero Node Agent守护进程，托管FSB模块；
8. `--use-volume-snapshots`：是否启使用快照；
9. `--namespace`：指定部署的namespace名称，默认为velero；
10. `--backup-location-config`：指定对象存储地址信息；

aws插件与velero版本对应关系：
![在这里插入图片描述](../../image/b8118f58e446476c8edeeb2410e30684.png)
### 卸载velero
如果您想从集群中完全卸载Velero，则以下命令将删除由velero install创建的所有资源:

```bash
kubectl delete namespace/velero clusterrolebinding/velero
kubectl delete crds -l component=velero
```

## 备份与恢复
备份命令：`velero create backup NAME [flags]`
**backup选项：**

- `--exclude-namespaces stringArray` : 要从备份中排除的名称空间
- `--exclude-resources stringArray`: 要从备份中排除的资源，如`storageclasses.storage.k8s.io`
- `--include-cluster-resources optionalBool[=true]`: 包含集群资源类型
- `--include-namespaces stringArray`: 要包含在备份中的名称空间(默认'*')
- `--include-resources stringArray`: 备份中要包括的资源
- `--labels mapStringString`: 给这个备份加上标签
- `-o, --output string`: 指定输出格式，支持'table'、'json'和'yaml'；
- `-l, --selector labelSelector`: 对指定标签的资源进行备份
- `--snapshot-volumes optionalBool[=true]`: 对 PV 创建快照
- `--storage-location string`: 指定备份的位置
- `--ttl duration`: 备份数据多久删掉
- `--volume-snapshot-locations strings`: 指定快照的位置，也就是哪一个公有云驱动



### 使用官方案例创建测试应用



```bash
$ kubectl apply -f examples/nginx-app/base.yaml 
namespace/nginx-example created
deployment.apps/nginx-deployment created
service/my-nginx created
 
# 查看资源清单
$ kubectl get all -n nginx-example
NAME                                    READY   STATUS    RESTARTS   AGE
pod/nginx-deployment-5c844b66c8-t5l9z   1/1     Running   0          27h
pod/nginx-deployment-5c844b66c8-vlkqj   1/1     Running   0          27h

NAME               TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
service/my-nginx   LoadBalancer   172.21.18.168   192.168.102.51   80:31831/TCP   27h

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-deployment   2/2     2            2           27h

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-deployment-5c844b66c8   2         2         2       27h

```

### 备份测试应用



```bash
$ velero backup create nginx-backup --include-namespaces nginx-example
Backup request "nginx-backup" submitted successfully.
Run `velero backup describe nginx-backup` or `velero backup logs nginx-backup` for more details.
```

选项：

- `--include-namespaces`：指定命名空间
- `--selector`：标签选择器，如app=nginx

### 查看备份列表



```bash
$ velero backup get
NAME           STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION   SELECTOR
nginx-backup   Completed   0        0          2024-08-15 11:17:18 +0800 CST   28d       default            <none>

 
# 查看备份详细信息
$ velero backup describe nginx-backup
 
# 查看备份日志
$ velero backup logs nginx-backup
```

登入minio控制台查看备份内容
![在这里插入图片描述](../../image/31ef2668779748f7aed7a01792598a27.png)
### 定时备份指南

```bash
# 使用cron表达式备份
$ velero schedule create nginx-daily --schedule="0 1 * * *" --include-namespaces nginx-example
 
# 使用一些非标准的速记 cron 表达式
$ velero schedule create nginx-daily --schedule="@daily" --include-namespaces nginx-example
 
# 手动触发定时任务
$ velero backup create --from-schedule nginx-daily
```
 更多cron示例请参考：[cron package’s documentation](https://pkg.go.dev/github.com/robfig/cron#hdr-Predefined_schedules) 


###  恢复
模拟灾难

```bash
# 删除nginx-example命名空间和资源
$ kubectl delete namespace nginx-example
# 检查是否删除
$ kubectl get all -n nginx-example
No resources found in nginx-example namespace.
```
恢复资源

```bash
$ velero backup get
NAME           STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION   SELECTOR
nginx-backup   Completed   0        0          2024-04-06 21:47:16 +0800 CST   29d       default            <none>

$ velero restore create --from-backup nginx-backup
Restore request "nginx-backup-20240406215611" submitted successfully.
Run `velero restore describe nginx-backup-20240406215611` or `velero restore logs nginx-backup-20240406215611` for more details.
```
检查恢复的资源

```bash
$ velero restore get
NAME                          BACKUP         STATUS      STARTED                         COMPLETED                       ERRORS   WARNINGS   CREATED                         SELECTOR
nginx-backup-20240406215611   nginx-backup   Completed   2024-04-06 21:56:11 +0800 CST   2024-04-06 21:56:12 +0800 CST   0        2          2024-04-06 21:56:11 +0800 CST   <none>
 
# 查看详细信息
$ velero restore describe nginx-backup-20240406215611
 
# 检查资源状态
$ kubectl get all -n nginx-example
NAME                                    READY   STATUS    RESTARTS   AGE
pod/nginx-deployment-5c844b66c8-t5l9z   1/1     Running   0          27h
pod/nginx-deployment-5c844b66c8-vlkqj   1/1     Running   0          27h

NAME               TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
service/my-nginx   LoadBalancer   172.21.18.168   192.168.102.51   80:31831/TCP   27h

NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-deployment   2/2     2            2           27h

NAME                                          DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-deployment-5c844b66c8   2         2         2       27h

```
参考: 
[https://www.cnblogs.com/nf01/p/18118159](https://www.cnblogs.com/nf01/p/18118159)
[https://github.com/vmware-tanzu/velero](https://github.com/vmware-tanzu/velero)
[https://velero.io/docs/v1.11/](https://velero.io/docs/v1.11/)
