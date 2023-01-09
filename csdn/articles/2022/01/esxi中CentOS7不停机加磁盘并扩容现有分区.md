+++
author = "南宫乘风"
title = "esxi中CentOS7不停机加磁盘并扩容现有分区"
date = "2022-01-25 17:35:53"
tags=['硬盘', '扩容']
categories=[]
image = "post/4kdongman/33.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104893746](https://blog.csdn.net/heian_99/article/details/104893746)

linux的磁盘容量扩容，基于lvm，即逻辑卷管理。具体是什么请百度，这里不细述。

此次操作的目的是为了给已存在的linux主机的其中一个数据分区扩容。

环境：esxi6.5  虚拟机系统centos7

![20200316104601736.png](https://img-blog.csdnimg.cn/20200316104601736.png)

简单来说，扩容这件事分三步

**一、从esxi中为此虚拟机增加硬盘，并让centos系统识别出此硬盘**

**二、将此硬盘进行分区、格式化**（重点是这里的分区不是类似于windows，分完就能用了，而它需要一个挂载的过程，要么单独挂载，要么加入lvm挂载，否则在linux中是无法访问的）

**三、卷组管理**
-    1、将分好区的硬盘创建为物理卷-    2、将此物卷直接进行挂载到文件系统-    3、或将此物理卷加入到lvm卷组中-    4、对加入到卷组的空间进行逻辑卷扩容或是创建为逻辑卷再进行扩容等操作
以下是本次操作的过程记录

## 1、首先看一下未添加硬盘前的系统磁盘状态，

![202003161047479.png](https://img-blog.csdnimg.cn/202003161047479.png)

## 2、在esxi中添加硬盘的过程就不说了，添加过硬盘，需要对scsi接口进行扫描，就相当于扫描新硬件

![20200316110633353.png](https://img-blog.csdnimg.cn/20200316110633353.png)

### 端口太多，一个个扫描太慢，我就写个简单脚本执行。

```
ls | sort &gt; /opt/host.txt
```

![20200316110801653.png](https://img-blog.csdnimg.cn/20200316110801653.png)

### **批量扫描脚本**

```

#!/bin/bash
DIR="/sys/class/scsi_host/"
for i in `cat host.txt`
do
        echo "- - -" &gt; $DIR$i/scan
        echo $DIR$i/scan
done
rm -rf /opt/host.txt

```

### 运行脚本

```
[root@kvm opt]# ls
backup  host.sh  host.txt  rh
[root@kvm opt]# pwd
/opt
[root@kvm opt]# bash host.sh 

```

![20200316111014697.png](https://img-blog.csdnimg.cn/20200316111014697.png)

## 3、可以看到新加的10G硬盘已经被识别为/dev/sdb

![20200316111142626.png](https://img-blog.csdnimg.cn/20200316111142626.png)

## 4、查看一下scsi的状态，以上都是准备工作，状态都对，后面操作就容易

```
cat /proc/scsi/scsi
```

![20200316111612685.png](https://img-blog.csdnimg.cn/20200316111612685.png)

### 5、对新硬盘进行分区，此处是新建了一个主分区，默认id为1，所以分好后就是sdb1

![20200316112118387.png](https://img-blog.csdnimg.cn/20200316112118387.png)

### 6、我们的目的是为了用lvm进行管理，所以在分完区后，要将分区属性标记为lvm的8e

![20200316112253487.png](https://img-blog.csdnimg.cn/20200316112253487.png)

### 7、分完后可以看到分区信息，/dev/sdb1的8e,然后重读一下分区表，刷新

![20200316112354827.png](https://img-blog.csdnimg.cn/20200316112354827.png)

已经分区成功了

![20200316112738878.png](https://img-blog.csdnimg.cn/20200316112738878.png)

![20200316113306596.png](https://img-blog.csdnimg.cn/20200316113306596.png)

## 8、上面分完区，下面当然就是加入卷了，先把sdb1做成一个新的物理卷



![20200316113804728.png](https://img-blog.csdnimg.cn/20200316113804728.png)

### 9、用vgdisplay查看一下卷组的状态，可以看到原先centos组里面没有空余，那么我们要做的就是把刚加的磁盘，刚分好的区，然后刚创建成的物理卷加入到这个centos组里去，加进组才能在组里进行分配嘛。所以vgextend centos /dev/sdb1,加完再看vgdisplay，空余空间为10G，很明显，新加的磁盘已处理待分配状态

![20200316114005356.png](https://img-blog.csdnimg.cn/20200316114005356.png)

```
[root@kvm dev]# vgextend centos_kvm /dev/sdb1
  Volume group "centos_kvm" successfully extended
```

![20200316114116853.png](https://img-blog.csdnimg.cn/20200316114116853.png)

![20200316114222108.png](https://img-blog.csdnimg.cn/20200316114222108.png)

### 10、最后就是剑指黄龙，我要给var进行扩容，lvresize -L +10G /dev/centos/var

```
[root@kvm centos_kvm]# lvresize -L +20G /dev/centos_kvm/root 
  Size of logical volume centos_kvm/root changed from &lt;26.00 GiB (6655 extents) to &lt;46.00 GiB (11775 extents).
  Logical volume centos_kvm/root successfully resized.
[root@kvm centos_kvm]# vgdisplay
  --- Volume group ---
  VG Name               centos_kvm
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  5
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               128.99 GiB
  PE Size               4.00 MiB
  Total PE              33022
  Alloc PE / Size       12543 / &lt;49.00 GiB
  Free  PE / Size       20479 / &lt;80.00 GiB
  VG UUID               K35BzQ-nhXT-zFsf-W1kp-T9iq-kcFx-hfTdTN

```

![20200316114711966.png](https://img-blog.csdnimg.cn/20200316114711966.png)

### 11、上面那一步不算完，记得不，之前我虽然分区了，创建卷了，加入卷组，但实际上我没格式化。那么OK，这里用xfs_growfs /dev/centos/var重新识别一下新卷的容量，是扩容后的哦，扩容时加上的新磁盘也就同时被格式化了。

xfs_growfs 是centos7的命令，在centos6.X中是resize2fs，其实还是6.x的命令好记。





此处讲的是直接将新加的磁盘扩容到已有分区，还可以做的是，在将新分区加入卷组后：

1、创建需要大小的独立逻辑卷，将它进行单独挂载使用。（别忘了改一下/etc/fstab，不然下次重启还要手动挂载）

```
   lvcreate -L 4G -n newlv centos  在centos卷组的空闲空间中划出4G的新逻辑卷，起名为newlv

    mkfs.xfs /dev/centos/newlv    将新的newlv格式化为xfs文件系统
```

1、不创新需要大小的独立逻辑卷，将自由空间扩容到现有的分区挂载点

基本就这些了。lvm管理说实话真挺爽的。特别是在esxi主机上使用，无需停机，直接加装扩容。

有正就有反，能装就得能卸，能扩就得能减。

1、直接扩容原有逻辑卷大小的卸载新加容量

>  
   lvreduce -L -10G /dev/centos/var  先把扩容的容量减掉 


   如果是创建成为一个独立的逻辑卷，则

>  
   lvremove /dev/centos/newlv1 


2、从卷组中删掉加入的磁盘分区

>  
   vgreduce centos /dev/sdb1 


3、从物理卷中卸掉sdb1

>  
 -   pvremove /dev/sdb1


最后就是在esxi中删硬件了。




