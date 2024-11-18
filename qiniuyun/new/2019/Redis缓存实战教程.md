---
author: 南宫乘风
categories:
- Java
date: 2019-10-28 10:10:11
description: 目录缓存使用缓存解决首页并发问题、缓存使用的简单设计、的整合步骤将整合到项目中将整合到项目中设计一个数据存储策越设计一个数据存储策越、的整合过程、引入依赖信息将本工程所有的统一放入里、写一个的工具类用。。。。。。。
image: http://image.ownit.top/4kdongman/81.jpg
tags:
- 技术记录
title: Redis缓存实战教程
---

<!--more-->

**目录**

 

[Redis缓存](#Redis%E7%BC%93%E5%AD%98)

[使用缓存Redis解决首页并发问题](#%E4%BD%BF%E7%94%A8%E7%BC%93%E5%AD%98Redis%E8%A7%A3%E5%86%B3%E9%A6%96%E9%A1%B5%E5%B9%B6%E5%8F%91%E9%97%AE%E9%A2%98)

[1、缓存使用的简单设计](#1%E3%80%81%E7%BC%93%E5%AD%98%E4%BD%BF%E7%94%A8%E7%9A%84%E7%AE%80%E5%8D%95%E8%AE%BE%E8%AE%A1)

[2、Redis的整合步骤](#2%E3%80%81Redis%E7%9A%84%E6%95%B4%E5%90%88%E6%AD%A5%E9%AA%A4)

[A 将Redis整合到项目中（Redis+Spring）](<#A 将Redis整合到项目中（Redis+Spring）>)

[B 设计一个数据存储策越](<#B 设计一个数据存储策越>)

[3、Redis的整合过程](#3%E3%80%81Redis%E7%9A%84%E6%95%B4%E5%90%88%E8%BF%87%E7%A8%8B)

 

[1、引入pom依赖信息（将本工程所有的Redis统一放入service-util里）](#1%E3%80%81%E5%BC%95%E5%85%A5pom%E4%BE%9D%E8%B5%96%E4%BF%A1%E6%81%AF%EF%BC%88%E5%B0%86%E6%9C%AC%E5%B7%A5%E7%A8%8B%E6%89%80%E6%9C%89%E7%9A%84Redis%E7%BB%9F%E4%B8%80%E6%94%BE%E5%85%A5service-util%E9%87%8C%EF%BC%89)

[2、写一个Redis的工具类（用来将Redis的池初始化到spring容器）](#2%E3%80%81%E5%86%99%E4%B8%80%E4%B8%AARedis%E7%9A%84%E5%B7%A5%E5%85%B7%E7%B1%BB%EF%BC%88%E7%94%A8%E6%9D%A5%E5%B0%86Redis%E7%9A%84%E6%B1%A0%E5%88%9D%E5%A7%8B%E5%8C%96%E5%88%B0spring%E5%AE%B9%E5%99%A8%EF%BC%89)

[3、写一个spring整合Redis的配置类](#3%E3%80%81%E5%86%99%E4%B8%80%E4%B8%AAspring%E6%95%B4%E5%90%88Redis%E7%9A%84%E9%85%8D%E7%BD%AE%E7%B1%BB)

[4、每隔引用工程引入service-util后，单独配置只能的redis的配置文件](#4%E3%80%81%E6%AF%8F%E9%9A%94%E5%BC%95%E7%94%A8%E5%B7%A5%E7%A8%8B%E5%BC%95%E5%85%A5service-util%E5%90%8E%EF%BC%8C%E5%8D%95%E7%8B%AC%E9%85%8D%E7%BD%AE%E5%8F%AA%E8%83%BD%E7%9A%84redis%E7%9A%84%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6)

 

[代码](#%E4%BB%A3%E7%A0%81)

[查询结果](#%E6%9F%A5%E8%AF%A2%E7%BB%93%E6%9E%9C)

[查看Redis数据库的数据](#%E6%9F%A5%E7%9C%8BRedis%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9A%84%E6%95%B0%E6%8D%AE)

 

---

# Redis缓存

重点要讲的是另外一个层面：尽量避免直接查询数据库。

解决办法就是：缓存

缓存可以理解是数据库的一道保护伞，任何请求只要能在缓存中命中，都不会直接访问数据库。而缓存的处理性能是数据库10-100倍。

## 使用缓存Redis解决首页并发问题

1.  用户第一次请求到redis
2.  如果redis没有数据，redis会请求mysql
3.  mysql会把数据返回给用户，同时会传到redis上
4.  第二次用户访问时，redis有数据，就不需要访问mysql。节省时间，降低消耗

 

 

![](http://image.ownit.top/csdn/2019102809542253.png)

## 1、缓存使用的简单设计

![](http://image.ownit.top/csdn/20191028095442596.png)

1.  连接缓存
2.  查询缓存
3.  如果缓存没有，查询mysql
4.  mysql查询结果存入redis

 

## 2、Redis的整合步骤

 

### A 将Redis整合到项目中（Redis+Spring）

 

![](http://image.ownit.top/csdn/20191028095521514.png)

## B 设计一个数据存储策越

 

企业中的存储策越（核心是：如何设计k）

数据对象名：数据对象id：对象属性

User:123:password 用户ID为123的密码

User:123:userename 用户ID为123的名字

 

## 3、Redis的整合过程

 

### 1、引入pom依赖信息（将本工程所有的Redis统一放入service-util里）

 

```java
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
</dependency>
```

创建两个类RedisConfig和RedisUtil

RedisConfig负责在spring容器启动时自动注入，而RedisUtil就是被注入的工具类以供其他模块调用。

### 2、写一个Redis的工具类（用来将Redis的池初始化到spring容器）

**RedisUtil**

```java
public class RedisUtil {

    private  JedisPool jedisPool;

    public void initPool(String host,int port ,int database){
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(200);
        poolConfig.setMaxIdle(30);
        poolConfig.setBlockWhenExhausted(true);
        poolConfig.setMaxWaitMillis(10*1000);
        poolConfig.setTestOnBorrow(true);
        jedisPool=new JedisPool(poolConfig,host,port,20*1000);
    }

    public Jedis getJedis(){
        Jedis jedis = jedisPool.getResource();
        return jedis;
    }

}
```

 

 

### 3、写一个spring整合Redis的配置类

将Redis的链接池创建到spring的容器中

**RedisConfig**

 

```java
@Configuration
public class RedisConfig {

    //读取配置文件中的redis的ip地址
    @Value("${spring.redis.host:disabled}")
    private String host;

    @Value("${spring.redis.port:0}")
    private int port;

    @Value("${spring.redis.database:0}")
    private int database;

    @Bean
    public RedisUtil getRedisUtil(){
        if(host.equals("disabled")){
            return null;
        }
        RedisUtil redisUtil=new RedisUtil();
        redisUtil.initPool(host,port,database);
        return redisUtil;
    }

}
```

### 4、每隔引用工程引入service-util后，单独配置只能的redis的配置文件

 

Service-util的配置文件没有作用

同时，任何模块想要调用redis都必须在application.properties配置，否则不会进行注入

```java
#Redis配置
//读取配置文件中的redis的ip地址
spring.redis.host=192.168.1.111
#Redis端口号
spring.redis.port=6379
#数据库
spring.redis.database=0
```

## 代码

这是从数据库调用mysql，查询数据

```java
 /**
     * 从数据库调用
     *
     * @param skuId
     * @return
     */
    public PmsSkuInfo getSkuByIdFromDb(String skuId) {
        //sku的商品对象
        PmsSkuInfo pmsSkuInfo = new PmsSkuInfo();
        pmsSkuInfo.setId(skuId);
        PmsSkuInfo skuInfo = pmsSkuInfoMapper.selectOne(pmsSkuInfo);

        try {
            //sku的图片集合
            PmsSkuImage pmsSkuImage = new PmsSkuImage();
            List<PmsSkuImage> pmsSkuImages = pmsSkuImageMapper.select(pmsSkuImage);
            skuInfo.setSkuImageList(pmsSkuImages);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return skuInfo;

    }
```

这个是Redis的代码，判断redis中是否有数据，

如果没有，就调用上面的代码，查询mysql数据库。返回结果，在写入redis数据库中。

如果有，直接调用redis数据库中的数据。

```java
/**
     * 商品详细图
     * 主要是item前端的东西，调用此处的服务，方便
     * 使用Redis缓存，解决高并发
     *
     * @param skuId
     * @return
     */
    @Override
    public PmsSkuInfo getSkuById(String skuId) {

        PmsSkuInfo pmsSkuInfo = new PmsSkuInfo();

        //链接缓存
        Jedis jedis = redisUtil.getJedis();

        //查询缓存
        String skuKey = "sky:" + skuId + ":info";
        String skuJson = jedis.get("skuKey");
        //可以吧json的字符串转换成jav的对象类
        if (StringUtils.isNotBlank(skuJson)) {// if (skuJson!=null&&!skuJson.equals(""))
            pmsSkuInfo = JSON.parseObject(skuJson, PmsSkuInfo.class);
        } else {
            //如果缓存没有，查询mysql
            pmsSkuInfo = getSkuByIdFromDb(skuId);

            if (pmsSkuInfo != null) {
                //mysql查询结果存入redis
                jedis.set("sku" + skuId + ":info", JSON.toJSONString(pmsSkuInfo));
            }
        }


        jedis.close();

        return pmsSkuInfo;
    }
```

## 查询结果

![](http://image.ownit.top/csdn/20191028100509713.png)

 

## 查看Redis数据库的数据

 

![](http://image.ownit.top/csdn/20191028100711216.png)