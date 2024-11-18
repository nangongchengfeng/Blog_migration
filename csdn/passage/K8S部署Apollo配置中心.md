#K8S部署Apollo配置中心
本文将介绍如何在 Spring Boot 中集成阿波罗（Apollo）和 Consul，并使用 Apollo 和 Consul 实现配置管理和服务注册与发现的功能。

# 1. 什么是阿波罗

阿波罗是携程开源的分布式配置中心，支持多种编程语言和框架。它提供了一套完整的配置管理解决方案，可以帮助开发者实现配置管理、版本控制、灰度发布等功能。

Apollo（阿波罗）是携程框架部门研发的分布式配置中心，能够集中化管理应用不同环境、不同集群的配置，配置修改后能够实时推送到应用端，并且具备规范的权限、流程治理等特性，适用于微服务配置管理场景。服务端基于 Spring Boot 和 Spring Cloud 开发，打包后可以直接运行，不需要额外安装 Tomcat 等应用容器。

Apollo 支持 4 个维度管理 Key-Value 格式的配置：
1. application (应用)
	1. environment (环境)
	1. cluster (集群)
	1. namespace (命名空间 Namespace 是配置项的集合，类似于一个配置文件的概念)

<img alt="" src="https://img-blog.csdnimg.cn/img_convert/256a3b00b422c88626e98bc63efa701f.jpeg" />

上图是Apollo配置中心中一个项目的配置首页
- 在页面左上方的环境列表模块展示了所有的环境和集群，用户可以随时切换。
	- 页面中央展示了两个namespace(application和FX.apollo)的配置信息，默认按照表格模式展示、编辑。用户也可以切换到文本模式，以文件形式查看、编辑。
	- 页面上可以方便地进行发布、回滚、灰度、授权、查看更改历史和发布历史等操作。

<img alt="" src="https://img-blog.csdnimg.cn/img_convert/25f4be0c80b62161d10eff07ac53df42.jpeg" />

## 1.1 集成 Apollo 的原理

Spring Boot 集成阿波罗可以通过引入 `apollo-client` 客户端库，并在 Spring Boot 应用程序中配置连接信息和获取配置信息来实现。具体流程如下：
<li>
	Spring Boot 应用程序启动时，先加载 `bootstrap.yml` 或者 `bootstrap.properties` 文件中的配置信息。
	</li>
	<li>
	在 `bootstrap.yml` 或者 `bootstrap.properties` 中配置阿波罗的连接信息（例如，阿波罗的地址、应用程序名称等）。
	</li>
	<li>
	在 Spring Boot 应用程序中注入 `@Value` 注解中指定的阿波罗配置项的值，即可使用阿波罗管理的配置信息。
	</li>
	<li>
	如果阿波罗的配置信息发生改变，Spring Boot 应用程序会自动从阿波罗更新最新的配置信息，并重新加载应用程序的配置。
	</li>

## 1.2. 集成 Apollo 的优势

集成阿波罗可以带来以下优势：
<li>
	管理多个环境的配置：阿波罗提供了环境切换和灰度发布的功能，可以轻松管理多个环境（例如，开发环境、测试环境、生产环境等）的配置信息。
	</li>
	<li>
	实时更新配置：阿波罗支持实时更新配置信息，可以在不重启应用程序的情况下动态更新配置信息。
	</li>
	<li>
	版本控制：阿波罗提供了版本控制的功能，可以记录每个配置项的历史版本，方便回滚和恢复数据。
	</li>
	<li>
	集成多种框架：阿波罗支持多种编程语言和框架，可以轻松集成到各种应用程序中。
	</li>



# 2、SpringBoot实战集成Apollo

<img alt="" height="1024" src="https://img-blog.csdnimg.cn/fcbacc65f870473e9afdc9cd95181583.png" width="1200" />

 

## 1、引入依赖

## 2、增加配置文件

## 3、Apollo配置（公用配置，引用）

<img alt="" height="899" src="https://img-blog.csdnimg.cn/d0d94716de2d47919f092b044f20507c.png" width="1200" />

 

##  4、Apollo项目配置

上面为公共的配置引用，可以被多个项目使用

接下来创建一个单独的Apollo项目。

