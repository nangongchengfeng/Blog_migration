---
author: 南宫乘风
categories:
- 项目实战
date: 2023-03-15 19:28:27
description: 是什么是一个基于的服务发现工具，用于配置和管理系统和服务之间的依赖关系。它提供了一个简单的方式来注册、发现和配置服务，并包括健康检查、负载均衡和故障转移等功能。是一种分布式系统，用于在大型分布式系统中。。。。。。。
image: http://image.ownit.top/4kdongman/50.jpg
tags:
- java
- 运维
- 开发语言
title: SpringBoot（微服务）注册分布式Consul
---

<!--more-->

# Consul是什么

Consul是一个基于HTTP的服务发现工具，用于配置和管理系统和服务之间的依赖关系。它提供了一个简单的方式来注册、发现和配置服务，并包括健康检查、负载均衡和故障转移等功能。

Consul是一种分布式系统，用于在大型分布式系统中实现服务发现和配置共享。它使用Raft协议来实现强一致性，保证了在多个节点之间进行的数据更新的原子性。

Consul客户端可以将它们自己的服务信息注册到Consul服务器。这样，Consul服务器将自动成为所有服务的服务目录。此外，Consul还提供了一个健康检查机制，以确保已注册的服务仍然可以正常工作。

当一个客户端想要调用一个服务时，它可以从Consul服务器获取服务的网络位置信息。然后，客户端将使用此信息建立与服务的网络连接。

Consul通过HTTP API公开其服务发现和配置共享功能，这使得使用Consul与其他系统相当容易，如Kubernetes等容器编排工具。

总之，Consul的分布式注册原理是通过服务端和客户端之间的交互来实现服务发现和健康检查。客户端将服务信息注册到Consul服务器，然后从Consul服务器获取服务信息并建立网络连接。Consul使用Raft协议确保强一致性，并提供HTTP API进行访问。

# Consul原理

