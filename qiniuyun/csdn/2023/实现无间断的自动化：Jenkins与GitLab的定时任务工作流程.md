---
author: 南宫乘风
categories:
- 项目实战
- Jenkins
date: 2023-06-12 11:20:03
description: 简介：是一个流行的开源自动化服务器，而是一个强大的代码托管和协作平台。通过结合和，我们可以建立一个强大的定时任务自动化工作流程，实现代码拉取、构建、测试和部署的自动化。本篇博客将介绍如何使用与相结合，。。。。。。。
image: ../../title_pic/12.jpg
slug: '202306121120'
tags:
- jenkins
- 自动化
- gitlab
title: 实现无间断的自动化：Jenkins与GitLab的定时任务工作流程
---

<!--more-->

## 简介：
Jenkins是一个流行的开源自动化服务器，而GitLab是一个强大的代码托管和协作平台。通过结合Jenkins和GitLab，我们可以建立一个强大的定时任务自动化工作流程，实现代码拉取、构建、测试和部署的自动化。本篇博客将介绍如何使用Jenkins与GitLab相结合，构建一个完整的定时任务自动化流程。

## 背景
目前我们的代码存放在gitlab中，有版本控制比较方便开发。现在有个Crontab的仓库存放，日常的定时任务脚本。
如果放在Linux的crontab上，代码更新完毕 需要及时拉取才会 执行新的代码，比较麻烦。这边就采用jenkins的crontab来执行定时任务

## 优势
Jenkins可以满足您提到的核心需求，并提供以下功能：

- 审计执行日志：Jenkins记录每个任务的执行日志，并提供可视化界面来查看和审计任务的执行历史。您可以随时查看任务的执行输出、错误信息以及任何产生的警告或异常。

- 任务超时强制kill：Jenkins允许您为每个任务设置超时时间。如果任务在指定的时间内未完成，Jenkins会强制终止任务的执行，以防止无限循环或资源占用等问题。

- 任务的超时重试：Jenkins提供了内置的插件，如Pipeline和Job DSL，可以轻松地编写自定义的任务流程，并支持任务的超时重试。您可以在任务失败或超时后自动触发重试，并设置重试次数和时间间隔，以确保任务能够成功完成。

- 错误重试和自定义次数：Jenkins提供了灵活的错误处理机制，您可以在任务执行失败时自定义处理逻辑。您可以设置任务在遇到错误时自动触发重试，并指定重试次数和重试间隔，以便应对临时性的错误和问题。

Jenkins作为一个开源的自动化服务器，具有广泛的社区支持和丰富的插件生态系统，可以满足各种复杂的任务调度和自动化需求。通过适当的配置和使用插件，您可以实现高度定制化的任务调度和执行流程，满足您特定的需求，并确保任务的可靠执行和错误处理。

## Gitlab创建仓库
1. 登录GitLab：打开您的Web浏览器，输入GitLab的URL，并使用您的GitLab账户登录。
2. 导航到项目页面：登录后，您将看到GitLab的仪表板或项目列表。点击页面顶部的“+”按钮或导航栏上的“New project”按钮。
3. 创建新项目：在新项目页面上，您需要提供以下信息来创建新的仓库：

    * 项目路径：指定项目的路径，也就是项目在GitLab上的URL地址。它将用于在仓库的URL中唯一标识您的项目。
    * 可见级别：选择您希望谁能访问您的项目。您可以选择公开（Public）、私有（Private）或内部（Internal）可见性级别。
    * 项目名称：为您的项目指定一个易于识别的名称。
    * 描述（可选）：提供关于项目的简要描述，以便其他人了解项目的目的和内容。
    * 初始化仓库：选择是否要初始化一个空的仓库，或者您可以选择从现有的代码库导入代码。
