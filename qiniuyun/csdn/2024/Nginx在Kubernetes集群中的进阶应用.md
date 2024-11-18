---
author: 南宫乘风
categories:
- Nginx
- ''
- Kubernetes项目实战
date: 2024-04-02 16:13:11
description: 简介在现代环境中，作为负载均衡器与的资源的结合，为应用程序提供了强大的路由和安全解决方案。本文将深入探讨如何利用的灵活性和功能，实现高效、安全的外部访问控制，以及如何配置以优化流量管理和支持。可以与的。。。。。。。
image: ../../title_pic/74.jpg
slug: '202404021613'
tags:
- nginx
- kubernetes
- 运维
title: Nginx在Kubernetes集群中的进阶应用
---

<!--more-->

## 简介

在现代DevOps环境中，Nginx作为负载均衡器与Kubernetes的Ingress资源的结合，为应用程序提供了强大的路由和安全解决方案。本文将深入探讨如何利用Nginx的灵活性和功能，实现高效、安全的外部访问控制，以及如何配置Ingress以优化流量管理和SSL/TLS支持。


Nginx 可以与 Kubernetes 的 Ingress 资源配合使用，以提供高级的路由和负载均衡功能。Ingress 允许你通过定义规则来管理外部访问集群内服务的路径。当与 Nginx Ingress 控制器结合使用时，你可以利用 Nginx 的强大功能来处理 HTTP 和 HTTPS 流量，包括 SSL/TLS 终端、虚拟主机、重写和更多。
![在这里插入图片描述](../../image/ee486123f1ce48ea990d66e887d766d4.png)
## 环境

* **Nginx服务**：部署在公网，IP地址为172.1x.1x9.90，作为集群的入口点。
* **内网环境**：基于Kubernetes的集群，使用Ingress资源管理服务间的通信。

## Nginx构建步骤

### 公网Nginx为入口

在现代的网络架构中，使用 Nginx 作为反向代理服务器是一种常见的做法，它可以帮助我们将公网流量有效地转发到内网的应用程序服务器。

#### **http_proxy.conf**

```yml
[root@monitor conf]# cat http_proxy.conf 
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_http_version 1.1;
proxy_set_header Connection "";
```

这是一个配置文件，通常用于设置 HTTP 代理服务器的行为。下面是每一行的解释：

* `proxy_set_header Host $host;`    这一行设置代理服务器向目标服务器发送请求时，将使用原始请求中的 `Host` 头部。`$host` 是 Nginx 配置中的变量，代表请求行中的主机名。
* `proxy_set_header X-Real-IP $remote_addr;`    这里配置代理服务器向目标服务器发送请求时，会添加一个 `X-Real-IP` 头部，其值为发起请求的客户端的 IP 地址。`$remote_addr` 是 Nginx 配置中的变量，代表客户端的 IP 地址。
* `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`    这一行配置代理服务器在向目标服务器发送请求时，会添加一个 `X-Forwarded-For` 头部，用于表示发起请求的原始客户端的 IP 地址。`$proxy_add_x_forwarded_for` 是一个变量，它包含了原始请求中的 `X-Forwarded-For` 头部的值，如果有的话。
* `proxy_http_version 1.1;`<br />这里指定代理服务器使用 HTTP 版本 1.1 与目标服务器进行通信。这是因为 HTTP/1.1 支持持久连接，可以提高性能和效率。
* `proxy_set_header Connection "";`<br />这一行设置代理服务器向目标服务器发送请求时，`Connection` 头部将不会被发送。这通常用于防止目标服务器关闭连接，特别是在使用 HTTP/1.1 或 HTTP/2 时，持久连接是有益的。

这些配置通常用于确保代理服务器正确地转发客户端的请求到目标服务器，并且目标服务器能够接收到正确的原始请求信息。

#### **https_proxy.conf**

```yml
[root@monitor conf]# cat https_proxy.conf 
add_header Front-End-Https on;
proxy_http_version 1.1;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Connection "";
proxy_set_header X-Forwarded-Proto https;
proxy_set_header X-Forwarded-HTTPS on;
proxy_connect_timeout 90;
proxy_send_timeout 90;
proxy_read_timeout 90;
proxy_buffer_size 256k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;
proxy_temp_file_write_size 256k;
proxy_max_temp_file_size 8m;

```

