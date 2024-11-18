---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2023-12-04 09:42:25
description: 安装、简介访问方式在中，服务和的地址仅可以在集群网络内部使用，对于集群外的应用是不可见的。为了使外部的应用能够访问集群内的服务，在目前提供了以下几种方案：集群对外暴露服务的方式目前只有三种：；；缺点：。。。。。。。
image: ../../title_pic/77.jpg
slug: '202312040942'
tags:
- Kubernetes
- Ingress
- Nginx
title: Kubernetes安装ingress-nginx
---

<!--more-->

# Kubernetes安装ingress-nginx

# 1 、Ingress 简介

## 1.1   kubernetes访问方式

在Kubernetes中，服务和Pod的IP地址仅可以在集群网络内部使用，对于集群外的应用是不可见的。为了使外部的应用能够访问集群内的服务，在Kubernetes 目前 提供了以下几种方案：

K8s集群对外暴露服务的方式目前只有三种：Loadbalancer；NodePort；Ingress

* Loadbalancer 缺点：需要阿里云等公有云支持，而且需要额外支付费用
* NodePort 缺点：要暴露端口，端口范围只能是 30000-32767
* Ingress 好处：Ingress 不会公开任意端口或协议。可能就是带来一些学习成本，需要了解Traefik和Nginx的常用配置和反向代理。

一图看Ingress流程,由图可知，ingress充当的是代理的角色，把外部来的请求，根据路由地址转发到k8s中匹配到的后端service，而且service又连接了deployment，一个deployment又跑了N个Pod，达到了流量转发的目的。

‍

service只能通过四层负载就是ip+端口的形式来暴露

* NodePort：会占用集群机器的很多端口，当集群服务变多的时候，这个缺点就越发明显
* LoadBalancer：每个Service都需要一个LB，比较麻烦和浪费资源，并且需要 k8s之外的负载均衡设备支持

ingress可以提供7层的负责对外暴露接口，而且可以调度不同的业务域，不同的url访问路径的业务流量。

* Ingress：K8s 中的一个资源对象，作用是定义请求如何转发到 service 的规则
* Ingress Controller：具体实现反向代理及负载均衡的程序，对Ingress定义的规则进行解析，根据配置的规则来实现请求转发，有很多种实现方式，如 Nginx、Contor、Haproxy等

‍

‍

## 1.2  Ingress 组成

ingress controller

　　将新加入的Ingress转化成Nginx的配置文件并使之生效

ingress服务

　　将Nginx的配置抽象成一个Ingress对象，每添加一个新的服务只需写一个新的Ingress的yaml文件即可

‍

## 1.3 Ingress 工作原理

1.ingress controller通过和kubernetes api交互，动态的去感知集群中ingress规则变化，

2.然后读取它，按照自定义的规则，规则就是写明了哪个域名对应哪个service，生成一段nginx配置，

3.再写到nginx-ingress-control的pod里，这个Ingress controller的pod里运行着一个Nginx服务，控制器会把生成的nginx配置写入/etc/nginx.conf文件中，

4.然后reload一下使配置生效。以此达到域名分配置和动态更新的问题。

![image](../../image/8723382c73f44062b2a1d9b5e4373efa.png)​

* 用户编写 Ingress Service规则， 说明每个域名对应 K8s集群中的哪个Service
* Ingress控制器会动态感知到 Ingress 服务规则的变化，然后生成一段对应的Nginx反向代理配置
* Ingress控制器会将生成的Nginx配置写入到一个运行中的Nginx服务中，并动态更新
* 然后客户端通过访问域名，实际上Nginx会将请求转发到具体的Pod中，到此就完成了整个请求的过程

![image](../../image/84fc5ef7133c490f9db6ee9145c41c79.png)​

## 1.4 Ingress可以解决什么问题

1.动态配置服务

　　如果按照传统方式, 当新增加一个服务时, 我们可能需要在流量入口加一个反向代理指向我们新的k8s服务. 而如果用了Ingress, 只需要配置好这个服务, 当服务启动时, 会自动注册到Ingress的中, 不需要而外的操作.

2.减少不必要的端口暴露

