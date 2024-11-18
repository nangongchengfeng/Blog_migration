---
author: 南宫乘风
categories:
- Jenkins
date: 2022-05-26 18:26:46
description: 前文安装部署使用南宫乘风的博客博客安装部署使用南宫乘风的博客博客入门配置南宫乘风的博客博客入门配置南宫乘风的博客博客集成南宫乘风的博客博客集成南宫乘风的博客博客的流水线的流水线流水线整合钉钉南宫乘风的。。。。。。。
image: ../../title_pic/70.jpg
slug: '202205261826'
tags:
- kubernetes
- jenkins
- 容器
title: Jenkins集成Kubernetes集群
---

<!--more-->

![](../../image/format,png.jpg)

# 前文

[Jenkins安装部署使用\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858 "Jenkins安装部署使用_南宫乘风的博客-CSDN博客")

[Jenkins入门配置\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124809338 "Jenkins入门配置_南宫乘风的博客-CSDN博客")

[Jenkins集成Sonar Qube\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124814780 "Jenkins集成Sonar Qube_南宫乘风的博客-CSDN博客")

[Jenkins的流水线（Pipeline）](https://blog.csdn.net/heian_99/article/details/124815450 "Jenkins的流水线（Pipeline）")

[Jenkins流水线整合钉钉\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124816190?spm=1001.2014.3001.5501 "Jenkins流水线整合钉钉_南宫乘风的博客-CSDN博客")[Kubernetes安装Jenkins\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124985786?spm=1001.2014.3001.5501 "Kubernetes安装Jenkins_南宫乘风的博客-CSDN博客")

**目录**

[1、Kubernetes 环境安装 Jenkins](<#1、Kubernetes 环境安装 Jenkins>)

[2、Jenkins 安装插件](<#2、Jenkins 安装插件>)

[3、云配置](#3%E3%80%81%E4%BA%91%E9%85%8D%E7%BD%AE)

[4、Template 模板配置](<#4、Template 模板配置>)

[5、Jenkins-slave 启动测试](<#5、Jenkins-slave 启动测试>)

[6、实战环境](#6%E3%80%81%E5%AE%9E%E6%88%98%E7%8E%AF%E5%A2%83)

[7、运行结果](#7%E3%80%81%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C)

---

## 1、Kubernetes 环境安装 Jenkins

<https://blog.csdn.net/heian_99/article/details/124985786>

## 2、Jenkins 安装插件

```bash
插件:
kubernets
pipeline
docker pipeline
docker
Kubernetes Cli
Config File Provider
Pipeline Utility Steps

Jenkins源：https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json
```

## 3、云配置

Dashboard > 系统管理 > 节点管理 > configureClouds

参考：<https://github.com/jenkinsci/kubernetes-plugin>

 

![](../../image/c32d4eee445f444ea7f1eeba1fff7352.png)

 

 

![](../../image/d916244ad3fe47cca2e5659f2b0c8c81.png)

 ![](../../image/3dccc5fd059841f7962a43f73faccda2.png)

 

这里是配置连接Kubernetes集群，启动 Jenkins Slave 代理的相关配置。

- **名称：** kubernetes
- **Kubernetes 地址：** [kubernetes.default.svc.cluster.local](https://link.juejin.cn/?target=https%3A%2F%2Fkubernetes.default.svc.cluster.local%2F "kubernetes.default.svc.cluster.local") \(默认集群内调用 k8s api 地址\)
- **禁用 HTTPS 证书检查：** 勾选 \(不验证https\)
- **凭据：** 新增凭据—>Secret text—>Secret 设置 kubernetes 的 Token \(进入 k8s dashboard 的 token 等都行\)
- **Jenkins地址：** [jenkins.mydlqcloud:8080/jenkins](https://link.juejin.cn/?target=http%3A%2F%2Fjenkins.mydlqcloud%3A8080%2Fjenkins "jenkins.mydlqcloud:8080/jenkins") \(用于代理与 Jenkins 连接的地址，用的是 k8s 集群中 jenkins 服务的地址为“[http://jenkins服务名.jenkins所在namespace:jenkins端口号/jenkins后缀”](https://link.juejin.cn/?target=http%3A%2F%2Fxn--jenkins-6k1lv9hx32e.xn--jenkinsnamespace-k412at47l%3Ajenkins%25E7%25AB%25AF%25E5%258F%25A3%25E5%258F%25B7%2Fjenkins%25E5%2590%258E%25E7%25BC%2580%25E2%2580%259D "http://jenkins服务名.jenkins所在namespace:jenkins端口号/jenkins后缀”")\)
- **其他：** 默认即可

## 4、Template 模板配置

这里配置 Jenkins Slave 在 kubernetes 集群中启动的 Pod 的配置，这里将设置四个镜像，分别是：

- **Jenkins Slave：** 用于执行 Jenkins Job 命令。
- **Helm-Kubectl：** 用于执行 Helm 命令。
- **Docker** 用于编译、推送 Docker 镜像
- **Maven：** 用于Maven编译、打包。

这里将这四个镜像融入到一个 Pod 之中，方便执行各种命令来完成持续部署交互过程。

![](../../image/99a44e897ff3408aa9f104bc20537141.png)

 ![](../../image/1caad9c3f6e148108a3c385f5681ad7c.png)

 

```bash
[root@master01 Jenkins]# cat maven.yaml 
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: maven-pvc
  namespace: jenkins
spec:
  storageClassName: "nfsdata"
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```

```bash
Kubernetes地址：https://kubernetes.default.svc.cluster.local/

Jenkins-master：http://jenkins.jenkins.svc.cluster.local:8080

Jenkins-slave：jenkins.jenkins.svc.cluster.local:50000



jnlp-slave
cnych/jenkins:jnlp6

maven
maven:3.8.5-openjdk-8-slim

docker
registry.cn-shanghai.aliyuncs.com/mydlq/docker:18.06.2-dind

helm-kubectl
registry.cn-shanghai.aliyuncs.com/mydlq/helm-kubectl:2.13.1


/var/run/docker.sock
/usr/bin/docker
/etc/docker
```

注意：docker需要填写sleep

![](../../image/3c80db3bbb944ffc99377165b62b73f9.png) 

 

## 5、Jenkins-slave 启动测试

![](../../image/36810bad770a413997062f38a7adb49e.png)

 ![](../../image/aa9d30d73b694f81a8558e98807064c6.png)

```bash
def label = "jnlp-slave"

podTemplate(label: label,cloud: 'kubernetes' ){
    node (label) {
        stage('Git阶段'){
            echo "1、开始拉取代码"
            sh "git version"
        }
        stage('Maven阶段'){
            container('maven') {
                echo "2、开始Maven编译、推送到本地库"
                sh "mvn -version"
            }
        }
        stage('Docker阶段'){
            container('docker') {
                echo "3、开始读取Maven pom变量，并执行Docker编译、推送、删除"
                sh "docker version"
            }
        }
         stage('Helm阶段'){
            container('helm-kubectl') {
                echo "4、开始检测Kubectl环境，测试执行Helm部署，与执行部署"
                sh "helm version"
            }
        }
    }
}
```

![](../../image/b0324852234442f8a3c14e8da79a4440.png)

 

## 6、实战环境

 

![](../../image/5b06bece890a495f98271d74623437a6.png)

 

```bash
pipeline {
        agent 
        {
        label 'jnlp-slave'
        }
 
    // 存放所有任务的合集
    stages {
        stage('拉取Git代码') {
            steps {
                echo '拉取Git代码'
				 sh 'git clone https://gitee.com/chengfeng99/java-demo.git'
            }
        }
 
        stage('检测代码质量') {
            steps {
                echo '检测代码质量'
                withSonarQubeEnv('sonarqube') { // Will pick the global server connection you have configured       
            // 这里使用名字叫做maven的容器运行
            container("maven") {
                sh '''
				cd /home/jenkins/agent/workspace/k8s-demo/java-demo
				mvn sonar:sonar  -Dsonar.projectname=${JOB_NAME} -Dsonar.projectKey=${JOB_NAME} -Dsonar.java.binaries=target/ -Dsonar.login=19d0d6b885e18455d257d61da08776bd4e180c04
				'''
            }
            }
        }
 }
        stage('构建代码') {
            steps {
                echo '构建代码'
                   container('maven') {
                    sh ''' 
					cd /home/jenkins/agent/workspace/k8s-demo/java-demo
					mvn clean  package  -Dmaven.test.skip=true
					'''
                    //打包跳过测试
                }
            }
        }
 
        stage('制作自定义镜像并发布Harbor') {
            steps {
                echo '制作自定义镜像并发布Harbor'
            }
        }
 
        stage('基于Harbor部署工程') {
            steps {
                echo '基于Harbor部署工程'
            }
        }
    }
}
```

## 7、运行结果

![](../../image/77b033106c3749538159eeb6c5f803ce.png)

 

![](../../image/36810bad770a413997062f38a7adb49e.png)

![](../../image/8ca6ab5caeac4a33819290d82400e416.png)