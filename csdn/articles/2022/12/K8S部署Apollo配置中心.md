+++
author = "南宫乘风"
title = "K8S部署Apollo配置中心"
date = "2022-12-29 10:03:56"
tags=['kubernetes', 'java', '容器']
categories=[' Kubernetes项目实战', ' Kubernetes应用']
image = "post/4kdongman/22.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/128476559](https://blog.csdn.net/heian_99/article/details/128476559)

# <a id="K8SApollo_0"></a>K8S部署Apollo配置中心

参考文档: [https://github.com/apolloconfig/apollo/tree/v1.8.0](https://github.com/apolloconfig/apollo/tree/v1.8.0)

```
	[K8S部署apollo配置中心](https://www.cnblogs.com/Fengyinyong/p/14903725.html)

	[apollo官网文档](https://www.apolloconfig.com/#/zh/README)

```

# <a id="1_9"></a>1、错误问题记录

在k8s里面部署时也遇到了同样的一些问题，在此记录下：
<li> 提示`exec user process caused "no such file or directory"` 
  <ul>- 由于将Windows文件拷贝到CentOS里面导致的换行符不对，解决方案是在CentOS虚机内git clone 当前仓储
构建的docker镜像启动失败
- 同上一个问题，从Windows拷贝过去的文件权限不正确导致的shell脚本执行失败，解决方案同上或者chmod +x
一个环境的admin server由于健康检查不过导致不断重启
- 数据库帐号填错了导致无法登录数据库引发的问题
# <a id="2_23"></a>2、介绍

Apollo（阿波罗）是携程框架部门研发的分布式配置中心，能够集中化管理应用不同环境、不同集群的配置，配置修改后能够实时推送到应用端，并且具备规范的权限、流程治理等特性，适用于微服务配置管理场景。

服务端基于Spring Boot和Spring Cloud开发，打包后可以直接运行，不需要额外安装Tomcat等应用容器。

Java客户端不依赖任何框架，能够运行于所有Java运行时环境，同时对Spring/Spring Boot环境也有较好的支持。

.Net客户端不依赖任何框架，能够运行于所有.Net运行时环境。

‍

说明：最近在用K8S部署微服务，而微服务的配置文件众多，需要一个配置中心来处理配置文件。于是采用apollo来作为配置中心。本实例介绍了如何采用K8S部署高可用的apollo集群。

‍

# <a id="3_39"></a>3、环境配置

mysql5.7.39

注意：mysql的版本一定要大于5.7，不然导入数据库sql文件会报错的

因为实验方便，给root远程登录权限（切忌，生产环境，禁用root，单独数据库配置单独账号）

|数据库名称|IP|作用|远程账号|
|------
|DevApolloConfigDB|192.168.102.20|DEV环境的配置|root|
|ProdApolloConfigDB|192.168.102.20|PRO环境的配置|root|
|ApolloPortalDB|192.168.102.20|WEB界面管理|root|

‍

安装Apollo版本：1.8.0（注意：sql文件和jar版本一定要对应）

（目前官方给4套环境部署安装，我这边采用PRO和DEV环境）

已经构建成功的Kubernetes集群，

```
[root@bt nginx]# kubectl get node 
NAME       STATUS   ROLES                  AGE     VERSION
master01   Ready    control-plane,master   2d16h   v1.23.0
node01     Ready    &lt;none&gt;                 2d16h   v1.23.0
node02     Ready    &lt;none&gt;                 2d16h   v1.23.0


```

# <a id="4Apollo_70"></a>4、Apollo安装

‍

## <a id="1Apollo_74"></a>1、克隆Apollo代码

官方地址：[https://github.com/apolloconfig/apollo](https://github.com/apolloconfig/apollo)

在Centos上克隆（因为字符原因，所以要在Linux克隆，千万不要win上下载上传，容易出问题）

```
git clone https://github.com/apolloconfig/apollo.git

cd apollo 

#查看版本，
git tag
#切换分支
git checkout v1.8.0
#创建新的分支，切换
git checkout -b heian

```

![db0cf33946a24fe3bd720aaf2232fa31.png](https://img-blog.csdnimg.cn/db0cf33946a24fe3bd720aaf2232fa31.png)

## <a id="2Mysql_97"></a>2、初始化Mysql数据库

![a7854fd0cfbf45288a809c83a73a4d3b.png](https://img-blog.csdnimg.cn/a7854fd0cfbf45288a809c83a73a4d3b.png)

```
[root@bt db]# pwd
/opt/apollo/scripts/apollo-on-kubernetes/db
[root@bt db]# ls
config-db-dev  config-db-prod  config-db-test-alpha  config-db-test-beta  portal-db
[root@bt db]# tree .
.
├── config-db-dev
│?? └── apolloconfigdb.sql
├── config-db-prod
│?? └── apolloconfigdb.sql
├── config-db-test-alpha
│?? └── apolloconfigdb.sql
├── config-db-test-beta
│?? └── apolloconfigdb.sql
└── portal-db
    └── apolloportaldb.sql

大胆执行，数据库名称官方定义过，不会冲突
执行dev环境
 cd config-db-dev/
[root@bt config-db-dev]# mysql -uroot -p &lt; apolloconfigdb.sql 
Enter password: 
执行pro环境
 cd config-db-pro/
[root@bt config-db-dev]# mysql -uroot -p &lt; apolloconfigdb.sql 
Enter password: 

执行portal环境
cd portal-db/
[root@bt config-db-dev]# mysql -uroot -p &lt; apolloportaldb.sql

```

![afb450cb2a2b41b7935e39940a6fb02d.png](https://img-blog.csdnimg.cn/afb450cb2a2b41b7935e39940a6fb02d.png)

![b4bee421610d442c90f4c8644074ebc9.png](https://img-blog.csdnimg.cn/b4bee421610d442c90f4c8644074ebc9.png)

## <a id="3jar_141"></a>3、下载jar版本

‍

官方下载地址：[https://github.com/apolloconfig/apollo/releases/tag/v1.8.0](https://github.com/apolloconfig/apollo/releases/tag/v1.8.0)

```
cd /opt/apollo
wget https://github.com/apolloconfig/apollo/releases/download/v1.8.0/apollo-adminservice-1.8.0-github.zip
wget https://github.com/apolloconfig/apollo/releases/download/v1.8.0/apollo-configservice-1.8.0-github.zip
wget https://github.com/apolloconfig/apollo/releases/download/v1.8.0/apollo-portal-1.8.0-github.zip

```

进行解压，需要其中的jar

```
​    解压 apollo-portal-1.8.0-github.zip
​  获取 apollo-portal-1.8.0.jar, 重命名为 apollo-portal.jar, 放到 scripts/apollo-on-kubernetes/apollo-portal-server

​    解压 apollo-adminservice-1.8.0-github.zip
​  获取 apollo-adminservice-1.8.0.jar, 重命名为 apollo-adminservice.jar, 放到 scripts/apollo-on-kubernetes/apollo-admin-server

​    解压 apollo-configservice-1.8.0-github.zip
​  获取 apollo-configservice-1.8.0.jar, 重命名为 apollo-configservice.jar, 放到 scripts/apollo-on-kubernetes/apollo-config-se

```

![8a27e0fc834249a8bde1469e640aa817.png](https://img-blog.csdnimg.cn/8a27e0fc834249a8bde1469e640aa817.png)

## <a id="4Docker_170"></a>4、构建Docker镜像

1、采用K8S部署apollo时，需要用到多个镜像。这些镜像，需要自己构建

2、如果麻烦，可以去官方镜像 [https://hub.docker.com/u/apolloconfig](https://hub.docker.com/u/apolloconfig)

![489f24d76ab849ecb4bb0d6ef400c82d.png](https://img-blog.csdnimg.cn/489f24d76ab849ecb4bb0d6ef400c82d.png)

```
docker pull apolloconfig/apollo-configservice:1.8.0
docker pull apolloconfig/apollo-adminservice:1.8.0
docker pull apolloconfig/apollo-portal:1.8.0
还需要一个alpine-bash-3.8 做初始化镜像操作
docker pull zgadocker/alpine-bash-3.8-image:latest
测试这个不行，就按照下方自己打包

```

![f87d5505250648d3b0af893ace8b8f75.png](https://img-blog.csdnimg.cn/f87d5505250648d3b0af893ace8b8f75.png)

### <a id="alpinebash38image_190"></a>alpine-bash-3.8-image

```
[root@bt apollo-on-kubernetes]# cd alpine-bash-3.8-image
[root@bt alpine-bash-3.8-image]# docker build -t harbor.ownit.top/ownit/alpine-bash:3.8 .
[root@bt alpine-bash-3.8-image]# docker push harbor.ownit.top/ownit/alpine-bash:3.8


```

### <a id="apolloconfigserver_199"></a>apollo-config-server

```
[root@bt apollo-on-kubernetes]# cd apollo-config-server
[root@bt apollo-config-server]# docker build -t harbor.ownit.top/ownit/apollo-configservice:1.8.0 .
[root@bt apollo-config-server]# docker push harbor.ownit.top/ownit/apollo-configservice:1.8.0


```

### <a id="apolloadminserver_208"></a>apollo-admin-server

```
[root@bt apollo-on-kubernetes]# cd apollo-admin-server
[root@bt apollo-admin-server]# docker build -t harbor.ownit.top/ownit/apollo-adminservice:1.8.0 .
[root@bt apollo-admin-server]# docker  push harbor.ownit.top/ownit/apollo-adminservice:1.8.0

```

### <a id="apolloportalserver_216"></a>apollo-portal-server

```
[root@bt apollo-on-kubernetes]# cd apollo-portal-server
[root@bt apollo-portal-server]# docker build -t harbor.ownit.top/ownit/apollo-portal:1.8.0 .
[root@bt apollo-portal-server]# docker push harbor.ownit.top/ownit/apollo-portal:1.8.0

```

### <a id="_224"></a>验证

![08e3a4dd12f6435ab5851269ad5301fc.png](https://img-blog.csdnimg.cn/08e3a4dd12f6435ab5851269ad5301fc.png)

## <a id="5Yaml_229"></a>5、配置Yaml文件

![c54d4807c598421380a91f2c54a3fd5c.png](https://img-blog.csdnimg.cn/c54d4807c598421380a91f2c54a3fd5c.png)

<th align="center">环境</th><th align="center">文件名称</th><th align="center">执行顺序</th>
|------
<td align="center">dev</td><td align="center">service-apollo-config-server-dev.yaml</td><td align="center">1</td>
<td align="center">dev</td><td align="center">service-apollo-admin-server-dev.yaml</td><td align="center">2</td>
<td align="center">pro</td><td align="center">service-apollo-config-server-prod.yaml</td><td align="center">3</td>
<td align="center">pro</td><td align="center">service-apollo-admin-server-prod.yaml</td><td align="center">4</td>
<td align="center">portal</td><td align="center">service-apollo-portal-server.yaml</td><td align="center">5</td>

### <a id="1serviceapolloconfigserverdevyaml_242"></a>1、service-apollo-config-server-dev.yaml

```
---
# configmap for apollo-config-server-dev
kind: ConfigMap
apiVersion: v1
metadata:
  namespace: sre
  name: configmap-apollo-config-server-dev
data:
  application-github.properties: |
    spring.datasource.url = jdbc:mysql://192.168.102.20:3306/DevApolloConfigDB?characterEncoding=utf8&amp;serverTimezone=Asia/Shanghai
    spring.datasource.username = root
    spring.datasource.password = 123456
    eureka.service.url = http://statefulset-apollo-config-server-dev-0.service-apollo-meta-server-dev:8080/eureka/,http://statefulset-apollo-config-server-dev-1.service-apollo-meta-server-dev:8080/eureka/,http://statefulset-apollo-config-server-dev-2.service-apollo-meta-server-dev:8080/eureka/

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-meta-server-dev
  labels:
    app: service-apollo-meta-server-dev
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  selector:
    app: pod-apollo-config-server-dev
  type: ClusterIP
  clusterIP: None
  sessionAffinity: ClientIP

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-config-server-dev
  labels:
    app: service-apollo-config-server-dev
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30002
  selector:
    app: pod-apollo-config-server-dev 
  type: NodePort
  sessionAffinity: ClientIP

---
kind: StatefulSet
apiVersion: apps/v1
metadata:
  namespace: sre
  name: statefulset-apollo-config-server-dev
  labels:
    app: statefulset-apollo-config-server-dev
spec:
  serviceName: service-apollo-meta-server-dev
  replicas: 1
  selector:
    matchLabels:
      app: pod-apollo-config-server-dev
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: pod-apollo-config-server-dev
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - pod-apollo-config-server-dev
              topologyKey: kubernetes.io/hostname

      volumes:
        - name: volume-configmap-apollo-config-server-dev
          configMap:
            name: configmap-apollo-config-server-dev
            items:
              - key: application-github.properties
                path: application-github.properties
    
      containers:
        - image: harbor.ownit.top/ownit/apollo-configservice:1.8.0
          securityContext:
            privileged: true
          imagePullPolicy: IfNotPresent
          name: container-apollo-config-server-dev
          ports:
            - protocol: TCP
              containerPort: 8080
        
          volumeMounts:
            - name: volume-configmap-apollo-config-server-dev
              mountPath: /apollo-config-server/config/application-github.properties
              subPath: application-github.properties
        
          env:
            - name: APOLLO_CONFIG_SERVICE_NAME
              value: "service-apollo-config-server-dev.sre"
        
          readinessProbe:
            tcpSocket:
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
        
          livenessProbe:
            tcpSocket:
              port: 8080
            initialDelaySeconds:  120
            periodSeconds: 10
        
      dnsPolicy: ClusterFirst
      restartPolicy: Always

```

### <a id="2serviceapolloadminserverdevyaml_374"></a>2、service-apollo-admin-server-dev.yaml

```
---
# configmap for apollo-admin-server-dev
kind: ConfigMap
apiVersion: v1
metadata:
  namespace: sre
  name: configmap-apollo-admin-server-dev
data:
  application-github.properties: |
    spring.datasource.url = jdbc:mysql://192.168.102.20:3306/DevApolloConfigDB?characterEncoding=utf8&amp;serverTimezone=Asia/Shanghai
    spring.datasource.username = root
    spring.datasource.password = 123456
    eureka.service.url = http://statefulset-apollo-config-server-dev-0.service-apollo-meta-server-dev:8080/eureka/,http://statefulset-apollo-config-server-dev-1.service-apollo-meta-server-dev:8080/eureka/,http://statefulset-apollo-config-server-dev-2.service-apollo-meta-server-dev:8080/eureka/

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-admin-server-dev
  labels:
    app: service-apollo-admin-server-dev
spec:
  ports:
    - protocol: TCP
      port: 8090
      targetPort: 8090
  selector:
    app: pod-apollo-admin-server-dev
  type: ClusterIP
  sessionAffinity: ClientIP

---
kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: sre
  name: deployment-apollo-admin-server-dev
  labels:
    app: deployment-apollo-admin-server-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-apollo-admin-server-dev
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: pod-apollo-admin-server-dev
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - pod-apollo-admin-server-dev
              topologyKey: kubernetes.io/hostname
    
      volumes:
        - name: volume-configmap-apollo-admin-server-dev
          configMap:
            name: configmap-apollo-admin-server-dev
            items:
              - key: application-github.properties
                path: application-github.properties
    
      initContainers:
        - image: harbor.ownit.top/ownit/alpine-bash:3.8
          name: check-service-apollo-config-server-dev
          command: ['bash', '-c', "curl --connect-timeout 2 --max-time 5 --retry 60 --retry-delay 1 --retry-max-time 120 service-apollo-config-server-dev.sre:8080"]
    
      containers:
        - image: harbor.ownit.top/ownit/apollo-adminservice:1.8.0
          securityContext:
            privileged: true
          imagePullPolicy: IfNotPresent
          name: container-apollo-admin-server-dev
          ports:
            - protocol: TCP
              containerPort: 8090
        
          volumeMounts:
            - name: volume-configmap-apollo-admin-server-dev
              mountPath: /apollo-admin-server/config/application-github.properties
              subPath: application-github.properties
        
          env:
            - name: APOLLO_ADMIN_SERVICE_NAME
              value: "service-apollo-admin-server-dev.sre"
        
          readinessProbe:
            tcpSocket:
              port: 8090
            initialDelaySeconds: 10
            periodSeconds: 5
        
          livenessProbe:
            tcpSocket:
              port: 8090
            initialDelaySeconds: 120
            periodSeconds: 10
        
      dnsPolicy: ClusterFirst
      restartPolicy: Always


```

### <a id="3serviceapolloconfigserverprodyaml_494"></a>3、service-apollo-config-server-prod.yaml

```

---
# configmap for apollo-config-server-prod
kind: ConfigMap
apiVersion: v1
metadata:
  namespace: sre
  name: configmap-apollo-config-server-prod
data:
  application-github.properties: |
    spring.datasource.url = jdbc:mysql://192.168.102.20:3306/ProdApolloConfigDB?characterEncoding=utf8&amp;serverTimezone=Asia/Shanghai
    spring.datasource.username = root
    spring.datasource.password = 123456
    eureka.service.url = http://statefulset-apollo-config-server-prod-0.service-apollo-meta-server-prod:8080/eureka/,http://statefulset-apollo-config-server-prod-1.service-apollo-meta-server-prod:8080/eureka/,http://statefulset-apollo-config-server-prod-2.service-apollo-meta-server-prod:8080/eureka/

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-meta-server-prod
  labels:
    app: service-apollo-meta-server-prod
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  selector:
    app: pod-apollo-config-server-prod
  type: ClusterIP
  clusterIP: None
  sessionAffinity: ClientIP

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-config-server-prod
  labels:
    app: service-apollo-config-server-prod
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30005
  selector:
    app: pod-apollo-config-server-prod
  type: NodePort
  sessionAffinity: ClientIP

---
kind: StatefulSet
apiVersion: apps/v1
metadata:
  namespace: sre
  name: statefulset-apollo-config-server-prod
  labels:
    app: statefulset-apollo-config-server-prod
spec:
  serviceName: service-apollo-meta-server-prod
  replicas: 1
  selector:
    matchLabels:
      app: pod-apollo-config-server-prod
  updateStrategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: pod-apollo-config-server-prod
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - pod-apollo-config-server-prod
              topologyKey: kubernetes.io/hostname
    
      volumes:
        - name: volume-configmap-apollo-config-server-prod
          configMap:
            name: configmap-apollo-config-server-prod
            items:
              - key: application-github.properties
                path: application-github.properties
    
      containers:
        - image: harbor.ownit.top/ownit/apollo-configservice:1.8.0
          securityContext:
            privileged: true
          imagePullPolicy: Always
          name: container-apollo-config-server-prod
          ports:
            - protocol: TCP
              containerPort: 8080

          volumeMounts:
            - name: volume-configmap-apollo-config-server-prod
              mountPath: /apollo-config-server/config/application-github.properties
              subPath: application-github.properties
          env:
            - name: APOLLO_CONFIG_SERVICE_NAME
              value: "service-apollo-config-server-prod.sre"
        
          readinessProbe:
            tcpSocket:
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
        
          livenessProbe:
            tcpSocket:
              port: 8080
            initialDelaySeconds: 120
            periodSeconds: 10
        
      dnsPolicy: ClusterFirst
      restartPolicy: Always


```

### <a id="3serviceapolloadminserverprodyaml_627"></a>3、service-apollo-admin-server-prod.yaml

```
---
# configmap for apollo-admin-server-prod
kind: ConfigMap
apiVersion: v1
metadata:
  namespace: sre
  name: configmap-apollo-admin-server-prod
data:
  application-github.properties: |
    spring.datasource.url = jdbc:mysql://192.168.102.20:3306/ProdApolloConfigDB?characterEncoding=utf8&amp;serverTimezone=Asia/Shanghai
    spring.datasource.username = root
    spring.datasource.password = 123456
    eureka.service.url = http://statefulset-apollo-config-server-prod-0.service-apollo-meta-server-prod:8080/eureka/,http://statefulset-apollo-config-server-prod-1.service-apollo-meta-server-prod:8080/eureka/,http://statefulset-apollo-config-server-prod-2.service-apollo-meta-server-prod:8080/eureka/

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-admin-server-prod
  labels:
    app: service-apollo-admin-server-prod
spec:
  ports:
    - protocol: TCP
      port: 8090
      targetPort: 8090
  selector:
    app: pod-apollo-admin-server-prod  
  type: ClusterIP
  sessionAffinity: ClientIP

---
kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: sre
  name: deployment-apollo-admin-server-prod
  labels:
    app: deployment-apollo-admin-server-prod
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-apollo-admin-server-prod
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: pod-apollo-admin-server-prod
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - pod-apollo-admin-server-prod
              topologyKey: kubernetes.io/hostname
    
      volumes:
        - name: volume-configmap-apollo-admin-server-prod
          configMap:
            name: configmap-apollo-admin-server-prod
            items:
              - key: application-github.properties
                path: application-github.properties
    
      initContainers:
        - image: harbor.ownit.top/ownit/alpine-bash:3.8
          name: check-service-apollo-config-server-prod
          command: ['bash', '-c', "curl --connect-timeout 2 --max-time 5 --retry 50 --retry-delay 1 --retry-max-time 120 service-apollo-config-server-prod.sre:8080"]
    
      containers:
        - image: harbor.ownit.top/ownit/apollo-adminservice:1.8.0
          securityContext:
            privileged: true
          imagePullPolicy: IfNotPresent
          name: container-apollo-admin-server-prod
          ports:
            - protocol: TCP
              containerPort: 8090
        
          volumeMounts:
            - name: volume-configmap-apollo-admin-server-prod
              mountPath: /apollo-admin-server/config/application-github.properties
              subPath: application-github.properties
        
          env:
            - name: APOLLO_ADMIN_SERVICE_NAME
              value: "service-apollo-admin-server-prod.sre"
        
          readinessProbe:
            tcpSocket:
              port: 8090
            initialDelaySeconds: 10
            periodSeconds: 5
        
          livenessProbe:
            tcpSocket:
              port: 8090
            initialDelaySeconds: 120
            periodSeconds: 10

      dnsPolicy: ClusterFirst
      restartPolicy: Always


```

### <a id="5serviceapolloportalserveryaml_747"></a>5、service-apollo-portal-server.yaml

```
---
# 为外部 mysql 服务设置 service
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-mysql-for-portal-server
  labels:
    app: service-mysql-for-portal-server
spec:
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
  type: ClusterIP
  sessionAffinity: None
---
kind: Endpoints
apiVersion: v1
metadata:
  namespace: sre
  name: service-mysql-for-portal-server
subsets:
  - addresses:
      # 更改为你的 mysql addresses, 例如 1.1.1.1
      - ip: 192.168.102.20
    ports:
      - protocol: TCP
        port: 3306

---
# configmap for apollo-portal-server
kind: ConfigMap
apiVersion: v1
metadata:
  namespace: sre
  name: configmap-apollo-portal-server
data:
  application-github.properties: |
    spring.datasource.url = jdbc:mysql://192.168.102.20:3306/ApolloPortalDB?characterEncoding=utf8
    # mysql username
    spring.datasource.username = root
    # mysql password
    spring.datasource.password = 123456
  apollo-env.properties: |
    dev.meta=http://service-apollo-config-server-dev.sre:8080
    fat.meta=http://service-apollo-config-server-test-alpha.sre:8080
    uat.meta=http://service-apollo-config-server-test-beta.sre:8080
    pro.meta=http://service-apollo-config-server-prod.sre:8080

---
kind: Service
apiVersion: v1
metadata:
  namespace: sre
  name: service-apollo-portal-server
  labels:
    app: service-apollo-portal-server
spec:
  ports:
    - protocol: TCP
      port: 8070
      targetPort: 8070
      nodePort: 30001
  selector:
    app: pod-apollo-portal-server
  type: NodePort
  # portal session 保持
  sessionAffinity: ClientIP

---
kind: Deployment
apiVersion: apps/v1
metadata:
  namespace: sre
  name: deployment-apollo-portal-server
  labels:
    app: deployment-apollo-portal-server
spec:
  # 3 个实例
  replicas: 1
  selector:
    matchLabels:
      app: pod-apollo-portal-server
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: pod-apollo-portal-server
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - pod-apollo-portal-server
              topologyKey: kubernetes.io/hostname
    
      volumes:
        - name: volume-configmap-apollo-portal-server
          configMap:
            name: configmap-apollo-portal-server
            items:
              - key: application-github.properties
                path: application-github.properties
              - key: apollo-env.properties
                path: apollo-env.properties
    
      initContainers:
        # 确保 admin-service 正常提供服务
        - image: harbor.ownit.top/ownit/alpine-bash:3.8
          name: check-service-apollo-admin-server-dev
          command: ['bash', '-c', "curl --connect-timeout 2 --max-time 5 --retry 60 --retry-delay 1 --retry-max-time 120 service-apollo-admin-server-dev.sre:8090"]
        # - image: harbor.ownit.top/ownit/alpine-bash:3.8
        #   name: check-service-apollo-admin-server-alpha
        #   command: ['bash', '-c', "curl --connect-timeout 2 --max-time 5 --retry 60 --retry-delay 1 --retry-max-time 120 service-apollo-admin-server-test-alpha.sre:8090"]
        # - image: harbor.ownit.top/ownit/alpine-bash:3.8
        #   name: check-service-apollo-admin-server-beta
        #   command: ['bash', '-c', "curl --connect-timeout 2 --max-time 5 --retry 60 --retry-delay 1 --retry-max-time 120 service-apollo-admin-server-test-beta.sre:8090"]
        - image: harbor.ownit.top/ownit/alpine-bash:3.8
          name: check-service-apollo-admin-server-prod
          command: ['bash', '-c', "curl --connect-timeout 2 --max-time 5 --retry 60 --retry-delay 1 --retry-max-time 120 service-apollo-admin-server-prod.sre:8090"]  
    
      containers:
        - image: harbor.ownit.top/ownit/apollo-portal:1.8.0    # 更改为你的 docker registry 下的 image
          securityContext:
            privileged: true
          imagePullPolicy: IfNotPresent
          name: container-apollo-portal-server
          ports:
            - protocol: TCP
              containerPort: 8070
        
          volumeMounts:
            - name: volume-configmap-apollo-portal-server
              mountPath: /apollo-portal-server/config/application-github.properties
              subPath: application-github.properties
            - name: volume-configmap-apollo-portal-server
              mountPath: /apollo-portal-server/config/apollo-env.properties
              subPath: apollo-env.properties
        
          env:
            - name: APOLLO_PORTAL_SERVICE_NAME
              value: "service-apollo-portal-server.sre"
        
          readinessProbe:
            tcpSocket:
              port: 8070
            initialDelaySeconds: 10
            periodSeconds: 5
        
          livenessProbe:
            tcpSocket:
              port: 8070
            # 120s 内, server 未启动则重启 container
            initialDelaySeconds: 120
            periodSeconds: 15
        
      dnsPolicy: ClusterFirst
      restartPolicy: Always


```

## <a id="6Yaml_922"></a>6、执行Yaml文件

```
# create namespace
kubectl create namespace sre

dev环境
kubectl apply -f apollo-env-dev/service-apollo-config-server-dev.yaml --record 
kubectl apply -f apollo-env-dev/service-apollo-admin-server-dev.yaml --record

pro环境
kubectl apply -f apollo-env-prod/service-apollo-config-server-prod.yaml --record
kubectl apply -f apollo-env-prod/service-apollo-admin-server-prod.yaml --record


```

![3b91b8bad82840bca7746f93b7560635.png](https://img-blog.csdnimg.cn/3b91b8bad82840bca7746f93b7560635.png)

## <a id="7ingress_941"></a>7、配置ingress域名

### <a id="apolloingressyaml_943"></a>apollo-ingress.yaml

```
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: sre
  name: service-apollo-portal-server
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/proxy-body-size: "0"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
    kubernetes.io/tls-acme: "true"
    cert-manager.io/cluster-issuer: "example-issuer"
  labels:
    app: service-apollo-portal-server
spec:
  rules:
  - host: apollo.ownit.top
    http:
      paths:
      - pathType: Prefix
        path: /
        backend:
          service:
            name: service-apollo-portal-server
            port:
              number: 8070


```

![74b3337b9f214fe4b43f44fff2f95a93.png](https://img-blog.csdnimg.cn/74b3337b9f214fe4b43f44fff2f95a93.png)

## <a id="8nginx_979"></a>8、配置nginx代理

‍

**nginx配置**

apollo.ownit.top.conf

```
server {<!-- -->
        listen       80;
        server_name  apollo.ownit.top;
        rewrite ^/(.*)$ https://$host/$1 permanent;
        # IP白名单
        include /opt/nginx/whitelist/corporation.conf;
}
server {<!-- -->
        listen       443 ssl;
        server_name  apollo.ownit.top;
        # IP白名单
        include /opt/nginx/whitelist/corporation.conf;

        #ssl                   on;
        ssl_certificate      /opt/nginx/ssl/ownit.top.crt;
        ssl_certificate_key  /opt/nginx/ssl/ownit.top.key;
        include ssl.conf;

        location / {<!-- -->
            proxy_pass  http://kubernetes-cluster; #转发到k8s的ingress 80端口
            include https_proxy.conf;
        }
	access_log  /www/wwwlogs/apollo.ownit.top.log;
    error_log  /www/wwwlogs/apollo.ownit.top.error.log;

}

[root@bt nginx]# nginx  -t 
nginx: the configuration file /www/server/nginx/conf/nginx.conf syntax is ok
nginx: configuration file /www/server/nginx/conf/nginx.conf test is successful
[root@bt nginx]# nginx  -s reload


```

kubernetes-cluster.conf 转发

```
[root@bt nginx]# cat kubernetes-cluster.conf 
upstream kubernetes-cluster {<!-- -->
  server 192.168.102.40 weight=5;
  keepalive 16;
}



```

## <a id="9powerdns_1034"></a>9、配置powerdns域名解析

![4360b880e5334c80a2e016d14a2b0d33.png](https://img-blog.csdnimg.cn/4360b880e5334c80a2e016d14a2b0d33.png)<br> ![75c5a99e00444560bbac611c38882605.png](https://img-blog.csdnimg.cn/75c5a99e00444560bbac611c38882605.png)

## <a id="10_1040"></a>10、测试验证

[https://apollo.ownit.top/](https://apollo.ownit.top/)

默认账号/密码：apollo / admin

如果没有ingress，则可使用nodeport访问

k8s节点ip+30001 端口即可访问

http://k8s节点ip:30001/

![2e6401ddc080459fb6dafc388e44286e.png](https://img-blog.csdnimg.cn/2e6401ddc080459fb6dafc388e44286e.png)<br> ![b9518b59dbcf4b4689daf8eb67414ca6.png](https://img-blog.csdnimg.cn/b9518b59dbcf4b4689daf8eb67414ca6.png)

# <a id="5Apollo_1056"></a>5、Apollo配置使用

## <a id="1_1058"></a>1、添加超级管理员用户

1、管理员用户选择 管理员工具-&gt;系统参数

![63109a990fd64c7a8b478c14525476cf.png](https://img-blog.csdnimg.cn/63109a990fd64c7a8b478c14525476cf.png)

2、填入系统内置Key：superAdmin 并点击查询，在value部分添加要加入人的用户id(LDAP用户ID为准，可通过wiki后台用户列表查询)后保存即可

![19b4d160b5df441b9bfff9d2f21590d4.png](https://img-blog.csdnimg.cn/19b4d160b5df441b9bfff9d2f21590d4.png)

## <a id="2organizations_1070"></a>2、新增部门：organizations

```
[{<!-- -->"orgId":"kaifa","orgName":"开发部门"},{<!-- -->"orgId":"yunwei","orgName":"运维部门"},{<!-- -->"orgId":"ceshi","orgName":"测试部门"}]

```

![9f4ffe7ee5b54ba2ad108103a53e0c3b.png](https://img-blog.csdnimg.cn/9f4ffe7ee5b54ba2ad108103a53e0c3b.png)

## <a id="3apolloportalenvs_1079"></a>3、新增环境：apollo.portal.envs

apollo.portal.envs

![327f30d1f9744b389345b4c48a268ca8.png](https://img-blog.csdnimg.cn/327f30d1f9744b389345b4c48a268ca8.png)

# <a id="6namespace_1086"></a>6、namespace管理

## <a id="namespace_1088"></a>私有namespace

### <a id="1namespace_1090"></a>1、添加namespace

Namespace作为配置的分类，可当成一个配置文件。<br> 以添加rocketmq配置为例，添加"spring-rocketmq”Namespace配置rocketmq相关信息。

1、添加项目私有Namespace:spring-rocketmq<br> 进入项目首页，点击左下脚的”添加Namespace”，共包括两项:关联公共Namespace和创建Namespace ,这里选择"创建Namespace"

![c1c941a045644dd19b75eb714cac38c9.png](https://img-blog.csdnimg.cn/c1c941a045644dd19b75eb714cac38c9.png)<br> ![3f3b4f68a5b94c2786af826669d0ded7.png](https://img-blog.csdnimg.cn/3f3b4f68a5b94c2786af826669d0ded7.png)

2、填写详细的信息<br> 有两种选择，一种是public（所有项目的）；另一种是private（当前项目的）；如下图所示

![f3eb565acb1b4a23b52b344c5bec50af.png](https://img-blog.csdnimg.cn/f3eb565acb1b4a23b52b344c5bec50af.png)

![bc8c60acd7a34147a64323a90c1dc965.png](https://img-blog.csdnimg.cn/bc8c60acd7a34147a64323a90c1dc965.png)

3、提交过后会自动跳转到下面的页面（操控权限）

![199acd3da7a54578ab0f4c953ecad57b.png](https://img-blog.csdnimg.cn/199acd3da7a54578ab0f4c953ecad57b.png)

4、不操作返回首页

![f5530ee353304a67830aff1f264a519d.png](https://img-blog.csdnimg.cn/f5530ee353304a67830aff1f264a519d.png)

![1d278a07c0ca40c488c39db843a56779.png](https://img-blog.csdnimg.cn/1d278a07c0ca40c488c39db843a56779.png)

### <a id="2namespace_1123"></a>2、为namespace操作配置

可以按之前的方法进行操作，也可以通过下面的内容进行批量操作<br> 如：

```
rocketmq.name-server = 127.0.0.0:9876
rocketmq.producer.group = PID_ACCOUNT

```

![62b86eaf5a3b4a7ea2cd279f9841e291.png](https://img-blog.csdnimg.cn/62b86eaf5a3b4a7ea2cd279f9841e291.png)

![8ef0277ab38c47ac896e21daf63ec65c.png](https://img-blog.csdnimg.cn/8ef0277ab38c47ac896e21daf63ec65c.png)

![9363de39a2b0469bb32f8f34fd8c3474.png](https://img-blog.csdnimg.cn/9363de39a2b0469bb32f8f34fd8c3474.png)

发布

![7631b463f3d34ac18555c208fa772135.png](https://img-blog.csdnimg.cn/7631b463f3d34ac18555c208fa772135.png)

![ea7d42602238411db453dcfcd5ebe38d.png](https://img-blog.csdnimg.cn/ea7d42602238411db453dcfcd5ebe38d.png)

‍

### <a id="3namespace_1152"></a>3、获取namespace里面的数据

修改代码

```
	public class GetConfigTest {<!-- -->
	    public static void main(String[] args) {<!-- -->
	        while (true){<!-- -->
	            try {<!-- -->
	                Thread.sleep(1000);
	            } catch (InterruptedException e) {<!-- -->
	                e.printStackTrace();
	            }

	//            Config appConfig = ConfigService.getAppConfig();
	            //读取指定的namespace下的配置信息
	            Config config = ConfigService.getConfig("spring-rocketmq");
	            //获取配置信息,第一个参数:配置的key，第二个参数:默认值
	            String value = config.getProperty("rocketmq.producer.group", null);
	            System.out.printf("现在：%s, sms.enable: %s%n", new Date().toString(),value);
	        }


	    }
	}


```

`运行结果`

![92d1e2cf8a9a49b2ae5e7cb65d4a8868.png](https://img-blog.csdnimg.cn/92d1e2cf8a9a49b2ae5e7cb65d4a8868.png)

## <a id="_1185"></a>公共配置

### <a id="1namespace_1187"></a>1、添加公共的namespace

在项目开发中，有一些配置可能是通用的，我们可以通过把这些通用的配置放到公共的Namespace中，这样其他项目要使用时可以直接添加需要的Namespace
1. 新建common-template项目
![c414b459a52c4213ba824ea51479b778.png](https://img-blog.csdnimg.cn/c414b459a52c4213ba824ea51479b778.png)

2、新建namespace<br> ![0d25ef27236e47df8e987a4aaf6fc918.png](https://img-blog.csdnimg.cn/0d25ef27236e47df8e987a4aaf6fc918.png)<br> ![01b82a2e27dc4e71b1813668f7e049fa.png](https://img-blog.csdnimg.cn/01b82a2e27dc4e71b1813668f7e049fa.png)<br> ![392797789979465c96a7f9d151a73781.png](https://img-blog.csdnimg.cn/392797789979465c96a7f9d151a73781.png)

3、添加配置信息

![1dbbb45a5c8245fba748fe4e0e82e66b.png](https://img-blog.csdnimg.cn/1dbbb45a5c8245fba748fe4e0e82e66b.png)

![97f1a177d80141cab9f659122327e4a2.png](https://img-blog.csdnimg.cn/97f1a177d80141cab9f659122327e4a2.png)

### <a id="2namespace_1211"></a>2、前往其他的项目去关联第一步的namespace

![7b0693633ce040338d2ea5c9b9b15bfb.png](https://img-blog.csdnimg.cn/7b0693633ce040338d2ea5c9b9b15bfb.png)

![5130e0ba0c874d08baffdb32f0893efb.png](https://img-blog.csdnimg.cn/5130e0ba0c874d08baffdb32f0893efb.png)

![afdced2545ef43caae9736c815d372fd.png](https://img-blog.csdnimg.cn/afdced2545ef43caae9736c815d372fd.png)

‍

### <a id="3_1224"></a>3、修改公共配置

修改server.servlet.context-path为：/account-service

![2971ffe5cdb24f5baf060075737c7e17.png](https://img-blog.csdnimg.cn/2971ffe5cdb24f5baf060075737c7e17.png)

![d3460ef4a2374ecea7869c782ac0d728.png](https://img-blog.csdnimg.cn/d3460ef4a2374ecea7869c782ac0d728.png)

![c09ef783b0cd4e43b8e1ec91dcf21617.png](https://img-blog.csdnimg.cn/c09ef783b0cd4e43b8e1ec91dcf21617.png)

![68356852a1a74b599365b681824a21de.png](https://img-blog.csdnimg.cn/68356852a1a74b599365b681824a21de.png)

### <a id="4_1240"></a>4、使用代码读取配置信息

`注意：如果项目不一样的话，就需要去将之前在运行里面的环境进行修改，如下`

![8e306e85dd304afe83b5eb8d3664e313.png](https://img-blog.csdnimg.cn/8e306e85dd304afe83b5eb8d3664e313.png)

修改代码：

```
public class GetConfigTest {<!-- -->
    public static void main(String[] args) {<!-- -->
        while (true){<!-- -->
            try {<!-- -->
                Thread.sleep(1000);
            } catch (InterruptedException e) {<!-- -->
                e.printStackTrace();
            }

//            Config appConfig = ConfigService.getAppConfig();
            //读取指定的namespace下的配置信息
            Config config = ConfigService.getConfig("TEST1.spring-boot-http");
            //获取配置信息,第一个参数:配置的key，第二个参数:默认值
            String value = config.getProperty("server.servlet.context-path", null);
            System.out.printf("现在：%s, sms.enable: %s%n", new Date().toString(),value);
        }


    }
}


```

![f8e74ab91e944df6a5be00ffa1655c5a.png](https://img-blog.csdnimg.cn/f8e74ab91e944df6a5be00ffa1655c5a.png)
