+++
author = "南宫乘风"
title = "Idea SpringBoot 对数据库实例详解"
date = "2019-12-18 17:45:19"
tags=['springboot']
categories=['Java']
image = "post/4kdongman/76.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103599750](https://blog.csdn.net/heian_99/article/details/103599750)

![20191218161129253.png](https://img-blog.csdnimg.cn/20191218161129253.png)

SpringBoot 是 SpringMVC 的升级，对于编码、配置、部署和监控，更加简单

**微服务**

Spring 为 微服务提供了一整套的组件-SpringClound , SpirngBoot 就是该基础。

![20191218161207753.png](https://img-blog.csdnimg.cn/20191218161207753.png)

# **第一个SpringBoot程序**

maven配置的中央仓库阿里云镜像

setting.xml

```
	 &lt;mirror&gt;
      &lt;id&gt;nexus-aliyun&lt;/id&gt;
      &lt;mirrorOf&gt;*&lt;/mirrorOf&gt;
      &lt;name&gt;Nexus aliyun&lt;/name&gt;
      &lt;url&gt;	https://maven.aliyun.com/nexus/content/groups/public/&lt;/url&gt;
    &lt;/mirror&gt;

```

**使用IDEA创建SpringBoot项目**

![20191218161546514.png](https://img-blog.csdnimg.cn/20191218161546514.png)

![20191218161523788.png](https://img-blog.csdnimg.cn/20191218161523788.png)

![20191218161627603.png](https://img-blog.csdnimg.cn/20191218161627603.png)

![20191218161648647.png](https://img-blog.csdnimg.cn/20191218161648647.png)

项目结构为：

![20191218161733175.png](https://img-blog.csdnimg.cn/20191218161733175.png)

项目默认的 maven pom.xml文件

运行SpirngbootdemoApplication的main方法，就能开始运行。

控制台输出：

![20191218161816163.png](https://img-blog.csdnimg.cn/20191218161816163.png)

从这里可以看到 Tomcat 的端口号，因为还没有自定义Controller，所以还没有视图，下面来创建一个输出Hello SpringBoot!的视图。

创建一个HelloController，位于controller包下

HelloController.java

```
package com.jxust.controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {
  
 @RequestMapping("/hello")
 public String say(){
  return "Hello SpringBoot!";
 }
}
```

@RestController Spring4 之后新加的注解,原来返回json需要@ResponseBody配合@Controller,现在一个顶俩

在浏览器中输入[http://localhost:8080/hello](http://localhost:8080/hello)就能输出Hello SpringBoot!这句话。

![20191218161907867.png](https://img-blog.csdnimg.cn/20191218161907867.png)

自定义属性配置

用到的是application.properties这个文件

![2019121816201241.png](https://img-blog.csdnimg.cn/2019121816201241.png)

配置端口号和访问前缀

**application.properties**

```
server.port=8081
server.context-path=/springboot
```

![20191218162055846.png](https://img-blog.csdnimg.cn/20191218162055846.png)

除了使用.properties格式的文件，还可以使用.yml格式的配置文件(推荐)，更加简便

**application.yml**

把原来的application.properties文件删除

![2019121816233860.png](https://img-blog.csdnimg.cn/2019121816233860.png)

注意格式，空格不能少

获取配置文件中的属性值

我们也可以在配置文件中，配置数据，在 Controller 中获取,比如：

```
server:
  port: 8080
  servlet:
    context-path: /springboot

heian : 乘风破浪
```

HelloController 获取配置文件中的值

HelloController.java

```
@RestController
public class HelloController {
    @Value("${heian}")
    private String heian;
    @RequestMapping(value = "/heain",method = RequestMethod.GET)
    public String heian(){
        return heian;
    }
}
```

返回的为heian的值

![20191218163012391.png](https://img-blog.csdnimg.cn/20191218163012391.png)

配置文件中值配置方式的多样化

配置文件的值可以是多个，也可以是组合，如：

**application.yml**

```
name: 乘风
age: 22
或者
name: 乘风
age: 22
content: "name: ${name},age: ${age}"
或者
server:
 port: 8080
 context-path: /springboot
person:
 name: 乘风
 age: 22
```

**前两种配置获取值的方式都是一样的,但是对于这种方式，person 有相应的两个属性，需要这样处理**

**PersonProperties.java**

```
package com.example.demo.controller;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * @Author:南宫乘风
 * @Date:2019/12/18 16:01
 */
@Component
@ConfigurationProperties(prefix = "person")
public class PersonProperties {
    private String name;
    private String age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAge() {
        return age;
    }

    public void setAge(String age) {
        this.age = age;
    }
}

```

Alt+insert快捷键提示生成 Getter and Setter

pom.xml需要加入下面的依赖,处理警告

```
&lt;dependency&gt;
 &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
 &lt;artifactId&gt;spring-boot-configuration-processor&lt;/artifactId&gt;
 &lt;optional&gt;true&lt;/optional&gt;
&lt;/dependency&gt;
```

**HelloController.java**

```
   @Autowired
    PersonProperties personProperties;

    @RequestMapping(value = "/heian", method = RequestMethod.GET)
    public String hello() {
        return "名字： "+personProperties.getName()+"    年龄： "+personProperties.getAge();
    }
```

![20191218163405837.png](https://img-blog.csdnimg.cn/20191218163405837.png)

关于配置文件application.yml的多套配置

类似 il8n 文件国际化的配置方式i18n_en_US.properties和i18n_zh_CN.properties

这样能解决，需要频繁修改配置的尴尬

![20191218163423152.png](https://img-blog.csdnimg.cn/20191218163423152.png)

由application.yml配置文件决定使用那套配置文件。

**application.yml**

```
spring:
 profiles:
 active: a
```

**application-a.yml**

```
server:
  port: 8080
  servlet:
    context-path: /springboot

person :
  name : 南宫乘风A
  age : 20
```

**application-b.yml**

```
server:
  port: 8080
  servlet:
    context-path: /springboot

person :
  name : 南宫乘风B
  age : 22
```

## SpringBoot增删改查实例

**完整的项目结构**

![20191218164100305.png](https://img-blog.csdnimg.cn/20191218164100305.png)

Controller的使用
- @Controller 处理http请求- @RestController Spring4 之后新加的注解，原来返回json需要@ResponseBody配合@Controller- @RequestMapping 配置url映射
对于 REST 风格的请求

**对于 Controller 中的方法上的注解**

```
@RequestMapping(value = “/hello”,method = RequestMethod.GET) 
@RequestMapping(value = “/hello”,method = RequestMethod.POST)
 @RequestMapping(value = “/hello”,method = RequestMethod.DELETE)
 @RequestMapping(value = “/hello”,method = RequestMethod.PUT)

```

**SpringBoot 对上面的注解进行了简化**

```
@GetMapping(value = “/girls”)
@PostMapping(value = “/girls”) 
@PutMapping(value = “/girls/{id}”) 
@DeleteMapping(value = “/girls/{id}”)

```

**浏览器需要发送不同方式的请求，可以安装HttpRequester插件，火狐浏览器可以直接搜索该组件安装。**

![20191218164425261.png](https://img-blog.csdnimg.cn/20191218164425261.png)

**spring-data-jpa**

JPA全称Java Persistence API.JPA通过JDK 5.0注解或XML描述对象－关系表的映射关系，并将运行期的实体对象持久化到数据库中。

Hibernate3.2+、TopLink 10.1.3以及OpenJPA都提供了JPA的实现。

利用JPA创建MySQL数据库

**pom.xml加入JPA和MySQL的依赖**

```
&lt;dependency&gt;
   &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
   &lt;artifactId&gt;spring-boot-starter-data-jpa&lt;/artifactId&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
   &lt;groupId&gt;mysql&lt;/groupId&gt;
   &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
  &lt;/dependency&gt;
   &lt;!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java --&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;version&gt;5.1.38&lt;/version&gt;
        &lt;/dependency&gt;
```

**配置JPA和数据库**

**application.yml**

```
spring:
  profiles:
  active: a
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url : jdbc:mysql://127.0.0.1:3306/heian
    username: root
    password: root
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
```

格式很重要

需要自己手动去创建 db_person 数据库

创建与数据表对应的实体类Person

![20191218165229836.png](https://img-blog.csdnimg.cn/20191218165229836.png)

**Person.java**

```
package com.example.demo.entity;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

/**
 * @Author:南宫乘风
 * @Date:2019/12/18 16:38
 */
@Entity
public class Person {
    @Id
    @GeneratedValue
    private Integer id;
    private String name;
    private Integer age;

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
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}

```

运行项目后，查看数据库，会自动创建表 person

![20191218165822570.png](https://img-blog.csdnimg.cn/20191218165822570.png)

接下来就可以进行person表的增删改查了

**创建控制器PersonController.java**

首先创建一个接口PersonMapper，位于dao包下,PersonController调用该接口继承自JpaRepository的方法，来实现和数据库交互

这个PersonMapper接口的功能，与SSM框架中 dao 层接口功能有异曲同工之妙；在SSM框架中，Service层通过该接口，间接执行Mybatis数据库映射文件(.xml)里的相应sql语句，执行数据库增删改查的操作。(Mapper自动实现DAO接口)

**PersonMapper.java**

```
package com.example.demo.dao;
import com.example.demo.entity.Person;
import org.springframework.data.jpa.repository.JpaRepository;
/**
 * @Author:南宫乘风
 * @Date:2019/12/18 16:38
 */
public interface PersonMapper extends JpaRepository&lt;Person,Integer&gt; {
}
```

**PersonController.java**

```
package com.example.demo.controller;
import com.example.demo.dao.PersonMapper;
import com.example.demo.entity.Person;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
/**
 * @Author:南宫乘风
 * @Date:2019/12/18 16:39
 */
@RestController
public class PersonController {
    @Autowired
    PersonMapper personMapper;
    @GetMapping(value = "/person")
    public List&lt;Person&gt; personList(){
        return personMapper.findAll();
    }
}
```

在数据库中添加两条数据

![20191218170434863.png](https://img-blog.csdnimg.cn/20191218170434863.png)

启动项目执行请求[http://localhost:8080/person](http://localhost:8081/springboot/person)

![20191218170829433.png](https://img-blog.csdnimg.cn/20191218170829433.png)

**控制台输出的sql语句：**

![20191218170844354.png](https://img-blog.csdnimg.cn/20191218170844354.png)

**其他增删改查的方法**

**PersonController.java**

```
/**
     * 添加一个人员
     * @param name
     * @param age
     * @return
     */
    @PostMapping(value = "/person")
    public Person add(@RequestParam("name") String name, @RequestParam("age") Integer age) {

        Person person = new Person();
        person.setName(name);
        person.setAge(age);
        return personMapper.save(person);
    }
```

**利用ApiPost测试【已经成功】**

![20191218172123678.png](https://img-blog.csdnimg.cn/20191218172123678.png)

**更新其他方法**
