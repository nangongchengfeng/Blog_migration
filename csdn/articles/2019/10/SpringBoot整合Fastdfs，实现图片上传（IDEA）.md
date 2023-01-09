+++
author = "南宫乘风"
title = "SpringBoot整合Fastdfs，实现图片上传（IDEA）"
date = "2019-10-10 15:20:18"
tags=[]
categories=['Java']
image = "post/4kdongman/44.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/102482992](https://blog.csdn.net/heian_99/article/details/102482992)

## **我们部署Fastdfs，就是为了实现文件的上传。**

## **现在使用idea整合Fastdfs，实现图片上传**

![20191010151000258.png](https://img-blog.csdnimg.cn/20191010151000258.png)

# **部署环境：[Centos7部署分布式文件存储(Fastdfs)](https://blog.csdn.net/heian_99/article/details/102477556)**

## 利用Java客户端调用FastDFS

服务器安装完毕后，咱们通过Java调用fastdfs

**加载Maven****依赖**

fastdfs 没有在中心仓库中提供获取的依赖坐标。

只能自己通过源码方式编译，打好jar 包，安装到本地仓库。

官方仓库地址：

[https://github.com/happyfish100/fastdfs-client-java](https://github.com/happyfish100/fastdfs-client-java)

![20191010151121745.png](https://img-blog.csdnimg.cn/20191010151121745.png)

直接用idea 直接把这个源码作为模块导入工程

![20191010151144279.png](https://img-blog.csdnimg.cn/20191010151144279.png)

 

别的不用改，只把pom.xml中的版本改成1.27。

![20191010151328841.png](https://img-blog.csdnimg.cn/20191010151328841.png)

然后右边 执行install 就好了

![20191010151340328.png](https://img-blog.csdnimg.cn/20191010151340328.png)

安装好了 ，别的模块就可以直接使用这个坐标了。

```
    &lt;dependency&gt;
            &lt;groupId&gt;org.csource&lt;/groupId&gt;
            &lt;artifactId&gt;fastdfs-client-java&lt;/artifactId&gt;
            &lt;version&gt;1.27-SNAPSHOT&lt;/version&gt;
        &lt;/dependency&gt;
```

而这个fastdfs-client-java模块可以从idea 中删除。

### **然后可以进行一下上传的测试**

![20191010151556854.png](https://img-blog.csdnimg.cn/20191010151556854.png)

 

```
package com.atguigu.gmall.manage;

import org.csource.common.MyException;
import org.csource.fastdfs.ClientGlobal;
import org.csource.fastdfs.StorageClient;
import org.csource.fastdfs.TrackerClient;
import org.csource.fastdfs.TrackerServer;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.io.IOException;

@RunWith(SpringRunner.class)
@SpringBootTest
public class GmallManageWebApplicationTests {


    @Test
    public void contextLoads() throws IOException, MyException {

        //配置fdfs的全局连接地址
        String tracker = GmallManageWebApplicationTests.class.getResource("/tracker.conf").getPath();//获取配置文件路径

        ClientGlobal.init(tracker);

        TrackerClient trackerClient = new TrackerClient();
        //获得一个trackerserver的实例
        TrackerServer trackerServer = trackerClient.getConnection();
        //通过tracker获得storage客户端
        StorageClient storageClient = new StorageClient(trackerServer, null);

        String[] uploadInfos = storageClient.upload_file("g:/9.gif", "gif", null);

        String url="http://192.168.116.129";

        for (String uploadInfo : uploadInfos){
            url+="/"+uploadInfo;

        }
        System.out.println(url);
    }
}

```

### **加入tracker.conf文件**

![20191010151700924.png](https://img-blog.csdnimg.cn/20191010151700924.png)

```
tracker_server=192.168.67.162:22122

# 连接超时时间，针对socket套接字函数connect，默认为30秒
connect_timeout=30000

# 网络通讯超时时间，默认是60秒
network_timeout=60000

```

打印结果

![20191010151830915.png](https://img-blog.csdnimg.cn/20191010151830915.png)

 

这个打印结果实际上就是我们访问的路径，加上服务器地址我们可以拼接成一个字符串

[http://192.168.116.129/group1/M00/00/00/wKh0gV2dHmGAFpUzAA7-f54U48M105.gif](http://192.168.116.129/group1/M00/00/00/wKh0gV2dHmGAFpUzAA7-f54U48M105.gif)

直接放到浏览器去访问

![20191010151956264.png](https://img-blog.csdnimg.cn/20191010151956264.png)

 

 
