+++
author = "南宫乘风"
title = "Maven+SSM框架，实现单表简单的增删改查"
date = "2019-09-16 20:26:56"
tags=[]
categories=['Java']
image = "post/4kdongman/49.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100899244](https://blog.csdn.net/heian_99/article/details/100899244)

**目录**

[1.创建web Maven项目](#1.%E5%88%9B%E5%BB%BAweb%20Maven%E9%A1%B9%E7%9B%AE)

[2.创建java源码文件和resources资源文件](#2.%E5%88%9B%E5%BB%BAjava%E6%BA%90%E7%A0%81%E6%96%87%E4%BB%B6%E5%92%8Cresources%E8%B5%84%E6%BA%90%E6%96%87%E4%BB%B6)

[3.创建数据库配置文件：jdbc.properties](#2.%E5%88%9B%E5%BB%BA%E6%95%B0%E6%8D%AE%E5%BA%93%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9Ajdbc.properties)

[4.项目总体目录：](#3.%E9%A1%B9%E7%9B%AE%E6%80%BB%E4%BD%93%E7%9B%AE%E5%BD%95%EF%BC%9A)

[5.添加spring配置文件：applicationContext.xml](#4.%E6%B7%BB%E5%8A%A0spring%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9AapplicationContext.xml)

[6.添加springMVC配置文件：springMVC.xml](#5.%E6%B7%BB%E5%8A%A0springMVC%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%EF%BC%9AspringMVC.xml)

[7.修改web.xml](#7.%E4%BF%AE%E6%94%B9web.xml)

[8.创建数据库相关表](#8.%E5%88%9B%E5%BB%BA%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9B%B8%E5%85%B3%E8%A1%A8)

[9.根据数据库表创建pojo类：User.java](#7.%E6%A0%B9%E6%8D%AE%E6%95%B0%E6%8D%AE%E5%BA%93%E8%A1%A8%E5%88%9B%E5%BB%BApojo%E7%B1%BB%EF%BC%9AUser.java)

[10.编写dao层-&gt;mapper接口和xml文件 ：UserMapper.java、UserMapper.xml](#10.%E7%BC%96%E5%86%99dao%E5%B1%82-%3Emapper%E6%8E%A5%E5%8F%A3%E5%92%8Cxml%E6%96%87%E4%BB%B6%20%EF%BC%9AUserMapper.java%E3%80%81UserMapper.xml)

[11.编写service层-&gt;UserService.java、UserServiceImpl.java](#11.%E7%BC%96%E5%86%99service%E5%B1%82-%3EUserService.java%E3%80%81UserServiceImpl.java)

[12.编写controller层-&gt;UserController.java](#12.%E7%BC%96%E5%86%99controller%E5%B1%82-%3EUserController.java)

[13.在jsp文件夹下创建edit.jsp和view.jsp](#13.%E5%9C%A8jsp%E6%96%87%E4%BB%B6%E5%A4%B9%E4%B8%8B%E5%88%9B%E5%BB%BAedit.jsp%E5%92%8Cview.jsp)

[14.配置tomcat，启动服务器（记得加载项目名）](#14.%E9%85%8D%E7%BD%AEtomcat%EF%BC%8C%E5%90%AF%E5%8A%A8%E6%9C%8D%E5%8A%A1%E5%99%A8%EF%BC%88%E8%AE%B0%E5%BE%97%E5%8A%A0%E8%BD%BD%E9%A1%B9%E7%9B%AE%E5%90%8D%EF%BC%89)

[15.查看运行结果（已经成功）](#15.%E6%9F%A5%E7%9C%8B%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C%EF%BC%88%E5%B7%B2%E7%BB%8F%E6%88%90%E5%8A%9F%EF%BC%89)

[16.项目源码](#16.%E9%A1%B9%E7%9B%AE%E6%BA%90%E7%A0%81)

前言：学习maven后，感觉很厉害就搭建个项目小项目玩玩。

功能：实现表的增删改查

工具：IDEA    jdk 1.8   mysql  

整体项目结构：

![2019091620011890.png](https://img-blog.csdnimg.cn/2019091620011890.png)

### 1.创建web Maven项目

![20190916195653894.png](https://img-blog.csdnimg.cn/20190916195653894.png)

![2019091619584781.png](https://img-blog.csdnimg.cn/2019091619584781.png)

![20190916195913390.png](https://img-blog.csdnimg.cn/20190916195913390.png)

![20190916195940401.png](https://img-blog.csdnimg.cn/20190916195940401.png)

，接下来在pom文件加入项目所需依赖：

```
 &lt;dependencies&gt;
    &lt;!--Spring框架核心库 --&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;org.springframework&lt;/groupId&gt;
      &lt;artifactId&gt;spring-context&lt;/artifactId&gt;
      &lt;version&gt;4.2.4.RELEASE&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;org.springframework&lt;/groupId&gt;
      &lt;artifactId&gt;spring-tx&lt;/artifactId&gt;
      &lt;version&gt;4.2.4.RELEASE&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!-- Spring Web --&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;org.springframework&lt;/groupId&gt;
      &lt;artifactId&gt;spring-webmvc&lt;/artifactId&gt;
      &lt;version&gt;4.2.4.RELEASE&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!--连接驱动--&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;mysql&lt;/groupId&gt;
      &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
      &lt;version&gt;5.1.46&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!--数据源--&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;com.alibaba&lt;/groupId&gt;
      &lt;artifactId&gt;druid&lt;/artifactId&gt;
      &lt;version&gt;1.1.10&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!-- mybatis ORM框架 --&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
      &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
      &lt;version&gt;3.4.1&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!--mybatis-spring适配器 --&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
      &lt;artifactId&gt;mybatis-spring&lt;/artifactId&gt;
      &lt;version&gt;1.3.0&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!--整合mybatis如果不加这个包会报错 java.lang.NoClassDefFoundError: org/springframewor--&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;org.springframework&lt;/groupId&gt;
      &lt;artifactId&gt;spring-jdbc&lt;/artifactId&gt;
      &lt;version&gt;4.2.4.RELEASE&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;!--测试--&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;junit&lt;/groupId&gt;
      &lt;artifactId&gt;junit&lt;/artifactId&gt;
      &lt;version&gt;4.12&lt;/version&gt;
      &lt;scope&gt;test&lt;/scope&gt;
    &lt;/dependency&gt;
    &lt;!--引入JSTL标签--&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;javax.servlet&lt;/groupId&gt;
      &lt;artifactId&gt;jstl&lt;/artifactId&gt;
      &lt;version&gt;1.2&lt;/version&gt;
    &lt;/dependency&gt;
    &lt;dependency&gt;
      &lt;groupId&gt;taglibs&lt;/groupId&gt;
      &lt;artifactId&gt;standard&lt;/artifactId&gt;
      &lt;version&gt;1.1.2&lt;/version&gt;
    &lt;/dependency&gt;

  &lt;/dependencies&gt;

```

### <a name="t1"></a>2.创建java源码文件和resources资源文件

![20190916200434156.png](https://img-blog.csdnimg.cn/20190916200434156.png)

![20190916200522425.png](https://img-blog.csdnimg.cn/20190916200522425.png)

### 3.创建数据库配置文件：jdbc.properties

resources目录下添加：jdbc.properties

```
#数据库配置文件
jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/test?useUnicode=true&amp;characterEncoding=utf8
jdbc.username=root
jdbc.password=root
```

### <a name="t2"></a>4.项目总体目录：

先给出项目总体目录

创建好java目录下的分层的包，resources下创建存放mapper的包，WEB-INF下创建jsp放跳转的页面（下面的配置文件中会配置这些路径）

![20190916200721919.png](https://img-blog.csdnimg.cn/20190916200721919.png)

### <a name="t3"></a>5.添加spring配置文件：applicationContext.xml

resources目录下添加：applicationContext.xml

```
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd
     http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd"&gt;

    &lt;!-- 导入数据库配置文件 --&gt;
    &lt;context:property-placeholder location="classpath:jdbc.properties"/&gt;
    &lt;!-- 扫描包  这里的包需要根据自己java目录下的包名修改 --&gt;
    &lt;context:component-scan base-package="com.demo.service" /&gt;
    &lt;!-- 配置数据库连接池 --&gt;
    &lt;bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource"&gt;
        &lt;!-- 基本属性 url、user、password --&gt;
        &lt;property name="url" value="${jdbc.url}" /&gt;
        &lt;property name="username" value="${jdbc.username}" /&gt;
        &lt;property name="password" value="${jdbc.password}" /&gt;

    &lt;/bean&gt;

    &lt;!--Mybatis的SessionFactory配置--&gt;
    &lt;bean id="sqlSession" class="org.mybatis.spring.SqlSessionFactoryBean"&gt;
        &lt;property name="typeAliasesPackage" value="com.demo.pojo" /&gt;
        &lt;property name="dataSource" ref="dataSource"/&gt;
        &lt;property name="mapperLocations" value="classpath:mapper/*.xml"/&gt;

    &lt;/bean&gt;

    &lt;!--Mybatis的Mapper文件识别--&gt;
    &lt;bean class="org.mybatis.spring.mapper.MapperScannerConfigurer"&gt;
        &lt;property name="basePackage" value="com.demo.dao"/&gt;
    &lt;/bean&gt;

&lt;/beans&gt;
```

### <a name="t4"></a>6.添加springMVC配置文件：springMVC.xml

resources目录下添加：springMVC.xml，并且根据文件中‘视图定位’的配置，所以在WEB-INF下创建jsp文件夹

```
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-3.0.xsd
        http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-3.2.xsd"&gt;


    &lt;context:component-scan base-package="com.demo.controller" /&gt;
    &lt;!--
        配置如果没有&lt;mvc:annotation-driven/&gt;，
        那么所有的Controller可能就没有解析，所有当有请求时候都没有匹配的处理请求类，
        就都去&lt;mvc:default-servlet-handler/&gt;即default servlet处理了。
        添加上&lt;mvc:annotation-driven/&gt;后，
        相应的do请求被Controller处理，而静态资源因为没有相应的Controller就会被default servlet处理。
        总之没有相应的Controller就会被default servlet处理就ok了。
    --&gt;
    &lt;mvc:annotation-driven /&gt;
    &lt;!--开通静态资源的访问--&gt;
    &lt;mvc:default-servlet-handler /&gt;

    &lt;!-- 视图定位 --&gt;
    &lt;bean class="org.springframework.web.servlet.view.InternalResourceViewResolver"&gt;
        &lt;property name="viewClass" value="org.springframework.web.servlet.view.JstlView" /&gt;
        &lt;property name="prefix" value="/WEB-INF/view/" /&gt;
        &lt;property name="suffix" value=".jsp" /&gt;
    &lt;/bean&gt;

&lt;/beans&gt;
```

### <a name="t5"></a>7.修改web.xml

```
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns="http://java.sun.com/xml/ns/javaee"
         xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
         version="2.5"&gt;

  &lt;!-- spring的配置文件--&gt;
  &lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;classpath:applicationContext.xml&lt;/param-value&gt;
  &lt;/context-param&gt;
  &lt;listener&gt;
    &lt;listener-class&gt;org.springframework.web.context.ContextLoaderListener&lt;/listener-class&gt;
  &lt;/listener&gt;

  &lt;!--中文过滤器--&gt;
  &lt;filter&gt;
    &lt;filter-name&gt;CharacterEncodingFilter&lt;/filter-name&gt;
    &lt;filter-class&gt;org.springframework.web.filter.CharacterEncodingFilter&lt;/filter-class&gt;
    &lt;init-param&gt;
      &lt;param-name&gt;encoding&lt;/param-name&gt;
      &lt;param-value&gt;utf-8&lt;/param-value&gt;
    &lt;/init-param&gt;
  &lt;/filter&gt;
  &lt;filter-mapping&gt;
    &lt;filter-name&gt;CharacterEncodingFilter&lt;/filter-name&gt;
    &lt;url-pattern&gt;/*&lt;/url-pattern&gt;
  &lt;/filter-mapping&gt;

  &lt;!-- spring mvc核心：分发servlet --&gt;
  &lt;servlet&gt;
    &lt;servlet-name&gt;mvc-dispatcher&lt;/servlet-name&gt;
    &lt;servlet-class&gt;org.springframework.web.servlet.DispatcherServlet&lt;/servlet-class&gt;
    &lt;!-- spring mvc的配置文件 --&gt;
    &lt;init-param&gt;
      &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
      &lt;param-value&gt;classpath:springMVC.xml&lt;/param-value&gt;
    &lt;/init-param&gt;
    &lt;load-on-startup&gt;1&lt;/load-on-startup&gt;
  &lt;/servlet&gt;
  &lt;servlet-mapping&gt;
    &lt;servlet-name&gt;mvc-dispatcher&lt;/servlet-name&gt;
    &lt;url-pattern&gt;/&lt;/url-pattern&gt;
  &lt;/servlet-mapping&gt;

&lt;/web-app&gt;
```

### <a name="t6"></a>8.创建数据库相关表

 

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

```
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

### 10.编写dao层-&gt;mapper接口和xml文件 ：UserMapper.java、UserMapper.xml

UserMapper.xml放在resources\mapper下，UserMapper.java放在com.demo.dao这个包下：

注意namespace="com.demo.dao.UserMapper"，这里一定写对应的mapper接口具体路径

UserMapper接口的编写规则：

  (1）方法名和对应的mapper配置文件中查询语句的id相同

（2）返回类型和resultType的类型一致，没有就是void。

（3）方法中的参数列表中的类型和parameterType一致。

（4）mapper配置文件的namespace对应mapper接口类的全路径。

 

UserMapper.java

```
package com.demo.dao;

import com.demo.pojo.User;

import java.util.List;

public interface UserMapper {

    List&lt;User&gt; list();

    void del(int id);

    void update(User user);

    void add(User user);

    User get(int id);

}
```

 

UserMapper.xml

 

```
&lt;?xml version="1.0" encoding="UTF-8" ?&gt;
&lt;!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" &gt;
&lt;mapper namespace="com.demo.dao.UserMapper" &gt;

    &lt;select id="list" resultType="user"&gt;
    select * from user
  &lt;/select&gt;

    &lt;update id="update" parameterType="user"&gt;
     update user set name=#{name} ,password=#{password} where id=#{id}
  &lt;/update&gt;

    &lt;insert id="add" parameterType="user"&gt;
     insert into user values (null,#{name},#{password});
  &lt;/insert&gt;

    &lt;delete id="del"&gt;
    delete from user where id=#{id}
  &lt;/delete&gt;

    &lt;select id="get" resultType="user"&gt;
    select * from user where id =#{id}
  &lt;/select&gt;

&lt;/mapper&gt;
```

 

### <a name="t9"></a>11.编写service层-&gt;UserService.java、UserServiceImpl.java

 

UserService.java

```
package com.demo.service;

import com.demo.pojo.User;

import java.util.List;

public interface UserService {

    List&lt;User&gt; list();
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
    public List&lt;User&gt; list() {
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

### <a name="t10"></a>12.编写controller层-&gt;UserController.java

```
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
        List&lt;User&gt; us= userService.list();
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

### <a name="t11"></a>13.在jsp文件夹下创建edit.jsp和view.jsp

edit.jsp

```
&lt;%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Title&lt;/title&gt;
    &lt;style&gt;
        #edit{width:300px;height:500px;margin: 100px auto}
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div id="edit"&gt;
    &lt;form action="/update"&gt;
        姓名：&lt;input type="text" name="name" value="${user.name}"/&gt;&lt;br/&gt;
        密码：&lt;input type="text" name="password" value="${user.password}"/&gt;&lt;br/&gt;
        &lt;input type="hidden" value="${user.id}" name="id"&gt;
        &lt;button type="submit" value=""&gt;修改&lt;/button&gt;
    &lt;/form&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;
```

view.jsp

```
&lt;%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %&gt;
&lt;%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Title&lt;/title&gt;
    &lt;style&gt;
        table,table tr th, table tr td { border:1px solid rgba(41, 36, 35, 0.96); }
        #mytable{width:300px;margin: 100px auto}
        #add{width:300px;height:500px;margin: 100px auto}
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div id="list"&gt;
    &lt;table id="mytable"&gt;
        &lt;thead&gt;
        &lt;th&gt;id&lt;/th&gt;
        &lt;th&gt;名字&lt;/th&gt;
        &lt;th&gt;密码&lt;/th&gt;
        &lt;th&gt;修改&lt;/th&gt;
        &lt;th&gt;删除&lt;/th&gt;
        &lt;/thead&gt;
        &lt;tbody&gt;
        &lt;c:forEach items="${us}" var="user"&gt;
            &lt;tr&gt;
                &lt;td&gt;${user.id}&lt;/td&gt;
                &lt;td&gt;${user.name}&lt;/td&gt;
                &lt;td&gt;${user.password}&lt;/td&gt;
                &lt;td&gt;&lt;a href="editUI?id=${user.id}"&gt;edit&lt;/a&gt; &lt;/td&gt;
                &lt;td&gt;&lt;a href="del?id=${user.id}"&gt;delete&lt;/a&gt;&lt;/td&gt;
            &lt;/tr&gt;
        &lt;/c:forEach&gt;
        &lt;/tbody&gt;
    &lt;/table&gt;
&lt;/div&gt;

&lt;div id="add"&gt;
    &lt;form action="/add"&gt;
        姓名：&lt;input type="text" name="name" value=""/&gt;&lt;br/&gt;
        密码：&lt;input type="text" name="password" value=""/&gt;&lt;br/&gt;
        &lt;button type="submit"&gt;添加&lt;/button&gt;
    &lt;/form&gt;
&lt;/div&gt;


&lt;/body&gt;
&lt;/html&gt;
```

最后把index.jsp内容修改为:

```
&lt;%@ page contentType="text/html;charset=UTF-8" language="java" isELIgnored="false" %&gt;
&lt;html&gt;
&lt;head&gt;
    &lt;title&gt;Title&lt;/title&gt;

&lt;/head&gt;
&lt;body&gt;
&lt;%
    response.sendRedirect(request.getContextPath()+"/list");
%&gt;
&lt;/body&gt;
&lt;/html&gt;
```

### <a name="t12"></a>14.配置tomcat，启动服务器（记得加载项目名）

![20190916201828767.png](https://img-blog.csdnimg.cn/20190916201828767.png)

 

### 15.查看运行结果（已经成功）

![20190916201954460.png](https://img-blog.csdnimg.cn/20190916201954460.png)

 

![20190916202024955.png](https://img-blog.csdnimg.cn/20190916202024955.png)

### 16.项目源码

源码+sql：[https://www.lanzous.com/i679e2d](https://www.lanzous.com/i679e2d)

如果有什么问题，可以私聊我，看见解决

欢迎不会的可以相互交流。

交流群：629383010（免费）

 

 
