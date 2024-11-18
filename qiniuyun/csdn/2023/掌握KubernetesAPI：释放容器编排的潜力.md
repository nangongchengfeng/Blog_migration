---
author: 南宫乘风
categories:
- Kubernetes
- ''
- Kubernetes项目实战
date: 2023-08-31 18:41:32
description: 使用、是什么？，应用程序接口：是一些预先定义的接口如函数、接口，或指软件系统不同组成部分衔接的约定。用来提供应用程序与开发人员基于某软件或硬件得以访问的一组例程，而又无需访问源码，或理解内部工作机制的。。。。。。。
image: ../../title_pic/43.jpg
slug: '202308311841'
tags:
- kubernetes
- 容器
- 云原生
title: 掌握Kubernetes API：释放容器编排的潜力
---

<!--more-->

## Kubernetes API使用
### 1、 API是什么？
API（Application Programming Interface，应用程序接口）： 是一些预先定义的接口（如函数、HTTP接口），或指软件系统不同组成部分衔接的约定。 用来提供应用程序与开发人员基于某软件或硬件得以访问的一组例程，而又无需访问源码，或理解内部工作机制的细节。 

K8s也提供API接口，提供这个接口的是管理节点的apiserver组件，apiserver服务负责提供HTTP API，以便用户、其他组件相互通信。  

有两种方式可以操作K8s中的资源：

- HTTP API：https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/  
- 客户端库： https://kubernetes.io/zh/docs/reference/using-api/client-libraries/  

### 2、K8s认证方式
K8s支持三种客户端身份认证：

- HTTPS 证书认证：基于CA证书签名的数字证书认证

- HTTP Token认证：通过一个Token来识别用户

- HTTP Base认证：用户名+密码的方式认证


**HTTPS证书认证（kubeconfig）：**
```python
import os
from kubernetes import client, config
config.load_kube_config(file_path)  # 指定kubeconfig配置文件
apps_api = client.AppsV1Api()  # 资源接口类实例化

for dp in apps_api.list_deployment_for_all_namespaces().items:
    print(dp)
```

**HTTP Token认证（ServiceAccount）：**

```python
from kubernetes import client, config
configuration = client.Configuration()
configuration.host = "https://192.168.31.61:6443"  # APISERVER地址
configuration.ssl_ca_cert="ca.crt"  # CA证书 
configuration.verify_ssl = True   # 启用证书验证
configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
client.Configuration.set_default(configuration)
apps_api = client.AppsV1Api() 
```
获取Token字符串：创建service account并绑定默认cluster-admin管理员集群角色：
```bash
# 创建用户
$ kubectl create serviceaccount dashboard-admin -n kube-system
# 用户授权
$ kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin
# 获取用户Token
$ kubectl describe secrets -n kube-system $(kubectl -n kube-system get secret | awk '/dashboard-admin/{print $1}')
```


其他常用资源接口类实例化：
```python
core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
apps_api = client.AppsV1Api()  # deployment
networking_api = client.NetworkingV1beta1Api()  # ingress
storage_api = client.StorageV1Api()  # storage_class
```

## Python调用