#### **ssl.conf**

```yml
[root@monitor conf]# cat ssl.conf 
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_ciphers "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES256-GCM-SHA384:AES128-GCM-SHA256:AES256-SHA256:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4";
ssl_prefer_server_ciphers  on;

ssl_stapling on;
ssl_stapling_verify off;
resolver 223.5.5.5 223.6.6.6 valid=300s;
resolver_timeout 10s;

```


#### Server的conf

```yml
server {
        listen       80;
        server_name   admin-uat.xxx.net;
        rewrite ^/(.*)$ https://$host/$1 permanent;
        #它执行了一个永久重定向策略，强制所有HTTP流量转向HTTPS，同时引用了公司白名单配置文件，以确保只有经过授权的用户或IP地址可以访问此服务。
        include /usr/local/openresty/nginx/whitelist/corporation.conf;
}
server {
        listen       443 ssl;
        server_name  admin-uat.xxx.net;
        include /usr/local/openresty/nginx/whitelist/corporation.conf;

        ssl                   on;
        ssl_certificate      /usr/local/openresty/nginx/ssl/xxx.net.crt;
        ssl_certificate_key  /usr/local/openresty/nginx/ssl/xxx.net.key;
        include ssl.conf;

        location / {
            proxy_pass  http://kubernetes-cluster;
            include https_proxy.conf;
        }
}

```

这个服务器块负责处理加密的HTTPS流量，配置了SSL证书和密钥以保证传输安全，并且在location上下文中设置了代理转发至名为`kubernetes-cluster`的上游服务器组。

#### 流量进行转发

```yml
[root@monitor vhosts]# cat kubernetes-cluster.conf 
upstream kubernetes-cluster {
  server 192.168.82.42 weight=5;
  keepalive 16;
}

```

这里定义了一个上游服务器池，包含了一台内网IP地址为192.168.82.42的服务器，权重设置为5，意味着相对其他可能存在的服务器，此服务器将接收到更多比例的请求。同时，保持16个活动连接（keepalive），有助于减少建立新连接的开销，提高性能。


### 内网Nginx


#### **default.conf**

```yml
server {
  listen 80 default_server;  # 监听80端口，默认服务器配置
  index index.html index.htm index.php;  # 默认的索引文件
  root /usr/share/nginx/html;  # 根目录配置

  location / {
    proxy_pass http://kubernetes-cluster;  # 反向代理到kubernetes-cluster
    include proxy.conf;  # 包含proxy.conf文件
  }

  location ~ ^/Bdata_Nginx_Status$ {
    stub_status on;  # 启用Nginx状态页面
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    allow 172.16.0.0/12;
    allow 192.168.0.0/16;
    deny all;  # 拒绝其他IP访问
  }

  location /Bdata_Check_Status {
    check_status;  # 启用Nginx健康检查
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    allow 172.16.0.0/12;
    allow 192.168.0.0/16;
    deny all;  # 拒绝其他IP访问
  }

  access_log /var/log/nginx/access.log main;  # 访问日志路径和格式
}

server {
  listen 443 ssl default_server;  # 监听443端口，默认服务器配置，启用SSL
  index index.html index.htm index.php;  # 默认的索引文件
  root /usr/share/nginx/html;  # 根目录配置

  ssl_certificate /etc/nginx/ssl/server.crt;  # SSL证书路径
  ssl_certificate_key /etc/nginx/ssl/server.key;  # SSL证书私钥路径

  location / {
    proxy_pass https://kubernetes-cluster-https;  # 反向代理到kubernetes-cluster-https
    include proxy.conf;  # 包含proxy.conf文件
  }

  location ~ ^/Bdata_Nginx_Status$ {
    stub_status on;  # 启用Nginx状态页面
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    allow 172.16.0.0/12;
    allow 192.168.0.0/16;
    deny all;  # 拒绝其他IP访问
  }

  location /Bdata_Check_Status {
    check_status;  # 启用Nginx健康检查
    allow 127.0.0.1;
    allow 10.0.0.0/8;
    allow 172.16.0.0/12;
    allow 192.168.0.0/16;
    deny all;  # 拒绝其他IP访问
  }

  access_log /var/log/nginx/access.log main;  # 访问日志路径和格式
}
```

