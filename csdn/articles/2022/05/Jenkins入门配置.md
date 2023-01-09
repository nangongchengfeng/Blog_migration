+++
author = "南宫乘风"
title = "Jenkins入门配置"
date = "2022-05-17 09:50:07"
tags=['jenkins', 'devops', 'git']
categories=['Jenkins']
image = "post/4kdongman/11.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/124809338](https://blog.csdn.net/heian_99/article/details/124809338)

[Jenkins安装部署使用_南宫乘风的博客-CSDN博客](https://blog.csdn.net/heian_99/article/details/124808858)

安装可以参考这篇文章，后续在这基础进行构建



由于Jenkins需要从Git拉取代码、需要本地构建、甚至需要直接发布自定义镜像到Docker仓库，所以Jenkins需要配置大量内容。

## 构建任务

准备好GitLab仓库中的项目，并且通过Jenkins配置项目的实现当前项目的[DevOps]()基本流程。
-  构建Maven工程发布到GitLab（Gitee、Github均可） 
[java-demo: api-gateway-demo](https://gitee.com/chengfeng99/java-demo.git)

![68376a7ce8ca4c899fab549b343f8d99.png](https://img-blog.csdnimg.cn/68376a7ce8ca4c899fab549b343f8d99.png)



Jenkins点击左侧导航新建任务

![c2c788114a9a4d34adda9b09b04d4368.png](https://img-blog.csdnimg.cn/c2c788114a9a4d34adda9b09b04d4368.png)



选择自由风格构建任务

![d7dc787fda9f488590cb170d6c204511.png](https://img-blog.csdnimg.cn/d7dc787fda9f488590cb170d6c204511.png)



## 配置源码拉取地址

Jenkins需要将Git上存放的源码存储到Jenkins服务所在磁盘的本地
-  配置任务源码拉取的地址 
![659875aca631427e9080a73110077e9f.png](https://img-blog.csdnimg.cn/659875aca631427e9080a73110077e9f.png)



Jenkins立即构建

点击任务demo中的立即构建

![12c022a48dcb41fa9a4f8c6ccb96df39.png](https://img-blog.csdnimg.cn/12c022a48dcb41fa9a4f8c6ccb96df39.png)

 查看构建工程的日志，点击上述的任务条即可

![3c9b59ae6e764ed2a98e5d4e38a82319.png](https://img-blog.csdnimg.cn/3c9b59ae6e764ed2a98e5d4e38a82319.png)


-  可以看到源码已经拉取带Jenkins本地，可以根据第三行日志信息，查看Jenkins本地拉取到的源码。 -  查看Jenkins容器中[/var/jenkins_home/workspace/d]()emo的源码 
源码存放位置

![fae77044512140059555ef614c6a4993.png](https://img-blog.csdnimg.cn/fae77044512140059555ef614c6a4993.png)



## 配置Maven构建代码

代码拉取到Jenkins本地后，需要在Jenkins中对代码进行构建，这里需要Maven的环境，而Maven需要Java的环境，接下来需要在Jenkins中安装JDK和Maven，并且配置到Jenkins服务。
-  准备JDK、Maven压缩包通过数据卷映射到Jenkins容器内部 
![fdd9f7d5b22047918505ade55ba777ab.png](https://img-blog.csdnimg.cn/fdd9f7d5b22047918505ade55ba777ab.png)

 解压压缩包，并配置Maven的settings.xml

```
&lt;!-- 阿里云镜像地址 --&gt;
&lt;mirror&gt;  
    &lt;id&gt;alimaven&lt;/id&gt;  
    &lt;name&gt;aliyun maven&lt;/name&gt;  
    &lt;url&gt;http://maven.aliyun.com/nexus/content/groups/public/&lt;/url&gt;
    &lt;mirrorOf&gt;central&lt;/mirrorOf&gt;          
&lt;/mirror&gt;
&lt;!-- JDK1.8编译插件 --&gt;
&lt;profile&gt;
    &lt;id&gt;jdk-1.8&lt;/id&gt;
    &lt;activation&gt;
        &lt;activeByDefault&gt;true&lt;/activeByDefault&gt;
        &lt;jdk&gt;1.8&lt;/jdk&gt;
    &lt;/activation&gt;
    &lt;properties&gt;
        &lt;maven.compiler.source&gt;1.8&lt;/maven.compiler.source&gt;
        &lt;maven.compiler.target&gt;1.8&lt;/maven.compiler.target&gt;
        &lt;maven.compiler.compilerVersion&gt;1.8&lt;/maven.compiler.compilerVersion&gt;
    &lt;/properties&gt;        
&lt;/profile&gt;
```

Jenkins配置JDK&amp;Maven并保存

![d2e8f8a9ffa34c38b8aac8833aa69821.png](https://img-blog.csdnimg.cn/d2e8f8a9ffa34c38b8aac8833aa69821.png)

 配置Jenkins任务构建代码

![2f68bbdb25aa478986424f9a06558099.png](https://img-blog.csdnimg.cn/2f68bbdb25aa478986424f9a06558099.png)

 立即构建测试，查看target下的jar包

[java-demo: api-gateway-demo](https://gitee.com/chengfeng99/java-demo.git)

![c323a7c4561e44dfb6c1a2caecd8acd8.png](https://img-blog.csdnimg.cn/c323a7c4561e44dfb6c1a2caecd8acd8.png)

## 配置Publish发布&amp;远程操作

jar包构建好之后，就可以根据情况发布到测试或生产环境，这里需要用到之前下载好的插件Publish Over SSH。
-  配置Publish Over SSH连接测试、生产环境 
Publish Over SSH配置

![04aa8a0941584adeb2060edcf22a85f3.png](https://img-blog.csdnimg.cn/04aa8a0941584adeb2060edcf22a85f3.png)

 ![f2eea35e4f034083959f283638e6f5bf.png](https://img-blog.csdnimg.cn/f2eea35e4f034083959f283638e6f5bf.png)



 配置任务的构建后操作，发布jar包到目标服务

![238250c6ba2944d19002ad5e0fb42bb9.png](https://img-blog.csdnimg.cn/238250c6ba2944d19002ad5e0fb42bb9.png)

 ![4102647d71ac41e2be4e45b7b2e1e601.png](https://img-blog.csdnimg.cn/4102647d71ac41e2be4e45b7b2e1e601.png)

 ![5094833367134c6086282d76db0fd132.png](https://img-blog.csdnimg.cn/5094833367134c6086282d76db0fd132.png)



![6dabff682161452e9b7ee1027f9b7aa5.png](https://img-blog.csdnimg.cn/6dabff682161452e9b7ee1027f9b7aa5.png)

 已经完成一次简单的构建交付

## 持续交付、部署

程序代码在经过多次集成操作到达最终可以交付，持续交付整体流程和持续集成类似，不过需要选取指定的发行版本
-  下载Git Parameter插件 
![1f595b7b5a0d404b8a6144ffd057d941.png](https://img-blog.csdnimg.cn/1f595b7b5a0d404b8a6144ffd057d941.png)

 

设置项目参数化构建

基于Git标签构建

![2fa818313a774b98acc2cbb5f5aba000.png](https://img-blog.csdnimg.cn/2fa818313a774b98acc2cbb5f5aba000.png)

 

![2c864ec677da4947a5168b76f12201af.png](https://img-blog.csdnimg.cn/2c864ec677da4947a5168b76f12201af.png)

 给项目添加tag版本

![ce487a64e8c14962b199940e75a5aa3e.png](https://img-blog.csdnimg.cn/ce487a64e8c14962b199940e75a5aa3e.png)

 任务构建时，采用Shell方式构建，拉取指定tag版本代码

![099dbd89f8ce41f980a6f0272bb732fc.png](https://img-blog.csdnimg.cn/099dbd89f8ce41f980a6f0272bb732fc.png)

 基于Parameter构建任务，任务发布到目标服务器

![54a960e298ab425598b3062eeba170b3.png](https://img-blog.csdnimg.cn/54a960e298ab425598b3062eeba170b3.png)

 