　　配置过k8s的都清楚, 第一步是要关闭防火墙的, 主要原因是k8s的很多服务会以NodePort方式映射出去, 这样就相当于给宿主机打了很多孔, 既不安全也不优雅. 而Ingress可以避免这个问题, 除了Ingress自身服务可能需要映射出去, 其他服务都不要用NodePort方式

# 2 、部署配置Ingress

## 2.1       部署文件介绍、准备

[https://kubernetes.github.io/ingress-nginx/deploy/](https://kubernetes.github.io/ingress-nginx/deploy/)

网上的资料一般是基于v0.30.0来安装，但是对于kubernetes@1.22来说要安装ingress-nginx@v1.0.0以上版本（目前最新版本是v1.0.4，本文采用v1.0.0），原因是 kubectl@v1.22版本不再支持v1beta1

如果安装ingress-nginx@v0.30.0版本后启动pod有如下问题

```
Failed to list *v1beta1.Ingress: the server could not find the requested resource
```

有一个版本的支持情况（[https://github.com/kubernetes/ingress-nginx/](https://github.com/kubernetes/ingress-nginx/)）

ingress [官方网站](https://link.juejin.cn/?target=https%3A%2F%2Fkubernetes.github.io%2Fingress-nginx%2F "https://kubernetes.github.io/ingress-nginx/") ingress [仓库地址](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fkubernetes%2Fingress-nginx "https://github.com/kubernetes/ingress-nginx")

ingress-nginx v1.0 最新版本 v1.0  
适用于 Kubernetes 版本 v1.19+ （包括 v1.19 ）  
Kubernetes-v1.22+ 需要使用 ingress-nginx>=1.0，因为networking.k8s.io/v1beta 已经移除

![image](../../image/75e6a580e18441bc90a297cec6364622.png)​

## 2.2 直接部署 ingress-nginx

直接部署比较简单，直接拉去 girhub 的文件就可以了，如果遇到长时间无响应，可以终止任务从新拉取。

拉取镜像yaml文件

```bash
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/baremetal/deploy.yaml

#更换国内镜像
sed -i 's@k8s.gcr.io/ingress-nginx/controller:v1.0.0\(.*\)@willdockerhub/ingress-nginx-controller:v1.0.0@' deploy.yaml
sed -i 's@k8s.gcr.io/ingress-nginx/kube-webhook-certgen:v1.0\(.*\)$@hzde0128/kube-webhook-certgen:v1.0@' deploy.yaml
```

‍

## 2.3 优化yaml配置文件

1、默认 ingress-nginx 随机提供 nodeport 端口，开启 hostNetwork 启用80、443端口。

‍

‍

需要在原deploy.yaml文件上修改修改后再部署

### 修改点如下

1：k8s.gcr.io/ingress-nginx/controller:v1.0.0@sha256:0851b34f69f69352bf168e6ccf30e1e20714a264ab1ecd1933e4d8c0fc3215c6 改为：willdockerhub/ingress-nginx-controller:v1.0.0

2：k8s.gcr.io/ingress-nginx/kube-webhook-certgen:v1.0@sha256:f3b6b39a6062328c095337b4cadcefd1612348fdd5190b1dcbcb9b9e90bd8068 改为：jettech/kube-webhook-certgen:v1.0.0

#3：Deployment修改点

```bash

  template:      
    metadata:    
      labels:    
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/component: controller
    spec:        
      dnsPolicy: ClusterFirstWithHostNet  #既能使用宿主机DNS，又能使用集群DNS  原文line：319
      hostNetwork: true                   #与宿主机共享网络
      nodeName: k8s-master-1              #设置只能在k8s-master-1节点运行
      tolerations:                        #设置能容忍master污点
      - key: node-role.kubernetes.io/master
        operator: Exists
      containers:   
        - name: controller
          image: willdockerhub/ingress-nginx-controller:v1.0.0
          imagePullPolicy: IfNotPresent

如果不关心 ingressClass 或者很多没有 ingressClass 配置的 ingress 对象， 添加参数 ingress-controller --watch-ingress-without-class=true 。


优化上传等参数
# Source: ingress-nginx/templates/controller-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
data:
  # header默认大小上限是4k，超过会返回400错误
  client_header_buffer_size: "16k"
  large_client_header_buffers: "4 16k"
  # 请求体默认大小上限是1m，超过会返回413错误
  proxy-body-size: "10m"



```

‍

修改后的yaml文件

```bash
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx

---
# Source: ingress-nginx/templates/controller-serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx
  namespace: ingress-nginx
automountServiceAccountToken: true
---
# Source: ingress-nginx/templates/controller-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
data:
  # header默认大小上限是4k，超过会返回400错误
  client_header_buffer_size: "16k"
  large_client_header_buffers: "4 16k"
  # 请求体默认大小上限是1m，超过会返回413错误
  proxy-body-size: "10m"

---
# Source: ingress-nginx/templates/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
  name: ingress-nginx
rules:
  - apiGroups:
      - ''
    resources:
      - configmaps
      - endpoints
      - nodes
      - pods
      - secrets
    verbs:
      - list
      - watch
  - apiGroups:
      - ''
    resources:
      - nodes
    verbs:
      - get
  - apiGroups:
      - ''
    resources:
      - services
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ''
    resources:
      - events
    verbs:
      - create
      - patch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - update
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingressclasses
    verbs:
      - get
      - list
      - watch
---
# Source: ingress-nginx/templates/clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
  name: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ingress-nginx
subjects:
  - kind: ServiceAccount
    name: ingress-nginx
    namespace: ingress-nginx
---
# Source: ingress-nginx/templates/controller-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx
  namespace: ingress-nginx
rules:
  - apiGroups:
      - ''
    resources:
      - namespaces
    verbs:
      - get
  - apiGroups:
      - ''
    resources:
      - configmaps
      - pods
      - secrets
      - endpoints
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ''
    resources:
      - services
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - update
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingressclasses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ''
    resources:
      - configmaps
    resourceNames:
      - ingress-controller-leader
    verbs:
      - get
      - update
  - apiGroups:
      - ''
    resources:
      - configmaps
    verbs:
      - create
  - apiGroups:
      - ''
    resources:
      - events
    verbs:
      - create
      - patch
---
# Source: ingress-nginx/templates/controller-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx
  namespace: ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ingress-nginx
subjects:
  - kind: ServiceAccount
    name: ingress-nginx
    namespace: ingress-nginx
---
# Source: ingress-nginx/templates/controller-service-webhook.yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller-admission
  namespace: ingress-nginx
spec:
  type: ClusterIP
  ports:
    - name: https-webhook
      port: 443
      targetPort: webhook
      appProtocol: https
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/component: controller
---
# Source: ingress-nginx/templates/controller-service.yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: http
      appProtocol: http
    - name: https
      port: 443
      protocol: TCP
      targetPort: https
      appProtocol: https
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/component: controller
---
# Source: ingress-nginx/templates/controller-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
      app.kubernetes.io/instance: ingress-nginx
      app.kubernetes.io/component: controller
  revisionHistoryLimit: 10
  minReadySeconds: 0
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/component: controller
    spec:
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
      nodeName: node01       
      tolerations:                          
      - key: node-role.kubernetes.io/master
        operator: Exists
      containers:
        - name: controller
          image: willdockerhub/ingress-nginx-controller:v1.0.0
          imagePullPolicy: IfNotPresent
          lifecycle:
            preStop:
              exec:
                command:
                  - /wait-shutdown
          args:
            - /nginx-ingress-controller
            - --election-id=ingress-controller-leader
            - --controller-class=k8s.io/ingress-nginx
            - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
            - --validating-webhook=:8443
            - --validating-webhook-certificate=/usr/local/certificates/cert
            - --validating-webhook-key=/usr/local/certificates/key
          securityContext:
            capabilities:
              drop:
                - ALL
              add:
                - NET_BIND_SERVICE
            runAsUser: 101
            allowPrivilegeEscalation: true
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: LD_PRELOAD
              value: /usr/local/lib/libmimalloc.so
          livenessProbe:
            failureThreshold: 5
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
            - name: https
              containerPort: 443
              protocol: TCP
            - name: webhook
              containerPort: 8443
              protocol: TCP
          volumeMounts:
            - name: webhook-cert
              mountPath: /usr/local/certificates/
              readOnly: true
          resources:
            requests:
              cpu: 100m
              memory: 90Mi
      nodeSelector:
        kubernetes.io/os: linux
      serviceAccountName: ingress-nginx
      terminationGracePeriodSeconds: 300
      volumes:
        - name: webhook-cert
          secret:
            secretName: ingress-nginx-admission
---
# Source: ingress-nginx/templates/controller-ingressclass.yaml
# We don't support namespaced ingressClass yet
# So a ClusterRole and a ClusterRoleBinding is required
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: nginx
  namespace: ingress-nginx
spec:
  controller: k8s.io/ingress-nginx
---
# Source: ingress-nginx/templates/admission-webhooks/validating-webhook.yaml
# before changing this value, check the required kubernetes version
# https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#prerequisites
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
  name: ingress-nginx-admission
webhooks:
  - name: validate.nginx.ingress.kubernetes.io
    matchPolicy: Equivalent
    rules:
      - apiGroups:
          - networking.k8s.io
        apiVersions:
          - v1
        operations:
          - CREATE
          - UPDATE
        resources:
          - ingresses
    failurePolicy: Fail
    sideEffects: None
    admissionReviewVersions:
      - v1
    clientConfig:
      service:
        namespace: ingress-nginx
        name: ingress-nginx-controller-admission
        path: /networking/v1/ingresses
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ingress-nginx-admission
  namespace: ingress-nginx
  annotations:
    helm.sh/hook: pre-install,pre-upgrade,post-install,post-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ingress-nginx-admission
  annotations:
    helm.sh/hook: pre-install,pre-upgrade,post-install,post-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
rules:
  - apiGroups:
      - admissionregistration.k8s.io
    resources:
      - validatingwebhookconfigurations
    verbs:
      - get
      - update
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ingress-nginx-admission
  annotations:
    helm.sh/hook: pre-install,pre-upgrade,post-install,post-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ingress-nginx-admission
subjects:
  - kind: ServiceAccount
    name: ingress-nginx-admission
    namespace: ingress-nginx
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ingress-nginx-admission
  namespace: ingress-nginx
  annotations:
    helm.sh/hook: pre-install,pre-upgrade,post-install,post-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
rules:
  - apiGroups:
      - ''
    resources:
      - secrets
    verbs:
      - get
      - create
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ingress-nginx-admission
  namespace: ingress-nginx
  annotations:
    helm.sh/hook: pre-install,pre-upgrade,post-install,post-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ingress-nginx-admission
subjects:
  - kind: ServiceAccount
    name: ingress-nginx-admission
    namespace: ingress-nginx
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/job-createSecret.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ingress-nginx-admission-create
  namespace: ingress-nginx
  annotations:
    helm.sh/hook: pre-install,pre-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
spec:
  template:
    metadata:
      name: ingress-nginx-admission-create
      labels:
        helm.sh/chart: ingress-nginx-4.0.1
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/version: 1.0.0
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/component: admission-webhook
    spec:
      containers:
        - name: create
          image: hzde0128/kube-webhook-certgen:v1.0
          imagePullPolicy: IfNotPresent
          args:
            - create
            - --host=ingress-nginx-controller-admission,ingress-nginx-controller-admission.$(POD_NAMESPACE).svc
            - --namespace=$(POD_NAMESPACE)
            - --secret-name=ingress-nginx-admission
          env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
      restartPolicy: OnFailure
      serviceAccountName: ingress-nginx-admission
      nodeSelector:
        kubernetes.io/os: linux
      securityContext:
        runAsNonRoot: true
        runAsUser: 2000
---
# Source: ingress-nginx/templates/admission-webhooks/job-patch/job-patchWebhook.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ingress-nginx-admission-patch
  namespace: ingress-nginx
  annotations:
    helm.sh/hook: post-install,post-upgrade
    helm.sh/hook-delete-policy: before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.1
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
spec:
  template:
    metadata:
      name: ingress-nginx-admission-patch
      labels:
        helm.sh/chart: ingress-nginx-4.0.1
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/version: 1.0.0
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/component: admission-webhook
    spec:
      containers:
        - name: patch
          image: hzde0128/kube-webhook-certgen:v1.0
          imagePullPolicy: IfNotPresent
          args:
            - patch
            - --webhook-name=ingress-nginx-admission
            - --namespace=$(POD_NAMESPACE)
            - --patch-mutating=false
            - --secret-name=ingress-nginx-admission
            - --patch-failure-policy=Fail
          env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
      restartPolicy: OnFailure
      serviceAccountName: ingress-nginx-admission
      nodeSelector:
        kubernetes.io/os: linux
      securityContext:
        runAsNonRoot: true
        runAsUser: 2000


```

开始执行

```bash
$ kubectl apply -f deploy.yaml
namespace/ingress-nginx created
serviceaccount/ingress-nginx created
configmap/ingress-nginx-controller created
clusterrole.rbac.authorization.k8s.io/ingress-nginx created
clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx created
role.rbac.authorization.k8s.io/ingress-nginx created
rolebinding.rbac.authorization.k8s.io/ingress-nginx created
service/ingress-nginx-controller-admission created
service/ingress-nginx-controller created
deployment.apps/ingress-nginx-controller created
ingressclass.networking.k8s.io/nginx created
validatingwebhookconfiguration.admissionregistration.k8s.io/ingress-nginx-admission created
serviceaccount/ingress-nginx-admission created
clusterrole.rbac.authorization.k8s.io/ingress-nginx-admission created
clusterrolebinding.rbac.authorization.k8s.io/ingress-nginx-admission created
role.rbac.authorization.k8s.io/ingress-nginx-admission created
rolebinding.rbac.authorization.k8s.io/ingress-nginx-admission created
job.batch/ingress-nginx-admission-create created
job.batch/ingress-nginx-admission-patch created
```

查看生成状态

```bash
[root@bt ingress]# kubectl get all -n ingress-nginx
NAME                                            READY   STATUS      RESTARTS   AGE
pod/ingress-nginx-admission-create-hdd2b        0/1     Completed   0          5d12h
pod/ingress-nginx-admission-patch-4x2nj         0/1     Completed   1          5d12h
pod/ingress-nginx-controller-6db5ddb4ff-jv4rr   1/1     Running     0          5d12h

NAME                                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/ingress-nginx-controller             ClusterIP   172.21.23.131   <none>        80/TCP,443/TCP   5d12h
service/ingress-nginx-controller-admission   ClusterIP   172.21.21.247   <none>        443/TCP          5d12h

NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ingress-nginx-controller   1/1     1            1           5d12h

NAME                                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/ingress-nginx-controller-6db5ddb4ff   1         1         1       5d12h

NAME                                       COMPLETIONS   DURATION   AGE
job.batch/ingress-nginx-admission-create   1/1           3s         5d12h
job.batch/ingress-nginx-admission-patch    1/1           4s         5d12h

[root@bt ingress]# kubectl get endpoints -n ingress-nginx ingress-nginx-controller
NAME                       ENDPOINTS                              AGE
ingress-nginx-controller   192.168.102.40:443,192.168.102.40:80   5d12h
[root@bt ingress]# kubectl get endpoints -n ingress-nginx ingress-nginx-controller-admission 
NAME                                 ENDPOINTS             AGE
ingress-nginx-controller-admission   192.168.102.40:8443   5d12h


```

这个时候ingress-nginx就安装完了，在kubernets之外的机器上访问每个节点，nginx都可以访问了，先不用管404的错误

```bash
[root@bt ingress]# curl http://node01
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
[root@bt ingress]# 

```

‍

# 3、 测试验证

配置nginx简单yaml文件

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: heian
  name: ingress-heian
  annotations:
    k8s.kuboard.cn/workload: ingress-heian
    deployment.kubernetes.io/revision: '1'
    k8s.kuboard.cn/service: ClusterIP
    k8s.kuboard.cn/ingress: 'true'
  labels:
    app: ingress-heian
spec:
  selector:
    matchLabels:
      app: ingress-heian
  revisionHistoryLimit: 10
  template:
    metadata:
      labels:
        app: ingress-heian
    spec:
      affinity: {}
      securityContext:
        seLinuxOptions: {}
      imagePullSecrets: []
      restartPolicy: Always
      initContainers: []
      containers:
        - image: 'wangyanglinux/myapp:v1'
          imagePullPolicy: IfNotPresent
          name: ingress-heian
          volumeMounts:
            - name: tz-config
              mountPath: /usr/share/zoneinfo/Asia/Shanghai
            - name: tz-config
              mountPath: /etc/localtime
            - name: timezone
              mountPath: /etc/timezone
          resources:
            limits:
              cpu: 100m
              memory: 100Mi
            requests:
              cpu: 10m
              memory: 10Mi
          env:
            - name: TZ
              value: Asia/Shanghai
            - name: LANG
              value: C.UTF-8
          lifecycle: {}
          ports:
            - name: web
              containerPort: 80
              protocol: TCP
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
      volumes:
        - name: tz-config
          hostPath:
            path: /usr/share/zoneinfo/Asia/Shanghai
            type: ''
        - name: timezone
          hostPath:
            path: /etc/timezone
            type: ''
      dnsPolicy: ClusterFirst
      dnsConfig:
        options: []
      schedulerName: default-scheduler
      terminationGracePeriodSeconds: 30
  progressDeadlineSeconds: 600
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  replicas: 1
 
---
apiVersion: v1
kind: Service
metadata:
  namespace: heian
  name: ingress-heian
  annotations:
    k8s.kuboard.cn/workload: ingress-heian
  labels:
    app: ingress-heian
spec:
  selector:
    app: ingress-heian
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
      name: ingress-web-1
      nodePort: 0
  sessionAffinity: None
 
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: heian
  name: ingress-heian
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/proxy-body-size: "0"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
    kubernetes.io/tls-acme: "true"
    cert-manager.io/cluster-issuer: "example-issuer"
  labels:
    app: ingress-heian
spec:
  rules:
  - host: ingress.ownit.top #域名
    http:
      paths:
      - pathType: Prefix
        path: /
        backend:
          service:
            name: ingress-heian
            port:
              number: 80
```

测试完成

```bash
[root@bt heian]# kubectl get pod,svc,ingress -n heian
NAME                                 READY   STATUS    RESTARTS   AGE
pod/ingress-heian-7ff9cbd9d5-w5f7v   1/1     Running   0          5d

NAME                    TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/ingress-heian   ClusterIP   172.21.24.68   <none>        80/TCP    5d

NAME                                      CLASS    HOSTS               ADDRESS          PORTS   AGE
ingress.networking.k8s.io/ingress-heian   <none>   ingress.ownit.top   192.168.102.40   80      5d
[root@bt heian]# curl https://ingress.ownit.top
Hello MyApp | Version: v1 | <a href="hostname.html">Pod Name</a>
[root@bt heian]# curl https://ingress.ownit.top/hostname.html
ingress-heian-7ff9cbd9d5-w5f7v


```

![image](../../image/bbf9bca0f1f94b7fb0d03472cf8b5a32.png)​

# 4、NGINX作为反向代理

1、安装nginx

```bash
yum install nginx nginx-mod-stream -y
```

2、配置kubernetes-cluster.conf

```bash
[root@bt nginx]# cat kubernetes-cluster.conf 
upstream kubernetes-cluster {
  server 192.168.102.40 weight=5;
  keepalive 16;
}

```

3、配置ingress访问接口

```bash
[root@bt nginx]# cat ingress.ownit.top.conf 
server {
        listen       80;
        server_name  ingress.ownit.top;
        rewrite ^/(.*)$ https://$host/$1 permanent;
        # IP白名单
        include /opt/nginx/whitelist/corporation.conf;
}
server {
        listen       443 ssl;
        server_name  ingress.ownit.top;
        # IP白名单
        include /opt/nginx/whitelist/corporation.conf;

        #ssl                   on;
        ssl_certificate      /opt/nginx/ssl/ownit.top.crt;
        ssl_certificate_key  /opt/nginx/ssl/ownit.top.key;
        include ssl.conf;

        location / {
            proxy_pass  http://kubernetes-cluster;
            include https_proxy.conf;
        }
	access_log  /www/wwwlogs/dns.ownit.top.log;
    error_log  /www/wwwlogs/dns.ownit.top.error.log;

}

```

4、则可以HTTPS访问到k8s里面的ingress域名

![image](../../image/bbf9bca0f1f94b7fb0d03472cf8b5a32.png)​

![image](../../image/d9574f7332294220b7e462f3f49db42e.png)​

‍