4. 完成设置：在提供必要信息后，单击页面下方的“Create project”按钮。GitLab将根据您提供的信息创建新的仓库，并将您重定向到新仓库的页面。
5. 配置仓库（可选）：在新仓库页面上，您可以进一步配置仓库的设置，例如添加项目成员、设置分支保护规则、启用CI/CD等。这些设置可以根据您的具体需求进行调整。
![](../../image/277229e1fa6f475fa37e8fcfd810abeb.png)
添加测试脚本
### **monitor.sh**
```bash
#!/bin/bash
echo "======================="
echo $(date)

#!/bin/bash
# @Author: danqing
# @Description: Host Daily Check Script
# beseem CentOS6.X CentOS7.X
# 
echo "Host Daily Check Script"
[ $(id -u) -gt 0 ] && echo "请用root用户执行此脚本！" && exit 1
 
 
if [ ! -d /root/check_log  ];then
  mkdir /root/check_log
  echo "/root/check_log检查日志存放目录创建成功"
else
  echo "/root/check_log检查日志存放目录已存在"
fi
 
 
function getSystem(){
echo ""
echo ""
echo "############################ 系统信息检查 ############################"
Default_LANG=${LANG}
OS=$(uname -o)
Release=$(cat /etc/redhat-release 2>/dev/null)
Kernel=$(uname -r)
Hostname=$(uname -n)
Nowdate=$(date +'%F %T')
LastReboot=$(who -b | awk '{print $3,$4}')
uptime=$(uptime | sed 's/.*up \([^,]*\), .*/\1/')
echo " 语言环境: $Default_LANG"
echo " 系统: $OS"
echo " 发行版本: $Release"
echo " 内核: $Kernel"
echo " 主机名: $Hostname"
echo " 当前时间: $Nowdate"
echo " 最后启动: $LastReboot"
echo " 运行时间: $uptime"
}
 
 
function getCpu(){
echo ""
echo ""
echo "############################ CPU检查 ############################"
Physical_CPUs=$(grep "physical id" /proc/cpuinfo| sort | uniq | wc -l)
Virt_CPUs=$(grep "processor" /proc/cpuinfo | wc -l)
CPU_Kernels=$(grep "cores" /proc/cpuinfo|uniq| awk -F ': ' '{print $2}')
CPU_Type=$(grep "model name" /proc/cpuinfo | awk -F ': ' '{print $2}' | sort | uniq)
CPU_Hz=$(cat /proc/cpuinfo | grep "cpu MHz" | uniq | awk -F':' '{sub(/ /,"",$2);printf "%s MHz\n",$2}')
CPU_Arch=$(uname -m)
CPU_Usage=$(cat /proc/loadavg | awk '{print $1}')
echo "物理CPU个数: $Physical_CPUs"
echo "逻辑CPU个数: $Virt_CPUs"
echo "每CPU核心数: $CPU_Kernels"
echo "CPU型号: $CPU_Type"
echo "CPU频率: $CPU_Hz"
echo "CPU架构: $CPU_Arch"
echo "CPU使用率: ${CPU_Usage}%"
}
 
 
function getMemory(){
echo ""
echo ""
echo "############################ 内存检查 ############################"
Memory_Used=$(awk '/MemTotal/{total=$2}/MemFree/{free=$2}END{print (total-free)/1024/1024}'  /proc/meminfo)
Memory_Total=$(awk '/MemTotal/{total=$2}END{print (total)/1024/1024}' /proc/meminfo)
# kb的换算是1000 kB的换算是1024
Memory_Usage=$(awk '/MemTotal/{total=$2}/MemFree/{free=$2}END{print (total-free)/total*100}'  /proc/meminfo)
echo "已使用内存/全部内存: ${Memory_Used}GB/${Memory_Total}GB"
echo "内存使用率: ${Memory_Usage}%"
}
 
 
function getDisk(){
echo ""
echo ""
echo "############################ 硬盘检查 ############################"
Disk_Count=$(lsblk |awk '/disk/{print $1}'|wc -l)
echo "硬盘数量: ${Disk_Count}个"
echo "硬盘分区情况: "
echo "`df -hTP | sort |grep -E "/sd|/mapper" |awk '{print ($1 "\t\n" "  文件系统"$2 "  合计"$3 "  已用"$4 "  剩余"$5 "  使用率"$6 "  挂载点"$7)}'`"
# -P, --portability 使用 POSIX 输出格式,方便shell过滤处理
smartctl -V >&/dev/null
if [ $? -eq 0 ]; then
    echo "smartctl工具已安装,可以进行硬盘健康检测: "
    for i in $(lsblk |awk '/disk/{print $1}')
    do
      echo "硬盘"$i   `smartctl -H /dev/$i |grep -Ei "OK|PASSED|FAILED|Failure|Failed"`
    done
else
    echo "smartctl工具未安装,无法进行硬盘健康检测"
fi
# "\n磁盘IO信息:$(iotop -bon 1 &>/dev/null || echo 'iotop 未安装信息获取失败')"
}
 
 
function getNetwork(){
echo ""
echo ""
echo "############################ 网络检查 ############################"
Network_Device=$(cat /proc/net/dev | awk 'NR>2 && $1 !~/lo/ {sub(/:/,"");print $1}')
for i in $Network_Device
do
  #echo "网卡：$i  状态: $(ip link show $Network_Device | awk 'NR==1{print $9}') RX: $(ethtool -g $Network_Device | grep "RX:" | tail -1 | awk '{print $2}') TX: $(ethtool -g $Network_Device | grep "TX:" | tail -1 | awk '{print $2}')"
  # rx是接收(receive),tx是发送(transport)
  Mac_Info=$(ip link | egrep -v "lo" | grep link | awk '{print $2}')
  echo "MAC地址: $Mac_Info"
  Private_Ip=$(ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\1", "g", $2)}')
  echo "IP地址: $Private_Ip"
  # Public_Ip=$(curl ifconfig.me -s)
  # echo "公网IP地址: $Public_Ip"
  Gateway=$(ip route | grep default | awk '{print $3}')
  # echo "网关地址: $Gateway"
  # Dns_Config=$(grep nameserver /etc/resolv.conf| grep -v "#" | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
  # echo "DNS地址: $Dns_Config"
  echo "网关连接情况: $(ping -c 4 -i 0.5 -W 3 $Gateway &>/dev/null && echo '正常通信' || echo '无法通信')"
  echo "外网连接情况: $(ping -c 4 -i 0.5 -W 3 baidu.com &>/dev/null && echo '正常通信' || echo '无法通信')"
  # 发送4次请求包，每次间隔0.5秒，最长等待时间为3秒
done
Listen_Port=$(ss -tuln | grep LISTEN | awk '{print $5}' | awk -F: '{print $2$4}' | sort |uniq -d | tr '\n' ',' | sed 's/,$//')
echo "系统运行的端口: $Listen_Port"
}
 
 
function check(){
echo "Host Daily Check Script"
getSystem
getCpu
getMemory
getDisk
getNetwork
}
 
 
RESULTFILE="/root/check_log/check-`date +%Y%m%d`.txt"
check > $RESULTFILE
echo "检查结果：$RESULTFILE"
cat  $RESULTFILE

```
## Jenkins配置Gitlab的认证凭证
在Jenkins中配置GitLab的认证凭证，您可以按照以下步骤进行操作：

