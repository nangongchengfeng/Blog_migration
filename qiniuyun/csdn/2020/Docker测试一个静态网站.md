---
author: 南宫乘风
categories:
- Docker
date: 2020-03-23 11:28:44
description: 使用测试静态网站将作为本地开发环境是的一个最简单的应用场景。这样的环境可以完全复制生产环境，并确保用户开发的东西在生产环境中也能运行。下面从将服务器安装到容器来架构一个简单的网站开始。这个网站暂且命名。。。。。。。
image: ../../title_pic/15.jpg
slug: '202003231128'
tags:
- docker
- 测试
- 静态
- 网站
- 容器
title: Docker测试一个静态网站
---

<!--more-->

# 使用Docker测试静态网站

**将Docker作为本地Web开发环境是Docker的一个最简单的应用场景。 这样的环境可以完全复制生产环境，并确保用户开发的东西在生产环境中也能运行。下面从将Nginx Web服务器安装到容器来架构一个简 单的网站开始。这个网站暂且命名为Sample。 **

## Sample网站的初始Dockerfile

**为了完成网站开发，从这个简单的Dockerfile开始。先来创建一个 目录，保存Dockerfile**

```bash
$ mkdir sample 
$ cd sample 
$ touch Dockerfile
```

现在还需要一些Nginx配置文件，才能运行这个网站。首先在这个示例 所在的目录里创建一个名为nginx的目录，用来存放这些配置文件。 然后我们可以从GitHub上下载作者准备好的示例文件

```bash
$ mkdir nginx && cd nginx 
$ wget https://raw.githubusercontent.com/jamtur01/dockerbook-code/master/code/5/sample/nginx/global.conf 
$ wget https://raw.githubusercontent.com/jamtur01/dockerbook-code/master/code/5/sample/nginx/nginx.conf 
$ cd ..
```

**现在看一下我们将要为Sample网站创建的Dockerfile，如代码清单**

```bash
FROM centos
MAINTAINER heian99 "heian99@163.com" 
ENV REFRESHED_AT 2014-06-01 
RUN yum -y update && yum  -y install nginx 
RUN mkdir -p /var/www/html/website 
ADD nginx/global.conf /etc/nginx/conf.d/ 
ADD nginx/nginx.conf /etc/nginx/nginx.conf 
EXPOSE 80
```

### 这个简单的Dockerfile内容包括以下几项。

- 安装Nginx。

- 在容器中创建一个目录/var/www/html/website/。

- 将来自我们下载的本地文件的Nginx配置文件添加到镜像中。

- 公开镜像的80端口。

**这个Nginx配置文件是为了运行Sample网站而配置的。将文件 nginx/global.conf用ADD指令复制到/etc/nginx/conf.d/目 录中。配置文件**

### **global.conf**

```bash
server {
        listen          0.0.0.0:80;
        server_name     _;

        root            /var/www/html/website;
        index           index.html index.htm;

        access_log      /var/log/nginx/default_access.log;
        error_log       /var/log/nginx/default_error.log;
}
```

这个文件将Nginx设置为监听80端口，并将网络服务的根路径设置 为/var/www/ html/website，这个目录是我们用RUN指令创建 的。  
我们还需要将Nginx配置为非守护进程的模式，这样可以让Nginx在 Docker容器里工作。将文件nginx/nginx.conf复制 到/etc/nginx目录就可以达到这个目的

### nginx.conf的清单

```bash
user www-data;#把这个删除掉，不然后面docker里面的nginx无法启动
worker_processes 4;
pid /run/nginx.pid;
daemon off;

events {  }

http {
  sendfile on;
  tcp_nopush on;
  tcp_nodelay on;
  keepalive_timeout 65;
  types_hash_max_size 2048;
  include /etc/nginx/mime.types;
  default_type application/octet-stream;
  access_log /var/log/nginx/access.log;
  error_log /var/log/nginx/error.log;
  gzip on;
  gzip_disable "msie6";
  include /etc/nginx/conf.d/*.conf;
}
```

在这个配置文件里，daemon off;选项阻止Nginx进入后台，强制其 在前台运行。这是因为要想保持Docker容器的活跃状态，需要其中运 行的进程不能中断。默认情况下，Nginx会以守护进程的方式启动，这 会导致容器只是短暂运行，在守护进程被fork启动后，发起守护进程 的原始进程就会退出，这时容器就停止运行了

