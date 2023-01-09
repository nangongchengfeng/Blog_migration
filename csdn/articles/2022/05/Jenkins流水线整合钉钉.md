+++
author = "南宫乘风"
title = "Jenkins流水线整合钉钉"
date = "2022-05-17 10:58:10"
tags=['jenkins', 'ci', '运维']
categories=['Jenkins']
image = "post/4kdongman/29.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/124816190](https://blog.csdn.net/heian_99/article/details/124816190)

# 前文

[Jenkins安装部署使用_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858)

[Jenkins入门配置_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124809338)

[Jenkins集成Sonar Qube_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124814780)

[Jenkins的流水线（Pipeline）](https://blog.csdn.net/heian_99/article/details/124815450)



在程序部署成功后，可以通过钉钉的机器人及时向群众发送部署的最终结果通知
-  安装插件 
![7b31facb4d9d40df9a951722e33a2b75.png](https://img-blog.csdnimg.cn/7b31facb4d9d40df9a951722e33a2b75.png)

 

![4bd3565abe544a219c70b6cbf90a4ce0.png](https://img-blog.csdnimg.cn/4bd3565abe544a219c70b6cbf90a4ce0.png)

 钉钉内部创建群组并构建机器人



 ![06d15202c344408bb986e510b815faea.png](https://img-blog.csdnimg.cn/06d15202c344408bb986e510b815faea.png)

 ![2846639eff97423a820bfb0ab1f4f3f9.png](https://img-blog.csdnimg.cn/2846639eff97423a820bfb0ab1f4f3f9.png)

 最终或获取到Webhook信息

```
https://oapi.dingtalk.com/robot/send?access_token=kej4ehkj34gjhg34jh5bh5jb34hj53b4
```

系统配置添加钉钉通知

![5c7548d451d84ca5a38e7d2bc9975d55.png](https://img-blog.csdnimg.cn/5c7548d451d84ca5a38e7d2bc9975d55.png)

 任务中追加流水线配置

```
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
echo "测试成功" &gt;&gt; log.txt
 date &gt;&gt; log.txt''', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: '', remoteDirectorySDF: false, removePrefix: '', sourceFiles: 'target/*.jar,docker/*')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
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

![d8e0b41b4ec04af888df95b0a3f88c26.png](https://img-blog.csdnimg.cn/d8e0b41b4ec04af888df95b0a3f88c26.png)

 ![3bc24a4879ca41029deafb2049b392eb.png](https://img-blog.csdnimg.cn/3bc24a4879ca41029deafb2049b392eb.png)

 
