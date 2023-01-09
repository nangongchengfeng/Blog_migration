+++
author = "南宫乘风"
title = "Tests in error:BlogApplicationTests.initializationError » IllegalState Unable to find a @Spri...【解决】"
date = "2019-11-18 09:42:22"
tags=['bug拮据']
categories=['错误问题解决', 'Java']
image = "post/4kdongman/28.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103117319](https://blog.csdn.net/heian_99/article/details/103117319)

刚刚写完一个项目，准备打包，却发现无法打包。

![20191118093843838.png](https://img-blog.csdnimg.cn/20191118093843838.png)

然后认真排查了一下问题。发现少引入了一个插件。

```
			&lt;plugin&gt;
				&lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
				&lt;artifactId&gt;maven-surefire-plugin&lt;/artifactId&gt;
				&lt;configuration&gt;
					&lt;skip&gt;true&lt;/skip&gt;
				&lt;/configuration&gt;
			&lt;/plugin&gt;

```

引入这个插件就可以完美运行打包了。

![20191118094122154.png](https://img-blog.csdnimg.cn/20191118094122154.png)

 

 

 

 

 
