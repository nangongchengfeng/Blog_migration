+++
author = "南宫乘风"
title = "nginx 配置实例-反向代理"
date = "2019-11-28 15:15:18"
tags=[]
categories=['Nginx']
image = "post/4kdongman/16.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103292763](https://blog.csdn.net/heian_99/article/details/103292763)

## 反向代理实例一 

**虚拟机IP：192.168.116.129**<br>**实现效果：使用 nginx 反向代理，访问 www.123.com 直接跳转到 虚拟机的****192.168.116.129****:8080 **

### **实验代码 **

**1） 启动一个 tomcat，浏览器地址栏输入 ****192.168.116.129****:8080，出现如下界面 **

![20191128143406253.png](https://img-blog.csdnimg.cn/20191128143406253.png)

**2） 通过修改本地 host 文件，将 www.123.com 映射到****192.168.116.129**

![20191128143641636.png](https://img-blog.csdnimg.cn/20191128143641636.png)

**配置完成之后，我们便可以通过 www.123.com:8080 访问到第一步出现的 Tomcat 初始界 面。那么如何只需要输入 www.123.com 便可以跳转到 Tomcat 初始界面呢？便用到 nginx 的反向代理。**

### 3） 在 nginx.conf 配置文件中增加如下配置 

![20191128143903860.png](https://img-blog.csdnimg.cn/20191128143903860.png)

**注意：修改配置文件后，需要重启nginx**

**如上配置，我们监听 80 端口，访问域名为 www.123.com，不加端口号时默认为 80 端口，故 访问该域名时会跳转到 127.0.0.1:8080 路径上。在浏览器端输入 www.123.com 结果如下：**<br>  

![2019112814412660.png](https://img-blog.csdnimg.cn/2019112814412660.png)

## 反向代理实例二 

**虚拟机ip:192.168.116.129**

**实现效果：使用 nginx 反向代理，根据访问的路径跳转到不同端口的服务中 nginx 监听端口为 9001，**

**访问 http://****192.168.116.129****:9001/edu/ 直接跳转到 ****192.168.116.129.****0.0.1:8080 **

**访问 http://****192.168.116.129****:9001/vod/ 直接跳转到 ****192.168.116.129****:8082 **

 

### 实验代码 

### <br> 1、准备工作

**（1）准备两个 tomcat 服务器，一个 8080 端口，一个 8082 端口 **

**（2）创建文件夹和测试页面 **

## 2、具体配

**修改 nginx 的配置文件 **

**在 http 块中添加 server{} **

```
   server{
        listen 9001;
        server_name localhost;
                location ~ /edu/ {
                                proxy_pass http://localhost:8080;
                        }
                  location ~ /dev/ {
                                proxy_pass http://localhost:8082;
                        }

}

```

**重启**

![20191128150902654.png](https://img-blog.csdnimg.cn/20191128150902654.png)

![20191128151024475.png](https://img-blog.csdnimg.cn/20191128151024475.png)

 

### **location 指令说明 **

语法如下：

![2019112815105882.png](https://img-blog.csdnimg.cn/2019112815105882.png)
- ** 1、= ：用于不含正则表达式的 uri 前，要求请求字符串与 uri 严格匹配，如果匹配 成功，就停止继续向下搜索并立即处理该请求。 **- **  2、~：用于表示 uri 包含正则表达式，并且区分大小写。 **- **  3、~*：用于表示 uri 包含正则表达式，并且不区分大小写。 **- **  4、^~：用于不含正则表达式的 uri 前，要求 Nginx 服务器找到标识 uri 和请求字 符串匹配度最高的 location 后，立即使用此 location 处理请求，而不再使用 location 块中的正则 uri 和请求字符串做匹配。 **- **  注意：如果 uri 包含正则表达式，则必须要有 ~ 或者 ~* 标识。 **
### 我改了一行配置，会实现下面修改。

有兴趣的朋友可以试试（猜猜我改的那个地方）

![20191128151354709.png](https://img-blog.csdnimg.cn/20191128151354709.png)

![20191128151434918.png](https://img-blog.csdnimg.cn/20191128151434918.png)

## 相关博文：

### [Nginx 简介与安装、常用的命令和配置文件](https://blog.csdn.net/heian_99/article/details/103264404)

## [nginx 配置实例-反向代理](https://blog.csdn.net/heian_99/article/details/103292763)

### [nginx 配置实例-负载均衡](https://blog.csdn.net/heian_99/article/details/103298249)

### [Nginx 配置实例-动静分离](https://blog.csdn.net/heian_99/article/details/103391378)

### [Nginx 配置高可用的集群](https://blog.csdn.net/heian_99/article/details/103391454)
