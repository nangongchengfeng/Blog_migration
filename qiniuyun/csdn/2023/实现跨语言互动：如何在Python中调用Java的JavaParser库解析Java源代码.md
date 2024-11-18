---
author: 南宫乘风
categories:
- Python学习
- Java
date: 2023-07-13 12:10:36
description: 、背景在多语言开发环境中，我们经常需要进行跨语言的操作。有时，我们可能会在环境下需要使用的库或者功能。这个博客将展示如何在中调用的库来解析源代码。、需求在许多软件开发场景中，我们可能需要解析源代码以获。。。。。。。
image: ../../title_pic/70.jpg
slug: '202307131210'
tags:
- python
- java
- 开发语言
title: 实现跨语言互动：如何在Python中调用Java的JavaParser库解析Java源代码
---

<!--more-->

## 1、背景
在多语言开发环境中，我们经常需要进行跨语言的操作。有时，我们可能会在Python环境下需要使用Java的库或者功能。这个博客将展示如何在Python中调用Java的JavaParser库来解析Java源代码。
## 2、需求
在许多软件开发场景中，我们可能需要解析Java源代码以获取其结构信息。比如说，我们可能希望知道源代码中定义了哪些类和方法。虽然Python库javalang可以在一定程度上满足我们的需求，但它不能产生我们想要的JSON格式的输出，该格式以类似于 [{"code": "xxxx"}, {"code": "xxxx"}, {"code": "xxxx"}] 的形式，列出了源代码中的每个类和方法。
为了解决这个问题，我们可以使用Java的JavaParser库。以下是一个示例，展示了如何使用JavaParser来解析Java源代码，并生成我们想要的JSON格式的输出。

## 3、JavaParser概述
JavaParser是一个Java库，可以用于解析Java源代码并生成抽象语法树（AST）。通过使用JavaParser，我们可以轻松地获取Java源代码的结构信息，比如类定义，方法定义等。
##  4、创建Java解析器应用
首先，我们需要创建一个新的Java类，我们将其命名为JavaFileParser。在JavaFileParser类中，我们将定义一个主方法，该方法将接受一个命令行参数，该参数指定了要解析的Java源文件的路径。

在主方法中，我们首先检查提供的文件路径是否指向一个实际存在的文件。如果文件不存在，我们将打印一条错误消息并退出。如果文件存在，我们将创建一个JavaParser实例，并使用它来解析源文件。

解析结果将被封装在一个Optional<CompilationUnit>对象中。如果解析成功，我们可以通过调用Optional的get方法来获取CompilationUnit对象。CompilationUnit对象表示了Java源文件的顶级结构。

接下来，我们创建一个JSONArray实例，然后遍历CompilationUnit中的所有类和接口。对于每个类或接口，我们创建一个JSONObject实例，并将类或接口的名称和源代码添加到这个JSONObject中。然后，我们将这个JSONObject添加到JSONArray中。

接着，我们遍历每个类或接口中的所有方法。对于每个方法，我们同样创建一个JSONObject实例，并将方法的名称和源代码添加到这个JSONObject中。然后，我们将这个JSONObject添加到JSONArray中。

最后，我们将JSONArray转换为字符串，并打印到控制台。

如果解析失败，我们将打印一条错误消息。
![在这里插入图片描述](../../image/db07cc0cde744eeeb9f48af0bc4c0b5d.png)

**pom.xml**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.5.12</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>

    <groupId>com.fujfu</groupId>
    <artifactId>java-file</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>java-file</name>
    <description>java-file</description>
    <properties>
        <java.version>1.8</java.version>
    </properties>
    <dependencies>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter</artifactId>
        </dependency>

        <dependency>
            <groupId>com.github.javaparser</groupId>
            <artifactId>javaparser-core</artifactId>
            <version>3.25.1</version>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.vaadin.external.google</groupId>
            <artifactId>android-json</artifactId>
            <version>0.0.20131108.vaadin1</version>
            <scope>compile</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