1. 登录Jenkins：打开您的Web浏览器，输入Jenkins的URL，并使用管理员账户登录到Jenkins控制台。
2. 导航到凭据页面：在Jenkins控制台的主页上，点击左侧导航栏中的"凭据"（Credentials）选项。
![在这里插入图片描述](../../image/5f6302adb44b46a3b49ff01f12d01f2d.png)

3. 创建新的凭据：在凭据页面，点击"系统"（System）下方的"全局凭据"（Global credentials）选项。
4. 添加凭据：在全局凭据页面，点击"添加凭据"（Add Credentials）按钮。
5. 选择凭据类型：在"添加凭据"页面，选择GitLab凭据的类型。根据您的GitLab配置，可以选择不同的类型，例如"Username with password"（用户名和密码）或"SSH Username with private key"（SSH用户名和私钥）等。
![在这里插入图片描述](../../image/be1283115ae34ae2b61f180a16af1646.png)

6. 填写凭据信息：根据您选择的凭据类型，填写相关的凭据信息。例如，如果选择"Username with password"，则需要提供GitLab的用户名和密码；如果选择"SSH Username with private key"，则需要提供GitLab的SSH用户名和私钥等信息。
![在这里插入图片描述](../../image/2c236aa268c94b84a8f8de03d51a3274.png)

7. 保存凭据：完成填写凭据信息后，点击页面下方的"保存"（Save）按钮，将凭据保存到Jenkins中。
8. 配置Jenkins项目：在Jenkins中的项目配置中，找到与GitLab相关的配置部分，例如构建触发器或源码管理。在这些配置中，您将看到"凭据"（Credentials）的选项。
9. 选择凭据：在相关配置中，找到"凭据"（Credentials）选项，并选择您之前保存的GitLab凭据。
10. 保存配置：完成凭据选择后，确保保存项目的配置。

完成上述步骤后，Jenkins将能够使用您配置的GitLab凭据进行与GitLab的交互，例如拉取代码、触发构建等操作。这样，您就可以通过Jenkins与GitLab进行无缝集成，并实现持续集成和持续交付的自动化流程。

## Jenkins设置定时任务
1. 登录Jenkins：使用管理员账户登录到Jenkins控制台。
2. 创建新项目：在Jenkins控制台主页上，点击"新建任务"（New Item）按钮。
3. 输入项目名称：为新项目指定一个易于识别的名称，并选择自由风格的软件项目（FreeStyle Project）类型。
![在这里插入图片描述](../../image/b6092e2fcd3f42baa0be8d9264fa52d2.png)

4. 配置源码管理：在项目配置页面的"源码管理"（Source Code Management）部分，选择Git作为源码管理工具，并填写GitLab仓库的URL。
5. 配置凭据：如果您之前在Jenkins中配置了GitLab的认证凭证，请在源码管理部分选择相应的凭据，以便Jenkins能够访问GitLab仓库。
![在这里插入图片描述](../../image/9037ad662c264df8b693eaf4045137ce.png)

6. 配置构建触发器：在项目配置页面的"构建触发器"（Build Triggers）部分，选择"定时构建"（Build periodically）选项。
7. 设置定时任务：在"定时构建"选项中，使用Cron表达式指定定期执行任务的时间。例如，要每天的上午9点执行任务，可以使用"0 9 * * *"的Cron表达式。
![在这里插入图片描述](../../image/7c4998301a234eee891b9702a207ebed.png)

8. 配置构建步骤：在项目配置页面的"构建"（Build）部分，配置需要执行的构建步骤。这可以是构建脚本、测试命令、部署操作或任何其他您希望Jenkins执行的任务。
![在这里插入图片描述](../../image/784d607c9959442282da27290761c14c.png)

9. 保存配置：完成配置后，确保保存项目的配置。

Jenkins将按照您设置的定时任务，定期拉取GitLab仓库中的代码，并执行您配置的构建步骤。您可以在Jenkins控制台的项目页面上查看每次构建的执行日志和结果，以及任何产生的警告或错误。

## Jenkins定时任务执行
### 时间
![在这里插入图片描述](../../image/cc6e47c6507145de9c0232eb2f52d266.png)
### 查询日志

![在这里插入图片描述](../../image/b5aefef3b2d54e03bef842769bf14cac.png)

