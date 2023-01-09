+++
author = "南宫乘风"
title = "spring的组件使用"
date = "2019-08-21 15:07:21"
tags=['java', 'spring']
categories=[]
image = "post/4kdongman/60.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/99963775](https://blog.csdn.net/heian_99/article/details/99963775)

### ![20190821150448606.png](https://img-blog.csdnimg.cn/20190821150448606.png)

### 源代码下载：[https://www.lanzous.com/i5p4mvc](https://www.lanzous.com/i5p4mvc)

 

###  * 组件扫描<br> * @Component：表示这个类需要在应用程序中被创建<br> * @ComponentScan：自动发现应用程序中被创建的类<br> *<br> * 自动装配<br> * @Autowired：自动满足bean之间的依赖<br> *<br> * 定义配置类<br> * @Configuration：表示当前类是一个配置类

#  

###  

### * @Autowired的使用方法<br> * 1：用在构造函数上（多种依赖的情况下）<br> * 2：用在成员变量上<br> * 3：用在setter方法上<br> * 4：用在任意方法上

 

### * 使用单元测试的方案<br> *<br> * 引入Spring单元测试模块<br> * maven：junit，spring-test<br> *<br> * @RunWith(SpringJUnit4ClassRunner.class) 加载配置类<br> * @ContextConfiguration(class=AppConfig.class)

 

 