**这个文件通过ADD指令复制到/etc/nginx/nginx.conf。**

**第一个指令以 目录/etc/nginx/ conf.d/结束，而第二个指令指定了文 件/etc/nginx/nginx.conf。将文件复制到Docker镜像时，这两 种风格都是可以用的。**

## 构建Sample网站和Nginx镜像

**利用之前的Dockerfile，可以用docker build命令构建出新的镜 像，并将这个镜像命名为heian/nginx**

```
docker build -t heian/nginx .
```

![](../../image/20200323104725505.png)

**这将构建并命名一个新镜像。下面来看看构建的执行步骤。使用 docker history命令查看构建新镜像的步骤和层级**

![](../../image/20200323105621292.png)

##  从Sample网站和Nginx镜像构建容器

现在可以使用heian/nginx镜像，并开始从这个镜像构建可以用 来测试Sample网站的容器。为此，需要添加Sample网站的代码。现在  
注意提示下载这段代码到sample目录

```bash
$ mkdir website && cd website 
$ wget http://raw.githubusercontent.com/jamtur01/dockerbook-code/master/code/5/sample/website/index.html
$ cd..
```

现在来看看如何使用docker run命令来运行一个容器

```bash
docker run -d -p 80 --name website  -v $PWD/website:/var/www/html/website heian/nginx nginx
```

上面命令如果有问题，那就执行下面的命令

```bash
docker run -d  -p 80 --name nginx -v $PWD/website:/var/www/html/website  heian/nginx /bin/bash -c "tail -f /dev/null;/usr/sbin/nginx"
```

> **可以看到，在执行docker run时传入了nginx作为容器的启动命令。一般情况下， 这个命令无法让Nginx以交互的方式运行。我们已经在提供给Docker的配置里加入了指令 daemon off，这个指令让Nginx启动后以交互的方式在前台运行**

![](../../image/20200323111606206.png)

可以看到，我们使用docker run命令从heian/nginx镜像创建 了一个名为website的容器。读者已经见过了大部分选项，不过-v选 项是新的。-v这个选项允许我们将宿主机的目录作为卷，挂载到容器 里。  
**回到刚才的例子。当我们因为某些原因不想把应用或者代码构建到镜 像中时，就体现出卷的价值了。例如：**

- 希望同时对代码做开发和测试；
- 代码改动很频繁，不想在开发过程中重构镜像；
- 希望在多个容器间共享代码

**\-v选项通过指定一个目录或者登上与容器上与该目录分离的本地宿主 机来工作，这两个目录用:分隔。如果容器目录不存在，Docker会自 动创建一个。**  
 

```bash
 docker run -d -p 80 --name website \
 -v $PWD/website:/var/www/html/website:ro \ 
heian/nginx nginx
```

**这将使目的目录/var/www/html/website变成只读状态。**

在Nginx网站容器里，我们通过卷将\$PWD/website挂载到容器 的/var/www/ html/website目录，顺利挂载了正在开发的本地网 站。在Nginx配置里（在配置文 件/etc/ngingx/conf.d/global.conf中），已经指定了这个目 录为Nginx服务器的工作目录。  
**现在，如果使用docker ps命令查看正在运行的容器，可以看到名为 website的容器正处于活跃状态，容器的80端口被映射到宿主机的 49161端口**

![](../../image/20200323112506809.png)

### 修改网站

![](../../image/20200323112652112.png)

我们已经得到了一个可以工作的网站！现在，如果要修改网站，该怎 么办？可以直接打开本地宿主机的website目录下的index.html文 件并修改

![](../../image/20200323112743234.png)

![](../../image/20200323112752462.png)

**可以看到，Sample网站已经更新了。显然这个修改太简单了，不过可 以看出，更复杂的修改也并不困难。更重要的是，正在测试网站的运 行环境，完全是生产环境里的真实状态。现在可以给每个用于生产的 网站服务环境（如Apache、Nginx）配置一个容器，给不同开发框架 的运行环境（如PHP或者Ruby on Rails）配置一个容器，或者给后端 数据库配置一个容器，等等。 **