+++
author = "南宫乘风"
title = "Jenkins的流水线（Pipeline）"
date = "2022-05-17 10:35:08"
tags=['jenkins', '运维']
categories=['Jenkins']
image = "post/4kdongman/99.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/124815450](https://blog.csdn.net/heian_99/article/details/124815450)

# 目录

[Jenkins安装部署使用_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858)

[Jenkins入门配置_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124809338)

[Jenkins集成Sonar Qube_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124814780)



# Jenkins流水线

## Jenkins流水线任务介绍



之前采用Jenkins的自由风格构建的项目，每个步骤流程都要通过不同的方式设置，并且构建过程中整体流程是不可见的，无法确认每个流程花费的时间，并且问题不方便定位问题。

Jenkins的Pipeline可以让项目的发布整体流程可视化，明确执行的阶段，可以快速的定位问题。并且整个项目的生命周期可以通过一个Jenkinsfile文件管理，而且Jenkinsfile文件是可以放在项目中维护。

所以Pipeline相对自由风格或者其他的项目风格更容易操作。

![a1efec7060a74096836cbb23bcdc0b1b.png](https://img-blog.csdnimg.cn/a1efec7060a74096836cbb23bcdc0b1b.png)



# Jenkins流水线任务

## 构建Jenkins流水线任务

构建任务

![11c73103b86243adaf390cd586e076b4.png](https://img-blog.csdnimg.cn/11c73103b86243adaf390cd586e076b4.png)

 生成Groovy脚本

Hello World脚本生成

![107b9a30323b4b70827c0b1b804a25fd.png](https://img-blog.csdnimg.cn/107b9a30323b4b70827c0b1b804a25fd.png)

 构建后查看视图

![c56ca4673c6348f8992bd6f07c8cd2e3.png](https://img-blog.csdnimg.cn/c56ca4673c6348f8992bd6f07c8cd2e3.png)

# Groovy脚本

Groovy脚本基础语法

```
// 所有脚本命令包含在pipeline{}中
pipeline {  
	// 指定任务在哪个节点执行（Jenkins支持分布式）
    agent any
    
    // 配置全局环境，指定变量名=变量值信息
    environment{
    	host = '172.17.1.22'
    }

    // 存放所有任务的合集
    stages {
    	// 单个任务
        stage('任务1') {
        	// 实现任务的具体流程
            steps {
                echo 'do something'
            }
        }
		// 单个任务
        stage('任务2') {
        	// 实现任务的具体流程
            steps {
                echo 'do something'
            }
        }
        // ……
    }
}
```

## 编写例子测试

```
pipeline {
    agent any

    // 存放所有任务的合集
    stages {
        stage('拉取Git代码') {
            steps {
                echo '拉取Git代码'
            }
        }

        stage('检测代码质量') {
            steps {
                echo '检测代码质量'
            }
        }

        stage('构建代码') {
            steps {
                echo '构建代码'
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

配置Grovvy脚本

![6538958ea23c43fa814956a52001f208.png](https://img-blog.csdnimg.cn/6538958ea23c43fa814956a52001f208.png)

 查看效果

![fde345cff9464a4caa0a8c588a9bd915.png](https://img-blog.csdnimg.cn/fde345cff9464a4caa0a8c588a9bd915.png)

 [Ps：涉及到特定脚本，Jenkins给予了充足的提示，可以自动生成命令]()

生成命令位置

![c1d8b5f0bd2b47a78155339f92a28d82.png](https://img-blog.csdnimg.cn/c1d8b5f0bd2b47a78155339f92a28d82.png)



# Jenkinsfile实现

Jenkinsfile方式需要将脚本内容编写到项目中的Jenkinsfile文件中，每次构建会自动拉取项目并且获取项目中Jenkinsfile文件对项目进行构建

配置pipeline

![60c19e380c214266b7ab1634d0e6d582.png](https://img-blog.csdnimg.cn/60c19e380c214266b7ab1634d0e6d582.png)

 准备Jenkinsfile

![d5272fbd9d0c45f0b97fe8972540c76f.png](https://img-blog.csdnimg.cn/d5272fbd9d0c45f0b97fe8972540c76f.png)

 [Jenkinsfile · 南宫乘风/java-demo - Gitee.com](https://gitee.com/chengfeng99/java-demo/blob/master/Jenkinsfile)

测试效果

![07f4398072da46d3a02d5a8af60b887b.png](https://img-blog.csdnimg.cn/07f4398072da46d3a02d5a8af60b887b.png)



# Jenkins流水线任务实现

参数化构建

添加参数化构建，方便选择不的项目版本

![48ff368ad442429f882d65fe0fb7d637.png](https://img-blog.csdnimg.cn/48ff368ad442429f882d65fe0fb7d637.png)



拉取Git代码

通过流水线语法生成Checkout代码的脚本

 ![c242282cd1994ff9a1368e3faa78a94a.png](https://img-blog.csdnimg.cn/c242282cd1994ff9a1368e3faa78a94a.png)

 ![1411ecf68f69499dbcb8db331577dbbe.png](https://img-blog.csdnimg.cn/1411ecf68f69499dbcb8db331577dbbe.png)



![a74b0c6dddda4f17af940df460e31446.png](https://img-blog.csdnimg.cn/a74b0c6dddda4f17af940df460e31446.png)

  将*/master更改为标签[${tag}]()

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
}
```

[Ps：由于采用变量，记得使用双引号](%0A)



进行构建

![10b06733348c46119c01d568ab90082e.png](https://img-blog.csdnimg.cn/10b06733348c46119c01d568ab90082e.png)

 已经成功

![93a1fd1e19164ff487ab75d0daacfd8a.png](https://img-blog.csdnimg.cn/93a1fd1e19164ff487ab75d0daacfd8a.png)












