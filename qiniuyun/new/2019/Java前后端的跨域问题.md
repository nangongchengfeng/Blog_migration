---
author: 南宫乘风
categories:
- Java
date: 2019-10-08 17:57:15
description: 前端后端前端和后端因为来自不同的网域，所以在的安全协议策略下，不信任解决方案，在的控制层加入跨域访问的注解。。。。。。。
image: http://image.ownit.top/4kdongman/38.jpg
tags:
- 技术记录
title: Java前后端的跨域问题
---

<!--more-->

### **1 前端127.0.0.1:8888**

### **2 后端127.0.0.1:8080**

### **前端和后端因为来自不同的网域，所以在http的安全协议策略下，不信任**

### **![](http://image.ownit.top/csdn/20191008175356195.png)**

### **3 解决方案，在springmvc的控制层加入`@CrossOrigin跨域访问的注解`**

### **![](http://image.ownit.top/csdn/20191008175549870.png)![](http://image.ownit.top/csdn/20191008175422648.png)**

### **![](http://image.ownit.top/csdn/20191008175637625.png)**