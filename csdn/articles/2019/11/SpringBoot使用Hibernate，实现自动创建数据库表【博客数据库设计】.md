+++
author = "南宫乘风"
title = "SpringBoot使用Hibernate，实现自动创建数据库表【博客数据库设计】"
date = "2019-11-11 17:52:14"
tags=[]
categories=['Java']
image = "post/4kdongman/41.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103013889](https://blog.csdn.net/heian_99/article/details/103013889)

我们准备设计博客，那就要设计数据库。

我们可以使用Hibernate来自动生成数据库。

博客数据库的结构：

实体类：
- 博客 Blog- 博客分类 Type- 博客标签 Tag- 博客评论 Comment- 用户 User


 



![20191111173830884.png](https://img-blog.csdnimg.cn/20191111173830884.png)

![20191111173940592.png](https://img-blog.csdnimg.cn/20191111173940592.png)

![20191111174002272.png](https://img-blog.csdnimg.cn/20191111174002272.png)

![20191111174020749.png](https://img-blog.csdnimg.cn/20191111174020749.png)

![20191111174033932.png](https://img-blog.csdnimg.cn/20191111174033932.png)

![20191111174045756.png](https://img-blog.csdnimg.cn/20191111174045756.png)

![20191111174057964.png](https://img-blog.csdnimg.cn/20191111174057964.png)

![20191111174110775.png](https://img-blog.csdnimg.cn/20191111174110775.png)

项目截图：

![20191111173550825.png](https://img-blog.csdnimg.cn/20191111173550825.png)

 

首先，在pom.xml中添加以下的一些依赖:

```
&lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-data-jpa&lt;/artifactId&gt;
&lt;/dependency&gt;

```

这样就可以使用Hibernate框架了，下面实现自动创建数据库表的功能:

打开application.properties文件添加以下的代码:

```
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true

```

![20191111174335474.png](https://img-blog.csdnimg.cn/20191111174335474.png)

 

这里除了update参数外还有其他的参数，这里解释一下:<br>  //1：value="create-drop" 表示当JPA应用的时候自动创建表，在解应用的时候删除相应的表，这个在做测试的时候比较有用，但在开发过程中不这么用<br> //2：value="create"这个在每次应用启动的时候都会创建数据库表（会删除以前数据库里的数据。<br> //3：value="update" 这个属性的作用是a:每次只会更新数据库表里的信息

下面是创建实体类的代码:

### Blog

```
package com.lrm.po;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "t_blog")
public class Blog {
    @Id
    @GeneratedValue
    private Long id;

    private String title;

    private String content;

    private String firstPicture;

    private String flag;

    private Integer views;

    private boolean appreciation;

    private boolean shareStatement;

    private boolean commentabled;

    private boolean published;

    private boolean recommend;

    private Date createTime;

    private Date updateTime;

    @ManyToOne
    private Type type;
    @ManyToMany(cascade = {CascadeType.PERSIST})
    private List&lt;Tag&gt; tags=new ArrayList&lt;&gt;();
    @ManyToOne
    private User user;

    @OneToMany(mappedBy = "blog")
    private List&lt;Comment&gt; comments = new ArrayList&lt;&gt;();
    public Blog() {

    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getFirstPicture() {
        return firstPicture;
    }

    public void setFirstPicture(String firstPicture) {
        this.firstPicture = firstPicture;
    }

    public String getFlag() {
        return flag;
    }

    public void setFlag(String flag) {
        this.flag = flag;
    }

    public Integer getViews() {
        return views;
    }

    public void setViews(Integer views) {
        this.views = views;
    }

    public boolean isAppreciation() {
        return appreciation;
    }

    public void setAppreciation(boolean appreciation) {
        this.appreciation = appreciation;
    }

    public boolean isShareStatement() {
        return shareStatement;
    }

    public void setShareStatement(boolean shareStatement) {
        this.shareStatement = shareStatement;
    }

    public boolean isCommentabled() {
        return commentabled;
    }

    public void setCommentabled(boolean commentabled) {
        this.commentabled = commentabled;
    }

    public boolean isPublished() {
        return published;
    }

    public void setPublished(boolean published) {
        this.published = published;
    }

    public boolean isRecommend() {
        return recommend;
    }

    public void setRecommend(boolean recommend) {
        this.recommend = recommend;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(Date updateTime) {
        this.updateTime = updateTime;
    }

    public Type getType() {
        return type;
    }

    public void setType(Type type) {
        this.type = type;
    }

    public List&lt;Tag&gt; getTags() {
        return tags;
    }

    public void setTags(List&lt;Tag&gt; tags) {
        this.tags = tags;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public List&lt;Comment&gt; getComments() {
        return comments;
    }

    public void setComments(List&lt;Comment&gt; comments) {
        this.comments = comments;
    }

    @Override
    public String toString() {
        return "Blog{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", content='" + content + '\'' +
                ", firstPicture='" + firstPicture + '\'' +
                ", flag='" + flag + '\'' +
                ", views=" + views +
                ", appreciation=" + appreciation +
                ", shareStatement=" + shareStatement +
                ", commentabled=" + commentabled +
                ", published=" + published +
                ", recommend=" + recommend +
                ", createTime=" + createTime +
                ", updateTime=" + updateTime +
                '}';
    }
}

```

### Comment

```
package com.lrm.po;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;


@Entity
@Table(name = "t_comment")
public class Comment {

    @Id
    @GeneratedValue
    private Long id;
    private String nickname;
    private String email;
    private String content;
    private String avatar;
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime;

    @ManyToOne
    private Blog blog;

    @OneToMany(mappedBy = "parentComment")
    private List&lt;Comment&gt; replyComments = new ArrayList&lt;&gt;();

    @ManyToOne
    private Comment parentComment;

    public Comment() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getAvatar() {
        return avatar;
    }

    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Blog getBlog() {
        return blog;
    }

    public void setBlog(Blog blog) {
        this.blog = blog;
    }

    public List&lt;Comment&gt; getReplyComments() {
        return replyComments;
    }

    public void setReplyComments(List&lt;Comment&gt; replyComments) {
        this.replyComments = replyComments;
    }

    public Comment getParentComment() {
        return parentComment;
    }

    public void setParentComment(Comment parentComment) {
        this.parentComment = parentComment;
    }

    @Override
    public String toString() {
        return "Comment{" +
                "id=" + id +
                ", nickname='" + nickname + '\'' +
                ", email='" + email + '\'' +
                ", content='" + content + '\'' +
                ", avatar='" + avatar + '\'' +
                ", createTime=" + createTime +
                '}';
    }
}

```

### Tag

```
package com.lrm.po;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "t_tag")
public class Tag {

    @Id
    @GeneratedValue
    private Long id;
    private String name;

    @ManyToMany(mappedBy = "tags")
    private List&lt;Blog&gt; blogs = new ArrayList&lt;&gt;();

    public Tag() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List&lt;Blog&gt; getBlogs() {
        return blogs;
    }

    public void setBlogs(List&lt;Blog&gt; blogs) {
        this.blogs = blogs;
    }

    @Override
    public String toString() {
        return "Tag{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}

```

### Type

```
package com.lrm.po;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "t_type")
public class Type {
    @Id
    @GeneratedValue
    private long id;

    private String name;

    @OneToMany(mappedBy = "type")
    private List&lt;Blog&gt; blogs = new ArrayList&lt;&gt;();

    public Type() {
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List&lt;Blog&gt; getBlogs() {
        return blogs;
    }

    public void setBlogs(List&lt;Blog&gt; blogs) {
        this.blogs = blogs;
    }

    @Override
    public String toString() {
        return "Type{" +
                "id=" + id +
                ", name='" + name + '\'' +
                '}';
    }
}

```

### User

```
package com.lrm.po;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Created by limi on 2017/10/14.
 */
@Entity
@Table(name = "t_user")
public class User {

    @Id
    @GeneratedValue
    private Long id;
    private String nickname;
    private String username;
    private String password;
    private String email;
    private String avatar;
    private Integer type;
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime;
    @Temporal(TemporalType.TIMESTAMP)
    private Date updateTime;

    @OneToMany(mappedBy = "user")
    private List&lt;Blog&gt; blogs = new ArrayList&lt;&gt;();

    public User() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNickname() {
        return nickname;
    }

    public void setNickname(String nickname) {
        this.nickname = nickname;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getAvatar() {
        return avatar;
    }

    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    public Integer getType() {
        return type;
    }

    public void setType(Integer type) {
        this.type = type;
    }

    public Date getCreateTime() {
        return createTime;
    }

    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    public Date getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(Date updateTime) {
        this.updateTime = updateTime;
    }


    public List&lt;Blog&gt; getBlogs() {
        return blogs;
    }

    public void setBlogs(List&lt;Blog&gt; blogs) {
        this.blogs = blogs;
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", nickname='" + nickname + '\'' +
                ", username='" + username + '\'' +
                ", password='" + password + '\'' +
                ", email='" + email + '\'' +
                ", avatar='" + avatar + '\'' +
                ", type=" + type +
                ", createTime=" + createTime +
                ", updateTime=" + updateTime +
                '}';
    }
}

```

OK，既然，实体类已将创建完毕，运行接口。就可以生成数据库。但是前提，你是配置数据库

```
spring:
  datasource:
    driver-class-name: com.mysql.jdbc.Driver
    url: jdbc:mysql://localhost:3306/blog?useUnicode=true&amp;characterEncoding=utf-8
    username: root
    password: root
```

![20191111174826317.png](https://img-blog.csdnimg.cn/20191111174826317.png)

## 测试结果：

![20191111175030797.png](https://img-blog.csdnimg.cn/20191111175030797.png)

![20191111175120678.png](https://img-blog.csdnimg.cn/20191111175120678.png)

真的很nice，确实是一波骚操作。

 
