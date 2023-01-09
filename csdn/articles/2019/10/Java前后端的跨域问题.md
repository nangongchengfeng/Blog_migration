+++
author = "南宫乘风"
title = "Java前后端的跨域问题"
date = "2019-10-08 17:57:15"
tags=[]
categories=['Java']
image = "post/4kdongman/90.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/102400260](https://blog.csdn.net/heian_99/article/details/102400260)

### **1 前端127.0.0.1:8888**

### **2 后端127.0.0.1:8080**

### **前端和后端因为来自不同的网域，所以在http的安全协议策略下，不信任**

### **![20191008175356195.png](https://img-blog.csdnimg.cn/20191008175356195.png)**

### **3 解决方案，在springmvc的控制层加入`@CrossOrigin跨域访问的注解`**

### **![20191008175549870.png](https://img-blog.csdnimg.cn/20191008175549870.png)![20191008175422648.png](https://img-blog.csdnimg.cn/20191008175422648.png)**

### **![20191008175637625.png](https://img-blog.csdnimg.cn/20191008175637625.png)**

 
