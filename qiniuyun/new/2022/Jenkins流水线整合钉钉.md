---
author: 南宫乘风
categories:
- Jenkins
date: 2022-05-17 10:58:10
description: 前文安装部署使用南宫乘风的博客博客安装部署使用南宫乘风的博客博客入门配置南宫乘风的博客博客入门配置南宫乘风的博客博客集成南宫乘风的博客博客集成南宫乘风的博客博客的流水线的流水线在程序部署成功后，可以通。。。。。。。
image: http://image.ownit.top/4kdongman/94.jpg
tags:
- jenkins
- ci
- 运维
title: Jenkins流水线整合钉钉
---

<!--more-->

# 前文

[Jenkins安装部署使用\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858 "Jenkins安装部署使用_南宫乘风的博客-CSDN博客")

[Jenkins入门配置\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124809338 "Jenkins入门配置_南宫乘风的博客-CSDN博客")

[Jenkins集成Sonar Qube\_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124814780 "Jenkins集成Sonar Qube_南宫乘风的博客-CSDN博客")

[Jenkins的流水线（Pipeline）](https://blog.csdn.net/heian_99/article/details/124815450 "Jenkins的流水线（Pipeline）")

在程序部署成功后，可以通过钉钉的机器人及时向群众发送部署的最终结果通知

- 安装插件

![](http://image.ownit.top/csdn/7b31facb4d9d40df9a951722e33a2b75.png)

 

![](http://image.ownit.top/csdn/4bd3565abe544a219c70b6cbf90a4ce0.png)

 钉钉内部创建群组并构建机器人

 ![](http://image.ownit.top/csdn/06d15202c344408bb986e510b815faea.png)

 ![](http://image.ownit.top/csdn/2846639eff97423a820bfb0ab1f4f3f9.png)

 最终或获取到Webhook信息

```bash
https://oapi.dingtalk.com/robot/send?access_token=kej4ehkj34gjhg34jh5bh5jb34hj53b4
```

系统配置添加钉钉通知

![](http://image.ownit.top/csdn/5c7548d451d84ca5a38e7d2bc9975d55.png)

 任务中追加流水线配置

```bash
pipeline {

    agent any
        environment{
        harborRepo = 'heianapp'
        harborUser = 'heian99'
        harborPasswd = 'NG+.mK4M-(s4CYX'
    }
    // 存放所有任务的合集
    stages {
        stage('拉取Git代码') {
            steps {
                echo '拉取Git代码'
                checkout([$class: 'GitSCM', branches: [[name: '${tag}']], extensions: [], userRemoteConfigs: [[url: 'https://gitee.com/chengfeng99/java-demo.git']]])
            }
        }

        stage('检测代码质量') {
            steps {
                echo '检测代码质量'
                 sh '/var/jenkins_home/sonar-scanner/bin/sonar-scanner -Dsonar.sources=./ -Dsonar.projectname=${JOB_NAME} -Dsonar.projectKey=${JOB_NAME} -Dsonar.java.binaries=target/ -Dsonar.login=19d0d6b885e18455d257d61da08776bd4e180c04'
            }
        }

        stage('构建代码') {
            steps {
                echo '构建代码'
                 sh '/var/jenkins_home/maven/bin/mvn clean package -DskipTests'
            }
        }

        stage('制作自定义镜像并发布Harbor') {
                        steps {
                echo '制作自定义镜像并发布Harbor'
                sh '''
                cp ./target/*.jar ./docker/demo.jar
                cd ./docker
                docker build -t ${JOB_NAME}:${BUILD_NUMBER} . '''
                
                 sh '''docker login -u ${harborUser} -p ${harborPasswd} 
                docker tag ${JOB_NAME}:${BUILD_NUMBER} ${harborUser}/${harborRepo}:${JOB_NAME}_${BUILD_NUMBER}
                docker push ${harborUser}/${harborRepo}:${JOB_NAME}_${BUILD_NUMBER}'''
            }
        }

        stage('基于Harbor部署工程') {
            steps {
                echo '基于Harbor部署工程'
				sshPublisher(publishers: [sshPublisherDesc(configName: 'node-Linux32', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: '''cd /opt/java/
echo "测试成功" >> log.txt
 date >> log.txt''', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: 'target/*.jar,docker/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
            }
        }
    }
	post {
        success {
            dingtalk (
                robot: 'Jenkins-DingDing',
                type:'MARKDOWN',
                title: "success: ${JOB_NAME}",
                text: ["- 成功构建:${JOB_NAME}项目!\n- 版本:${tag}\n- 持续时间:${currentBuild.durationString}\n- 任务:#${JOB_NAME}"]
            )
        }
        failure {
            dingtalk (
                robot: 'Jenkins-DingDing',
                type:'MARKDOWN',
                title: "fail: ${JOB_NAME}",
                text: ["- 失败构建:${JOB_NAME}项目!\n- 版本:${tag}\n- 持续时间:${currentBuild.durationString}\n- 任务:#${JOB_NAME}"]
            )
        }
    }
}
```

查看效果

![](http://image.ownit.top/csdn/d8e0b41b4ec04af888df95b0a3f88c26.png)

 ![](http://image.ownit.top/csdn/3bc24a4879ca41029deafb2049b392eb.png)