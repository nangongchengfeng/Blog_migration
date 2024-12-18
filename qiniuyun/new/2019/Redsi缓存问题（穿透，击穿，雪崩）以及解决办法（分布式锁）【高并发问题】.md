---
author: 南宫乘风
categories:
- Java
date: 2019-10-31 12:45:14
description: 常见问题缓存在高平发和安全压力下的一些问题缓存击穿是某一个热点在高并发访问的情况下，突然失效，导致大量的并发大金数据库的情况缓存穿透是利用和的机制缓存一旦不存在，就访问，直接让过缓存访问，而制造的请求。。。。。。。
image: http://image.ownit.top/4kdongman/53.jpg
tags:
- 技术记录
title: Redsi缓存问题（穿透，击穿，雪崩）以及解决办法（分布式锁）【高并发问题】
---

<!--more-->

# **Redsi常见问题**

**缓存在高平发和安全压力下的一些问题**

---

## **缓存击穿**

是某一个热点key在高并发访问的情况下，突然失效，导致大量的并发大金mysql数据库的情况

---

## **缓存穿透**

是利用redis和mysql的机制（redis缓存一旦不存在，就访问mysql），直接让过缓存访问mysql，而制造的db请求压力

一般在代码中防止

**解决： 为防止缓存穿透，将null或者空字符串设置给redis**

---

## **缓存雪崩**

缓存是采用了相同的过期时间，导致缓存在某一时刻同时全部失效，导致的db崩溃

**解决：设计不同的缓存失效时间**

---

## **如何解决缓存击穿的问题 ？**

**分布式锁**

 

![](http://image.ownit.top/csdn/20191031115359988.png)

**穿透：利用不存在的key去攻击mysql数据库**

**雪崩：缓存中的很多key失效，导致数据库负载过重宕机**

**击穿：在正常的访问情况下，如果缓存失效，如果保护mysql，重启缓存的过程**

**使用redis数据库的分布式锁，解决mysql的访问压力问题**

 

 

## 第一种分布式锁：redis自带一个分布式锁，set px nx

![](http://image.ownit.top/csdn/20191031115500254.png)

![](http://image.ownit.top/csdn/20191031115514354.png)

用完之后需要删除，不然别人不能访问。

![](http://image.ownit.top/csdn/20191031115530184.png)

**错误自旋代码（B为孤儿线程）**

![](http://image.ownit.top/csdn/20191031115559125.png)

**正确自旋代码**

![](http://image.ownit.top/csdn/20191031115645341.png)

 

 

**问题1 如果在redis中的锁已经过期了，然后锁过期的那个请求又执行完毕，回来删锁,删除了其他线程的锁，怎么办？**

 

**问题2 如果碰巧在查询redis锁还没删除的时候，正在网络传输时，锁过期了，怎么办？**

```java
String script ="if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";
jedis.eval(script, Collections.singletonList("lock"),Collections.singletonList(token));
```

![](http://image.ownit.top/csdn/20191031115747596.png)

## 第二种分布式锁：redisson框架，一个redis的带有juc的lock功能的客户端（既有jedis的功能，又有juc的功能）

![](http://image.ownit.top/csdn/20191031115806435.png)

### 整合

**引入pom**

```java
<!-- https://mvnrepository.com/artifact/org.redisson/redisson -->
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson</artifactId>
    <version>3.10.5</version>
</dependency>
```

**配置**

```java
spring.redis.host=192.168.159.130
spring.redis.port=6379
```

**配置类**

```java
@Configuration
public class GmallRedissonConfig {
    @Value("${spring.redis.host}")
    private String host;
    @Value("${spring.redis.port}")
    private String port;
    @Bean
    public RedissonClient redissonClient(){
        Config config = new Config();
        config.useSingleServer().setAddress("redis://"+host+":"+port);
        RedissonClient redisson = Redisson.create(config);
        return redisson;
    }
}
```

Redisson实现了juc的lock锁，并且可以在分布式的redis环境下使用

![](http://image.ownit.top/csdn/20191031115927845.png)

![](http://image.ownit.top/csdn/20191031115935544.png)

### 添加gmall-redisson-text

把需要的依赖添加的pom上

### ![](http://image.ownit.top/csdn/20191031120001347.png)

**配置application.properties**

 

 

```
# 服务端口
server.port=8082
# 日志级别
logging.level.root=info
```

**RedissonController**

```java
package com.atguigu.gmallredisson.redissonTest;
import com.atguigu.gmall.util.RedisUtil;
import org.apache.commons.lang3.StringUtils;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import redis.clients.jedis.Jedis;
@Controller
public class RedissonController {
    @Autowired
    RedisUtil redisUtil;
    @Autowired
    RedissonClient redissonClient;
    @RequestMapping("testRedisson")
    @ResponseBody
    public String testRedisson(){
        Jedis jedis = redisUtil.getJedis();
        RLock lock = redissonClient.getLock("lock");// 声明锁
        lock.lock();//上锁
        try {
            String v = jedis.get("k");
            if (StringUtils.isBlank(v)) {
                v = "1";
            }
            System.out.println("->" + v);
            jedis.set("k", (Integer.parseInt(v) + 1) + "");
        }finally {
            jedis.close();
            lock.unlock();// 解锁
    }
        return "success";
    }
}
```

### 设置非单例模式启动

![](http://image.ownit.top/csdn/20191031120107992.png)

点击取消单一示例

![](http://image.ownit.top/csdn/20191031120121350.png)

### 启动3个示例，端口分别为8080,8081,8082

![](http://image.ownit.top/csdn/20191031120134626.png)

### 配置nginx

![](http://image.ownit.top/csdn/20191031122011693.png)

##  下载安装apache测试工具\(apache\)

### 1 下载地址

<https://www.apachehaus.com/cgi-bin/download.plx>

![](http://image.ownit.top/csdn/20191031122042471.png)

### 2 安装即解压

![](http://image.ownit.top/csdn/20191031122109583.png)

### 3 修改apache服务的配置文件\(服务器的根目录\)

![](http://image.ownit.top/csdn/20191031122126492.png)

修改服务的根目录路径：

![](http://image.ownit.top/csdn/20191031122137776.png)

### 4 启动服务

查看443端口是否被占用

```
D:\ap\Apache24\bin>netstat -ano | findstr "443"
```

![](http://image.ownit.top/csdn/20191031124243606.png)

没有被占用，启动httpd.exe

```
D:\ap\Apache24\bin>httpd.exe
```

### 5 压测命令\(另起cmd输入命令\)

D:\\apache24\\bin>ab \-c 200 \-n 1000 http:nginx负载均衡/压力方法

测试：

```
D:\ap\Apache24\bin>ab -c 100 -n 10000 http://www.der-matech.com.cn/
```

![](http://image.ownit.top/csdn/20191031124434597.png)

```java
public String testRedisson(){
    Jedis jedis = redisUtil.getJedis();
    RLock lock = redissonClient.getLock("lock");// 声明锁

    lock.lock();//上锁
    try {
        String v = jedis.get("k");
        if (StringUtils.isBlank(v)) {
            v = "1";
        }
        System.out.println("->" + v);
        jedis.set("k", (Integer.parseInt(v) + 1) + "");
    }finally {
        jedis.close();
        lock.unlock();// 解锁
    }
    return "success";
}
```