[https://kubernetes.io/zh/docs/reference/using-api/client-libraries/](https://kubernetes.io/zh/docs/reference/using-api/client-libraries/  )
![在这里插入图片描述](../../image/5968b9a903d84ee59cde3f36daa4408d.png)

相关代码示例：[https://github.com/kubernetes-client/python/tree/master/examples](https://github.com/kubernetes-client/python/tree/master/examples)
### 1、安装插件模块
```python
pip install kubernetes
```
**k8s.yml 文件则是  /root/.kube/config**
### 2、deployment服务
#### **增加**
```python
import os
from kubernetes import client, config

config.load_kube_config("k8s.yml")  # 指定kubeconfig配置文件
apps_api = client.AppsV1Api()  # 资源接口类实例化
core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc


def deploy_create():
    """
    创建一个deployment,命名空间默认为default，如果要创建其他命名空间的，需要先创建命名空间
    :return:
    """
    namespace = "default"
    name = "api-test"
    replicas = 3
    labels = {'a': '1', 'b': '2'}  # 不区分数据类型，都要加引号
    image = "nginx"
    body = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector={'matchLabels': labels},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name="web",
                        image=image
                    )]
                )
            ),
        )
    )
    try:
        apps_api.create_namespaced_deployment(namespace=namespace, body=body)
    except Exception as e:
        status = getattr(e, "status")
        if status == 400:
            print(e)
            print("格式错误")
        elif status == 403:
            print("没权限")

if __name__ == '__main__':
    deploy_create()
```
![在这里插入图片描述](../../image/5ee6ac648cce432b939a5995f3671819.png)

#### **查询**
```python
import os
from kubernetes import client, config

config.load_kube_config("k8s.yml")  # 指定kubeconfig配置文件
apps_api = client.AppsV1Api()  # 资源接口类实例化
core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
def deploy_get():
    """
    查询一个deployment
    :return:
    """
    namespace = "default"
    name = "api-test"
    try:
        resp = apps_api.read_namespaced_deployment(namespace=namespace, name=name)
        print(resp)
        print("查询成功")
    except Exception as e:
        status = getattr(e, "status")
        if status == 404:
            print("没找到")
        elif status == 403:
            print("没权限")


if __name__ == '__main__':
    deploy_get()


```
![在这里插入图片描述](../../image/5bd32d4f6b9347edb29e13709f208ee4.png)

#### **修改**

```python
import os
from kubernetes import client, config

config.load_kube_config("k8s.yml")  # 指定kubeconfig配置文件
apps_api = client.AppsV1Api()  # 资源接口类实例化
core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc
def deploy_update():
    namespace = "default"
    name = "api-test"
    replicas = 6
    labels = {'a': '1', 'b': '2'}  # 不区分数据类型，都要加引号
    image = "nginx"
    body = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector={'matchLabels': labels},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(
                        name="web",
                        image=image
                    )]
                )
            ),
        )
    )
    try:
        apps_api.patch_namespaced_deployment(namespace=namespace, name=name, body=body)
    except Exception as e:
        status = getattr(e, "status")
        if status == 400:
            print(e)
            print("格式错误")
        elif status == 403:
            print("没权限")
        elif status == 404:
            print("没找到")


if __name__ == '__main__':
    deploy_update()
```
![在这里插入图片描述](../../image/ee091c1651fb4e578c169191002e138d.png)

#### **删除**

```python
import os
from kubernetes import client, config

config.load_kube_config("k8s.yml")  # 指定kubeconfig配置文件
apps_api = client.AppsV1Api()  # 资源接口类实例化
core_api = client.CoreV1Api()  # namespace,pod,service,pv,pvc

# 删除一个deployment
def deploy_delete():
    namespace = "default"
    name = "api-test"
    body = client.V1DeleteOptions()
    try:
        apps_api.delete_namespaced_deployment(namespace=namespace, name=name, body=body)
    except Exception as e:
        status = getattr(e, "status")
        if status == 404:
            print("没找到")
        elif status == 403:
            print("没权限")
        elif status == 409:
            print("冲突")

if __name__ == '__main__':
    deploy_delete()

```
![在这里插入图片描述](../../image/3eba6d98c25d4a4c84e2a81971ee6c64.png)
### 3、SVC服务
```python

def svc_get():
    """
    查询一个service
    :return: 
    """
    # 查询
    for svc in core_api.list_namespaced_service(namespace="default").items:
        print(svc.metadata.name)



def svc_delete():
    """
    删除一个service
    :return: 
    """
    namespace = "default"
    name = "api-test"
    body = client.V1DeleteOptions()
    try:
        core_api.delete_namespaced_service(namespace=namespace, name=name, body=body)
    except Exception as e:
        status = getattr(e, "status")
        if status == 404:
            print("没找到")
        elif status == 403:
            print("没权限")
        elif status == 409:
            print("冲突")

def svc_create():
    """
    创建一个service,命名空间默认为default，如果要创建其他命名空间的，需要先创建命名空间
    :return: 
    """
    namespace = "default"
    name = "api-test"
    selector = {'a': '1', 'b': '2'}  # 不区分数据类型，都要加引号
    port = 80
    target_port = 80
    type = "NodePort"
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=name
        ),
        spec=client.V1ServiceSpec(
            selector=selector,
            ports=[client.V1ServicePort(
                port=port,
                target_port=target_port
            )],
            type=type
        )
    )
    try:
        core_api.create_namespaced_service(namespace=namespace, body=body)
    except Exception as e:
        status = getattr(e, "status")
        if status == 400:
            print(e)
            print("格式错误")
        elif status == 403:
            print("没权限")

def svc_update():
    """
    更新一个service
    :return: 
    """
    namespace = "default"
    name = "api-test"
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name=name
        ),
        spec=client.V1ServiceSpec(
            selector={'a': '1', 'b': '2'},
            ports=[client.V1ServicePort(
                port=80,
                target_port=8080
            )],
            type="NodePort"
        )
    )
    try:
        core_api.patch_namespaced_service(namespace=namespace, name=name, body=body)
    except Exception as e:
        status = getattr(e, "status")
        if status == 400:
            print(e)
            print("格式错误")
        elif status == 403:
            print("没权限")


```
![在这里插入图片描述](../../image/6bc726b2028e432fabdc84cabb78e437.png)