**JavaFileParser**
```java
package com.fujfu.javafile;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.IOException;
import java.util.Optional;

public class JavaFileParser {
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.out.println("Please provide the file path as an argument.");
            return;
        }
        String filePath = args[0];
        File file = new File(filePath);

        if (!file.exists()) {
            System.out.println("File does not exist: " + filePath);
            return;
        }

        JavaParser javaParser = new JavaParser();
        ParseResult<CompilationUnit> parse = javaParser.parse(file);

        Optional<CompilationUnit> optionalCompilationUnit = parse.getResult();
        if (optionalCompilationUnit.isPresent()) {
            CompilationUnit compilationUnit = optionalCompilationUnit.get();

            JSONArray jsonArray = new JSONArray();

            // 遍历所有的类
            compilationUnit.findAll(ClassOrInterfaceDeclaration.class).forEach(c -> {
                JSONObject classJson = new JSONObject();
                try {
                    classJson.put("name", c.getName().asString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                try {
                    classJson.put("code", c.toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                jsonArray.put(classJson);

                // 遍历类中的所有方法
                c.findAll(MethodDeclaration.class).forEach(m -> {
                    JSONObject methodJson = new JSONObject();
                    try {
                        methodJson.put("name", m.getName().asString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    try {
                        methodJson.put("code", m.toString());
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    jsonArray.put(methodJson);
                });
            });

            System.out.println(jsonArray.toString());
            //jsonArray.toString() 循环
//            for (int i = 0; i < jsonArray.length(); i++) {
//                JSONObject jsonObject = null;
//                try {
//                    jsonObject = jsonArray.getJSONObject(i);
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//                try {
//                    System.out.println("Name: " + jsonObject.getString("name"));
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
////                try {
////                    System.out.println("Code: " + jsonObject.getString("code"));
////                } catch (JSONException e) {
////                    e.printStackTrace();
////                }
//            }
        } else {
            System.out.println("Failed to parse the file.");
        }
    }
}


```
## 5、Java单文件打包成Jar

![在这里插入图片描述](../../image/36908017cbd148538489591cab3f31ee.png)
![在这里插入图片描述](../../image/dd6a9701f6f74719b9bb7585c6236fe6.png)
![在这里插入图片描述](../../image/8b2e113076bf42beb440d2cc68ad9bf1.png)![在这里插入图片描述](../../image/dd9a87cbdf9d4ef1883be2929fa82b8e.png)
![在这里插入图片描述](../../image/6c83413dae494429a1b4561ce6581789.png)
![在这里插入图片描述](../../image/14b01049aa8c48bcb40aa0c819c1b49e.png)
![在这里插入图片描述](../../image/a0c6bfc3054148028d6ee2eed10e643e.png)
![在这里插入图片描述](../../image/908c3369fba8427b9b11c4e1204f3d38.png)
![在这里插入图片描述](../../image/b278587ea5204460b5333880824e2df9.png)

## 6、在Python中调用Java程序

首先，你需要一个用Java编写的程序，这个程序需要调用JavaParser库来解析Java源代码，并将解析结果转换为JSON格式输出。我们假设你已经有了这样的Java程序，并且你已经将它打包为名为javafilejson.jar的JAR文件。

然后，在Python中，我们将使用subprocess模块来调用这个JAR文件。subprocess模块允许我们从Python代码中执行外部命令，我们将使用它来运行java -jar javafilejson.jar {file_path}命令，其中{file_path}是你希望解析的Java源文件的路径。

命令的执行结果将被捕获并存储在output变量中。如果命令成功执行，我们将打印一条成功信息，然后解析output变量的内容，并以Python字典的形式打印出来。如果命令执行失败，我们将打印一条错误信息。

下面是具体的Python代码：

```python
import json
import subprocess

def execute_java_command(file_path):
    command = f'java -jar javafilejson.jar {file_path}'

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if process.returncode == 0:
        print("命令执行成功！")
        print("输出：")
        all_data = output.decode("gbk")
        lst = json.loads(all_data)
        for i in lst:
            print(i["name"], i["code"])
    else:
        print("命令执行失败！")
        print("错误信息：")
        print(error)

# 调用函数示例
file_path = "LoanInfoController.java"
execute_java_command(file_path)

```
![在这里插入图片描述](../../image/b6b15f4ba36b4a12acb054db93e3be74.png)
## 7、 总结
这就是如何在Python环境下调用Java的JavaParser库来解析Java源代码的方法。这种跨语言的解决方案不仅能够扩大我们的工具箱，还能够帮助我们更好地理解源代码的结构，并在需要的时候对其进行修改。

JavaParser官方文档：https://javaparser.org/
Python subprocess模块官方文档：https://docs.python.org/3/library/subprocess.html

以上就是我们关于"跨语言代码解析：利用Python调用Java的JavaParser解析Java源代码"的博客。希望这篇博客对你在跨语言开发过程中有所帮助。