创建一个单独的 Apollo 项目可以分为以下几个步骤：
<li>
	登录阿波罗控制台：在浏览器中输入 `https://config.xxx.com` 地址，使用阿波罗管理员账号登录阿波罗控制台。
	</li>
	<li>
	创建新项目：在阿波罗控制台中，点击左侧导航栏中的“AppList”，然后点击“Create App”按钮，在弹出的对话框中填写应用程序名称、所属集群、所属命名空间等信息，并点击“Create”按钮创建新项目。
	</li>
	<li>
	添加配置项：进入新创建的项目页面后，点击右侧的“Namespace List”标签页，然后选择需要添加配置项的命名空间。在命名空间页面中，点击“Add Item”按钮，填写配置项的 Key 和 Value，并选择该配置项所属的环境（如 dev、test、prod 等）和版本号。
	</li>
	<li>
	下载客户端库：在阿波罗控制台中，点击右上角的“Portal”菜单，进入开发者门户网站。在网站中，选择对应的编程语言和框架，然后下载对应的客户端库（例如，Java + Spring Boot 应用程序需要下载 `apollo-client` 客户端库）。
	</li>
	<li>
	集成客户端库：将下载好的客户端库引入应用程序的依赖中，然后在应用程序中添加连接阿波罗的配置信息，并使用客户端库从阿波罗获取配置信息。例如，在 Spring Boot 应用程序中，可以在 `bootstrap.yml` 文件中添加以下配置信息：
	</li>

其中，`your-application-name` 是应用程序的名称，`dev` 是配置环境的名称。`http://apollo-config-server-url` 是阿波罗的配置服务 URL。

        6.启动应用程序：将集成了 Apollo 的应用程序打包并启动，通过日志和控制台输出可以查看到应用程序从阿波罗获取配置信息的情况。

以上就是创建一个单独的 Apollo 项目的流程，需要注意的是在实际应用中还需根据具体情况进行调整和优化。

<img alt="" height="820" src="https://img-blog.csdnimg.cn/e78ad2f8ded249b9806f4c2d422bc5b6.png" width="1200" />

 

## 5、SpringBoot代码



### WebDemoApplication 启动类

### HelloWorldController类

### EmployeeController 类

<img alt="" height="543" src="https://img-blog.csdnimg.cn/083549268e9a485e9117c8d0a88d3dc2.png" width="1200" />

##  6、启动测试

<img alt="" height="598" src="https://img-blog.csdnimg.cn/be43b11d384c44168b9405544ef3248f.png" width="1187" />

 <img alt="" height="1029" src="https://img-blog.csdnimg.cn/555b2cb1f77a4dc59b5b09b51dbb55d0.png" width="1200" />

### name变量

<img alt="" height="364" src="https://img-blog.csdnimg.cn/b90420edb71145278f6a8a1fb6c7b81b.png" width="1200" />

<img alt="" height="377" src="https://img-blog.csdnimg.cn/f4aa8b2aa46c43af92e03fb1165ae04f.png" width="1200" />

 修改name变量，无需重启项目

 <img alt="" height="271" src="https://img-blog.csdnimg.cn/1353820e7c2e44938afe7232ec598306.png" width="1200" />

 <img alt="" height="331" src="https://img-blog.csdnimg.cn/f3c251cbea55437ba85a4a4b51f7a4eb.png" width="1200" />

###  测试两个接口

<img alt="" height="344" src="https://img-blog.csdnimg.cn/f023addc829d42eca688dd290aeb1d42.png" width="1200" />

 <img alt="" height="423" src="https://img-blog.csdnimg.cn/4868ecdb0c3844d082c732f6cb74aa0c.png" width="1200" />

###  Consul已经自动注册上

<img alt="" height="433" src="https://img-blog.csdnimg.cn/a726b3a09f794795a4542207ff46ffd2.png" width="1200" />

 <img alt="" height="391" src="https://img-blog.csdnimg.cn/5aeea8fe4a014e04a73153172b940ac7.png" width="1200" />

 

本文介绍了如何在 Spring Boot 中集成阿波罗，并详细说明了其原理和优势。通过使用阿波罗，可以轻松管理多个环境的配置信息，实现配置管理、版本控制、灰度发布等功能。同时，本文还给出了集成阿波罗的最佳实践，希望能够对开发者和运维在实际项目中使用阿波罗提供一些参考和帮助。

 参考文档：






