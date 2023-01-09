+++
author = "南宫乘风"
title = "[Linux小技巧] 将 rm 命令删除的文件放在回收站"
date = "2020-03-26 17:21:50"
tags=['rm', '命令', 'shell', '脚本', '脚本语言']
categories=[]
image = "post/4kdongman/60.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/105123382](https://blog.csdn.net/heian_99/article/details/105123382)

### 自定义rm命令

**linux系统的rm命令太危险，一不小心就会删除掉系统文件。 写一个shell脚本来替换系统的rm命令，要求当删除一个文件或者目录时，都要做一个备份，然后再删除。下面分两种情况，做练习：**

### **1. 简单的实现：**

假设有一个大的分区/data/，每次删除文件或者目录之前，都要先在/data/下面创建一个隐藏目录，以日期/时间命名，比如/data/.20170327/，然后把所有删除的文件同步到该目录下面，可以使用rsync -R 把文件路径一同同步，示例

```
#!/bin/bash
#name:南宫乘风
#email：heian99@163.com
fileName=$1
now=`date +%Y%y%d`
dir=$(/data/$now)
read  -p "你确定删除这文件或者目录吗 $1 ? yes|no :" input
if [ $input == "yes" ] || [ $input == "y" ]; then
     # 判断目录是否存在
     if [ ! -d $dir ]; then
        mkdir /data/$now
    fi
    # rsync同步要删除的文件和目录
     rsync -aR $1/ /data/$now/$1/
     rm -rf $1
    
elif [ $input == "no" ] || [ $input == "n" ]; then
     # 选择no退出
     exit 0
else
     # 如果选择别的输入符，提示
     echo "只能输入yes或者no"
     exit 0
fi
```

### **2.复杂的实现：**

不知道哪个分区有剩余空间，在删除之前先计算要删除的文件或者目录大小，然后对比系统的磁盘空间，如果够则按照上面的规则创建隐藏目录，并备份，如果没有足够空间，要提醒用户没有足够的空间备份并提示是否放弃备份，如果用户输入yes，则直接删除文件或者目录，如果输入no，则提示未删除，然后退出脚本，示例： 

```
#!/bin/bash
#name:南宫乘风
#email：heian99@163.com
now=$(date +%Y%m%d)
#判断文件大写
f_size=$(du -sk $dir | awk '{print $1}')
#判断磁盘大小
disk_szie=$(df -k| grep -vi filesystem | awk '{print $4}'|sort -n|tail -n1)
#判断最大的目录在哪里
big_filesystem=$(df -k|grep -vi filesystem | sort -n -k4 | tail -n1 | awk '{print $NF}')
#判断文件大小和磁盘大小比较
if [ $f_size -lt $disk_szie ]; then
     # 输入选项，准备开始删除工作
     read  -p "你确定删除这文件或者目录吗 $1 ? yes|no :" input
    if [ $input == "yes" ] || [ $input == "y" ]; then
         # 判断存放目录是否存在
         if [ ! -d $big_filesystem/data/$now ]; then
             # 不存在新建目录
            mkdir -p $big_filesystem/data/$now
         fi
         rsync -aR $1 $big_filesystem/$now/
         rm -rf $1
    #判断输入no的情况
    elif [ $input == "no" ] || [ $input == "n"]; then
         exit 0
    else
       # 如果选择别的输入符，提示
        echo "只能输入yes或者no"  
    fi
    
else
     # 判断磁盘空间不足的情况
     echo "这磁盘没有足够的空间备份: $1."
     read -p "你还想删除"$1"吗？ yes|no ：" input
     if [ $input == "yes" ] || [ $input == "n" ]; then
          # body
          echo "$1将会在3秒后删除，将不会有备份"
          for i in `seq 1 5`; do echo -ne "."; sleep 1; done
          rm -rf $1

     elif [ $input == "no" ] || [ $input == "n" ]; then
          echo "将不会删除 $1."
          exit 0
     else
          # 如果选择别的输入符，提示
           echo "只能输入yes或者no"  
     fi
     
fi
```

我的gitee：[https://gitee.com/chengfeng99/Linux-DevOps](https://gitee.com/chengfeng99/Linux-DevOps)

欢迎和我一起来讨论学习

![20200326172100697.png](https://img-blog.csdnimg.cn/20200326172100697.png)

#  
