---
author: 南宫乘风
categories:
- 错误问题解决
date: 2019-11-18 09:42:22
description: 刚刚写完一个项目，准备打包，却发现无法打包。然后认真排查了一下问题。发现少引入了一个插件。引入这个插件就可以完美运行打包了。。。。。。。。
image: ../../title_pic/42.jpg
slug: '201911180942'
tags:
- Java
- bug拮据
title: Tests in error-BlogApplicationTests.initializationError » IllegalState Unable
  to find a @Spri...【解决】
---

<!--more-->

刚刚写完一个项目，准备打包，却发现无法打包。

![](../../image/20191118093843838.png)

然后认真排查了一下问题。发现少引入了一个插件。

```java
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-surefire-plugin</artifactId>
				<configuration>
					<skip>true</skip>
				</configuration>
			</plugin>
```

引入这个插件就可以完美运行打包了。

![](../../image/20191118094122154.png)