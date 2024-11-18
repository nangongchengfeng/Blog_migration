---
author: 南宫乘风
categories:
- Java
date: 2019-09-16 20:26:56
description: 目录创建项目创建项目创建源码文件和资源文件创建数据库配置文件：项目总体目录：添加配置文件：添加配置文件：修改创建数据库相关表根据数据库表创建类：编写层接口和文件：、编写层接口和文件：、编写层、编写层在。。。。。。。
image: http://image.ownit.top/4kdongman/26.jpg
tags:
- 技术记录
title: Maven+SSM框架，实现单表简单的增删改查
---

<!--more-->

**目录**

[1.创建web Maven项目](<#1.创建web Maven项目>)

[2.创建java源码文件和resources资源文件](#2.%E5%88%9B%E5%BB%BAjava%E6%BA%90%E7%A0%81%E6%96%87%E4%BB%B6%E5%92%8Cresources%E8%B5%84%E6%BA%90%E6%96%87%E4%BB%B6)

[3.创建数据库配置文件：jdbc.properties](#2.%E5%88%9B%E5%BB%BA%E6%95%B0%E6%8D%AE%E5%BA%93%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9Ajdbc.properties)

[4.项目总体目录：](#3.%E9%A1%B9%E7%9B%AE%E6%80%BB%E4%BD%93%E7%9B%AE%E5%BD%95%EF%BC%9A)

[5.添加spring配置文件：applicationContext.xml](#4.%E6%B7%BB%E5%8A%A0spring%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9AapplicationContext.xml)

[6.添加springMVC配置文件：springMVC.xml](#5.%E6%B7%BB%E5%8A%A0springMVC%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9AspringMVC.xml)

[7.修改web.xml](#7.%E4%BF%AE%E6%94%B9web.xml)

[8.创建数据库相关表](#8.%E5%88%9B%E5%BB%BA%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9B%B8%E5%85%B3%E8%A1%A8)

[9.根据数据库表创建pojo类：User.java](#7.%E6%A0%B9%E6%8D%AE%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%88%9B%E5%BB%BApojo%E7%B1%BB%EF%BC%9AUser.java)

[10.编写dao层->mapper接口和xml文件 ：UserMapper.java、UserMapper.xml](<#10.编写dao层->mapper接口和xml文件 ：UserMapper.java、UserMapper.xml>)

[11.编写service层->UserService.java、UserServiceImpl.java](#11.%E7%BC%96%E5%86%99service%E5%B1%82-%3EUserService.java%E3%80%81UserServiceImpl.java)

[12.编写controller层->UserController.java](#12.%E7%BC%96%E5%86%99controller%E5%B1%82-%3EUserController.java)

[13.在jsp文件夹下创建edit.jsp和view.jsp](#13.%E5%9C%A8jsp%E6%96%87%E4%BB%B6%E5%A4%B9%E4%B8%8B%E5%88%9B%E5%BB%BAedit.jsp%E5%92%8Cview.jsp)

[14.配置tomcat，启动服务器（记得加载项目名）](#14.%E9%85%8D%E7%BD%AEtomcat%EF%BC%8C%E5%90%AF%E5%8A%A8%E6%9C%8D%E5%8A%A1%E5%99%A8%EF%BC%88%E8%AE%B0%E5%BE%97%E5%8A%A0%E8%BD%BD%E9%A1%B9%E7%9B%AE%E5%90%8D%EF%BC%89)

[15.查看运行结果（已经成功）](#15.%E6%9F%A5%E7%9C%8B%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C%EF%BC%88%E5%B7%B2%E7%BB%8F%E6%88%90%E5%8A%9F%EF%BC%89)

[16.项目源码](#16.%E9%A1%B9%E7%9B%AE%E6%BA%90%E7%A0%81)

---

前言：学习maven后，感觉很厉害就搭建个项目小项目玩玩。

功能：实现表的增删改查

工具：IDEA    jdk 1.8   mysql  

整体项目结构：

![](http://image.ownit.top/csdn/2019091620011890.png)

### 1.创建web Maven项目

![](http://image.ownit.top/csdn/20190916195653894.png)

![](http://image.ownit.top/csdn/2019091619584781.png)

![](http://image.ownit.top/csdn/20190916195913390.png)

![](http://image.ownit.top/csdn/20190916195940401.png)

，接下来在pom文件加入项目所需依赖：

```java
 <dependencies>
    <!--Spring框架核心库 -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>4.2.4.RELEASE</version>
    </dependency>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-tx</artifactId>
      <version>4.2.4.RELEASE</version>
    </dependency>
    <!-- Spring Web -->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-webmvc</artifactId>
      <version>4.2.4.RELEASE</version>
    </dependency>
    <!--连接驱动-->
    <dependency>
      <groupId>mysql</groupId>
      <artifactId>mysql-connector-java</artifactId>
      <version>5.1.46</version>
    </dependency>
    <!--数据源-->
    <dependency>
      <groupId>com.alibaba</groupId>
      <artifactId>druid</artifactId>
      <version>1.1.10</version>
    </dependency>
    <!-- mybatis ORM框架 -->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis</artifactId>
      <version>3.4.1</version>
    </dependency>
    <!--mybatis-spring适配器 -->
    <dependency>
      <groupId>org.mybatis</groupId>
      <artifactId>mybatis-spring</artifactId>
      <version>1.3.0</version>
    </dependency>
    <!--整合mybatis如果不加这个包会报错 java.lang.NoClassDefFoundError: org/springframewor-->
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-jdbc</artifactId>
      <version>4.2.4.RELEASE</version>
    </dependency>
    <!--测试-->
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.12</version>
      <scope>test</scope>
    </dependency>
    <!--引入JSTL标签-->
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>jstl</artifactId>
      <version>1.2</version>
    </dependency>
    <dependency>
      <groupId>taglibs</groupId>
      <artifactId>standard</artifactId>
      <version>1.1.2</version>
    </dependency>

  </dependencies>
```

### 2.创建java源码文件和resources资源文件

![](http://image.ownit.top/csdn/20190916200434156.png)

![](http://image.ownit.top/csdn/20190916200522425.png)

### 3.创建数据库配置文件：jdbc.properties

resources目录下添加：jdbc.properties

```sql
#数据库配置文件
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/test?useUnicode=true&characterEncoding=utf8
jdbc.username=root
jdbc.password=root
```

### 4.项目总体目录：

先给出项目总体目录

创建好java目录下的分层的包，resources下创建存放mapper的包，WEB-INF下创建jsp放跳转的页面（下面的配置文件中会配置这些路径）

![](http://image.ownit.top/csdn/20190916200721919.png)

### 5.添加spring配置文件：applicationContext.xml

resources目录下添加：applicationContext.xml

```java
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd
     http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

    <!-- 导入数据库配置文件 -->
    <context:property-placeholder location="classpath:jdbc.properties"/>
    <!-- 扫描包  这里的包需要根据自己java目录下的包名修改 -->
    <context:component-scan base-package="com.demo.service" />
    <!-- 配置数据库连接池 -->
    <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <!-- 基本属性 url、user、password -->
        <property name="url" value="${jdbc.url}" />
        <property name="username" value="${jdbc.username}" />
        <property name="password" value="${jdbc.password}" />

    </bean>

    <!--Mybatis的SessionFactory配置-->
    <bean id="sqlSession" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="typeAliasesPackage" value="com.demo.pojo" />
        <property name="dataSource" ref="dataSource"/>
        <property name="mapperLocations" value="classpath:mapper/*.xml"/>

    </bean>

    <!--Mybatis的Mapper文件识别-->
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="com.demo.dao"/>
    </bean>

</beans>
```

### 6.添加springMVC配置文件：springMVC.xml

resources目录下添加：springMVC.xml，并且根据文件中‘视图定位’的配置，所以在WEB-INF下创建jsp文件夹

```java
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd
        http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-3.2.xsd">


    <context:component-scan base-package="com.demo.controller" />
    <!--
        配置如果没有<mvc:annotation-driven/>，
        那么所有的Controller可能就没有解析，所有当有请求时候都没有匹配的处理请求类，
        就都去<mvc:default-servlet-handler/>即default servlet处理了。
        添加上<mvc:annotation-driven/>后，
        相应的do请求被Controller处理，而静态资源因为没有相应的Controller就会被default servlet处理。
        总之没有相应的Controller就会被default servlet处理就ok了。
    -->
    <mvc:annotation-driven />
    <!--开通静态资源的访问-->
    <mvc:default-servlet-handler />

    <!-- 视图定位 -->
    <bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <property name="viewClass" value="org.springframework.web.servlet.view.JstlView" />
        <property name="prefix" value="/WEB-INF/view/" />
        <property name="suffix" value=".jsp" />
    </bean>

</beans>
```

### 7.修改web.xml

```java
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns="http://java.sun.com/xml/ns/javaee"
         xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
         version="2.5">

  <!-- spring的配置文件-->
  <context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:applicationContext.xml</param-value>
  </context-param>
  <listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
  </listener>

  <!--中文过滤器-->
  <filter>
    <filter-name>CharacterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>utf-8</param-value>
    </init-param>
  </filter>
  <filter-mapping>
    <filter-name>CharacterEncodingFilter</filter-name>
    <url-pattern>/*</url-pattern>
  </filter-mapping>

  <!-- spring mvc核心：分发servlet -->
  <servlet>
    <servlet-name>mvc-dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <!-- spring mvc的配置文件 -->
    <init-param>
      <param-name>contextConfigLocation</param-name>
      <param-value>classpath:springMVC.xml</param-value>
    </init-param>
    <load-on-startup>1</load-on-startup>
  </servlet>
  <servlet-mapping>
    <servlet-name>mvc-dispatcher</servlet-name>
    <url-pattern>/</url-pattern>
  </servlet-mapping>

</web-app>
```

### 8.创建数据库相关表

 

```
/*
 Navicat Premium Data Transfer

 Source Server         : phpStudy
 Source Server Type    : MySQL
 Source Server Version : 50553
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 50553
 File Encoding         : 65001

 Date: 16/09/2019 19:46:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET gbk COLLATE gbk_chinese_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET gbk COLLATE gbk_chinese_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9 CHARACTER SET = gbk COLLATE = gbk_chinese_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'cheng', '128946');
INSERT INTO `user` VALUES (3, 'eff', 'f');
INSERT INTO `user` VALUES (4, 'fwefw', 'wef');
INSERT INTO `user` VALUES (8, 'fwef', '13');

SET FOREIGN_KEY_CHECKS = 1;
```

### 9.根据数据库表创建pojo类：User.java

pojo的编写规则：数据库字段对应类字段，字段类型要一直 。

```java
package com.demo.pojo;

import java.io.Serializable;

public class User implements Serializable {

    private Integer id;
    private String name;
    private String password;

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name == null ? null : name.trim();
    }
}
```

### 10.编写dao层->mapper接口和xml文件 ：UserMapper.java、UserMapper.xml

UserMapper.xml放在resources\\mapper下，UserMapper.java放在com.demo.dao这个包下：

注意namespace="com.demo.dao.UserMapper"，这里一定写对应的mapper接口具体路径

UserMapper接口的编写规则：

  \(1）方法名和对应的mapper配置文件中查询语句的id相同

（2）返回类型和resultType的类型一致，没有就是void。

（3）方法中的参数列表中的类型和parameterType一致。

（4）mapper配置文件的namespace对应mapper接口类的全路径。

 

UserMapper.java

```java
package com.demo.dao;

import com.demo.pojo.User;

import java.util.List;

public interface UserMapper {

    List<User> list();

    void del(int id);

    void update(User user);

    void add(User user);

    User get(int id);

}
```

 

UserMapper.xml

 

```java
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.demo.dao.UserMapper" >

    <select id="list" resultType="user">
    select * from user
  </select>

    <update id="update" parameterType="user">
     update user set name=#{name} ,password=#{password} where id=#{id}
  </update>

    <insert id="add" parameterType="user">
     insert into user values (null,#{name},#{password});
  </insert>

    <delete id="del">
    delete from user where id=#{id}
  </delete>

    <select id="get" resultType="user">
    select * from user where id =#{id}
  </select>

</mapper>
```

 

### 11.编写service层->UserService.java、UserServiceImpl.java

 

UserService.java

```java
package com.demo.service;

import com.demo.pojo.User;

import java.util.List;

public interface UserService {

    List<User> list();
    void del(int id);
    void update(User user);
    void add(User user);
    User get(int id);

}
```

 

UserServiceImpl.java

 

```
package com.demo.service.impl;

import com.demo.dao.UserMapper;
import com.demo.pojo.User;
import com.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserServiceImpl implements UserService{

    @Autowired
    UserMapper userMapper;
    public List<User> list() {
        return userMapper.list();
    }
    public void add(User user) {
        userMapper.add(user);
    }
    public void del(int id) {
        userMapper.del(id);
    }
    public void update(User user) {
        userMapper.update(user);
    }
    public User get(int id) {
        return userMapper.get(id);
    }


}
```

### 12.编写controller层->UserController.java

```java
package com.demo.controller;

import com.demo.pojo.User;
import com.demo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("")
public class UserController {

    @Autowired
    UserService userService;
    @RequestMapping("list")
    public String list(Model model){
        List<User> us= userService.list();
        model.addAttribute("us", us);
        return "view";
    }
    @RequestMapping("add")
    public String add(User user,Model model){
        userService.add(user);
        return "redirect:list";
    }
    @RequestMapping("del")
    public String del(int id){
        userService.del(id);
        return "redirect:list";
    }
    @RequestMapping("editUI")
    public String editUI(int id,Model model){
        User user = userService.get(id);
        model.addAttribute("user",user);
        return "edit";
    }
    @RequestMapping("update")
    public String update(User user){
        userService.update(user);
        return "redirect:list";
    }

}
```

### 13.在jsp文件夹下创建edit.jsp和view.jsp

edit.jsp

```java
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<html>
<head>
    <title>Title</title>
    <style>
        #edit{width:300px;height:500px;margin: 100px auto}
    </style>
</head>
<body>
<div id="edit">
    <form action="/update">
        姓名：<input type="text" name="name" value="${user.name}"/><br/>
        密码：<input type="text" name="password" value="${user.password}"/><br/>
        <input type="hidden" value="${user.id}" name="id">
        <button type="submit" value="">修改</button>
    </form>
</div>
</body>
</html>
```

view.jsp

```java
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head>
    <title>Title</title>
    <style>
        table,table tr th, table tr td { border:1px solid rgba(41, 36, 35, 0.96); }
        #mytable{width:300px;margin: 100px auto}
        #add{width:300px;height:500px;margin: 100px auto}
    </style>
</head>
<body>
<div id="list">
    <table id="mytable">
        <thead>
        <th>id</th>
        <th>名字</th>
        <th>密码</th>
        <th>修改</th>
        <th>删除</th>
        </thead>
        <tbody>
        <c:forEach items="${us}" var="user">
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.password}</td>
                <td><a href="editUI?id=${user.id}">edit</a> </td>
                <td><a href="del?id=${user.id}">delete</a></td>
            </tr>
        </c:forEach>
        </tbody>
    </table>
</div>

<div id="add">
    <form action="/add">
        姓名：<input type="text" name="name" value=""/><br/>
        密码：<input type="text" name="password" value=""/><br/>
        <button type="submit">添加</button>
    </form>
</div>


</body>
</html>
```

最后把index.jsp内容修改为:

```java
<%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %>
<html>
<head>
    <title>Title</title>

</head>
<body>
<%
    response.sendRedirect(request.getContextPath()+"/list");
%>
</body>
</html>
```

### 14.配置tomcat，启动服务器（记得加载项目名）

![](http://image.ownit.top/csdn/20190916201828767.png)

 

### 15.查看运行结果（已经成功）

![](http://image.ownit.top/csdn/20190916201954460.png)

 

![](http://image.ownit.top/csdn/20190916202024955.png)

### 16.项目源码

源码+sql：<https://www.lanzous.com/i679e2d>

如果有什么问题，可以私聊我，看见解决

欢迎不会的可以相互交流。

交流群：629383010（免费）