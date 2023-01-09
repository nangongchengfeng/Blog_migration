+++
author = "南宫乘风"
title = "Linux shell while循环语句"
date = "2019-04-01 19:32:44"
tags=['linux']
categories=['Linux Shell']
image = "post/4kdongman/14.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/88955260](https://blog.csdn.net/heian_99/article/details/88955260)

### **for ：明确循环次数<br> while ：不确定循环换次数**

### **while循环**

### （1）

**while CONDITION；do<br>       statement<br>       statement<br>       &lt;改变循环条件真假的语句&gt;<br> done**

### 编写脚本，计算1--100的和

```
#!/bin/bash
#
sum=0
i=1

while [ $i -le 100  ];do
    let sum=$sum+$i
    let i=$i+1
done

echo $sum
```

### <br>编写while循环，输入q退出（不输入q，不退出）

```
#!/bin/bash
#
read -p "请输入你的选择：" choice

while [ $choice != q  ];do
    echo -e "\033[31m输入错误\033[0m" #加的颜色代码
    read -p "请输入你的选择：" choice
done
```

### ![20190401192859102.png](https://img-blog.csdnimg.cn/20190401192859102.png)<br>**（2）**

while true；do<br>       statement<br>       statement<br>       &lt;break退出&gt;<br> done

###  

### 编写while循环，输入q退出（不输入q，不退出）

```
#/bin/bash
#
while true;do
    read -p "请输入你的选择" str
    echo "输入错误"
    if [ $str == q ];then
        break
    fi
done
```

### 编写脚本，每4秒查看系统的内存

```
#!/bin/bash
#
while true;do
    uptime
    sleep 3
done
```

![20190401193025486.png](https://img-blog.csdnimg.cn/20190401193025486.png)<br>**（3）**

while read line;do<br>     statement<br>     statement<br> done &lt; file

### <br>编写脚本，向系统每个用户打招呼

```
v#!/bin/bash
#
while read line;do
    sh_name=$(echo $line | awk -F: '{print $1}')
    echo "Hello $sh_name"

done &lt; /etc/passwd
```

### ![20190401193117987.png](https://img-blog.csdnimg.cn/20190401193117987.png)<br>编写脚本，统计/bin/bash /sbin/nologin的个数

```
[root@wei while]# cat 6.sh 
#!/bin/bash
#
bash_number=0
nologin_number=0

while read line;do
    sh_name=$(echo $line | awk -F: '{print $7}')
    case $sh_name in
        /bin/bash)
            let bash_number=$bash_number+1
            ;;
        /sbin/nologin)
            let nologin_number=$nologin_number+1
            ;;
    esac

done &lt; /etc/passwd

echo "bash用户数量：$bash_number"
echo "nologin_number用户数量：$nologin_number"
```

### 执行效果

```
[root@wei while]# ./6.sh 
bash用户数量：17
nologin_number用户数量：17
```

![20190401193158805.png](https://img-blog.csdnimg.cn/20190401193158805.png)

### <br>util循环：

### util CONDITION；do<br>     statement<br>     statement<br> done

### **条件为假时，执行循环，条件为真时，结束循环**

# <br>重点掌握

# if，case

# for，while
