+++
author = "南宫乘风"
title = "Git引起的 gitlab-runner 报错"
date = "2022-12-01 11:59:37"
tags=['git', 'gitlab', 'github']
categories=['错误问题解决']
image = "post/4kdongman/57.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/128129761](https://blog.csdn.net/heian_99/article/details/128129761)

在查看gitlab CI作业时，发现意外报错

```
重新初始化现存的 Git 版本库于 /home/gitlab-runner/builds/nzfEHD8s/0/devops/dig/.git/
fatal: git fetch-pack: expected shallow list
fatal: The remote end hung up unexpectedly
Cleaning up project directory and file based variables
00:00
ERROR: Job failed: exit status 1
```

![9e1bb93b2a564c38aa009350b889c13c.png](https://img-blog.csdnimg.cn/9e1bb93b2a564c38aa009350b889c13c.png)

 报错时由于git版本引起的，查看git版本

```
[root@bt dig]# git version
git version 1.8.3.1

```

使用[yum](https://so.csdn.net/so/search?q=yum&amp;spm=1001.2101.3001.7020) list | grep git，yum默认阿里云源里面最新的版本就是1.18.3 

我们需要升级git 的版本

## 1、安装源

```
yum install http://opensource.wandisco.com/centos/7/git/x86_64/wandisco-git-release-7-2.noarch.rpm
```

## 2、更新git软件

```
yum install git -y
```

3、检查版本测试

```
[root@bt dig]# git --version
git version 2.31.1
```

版本已经更新最2.31了，再次执行gitlab CI作业，报错已经解决了。

![d7e780b3bf9345d0b8c736b14cad3b8a.png](https://img-blog.csdnimg.cn/d7e780b3bf9345d0b8c736b14cad3b8a.png)

 
