---
author: 南宫乘风
categories:
- Java
date: 2019-11-14 18:00:16
description: 实现加密为了保护有些数据，就需要采取一些手段来进行数据的加密，防止被别人破解。简介的全称是信息摘要算法英文：，一种被广泛使用的密码散列函数，可以产生一个位字节，字节位的散列值常见的是用位的进制表示，比。。。。。。。
image: ../../title_pic/17.jpg
slug: '201911141800'
tags:
- MD5
- Java
title: Java使用MD5加密算法，实现等登陆功能
---

<!--more-->

## Java实现MD5加密

为了保护有些数据，就需要采取一些手段来进行数据的加密，防止被别人破解。

## MD5简介

md5的全称是**md5信息摘要算法（英文：MD5 Message-Digest Algorithm ）**，一种被广泛使用的密码散列函数，可以产生一个128位（16字节，1字节8位）的散列值（常见的是用32位的16进制表示，比如：0caa3b23b8da53f9e4e041d95dc8fa2c），用于确保信息传输的完整一致。

## 功能实现

### 1、MD5的工具类

```java

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
/**
 * 南宫乘风
 */
public class MD5Utils {
    /**
     * MD5加密类
     * @param str 要加密的字符串
     * @return    加密后的字符串
     */
    public static String code(String str){
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(str.getBytes());
            byte[]byteDigest = md.digest();
            int i;
            StringBuffer buf = new StringBuffer("");
            for (int offset = 0; offset < byteDigest.length; offset++) {
                i = byteDigest[offset];
                if (i < 0)
                    i += 256;
                if (i < 16)
                    buf.append("0");
                buf.append(Integer.toHexString(i));
            }
            //32位加密
            return buf.toString();
            // 16位的加密
            //return buf.toString().substring(8, 24);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    /**
     * 测试方法
     * @param args
     */
    public static void main(String[] args) {
        System.out.println(code("111111"));
    }
}
```

最下面这个是测试方法

![](../../image/20191114175329182.png)

### 2、项目中调用

我在项目的接口中调用MD5的方法

```java
public User checkUser(String username, String password) {
        User user = userRepository.findByUsernameAndPassword(username, MD5Utils.code(password));
        return user;
    }
```

**解析**：这就是用户登录把密码传递过来，进行MD5加密后，在和数据库中的密码进行对比（数据库中的密码是MD5格式存储的）

![](../../image/20191114175653987.png)

### 3、思路拓展（防止重要信息被盗用）

1.  账号注册
2.  密码登录
3.  信息保护
4.  资料加密

等等，许多的功能都可以用到这样的方法来进行加密。