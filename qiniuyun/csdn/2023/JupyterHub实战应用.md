---
author: 南宫乘风
categories:
- Linux服务应用
date: 2023-08-17 15:05:02
description: 一、是一个非常有用的工具，我们可以在浏览器中任意编辑调试我们的代码，并且支持语法，可以说是科研利器。但是这种情况适合个人使用，也就是以我们自己的主机作为服务器，然后我们用自己的浏览器编辑自己本机的代码。。。。。。。
image: ../../title_pic/45.jpg
slug: '202308171505'
tags:
- python
- ipython
title: JupyterHub实战应用
---

<!--more-->

## 一、JupyerHub

jupyter notebook 是一个非常有用的工具，我们可以在浏览器中任意编辑调试我们的python代码，并且支持markdown 语法，可以说是科研利器。但是这种情况适合个人使用，也就是jupyter notebook以我们自己的主机作为服务器，然后我们用自己的浏览器编辑自己本机的python代码。

最近公司搭建了业务模型的服务器，每个人都有一个用户可以使用GPU资源，但是每次写代码要在本地调试好了然后再ssh提交到服务器运行，如果有问题，还要再在本地更改然后再次提交，非常的麻烦。为了解决这个烦恼，我们在GPU服务器上搭建了jupyterhub, 它和notebook不同之处在于它是一个hub，哈哈，也就是notebook的服务器，把它装在服务器上，然后大家可以通过局域网在浏览器上进行python代码的编辑和调试。

jupyterhub 和 jupyter notebook一样是python的一个包，可以通过pip安装，也可以通过 conda安装，在服务器端安装就可以供大家使用。

## 二、环境
确保你的服务器环境满足以下要求：

- 一台运行支持的操作系统（如 Ubuntu、CentOS 等）的服务器
- 安装了 Python 和 pip
- 足够的系统资源（CPU、内存、磁盘空间）

### 1、Python环境
安装 Miniconda 是管理 Python 环境以及安装 Python 包的一个方便工具。
以下是在 CentOS 上安装 Miniconda 的步骤：
1. 下载 Miniconda 安装包：

在终端中执行以下命令，下载适用于 CentOS 的 Miniconda 安装包（64 位）：
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

或

curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
2. 运行安装脚本：

运行下载的脚本来安装 Miniconda。首先，给脚本执行权限：
```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh
```
然后运行安装脚本：

```bash
./Miniconda3-latest-Linux-x86_64.sh
```
按照提示，阅读许可协议并同意。

3. 配置 Miniconda：

安装过程中会提示你是否将 Miniconda 添加到 shell 的 PATH 中。选择 "yes"，这将允许你在终端中直接使用 conda 命令。

4. 重启终端：

安装完成后，为了使配置生效，关闭当前终端窗口，然后重新打开一个新的终端。

5.测试安装：

在新的终端中，运行以下命令来验证 conda 是否已成功安装：
```bash
root@bt:/home/fengkong# conda --version
conda 23.5.0

```
6. 安装插件补全

```bash
conda install -c conda-forge conda-bash-completion
```
备注：
```bash
3、配置环境变量：.bashrc
如果选择了init会自己配置
export PATH=~/miniconda3/bin:$PATH
3.5、卸载miniconda
找到miniconda3的文件夹，使用rm命令将它删除：
然后，用vim命令进入.bashrc文件，将conda的语句用#注释掉
最后，重新激活一下source .bashrc就可以了。
```
### 2、Jupyter Lab

安装 JupyterLab 非常简单，只需一行命令即可：
```bash
conda 安装 [Miniconda]
conda install -c conda-forge jupyterlab
or
pip 安装 pip install jupyterlab

```

1. 注册环境
```bash
conda create -n python3_7 python=3.7 ipykernel
or 创建后 conda install ipykernel
```

2. 环境添加到ipykernel
（添加的是当前环境 需要先activate到需要环境）
```bash
python -m ipykernel install --user --name python3_7 --display-name "python3_7"
```
3. 查看，删除注册到内核的环境
```bash
jupyter kernelspec list 查看
jupyter kernelspec remove python3_7 删除
conda remove -n py36 --all 删环境
```
4. 配置文件
```bash
jupyter lab --generate-config 生成配置
c.ServerApp.ip = '*' 所有人访问
c.LabApp.open_browser = False 不再默认打开浏览器
jupyter lab password 修改密码
conda config --set auto_activate_base false 禁止自启环境



打开这个`jupyterhub_config.py`
c.Spawner.default_url = '/lab'
c.JupyterHub.ip = '0.0.0.0'

```
5. 安装插件
```bash
conda install nodejs
```
6. 装中文
```bsah
pip install jupyterlab-language-pack-zh-CN
```

7. 启动
```bash
nohup jupyterhub -f  /opt/jupyterhub/jupyterhub_config.py &
```
![在这里插入图片描述](../../image/06413d9c91e24f7289485e4d26f17ef9.png)
![在这里插入图片描述](../../image/16a0b9a5c9c74e0885ad2f679878a52d.png)

### 3、关联系统的其它认证用户
用Root账户启动，才能关联系统的其它认证用户

平台环境基于jupyterhub+conda构建，默认环境是ubuntu账户下的conda环境，请勿用作开发环境，
请创建并使用自己的linux账户后，再自建环境使用

**环境注册命令**

环境名称 {python版本}_{具体功用(看是否专用项目)}_{使用人} 
示例：python38_{xx模型}_long
```bash
> 注册环境：在创建环境的同时添加ipykernel核心
conda create -n python38_xxx python=3.8 ipykernel 

> 环境添加到ipykernel（操作前必须先激活进入对应环境）
conda activate python38_xxx
python -m ipykernel install --user --name python38_xxx --display-name "python38_xxx"

内核注册异常处理
1、手动执行内核添加命令 如上: python -m ipykernel install --user --name python38_xxx --display-name "python38_xxx"
2、重启面板，File->HubControlPanel->stopMyServer&startMyServer
3、选择内核时可选中always start the preferred kernel，设置为默认内核环境
```
**导入windows环境包**
```bash
pip list --format=freeze > requirements.txt

进入到需要安装的环境
conda activate python38_xxx  

删除requirements.txt文件多余的包(conda自带或windows特有
类似：conda,clyent,distribute,pip,jupyter,setuptools,wheel .. 安装过程失败或卡住不动的包，建议删除后继再单独安装

pip导入
python -m pip install -r requirements.txt
```

![在这里插入图片描述](../../image/6a35f574310d4039a9005cc0f6d9e104.png)

