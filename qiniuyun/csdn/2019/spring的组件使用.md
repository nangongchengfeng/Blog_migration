---
author: 南宫乘风
categories:
- java
date: 2019-08-21 15:07:21
description: 源代码下载：组件扫描：表示这个类需要在应用程序中被创建：自动发现应用程序中被创建的类自动装配：自动满足之间的依赖定义配置类：表示当前类是一个配置类的使用方法：用在构造函数上多种依赖的情况下：用在成员变。。。。。。。
image: ../../title_pic/57.jpg
slug: '201908211507'
tags:
- spring
title: spring的组件使用
---

<!--more-->

### ![](../../image/20190821150448606.png)

### 源代码下载：<https://www.lanzous.com/i5p4mvc>

 

###  \* 组件扫描  
\* \@Component：表示这个类需要在应用程序中被创建  
\* \@ComponentScan：自动发现应用程序中被创建的类  
\*  
\* 自动装配  
\* \@Autowired：自动满足bean之间的依赖  
\*  
\* 定义配置类  
\* \@Configuration：表示当前类是一个配置类

 

 

### \* \@Autowired的使用方法  
\* 1：用在构造函数上（多种依赖的情况下）  
\* 2：用在成员变量上  
\* 3：用在setter方法上  
\* 4：用在任意方法上

 

### \* 使用单元测试的方案  
\*  
\* 引入Spring单元测试模块  
\* maven：junit，spring-test  
\*  
\* \@RunWith\(SpringJUnit4ClassRunner.class\) 加载配置类  
\* \@ContextConfiguration\(class=AppConfig.class\)