![](http://image.ownit.top/csdn/3c5ddb5da7638b3cb3bf867283b421a1.jpeg)

Consul采用的是集中式的注册中心架构，其中包含一个服务发现组件和一个KV存储组件。

服务发现组件：Consul中的服务发现是通过一组Agent和Server实现的。Agent是每个主机上运行的代理，用于与服务交互并报告本地运行状况。Server是负责在Consul集群中运行Raft算法的节点，以实现高可用性。

当服务启动时，它会向本地的Consul Agent发送一个服务注册请求，Agent会将服务的元数据信息（服务名、地址、端口等）注册到Consul的KV存储中。服务消费者可以通过向Agent发送服务发现请求来获取服务的地址和端口信息，然后向该地址发送请求以调用服务。

KV存储组件：Consul中的KV存储组件用于存储键值对信息，可以用于存储任何数据。在服务注册和发现中，服务元数据信息就是存储在KV存储中的。

当服务启动时，它会将自己的元数据信息存储到Consul的KV存储中，同时也会定期发送心跳请求告诉Consul服务还在运行。当服务终止时，它会发送一个注销请求告诉Consul将服务从KV存储中删除。

服务消费者可以从Consul的KV存储中获取服务的元数据信息，然后使用这些信息来调用服务。同时，服务消费者也可以监听KV存储中元数据信息的变化，当服务的元数据信息发生变化时，它会自动更新本地缓存。

总体来说，Consul的服务注册和发现过程如下：

1.  服务启动时，将自己的元数据信息注册到Consul的KV存储中，同时向本地的Consul Agent发送心跳请求告诉Consul服务还在运行。
2.  服务消费者向Consul Agent发送服务发现请求，Agent从KV存储中获取服务的元数据信息并返回给服务消费者。
3.  服务消费者使用获取到的服务元数据信息来调用服务。
4.  当服务终止时，它会发送一个注销请求告诉Consul将服务从KV存储中删除。

# 启动 Consul 集群

```bash
#启动第1个Server节点，集群要求要有3个Server，将容器8500端口映射到主机8900端口，同时开启管理界面 
docker run -d --name=consul1 -p 8900:8500 -e CONSUL_BIND_INTERFACE=eth0 consul agent --server=true --bootstrap-expect=3 --client=0.0.0.0 -ui 
 
#启动第2个Server节点，并加入集群 
docker run -d --name=consul2 -e CONSUL_BIND_INTERFACE=eth0 consul agent --server=true --client=0.0.0.0 --join 172.17.0.2 
 
#启动第3个Server节点，并加入集群 
docker run -d --name=consul3 -e CONSUL_BIND_INTERFACE=eth0 consul agent --server=true --client=0.0.0.0 --join 172.17.0.2 
 
#启动第4个Client节点，并加入集群 
docker run -d --name=consul4 -e CONSUL_BIND_INTERFACE=eth0 consul agent --server=false --client=0.0.0.0 --join 172.17.0.2 
```

第 1 个启动容器的 IP 一般是 172.17.0.2，后边启动的几个容器 IP 会排着来：172.17.0.3、172.17.0.4、172.17.0.5。

这些 Consul 节点在 Docker 的容器内是互通的，他们通过桥接的模式通信。但是如果主机要访问容器内的网络，需要做端口映射。

在启动第一个容器时，将 Consul 的 8500 端口映射到了主机的 8900 端口，这样就可以方便的通过主机的浏览器查看集群信息。

![](http://image.ownit.top/csdn/74d5626ea572e3a778029d48f5ee5b0c.jpeg)

# kubernetes集成Consul

![](http://image.ownit.top/csdn/353c7a733b0147e29fb3fcbbc3c6de35.png)

 

Kubernetes中的一个Pod中可以包含多个容器，这些容器可以协同工作，形成一个完整的服务。在这个例子中，一个Pod中包含了三个容器：Consul客户端容器、Java应用容器和Filebeat容器。

Consul客户端容器是用来向Kubernetes集群外的Consul服务器注册服务的。Consul客户端可以通过API或DNS接口与Consul服务器进行通信，将服务注册信息发送给Consul服务器，包括服务的名称、IP地址、端口号等元数据信息。

Java应用容器是用来运行业务应用程序的。它会通过Consul客户端容器中的API或DNS接口查询服务的信息，包括IP地址和端口号，以便能够与其它服务通信。

Filebeat容器则是用来收集Java应用程序的日志文件，并将其发送到指定的日志服务器进行处理和存储。

下面是大致的架构图：

```bash
                            +---------------------+
                             | Consul Server       |
                             | (集群外的Consul服务器) |
                             +---------------------+
                                        |
                                        | HTTP/DNS API
                                        |
                             +---------------------+
                             | Consul Client       |
                             | (Pod中的容器)       |
                             +---------------------+
                                      /  \
                                     /    \
                                    /      \
                       HTTP/DNS API       |       HTTP API
                         +-------+       |       +--------+
                         | Java  |       |       | File-  |
                         | App   |<------+------>| beat   |
                         |       |               |        |
                         +-------+               +--------+
```

在这个架构图中，Java应用容器和Filebeat容器都与Consul客户端容器通过HTTP/DNS API进行通信。Java应用容器使用Consul客户端容器提供的服务注册信息与其它服务进行通信，Filebeat容器则通过HTTP API将收集的日志文件发送到指定的日志服务器。Consul客户端容器通过HTTP API将服务注册信息发送给Kubernetes集群外的Consul服务器，以便其它服务可以发现和使用它们。

**以下是 Java 应用通过 Consul 客户端注册到 Consul 服务端的详细步骤流程：**

1.  Pod 中的 Consul 客户端启动，并向 Consul 集群发现服务请求。

2.  Consul 客户端会向 Consul 服务端的任一节点发出注册请求，告知它所在的服务名称、IP 地址、端口号、标签等信息，以及该服务的健康检查规则。

3.  Consul 服务端接收到注册请求后，会将该服务信息存储在本地的 KV 存储中，并将该服务的状态标记为“不健康”。

4.  Consul 客户端会根据所注册的健康检查规则，定期向 Consul 服务端发送健康检查请求，并根据响应结果更新本地的服务状态。

5.  当该服务的状态为“健康”时，Consul 客户端会将该服务的状态信息存储在本地的缓存中，并向本地的 Java 应用提供服务发现和负载均衡功能。

6.  Java 应用通过调用 Consul 客户端提供的 API，获取所需服务的 IP 地址和端口号，并通过这些信息与目标服务建立连接。

7.  如果需要对该服务进行修改或注销，Java 应用可以向 Consul 客户端发送对应的请求。

8.  Consul 客户端接收到请求后，会将请求转发给 Consul 服务端，并更新本地的缓存。

9.  Consul 服务端接收到请求后，会更新该服务在本地 KV 存储中的信息，并将该服务的状态标记为“不健康”。

10.  Consul 客户端会根据所注册的健康检查规则，定期向 Consul 服务端发送健康检查请求，并根据响应结果更新本地的服务状态。

总体架构图如下：

![](http://image.ownit.top/csdn/0213245b4db542f78a1cde1d56a74cc9.png)

 

在该架构中，Consul 客户端和 Java 应用都运行在 Pod 中，其中 Consul 客户端负责服务注册和服务发现，Java 应用则通过 Consul 客户端获取所需服务的信息。同时，Filebeat 用于收集应用的日志数据，并将其发送至目标日志存储系统。

# SpringBoot注册Consul

SpringBoot可以通过使用Consul的Java客户端库来实现与Consul的集成，该库提供了丰富的API，包括服务注册、服务发现、KV存储等功能。下面是SpringBoot注册Consul的大致步骤和原理：

1.  引入Consul客户端库

在SpringBoot项目的pom.xml中引入Consul客户端库的依赖，例如：

```java
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.4</version>
        <relativePath/>
    </parent>

    <groupId>com.springboot.demo</groupId>
    <artifactId>web-demo</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>web-demo</name>
    <description>web-demo</description>
    <properties>
        <java.version>1.8</java.version>
        <spring-cloud.version>Finchley.RELEASE</spring-cloud.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>


        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>2020.0.3</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

      2、配置Consul连接信息

在SpringBoot项目的application.yml文件中配置Consul的连接信息，例如：

```java
server:
  port: 1000
spring:
  application:
    name: heian
  cloud:
    consul:
      enabled: true
      host: 192.168.102.20  # 注册中心地址
      port: 8500  # 注册中心地址的端口
      discovery:
        hostname: 192.168.96.19 # 本地ip
        instance-id: ${spring.application.name}:${spring.cloud.consul.discovery.hostname}:${server.port}
        #health-check-path: ${server.servlet.context-path}/actuator/health # 如果配置了context-path就配置，没有就不配
        health-check-interval: 15s # 每隔15s做一次健康检查
        register: true
        register-health-check: true
        service-name: ${spring.application.name}

# 放开端口
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always
```

 3、实现服务注册

启动类

```java
@EnableDiscoveryClient
@SpringBootApplication
public class WebDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(WebDemoApplication.class, args);
    }


}
```

控制类

```java
package com.springboot.demo.webdemo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;

@RestController
@RequestMapping("/employee")
public class EmployeeController {

    @GetMapping
    public HashMap<String, String> index(){
        HashMap<String, String> hashmap = new HashMap<String, String>();
        hashmap.put("姓名", "王二");
        hashmap.put("年龄", "27");
        hashmap.put("工龄", "6");

        return hashmap;
    }
}
```

![](http://image.ownit.top/csdn/161f3cdecbb9477090393915924bc0e3.png)

 ![](http://image.ownit.top/csdn/43bffd71f45a409faba66be30018141f.png)

 ![](http://image.ownit.top/csdn/06f31db642b146638f8b51d9a37291b3.png)

 ![](http://image.ownit.top/csdn/1635d0a85ba443b69fef5111a81531bf.png)![](http://image.ownit.top/csdn/cae4583ceb0742228853fafc42f93f4c.png)

# 总结 

Spring Boot应用可以通过向Consul注册自身来实现服务发现和治理，使得其他服务可以在Consul中发现并调用它。

 

文档：

<https://www.cnblogs.com/qingyunye/p/12932493.html>

[一篇文章了解Consul服务发现实现原理 | Harries Blog™](http://www.liuhaihua.cn/archives/546262.html "一篇文章了解Consul服务发现实现原理 | Harries Blog™")