#### upstream

`kubernetes-cluster-https.conf`：

```
upstream kubernetes-cluster-https {
  server 172.31.154.47:443 weight=5;  # 后端服务的地址和端口，设置权重为5
  check interval=10000 rise=3 fall=2 timeout=1500 type=tcp;  # 配置健康检查参数
  keepalive 16;  # 配置 keepalive 连接数
}
```

`kubernetes-cluster.conf`：

```
upstream kubernetes-cluster {
  server 172.31.154.47 weight=5;  # 后端服务的地址和端口，设置权重为5
  check interval=10000 rise=3 fall=2 timeout=1500 type=tcp;  # 配置健康检查参数
  keepalive 16;  # 配置 keepalive 连接数
}
```

这些配置定义了负载均衡的 upstream 组，其中 `kubernetes-cluster-https` 用于处理 HTTPS 流量，而 `kubernetes-cluster` 用于处理 HTTP 流量。每个 upstream 组只包含一个后端服务器（IP 地址为 172.31.154.47），并分配了权重为 5。此外，还配置了健康检查参数和 keepalive 连接数。



### Ingress服务

上面的“172.31.154.47” 为 Ingress的IP

```yml
[dev][root@kubernetes-master-192.168.83.13 ~]# kubectl get svc -n ingress-nginx 
NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx   NodePort   172.31.154.47   <none>        80:30274/TCP,443:30994/TCP   4y22d

```


```yml
[dev][root@kubernetes-master-192.168.83.13 ~]# kubectl get ingresses -n uat hire-admin
NAME         HOSTS                      ADDRESS         PORTS   AGE
hire-admin   hire-admin-uat.xxx.net   172.31.154.47   80      2y4d

[dev][root@kubernetes-master-192.168.83.13 ~]# kubectl get ingresses -n uat hire-admin -oyaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx  # 使用 nginx 作为 Ingress 控制器
  name: hire-admin
  namespace: uat
  selfLink: /apis/extensions/v1beta1/namespaces/uat/ingresses/hire-admin
spec:
  rules:
  - host: hire-admin-uat.xxx.net  # Ingress 规则中的主机名
    http:
      paths:
      - backend:
          serviceName: hire-admin  # 后端服务的名称
          servicePort: 8503  # 后端服务的端口
        path: /  # Ingress 路径
status:
  loadBalancer:
    ingress:
    - ip: 172.31.154.47  # 负载均衡器的 IP 地址
```

### 后端服务

```yml
[dev][root@kubernetes-master-192.168.83.13 ~]# kubectl get svc -n uat    hire-admin 
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
hire-admin   ClusterIP   172.31.183.155   <none>        8503/TCP   2y4d

[dev][root@kubernetes-master-192.168.83.13 ~]# kubectl get svc -n uat hire-admin -oyaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"app":"hire-admin"},"name":"hire-admin","namespace":"uat"},"spec":{"ports":[{"name":"http","port":8503,"protocol":"TCP","targetPort":8503}],"selector":{"app":"hire-admin"}}}
  creationTimestamp: "2022-03-30T02:37:57Z"
  labels:
    app: hire-admin
  name: hire-admin
  namespace: uat
  resourceVersion: "260185009"
  selfLink: /api/v1/namespaces/uat/services/hire-admin
  uid: dc559c3a-abfb-4f70-927d-75ac5227b433
spec:
  clusterIP: 172.31.183.155  # Service 的 ClusterIP
  ports:
  - name: http
    port: 8503
    protocol: TCP
    targetPort: 8503  # Service 指向的目标端口
  selector:
    app: hire-admin
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}  # 没有负载均衡器相关的状态信息

```

总结来说，通过深度整合Nginx与Kubernetes Ingress资源，我们可以实现高度定制化的流量路由和负载均衡策略，不仅保障了服务的安全性和高可用性，同时也极大地提升了内外网交互的灵活性与响应速度。
