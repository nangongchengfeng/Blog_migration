+++
author = "南宫乘风"
title = "压缩，解压缩 和tar详细介绍"
date = "2019-01-23 23:19:14"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/44.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86618970](https://blog.csdn.net/heian_99/article/details/86618970)

# **文件压缩/解压缩  gzip   bzip2  xz**

## **只能压缩文件，不能压缩文件夹（压缩完后，文件会消失）**

**先建三个文件来进行演示**

```
touch ./{1..3}.txt

```

![20190123225310151.png](https://img-blog.csdnimg.cn/20190123225310151.png)

### ** 文件已经创建好，下面就开始介绍文件的压缩和解压（ gzip   bzip2    xz ）**

 

# <u>**gzip介绍：**</u>

**压缩： gzip  源文件**

```
gzip 1.txt
```

![20190123225534394.png](https://img-blog.csdnimg.cn/20190123225534394.png)

**解压缩 ： gzip -d 源文件**

```
gzip -d  1.txt.gz 
```

![20190123225717616.png](https://img-blog.csdnimg.cn/20190123225717616.png)

# <u>bzip2介绍</u>

**压缩：bzip2  源文件**

```
bzip2 2.txt
```

![20190123225948102.png](https://img-blog.csdnimg.cn/20190123225948102.png)

**解压缩 : bizp2  -d  源文件**

```
bzip2 -d 2.txt.bz2
```

![2019012323044277.png](https://img-blog.csdnimg.cn/2019012323044277.png)

# ** <u>xz介绍</u>**

**压缩：xz 源文件**

```
xz 3.txt
```

![20190123230639519.png](https://img-blog.csdnimg.cn/20190123230639519.png)

**解压缩：xz -d 源文件**

```
xz -d 3.txt.xz 

```

![20190123231253353.png](https://img-blog.csdnimg.cn/20190123231253353.png)

 

# **创建打包文件 ------tar**

## **1）创建打包文件   *.tar**

### **# tar cf 打包文件名称  源文件**

### **e：creat创建**

### **f :  file文件**

![20190123231536899.png](https://img-blog.csdnimg.cn/20190123231536899.png)

## **2)解包**

### ** # tar xf 打包文件名称 【-c解压到的目录】**

![20190123231729588.png](https://img-blog.csdnimg.cn/20190123231729588.png)

## **3）查看包**

### **#tar tvf 打包的文件名称 **

![20190123231619516.png](https://img-blog.csdnimg.cn/20190123231619516.png)

# **                                          调用gzip使用压缩  解压缩**

**压缩**

**#tar czf 打包文件名称  源文件**

**       z：调用gzip**

**解压缩：**

**# tar xzf 打包文件的名称 【-c 目录名称】**

 

# **                                     调用bzip2使用压缩  解压缩**

**压缩**

**#tar cjf 打包文件名称 目录名称**

**j：调用bzip2**

**解压缩**

**#tar xjf 打包文件名称 【-c 目录名称】**

 

# **                                  调用xz使用压缩  解压缩**

**压缩**

**#tar cJf 打包文件名称 目录名称**

**J：调用zx**

**解压缩**

**#tar xJf 打包文件名称 【-c 目录名称】**

 

 

 

 
