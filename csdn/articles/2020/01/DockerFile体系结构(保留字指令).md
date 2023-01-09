+++
author = "南宫乘风"
title = "DockerFile体系结构(保留字指令)"
date = "2020-01-03 12:01:16"
tags=['命令', 'docker', '镜像']
categories=['Docker']
image = "post/4kdongman/71.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103817642](https://blog.csdn.net/heian_99/article/details/103817642)

# **DockerFile体系结构(保留字指令)**

 

**FROM：基础镜像，当前新镜像是基于哪个镜像的**

**MAINTAINER：镜像维护者的姓名和邮箱地址**

**RUN：容器构建时需要运行的命令**

**EXPOSE：当前容器对外暴露出的端口**

**WORKDIR：指定在创建容器后，终端默认登陆的进来工作目录，一个落脚点**

**ENV：用来在构建镜像过程中设置环境变量**

ENV MY_PATH /usr/mytest

这个环境变量可以在后续的任何RUN指令中使用，这就如同在命令前面指定了环境变量前缀一样；

也可以在其它指令中直接使用这些环境变量，

比如：WORKDIR $MY_PATH

**ADD****:将宿主机目录下的文件拷贝进镜像且ADD命令会自动处理URL和解压tar压缩包**

**COPY****:类似ADD，拷贝文件和目录到镜像中。<br> 将从构建上下文目录中 &lt;源路径&gt; 的文件/目录复制到新的一层的镜像内的 &lt;目标路径&gt; 位置**

COPY src dest

COPY ["src", "dest"]

**VOLUME****:容器数据卷，用于数据保存和持久化工作**

**CMD****:指定一个容器启动时要运行的命令**

CMD容器启动命令<br> CND指令的格式和RUN 相似，也是两种格式:<br> ●shell 格式: CMD &lt;命令&gt; <br> ●exec格式: CID ["可执行文件”， “参数1"， “参数2”..]<br> .参数列表格式: CNO [“参数",“参数2”..]. 在指定了EITRYPOIT 指令后,用CID指定具体的参<br> 数。<br> Dockerfile 中可以有多个 CMD 指令，但只有最后一个生效，CMD 会被 docker run 之后的参数替换

**ENTRYPOINT :指定一个容器启动时要运行的命令**

**ENTRYPOINT 的目的和 CMD 一样，都是在指定容器启动程序及参数**

**ONBUILD:当构建一个被继承的Dockerfile时运行命令，父镜像在被子继承后父镜像的onbuild被触发**

![20200103115311689.png](https://img-blog.csdnimg.cn/20200103115311689.png)

![20200103114109463.png](https://img-blog.csdnimg.cn/20200103114109463.png)
