---
author: 南宫乘风
categories:
- 项目实战
- ''
- Kubernetes项目实战
date: 2024-04-11 18:30:08
description: 介绍在传统的业务系统中，应用微服务化后，需要一个统一的入口来将各个服务进行整合，这个入口可以是、、等等。而在中，同样需要一个工具来将应用的各个整合到统一的入口，这个工具就叫控制器，的中文翻译即为入口。。。。。。。。
image: ../../title_pic/73.jpg
slug: '202404111830'
tags:
- 云原生
- ingress
title: Ingress配置优化和追踪
---

<!--more-->


## 介绍

在传统的业务系统中，应用微服务化后，需要一个统一的入口来将各个服务进行整合，这个入口可以是Nginx、Apache、HAproxy等等。而在K8s中，同样需要一个工具来将应用的各个service整合到统一的入口，这个工具就叫Ingress控制器，Ingress的中文翻译即为“入口”。

![在这里插入图片描述](../../image/b43e8a796e434a0cbddd30d0a2bac58d.png)
**Ingress-nginx：** 它是由Kubernetes社区基于Nginx Web服务器开发的，并补充了一组用于实现额外功能的Lua插件，作为“官方”默认控制器支持当然最优。

**Github**​[https://github.com/kubernetes/ingress-nginx](https://github.com/kubernetes/ingress-nginx)

**说明文档**​[https://kubernetes.github.io/ingress-nginx/deploy/](https://kubernetes.github.io/ingress-nginx/deploy/)

**Nginx-ingress** 这是Nginx官方社区开发产品，Nginx ingress具有很高的稳定性，持续的向后兼容性，没有任何第三方模块，并且由于消除了Lua代码而保证了较高的速度。

**Github**​[https://github.com/nginxinc/kubernetes-ingress](https://github.com/nginxinc/kubernetes-ingress)

**说明文档**​[https://docs.nginx.com/nginx-ingress-controller/installation/installation-with-manifests/](https://docs.nginx.com/nginx-ingress-controller/installation/installation-with-manifests/)
![在这里插入图片描述](../../image/6ec9beed76ee45168dc220ea49ae35a8.png)
Nginx Ingress Controller 基于 Nginx 实现了 Kubernetes Ingress API，Nginx 是公认的高性能网关，但如果不对其进行一些参数调优，就不能充分发挥出高性能的优势。Nginx Ingress工作原理：
![在这里插入图片描述](../../image/887fb5e275cd444ebc2c848b78965945.png)
## Kubernetes中ingress-nginx优化配置

描述: 在K8s集群中部署安装 ingress-nginx 后默认并未进行相应的优化配置，本小结将针对于生产环境的中的 ingress-nginx 控制器进行优化。

我们可以从 ingress-nginx-controller 资源的 Pod 、ConfigMap 、以及业务的 ingress 规则入手。

我们当时默认直接安装环境


```json
kubectl get deployments.apps -n ingress-nginx ingress-nginx-controller

# 整体就这个样子，但是没有任何优化，性能肯定欠缺
kubectl get deployments.apps -n ingress-nginx ingress-nginx-controller  -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
    #暴露Prometheus 端口进行监控
    prometheus.io/port: "10254"
    prometheus.io/scrape: "true"
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/version: 1.0.0
    helm.sh/chart: ingress-nginx-4.0.1
    k8s.kuboard.cn/name: ingress-nginx-controller
  name: ingress-nginx-controller
  namespace: ingress-nginx
  resourceVersion: "91407609"
  uid: a5452fcf-f99c-4866-b0a1-93fe9e165cb6
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/component: controller
      app.kubernetes.io/instance: ingress-nginx
      app.kubernetes.io/name: ingress-nginx
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app.kubernetes.io/component: controller
        app.kubernetes.io/instance: ingress-nginx
        app.kubernetes.io/name: ingress-nginx
    spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --election-id=ingress-controller-leader
        - --controller-class=k8s.io/ingress-nginx
        - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
        - --validating-webhook=:8443
        - --validating-webhook-certificate=/usr/local/certificates/cert
        - --validating-webhook-key=/usr/local/certificates/key
        - --watch-ingress-without-class=true
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
        - name: LD_PRELOAD
          value: /usr/local/lib/libmimalloc.so
        image: willdockerhub/ingress-nginx-controller:v1.0.0
        imagePullPolicy: IfNotPresent
        lifecycle:
          preStop:
            exec:
              command:
              - /wait-shutdown
 ...........
```

### 初始化Pod内核参数

温馨提示: 我们需要针对承载 ingress-nginx 的相关 Pod 容器进行内核参数优化。

```json
# 在 spec.template.spec 对象下添加一个初始化 initContainers 容器
      initContainers:
      - command:
        - /bin/sh
        - -c
        - |
          mount -o remount rw /proc/sys
          sysctl -w net.core.somaxconn=65535
          sysctl -w net.ipv4.ip_local_port_range="1024 65535"
          sysctl -w net.ipv4.tcp_tw_reuse=1
          sysctl -w fs.file-max=1048576
          sysctl -w fs.inotify.max_user_instances=16384
          sysctl -w fs.inotify.max_user_watches=524288
          sysctl -w fs.inotify.max_queued_events=16384
        image: busybox:1.29.3
        imagePullPolicy: IfNotPresent
        name: init-sysctl
        resources: {}
        securityContext:
          capabilities:
            add:
            - SYS_ADMIN
            drop:
            - ALL
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File


#修改deployment
 kubectl edit deployments.apps -n ingress-nginx ingress-nginx-controller
```
![在这里插入图片描述](../../image/8aceb8bf41054c5d80ec7045e69213de.png)
**注意：如果按照文档安装，指定机器的跑ingres，会调度失败，因为原先的pod已经占用了80和443端口（唯一方式：先删除pod（先把副本重置为0，修改完毕，在改成1），再修改deployment）**

由此看，定制化有优势，也有劣势。

因为上面的错误，给无生成大量的

主要是调度失败引起的。

```json
ingress-nginx-controller-5d9cbf7bd7-27q74 0/1 NodePorts 0 74s
ingress-nginx-controller-5d9cbf7bd7-5lh9x 0/1 NodePorts 0 75s

```
![在这里插入图片描述](../../image/862f5a42b34d4d28aaa0233099605db8.png)
```json
批量清除（清除完成可能一直卡，需要自己看一下数量）
kubectl get pods -n ingress-nginx -o custom-columns=NAME:.metadata.name,STATUS:.status.phase |grep "Failed" |awk '{print $1}' | xargs -r kubectl delete pod -n ingress-nginx
```
![在这里插入图片描述](../../image/d15189768d8741aeab4a11b3c1fe1ce3.png)
### Ingree的ConfigMap优化

 我们需要按照需要将下述K/V配置项插入到 ingress-nginx 的 configMap 里的 data 对象下。

```json
    spec:
      containers:
      - args:
        - /nginx-ingress-controller
        - --election-id=ingress-controller-leader
        - --controller-class=k8s.io/ingress-nginx
        - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
        - --validating-webhook=:8443
        - --validating-webhook-certificate=/usr/local/certificates/cert
        - --validating-webhook-key=/usr/local/certificates/key
        - --watch-ingress-without-class=true
```

ingress-nginx-controller 这一个就是 Ingree的configmap的配置文件

**ingress-nginx 资源查看**

```json
# 查看 Ingress-nginx 全局配置参数:
kubectl get cm -n ingress-nginx  ingress-nginx-controller -oyaml
```

默认没有任何数据
![在这里插入图片描述](../../image/cf48c686eed74dce990030608e868b43.png)
下面面是data的内容，部分可以再根据实际情况修改

在Ingress Nginx中，ConfigMap的修改可以实现所谓的"热加载"。这意味着当你更改Ingress Nginx的ConfigMap时，Ingress控制器能够接收这些更改并应用它们，而不需要重启Pods。控制器会监听ConfigMap的变化，并自动更新其配置，从而反映出所做的修改。

```json

[root@bt ingress]# kubectl apply -f  ingress-nginx-controller.yaml #热加载一下


[root@bt ingress]# cat ingress-nginx-controller.yaml 
apiVersion: v1
data:
  compute-full-forwarded-for: "true"
  forwarded-for-header: X-Forwarded-For
  log-format-upstream: '{"@timestamp":"$time_iso8601","time":"$time_local","remote_addr":"$remote_addr","http_x_forwarded_for":"$http_x_forwarded_for","remote_port":"$remote_port","remote_user":"$remote_user","host":"$host","upstream_addr":"$upstream_addr","upstream_status":"$upstream_status","upstream_response_time":$upstream_response_time,"upstream_cache_status":"$upstream_cache_status","request":"$request","status":"$status","request_time":$request_time,"body_bytes_sent":"$body_bytes_sent","http_referer":"$http_referer","http_user_agent":"$http_user_agent"}'
  proxy-body-size: 10g
  proxy-buffer-size: 256k
  proxy-connect-timeout: "90"
  proxy-read-timeout: "90"
  proxy-send-timeout: "90"
  use-forwarded-headers: "true"
  # 客户端请求头的缓冲区大小 
  client-header-buffer-size: "512k"
  # 设置用于读取大型客户端请求标头的最大值number和size缓冲区
  large-client-header-buffers: "4 512k"
  # 读取客户端请求body的缓冲区大小
  client-body-buffer-size: "128k"
  # 代理缓冲区大小
  proxy-buffer-size: "256k"
  # 代理body大小
  proxy-body-size: "50m"
  # 服务器名称哈希大小
  server-name-hash-bucket-size: "128"
  # map哈希大小
  map-hash-bucket-size: "128"
  # SSL加密套件
  ssl-ciphers: "ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA"
  # ssl 协议
  ssl-protocols: "TLSv1 TLSv1.1 TLSv1.2"
kind: ConfigMap
metadata:
  labels:
    app: ingress-nginx
  name: ingress-nginx-controller
  namespace: ingress-nginx

```

这个Json 更加全面，可以接入ELK展示

```json
{"@timestamp":"$time_iso8601","request_time":"$request_time","status":"$status","body_bytes_sent":"$body_bytes_sent","bytes_sent":"$bytes_sent","remote_addr":"$remote_addr","remote_user":"$remote_user","remote_port":"$remote_port","request_uri":"$request_uri","args":"$args","request_id":"$request_id","connection":"$connection","connection_requests":"$connection_requests","pid":"$pid","request_length":"$request_length","time_local":"$time_local","http_referer":"$http_referer","http_user_agent":"$http_user_agent","http_x_forwarded_for":"$http_x_forwarded_for","http_host":"$http_host","server_name":"$server_name","ssl_protocol":"$ssl_protocol","ssl_cipher":"$ssl_cipher","scheme":"$scheme","request_method":"$request_method","server_protocol":"$server_protocol","pipe":"$pipe","gzip_ratio":"$gzip_ratio","http_cf_ray":"$http_cf_ray","request_host":"$host","is_completion":"$request_completion","upstream":"$upstream_addr","upstream_name":"$proxy_host","upstream_status":"$upstream_status","upstream_bytes_sent":"$upstream_bytes_sent","upstream_bytes_received":"$upstream_bytes_received","upstream_connect_time":"$upstream_connect_time","upstream_header_time":"$upstream_header_time","upstream_response_time":"$upstream_response_time","upstream_response_length":"$upstream_response_length","upstream_cache_status":"$upstream_cache_status","nginx_host":"$hostname"}
```

![在这里插入图片描述](../../image/a3b0d497a57543b8b1da8494d45f129c.png)
### TCP和UPD


```json
        - /nginx-ingress-controller
        - --election-id=ingress-controller-leader
        - --controller-class=k8s.io/ingress-nginx
        - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller
        - --validating-webhook=:8443
        - --validating-webhook-certificate=/usr/local/certificates/cert
        - --validating-webhook-key=/usr/local/certificates/key
        - --watch-ingress-without-class=true
        - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services #增加tcp配置
        - --udp-services-configmap=$(POD_NAMESPACE)/udp-services #增加upd配置

```

除了 HTTP 流量之外，NGINX Ingress Controller 还可以负载 TCP 和 UDP 流量，因此您可以使用它来管理基于以下协议的各种应用和实用程序的流量，它们包括：

* **MySQL、LDAP 和 MQTT** —— 许多流行应用使用的基于 TCP 协议的应用
* **DNS、syslog 和 RADIUS** —— 边缘设备和非事务性应用使用的基于 UDP 协议的实用程序

[https://www.niewx.cn/2021/11/09/2021-11-09-Use-Nginx-Ingress-to-expose-TCP-and-udp-services/](https://www.niewx.cn/2021/11/09/2021-11-09-Use-Nginx-Ingress-to-expose-TCP-and-udp-services/)

[https://www.nginx-cn.net/blog/load-balancing-tcp-and-udp-traffic-in-kubernetes-with-nginx/](https://www.nginx-cn.net/blog/load-balancing-tcp-and-udp-traffic-in-kubernetes-with-nginx/)


## Ingress日志追踪

在当今互联网架构中，[Web](https://so.csdn.net/so/search?q=Web&spm=1001.2101.3001.7020)应用防火墙（WAF）与Nginx(Ingress)作为前端代理的整合越来越常见，特别是在提升Web应用程序的安全性方面。这种结构不仅增强了对应用的保护，还提升了系统的整体性能。在这种架构中，理解WAF与Nginx(ingress)如何协作，以及如何实现日志追踪的整合尤为重要。

### 用户访问流程日志分析

**总结：阿里云的WAF日志更加详细，Nginx层面的日志也是WAF过来的（数据一样的）**

下方四个截图的数据日志，就是一条的请求的访问。数据都是一样的，各个层面都有日志记录。毫无疑问 WAF更加专业 ，图像化更多。
![在这里插入图片描述](../../image/782a22c470fb4d8082446676b0190042.png)**阿里云的WAF**
![在这里插入图片描述](../../image/03fba65ea96642d48efe7a334313aa1d.png)
**Nginx中转**

```bash
server {
        listen      80;
        server_name xx.xxx.com;
        # IP白名单
        include /usr/local/openresty/nginx/whitelist/corporation.conf;
	    rewrite ^/(.*)$ https://$host/$1 permanent;
}
server {
        listen       443 ssl;
        server_name  kpi.xxxx.com;
        #proxy_read_timeout 180;
        #proxy_send_timeout 180;

        # IP白名单
        include /usr/local/openresty/nginx/whitelist/corporation.conf;

        ssl                   on;
        ssl_certificate      /usr/local/openresty/nginx/ssl/xxx.com.crt;
        ssl_certificate_key  /usr/local/openresty/nginx/ssl/xx.com.key;
        include ssl.conf;

        location / {
            proxy_pass  http://kubernetes-cluster;
            include https_proxy.conf;
        }
}
```

下方的地址为INgress的地址端口（可以看出，Nginx走https，Ingree走http）

```bash
[root@nginx sites]# cat kubernetes-cluster.conf 
upstream kubernetes-cluster {
        server 172.18.xxx.xxx:80;
}

```
![在这里插入图片描述](../../image/ea52b9c0f93f47bdaccae270b8801825.png)
**Ingree（中转）**

Ingress

```bash
[root@jenkins ops]# kubectl get ingresses -n prod new-fujfu-kpi-frontend -oyaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: new-fujfu-kpi-frontend
  namespace: prod
  resourceVersion: "3381713262"
spec:
  rules:
  - host: kpi.xxx.com
    http:
      paths:
      - backend:
          serviceName: new-fujfu-kpi-frontend
          servicePort: 80
        path: /
```

SVC

```bash
[root@jenkins ops]# kubectl get svc -n prod new-fujfu-kpi-frontend -oyaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: new-fujfu-kpi-frontend
  name: new-fujfu-kpi-frontend
  namespace: prod
spec:
  clusterIP: 172.21.14.20
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: new-fujfu-kpi-frontend
  sessionAffinity: None
  type: ClusterIP
```

Pod

```bash
[root@jenkins ops]# kubectl get pod  -n prod --show-labels | grep "new-fujfu-kpi-frontend"
new-fujfu-kpi-frontend.prod-8464c5df44-vsdcw             1/1     Running   0          185d     app=new-fujfu-kpi-frontend,notfixedvalue=value-20231009171117,pod-template-hash=8464c5df44

```

整个Ingree访问流程

Ingree的日志

```bash
kubectl logs -f nginx-ingress-controller-7795b48595-n2dcr -n kube-system |grep  "kpi.xxxx.com"
```
![在这里插入图片描述](../../image/17c5cba6dd0746179f4ea771bd8c0960.png)
**Nginx（Pod）**


Nginx前端 也只是Pod

pod中的Nginx配置

```bash
root@new-fujfu-kpi-frontend:/etc/nginx/conf.d# cat default.conf 
                server {
                    listen       80;
                    server_name  localhost;
                    root   /usr/share/nginx/html;
                    index  index.html index.htm;
                    location / {
                        try_files $uri /index.html;
                    }
                }
```

```bash
[root@jenkins ops]# kubectl get pod  -n prod --show-labels | grep "new-fujfu-kpi-frontend"
new-fujfu-kpi-frontend.prod-8464c5df44-vsdcw             1/1     Running   0          185d     app=new-fujfu-kpi-frontend,notfixedvalue=value-20231009171117,pod-template-hash=8464c5df44
```

日志时间不对，因为pod中差个8个小时引起的
![在这里插入图片描述](../../image/d3d583bdd623429e80cac21a9642afdc.png)
![在这里插入图片描述](../../image/583fb35641d7450f99d6d8817df56d87.png)
日志分析与可视化
利用自定义日志数据进行日志分析与可视化是提高安全性和响应能力的关键。通过集成SIEM工具、ELK栈（Elasticsearch、Logstash、Kibana）或其他日志分析平台，可以对日志数据进行实时监控、异常检测和攻击行为分析。这些工具能够帮助团队快速识别并响应安全威胁，同时提供直观的数据可视化，以便深入理解和改进安全策略。


参考文档：

[从逻辑上深入理解Kubernetes中Ingress及Nginx Ingress Controller的概念及原理](https://blog.csdn.net/sinat_32582203/article/details/120449471)

[https://www.cnblogs.com/varden/p/15128802.html](https://www.cnblogs.com/varden/p/15128802.html)

[https://www.modb.pro/db/405641](https://www.modb.pro/db/405641)


[Kubernetes安装ingress-nginx](https://blog.csdn.net/heian_99/article/details/134776164?spm=1001.2014.3001.5501)
