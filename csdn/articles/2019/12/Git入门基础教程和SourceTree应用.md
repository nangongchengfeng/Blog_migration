+++
author = "南宫乘风"
title = "Git入门基础教程和SourceTree应用"
date = "2019-12-05 13:45:27"
tags=[]
categories=['软件', 'Java', 'Nginx']
image = "post/4kdongman/49.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/103403143](https://blog.csdn.net/heian_99/article/details/103403143)

**目录**

 

[一、Git的安装](#%E4%B8%80%E3%80%81Git%E7%9A%84%E5%AE%89%E8%A3%85)

[1.1 图形化界面](#1.1%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%95%8C%E9%9D%A2)

[1.2 命令行界面](#1.2%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2)

[二、本地仓库的创建与提交](#%E4%BA%8C%E3%80%81%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93%E7%9A%84%E5%88%9B%E5%BB%BA%E4%B8%8E%E6%8F%90%E4%BA%A4)

[2.1 图形化界面](#2.1%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%95%8C%E9%9D%A2)

[2.1.1 首先在电脑上有一个空白目录](#2.1.1%20%E9%A6%96%E5%85%88%E5%9C%A8%E7%94%B5%E8%84%91%E4%B8%8A%E6%9C%89%E4%B8%80%E4%B8%AA%E7%A9%BA%E7%99%BD%E7%9B%AE%E5%BD%95)

[2.1.2 打开SourceTree](#2.1.2%20%E6%89%93%E5%BC%80SourceTree)

[ 2.1.3 点击左边"克隆/新建",创建本地仓库](#%C2%A02.1.3%20%E7%82%B9%E5%87%BB%E5%B7%A6%E8%BE%B9%22%E5%85%8B%E9%9A%86%2F%E6%96%B0%E5%BB%BA%22%2C%E5%88%9B%E5%BB%BA%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93)

[ 2.1.4 选择第一步中的空白目录，点击"创建"按钮](#%C2%A02.1.4%20%E9%80%89%E6%8B%A9%E7%AC%AC%E4%B8%80%E6%AD%A5%E4%B8%AD%E7%9A%84%E7%A9%BA%E7%99%BD%E7%9B%AE%E5%BD%95%EF%BC%8C%E7%82%B9%E5%87%BB%22%E5%88%9B%E5%BB%BA%22%E6%8C%89%E9%92%AE)

[ 2.1.5 此时左边会出现这个，代表本地仓库创建完成](#%C2%A02.1.5%20%E6%AD%A4%E6%97%B6%E5%B7%A6%E8%BE%B9%E4%BC%9A%E5%87%BA%E7%8E%B0%E8%BF%99%E4%B8%AA%EF%BC%8C%E4%BB%A3%E8%A1%A8%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93%E5%88%9B%E5%BB%BA%E5%AE%8C%E6%88%90)

[ 2.1.6 打开空白目录，在空白目录下新建文件，文件(内容/名称)随便输入](#%C2%A02.1.6%20%E6%89%93%E5%BC%80%E7%A9%BA%E7%99%BD%E7%9B%AE%E5%BD%95%EF%BC%8C%E5%9C%A8%E7%A9%BA%E7%99%BD%E7%9B%AE%E5%BD%95%E4%B8%8B%E6%96%B0%E5%BB%BA%E6%96%87%E4%BB%B6%EF%BC%8C%E6%96%87%E4%BB%B6%28%E5%86%85%E5%AE%B9%2F%E5%90%8D%E7%A7%B0%29%E9%9A%8F%E4%BE%BF%E8%BE%93%E5%85%A5)

[ 2.1.7 返回SourceTree，会发现未暂存文件中有你刚才修改或增加的文件](#%C2%A02.1.7%20%E8%BF%94%E5%9B%9ESourceTree%EF%BC%8C%E4%BC%9A%E5%8F%91%E7%8E%B0%E6%9C%AA%E6%9A%82%E5%AD%98%E6%96%87%E4%BB%B6%E4%B8%AD%E6%9C%89%E4%BD%A0%E5%88%9A%E6%89%8D%E4%BF%AE%E6%94%B9%E6%88%96%E5%A2%9E%E5%8A%A0%E7%9A%84%E6%96%87%E4%BB%B6)

[ 2.1.8 右键“未暂存文件”中的文件，点击添加](#%C2%A02.1.8%20%E5%8F%B3%E9%94%AE%E2%80%9C%E6%9C%AA%E6%9A%82%E5%AD%98%E6%96%87%E4%BB%B6%E2%80%9D%E4%B8%AD%E7%9A%84%E6%96%87%E4%BB%B6%EF%BC%8C%E7%82%B9%E5%87%BB%E6%B7%BB%E5%8A%A0)

[ 2.1.9 会发现“未暂存文件”中的文件进入了“已暂存文件”中](#%C2%A02.1.9%20%E4%BC%9A%E5%8F%91%E7%8E%B0%E2%80%9C%E6%9C%AA%E6%9A%82%E5%AD%98%E6%96%87%E4%BB%B6%E2%80%9D%E4%B8%AD%E7%9A%84%E6%96%87%E4%BB%B6%E8%BF%9B%E5%85%A5%E4%BA%86%E2%80%9C%E5%B7%B2%E6%9A%82%E5%AD%98%E6%96%87%E4%BB%B6%E2%80%9D%E4%B8%AD)

[ 2.1.10 在下方输入“本次提交的描述”，点击“提交按钮”](#%C2%A02.1.10%20%E5%9C%A8%E4%B8%8B%E6%96%B9%E8%BE%93%E5%85%A5%E2%80%9C%E6%9C%AC%E6%AC%A1%E6%8F%90%E4%BA%A4%E7%9A%84%E6%8F%8F%E8%BF%B0%E2%80%9D%EF%BC%8C%E7%82%B9%E5%87%BB%E2%80%9C%E6%8F%90%E4%BA%A4%E6%8C%89%E9%92%AE%E2%80%9D)

[ 2.1.11 点击master分支，会显示本次提交的详细信息](#%C2%A02.1.11%20%E7%82%B9%E5%87%BBmaster%E5%88%86%E6%94%AF%EF%BC%8C%E4%BC%9A%E6%98%BE%E7%A4%BA%E6%9C%AC%E6%AC%A1%E6%8F%90%E4%BA%A4%E7%9A%84%E8%AF%A6%E7%BB%86%E4%BF%A1%E6%81%AF)

[2.2 命令行界面](#2.2%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2)

[2.2.1 点击SourceTree右上角的“命令行模式”即可打开命令行窗口](#2.2.1%20%E7%82%B9%E5%87%BBSourceTree%E5%8F%B3%E4%B8%8A%E8%A7%92%E7%9A%84%E2%80%9C%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%A8%A1%E5%BC%8F%E2%80%9D%E5%8D%B3%E5%8F%AF%E6%89%93%E5%BC%80%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%AA%97%E5%8F%A3)

[ 2.2.2 命令识别](#%C2%A02.2.2%20%E5%91%BD%E4%BB%A4%E8%AF%86%E5%88%AB)

[三、工作流](#%E4%B8%89%E3%80%81%E5%B7%A5%E4%BD%9C%E6%B5%81)

[3.1 图形化界面](#3.1%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%95%8C%E9%9D%A2)

[3.1.1 首先在电脑上有一个空白目录](#3.1.1%20%E9%A6%96%E5%85%88%E5%9C%A8%E7%94%B5%E8%84%91%E4%B8%8A%E6%9C%89%E4%B8%80%E4%B8%AA%E7%A9%BA%E7%99%BD%E7%9B%AE%E5%BD%95)

[ 3.1.2 打开SourceTree](#%C2%A03.1.2%20%E6%89%93%E5%BC%80SourceTree)

[3.1.3 点击左边"克隆/新建",创建本地仓库](#3.1.3%20%E7%82%B9%E5%87%BB%E5%B7%A6%E8%BE%B9%22%E5%85%8B%E9%9A%86%2F%E6%96%B0%E5%BB%BA%22%2C%E5%88%9B%E5%BB%BA%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93)

[ 3.1.4 选择第一步中的空白目录，点击"创建"按钮](#%C2%A03.1.4%20%E9%80%89%E6%8B%A9%E7%AC%AC%E4%B8%80%E6%AD%A5%E4%B8%AD%E7%9A%84%E7%A9%BA%E7%99%BD%E7%9B%AE%E5%BD%95%EF%BC%8C%E7%82%B9%E5%87%BB%22%E5%88%9B%E5%BB%BA%22%E6%8C%89%E9%92%AE)

[ 3.1.5 打开刚才创建的demo2目录，在里面添加一个文件(内容自定)](#%C2%A03.1.5%20%E6%89%93%E5%BC%80%E5%88%9A%E6%89%8D%E5%88%9B%E5%BB%BA%E7%9A%84demo2%E7%9B%AE%E5%BD%95%EF%BC%8C%E5%9C%A8%E9%87%8C%E9%9D%A2%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA%E6%96%87%E4%BB%B6%28%E5%86%85%E5%AE%B9%E8%87%AA%E5%AE%9A%29)

[3.1.6 打开SourceTree，将刚才修改的文件添加进暂存区](#3.1.6%20%E6%89%93%E5%BC%80SourceTree%EF%BC%8C%E5%B0%86%E5%88%9A%E6%89%8D%E4%BF%AE%E6%94%B9%E7%9A%84%E6%96%87%E4%BB%B6%E6%B7%BB%E5%8A%A0%E8%BF%9B%E6%9A%82%E5%AD%98%E5%8C%BA)

[ 3.1.7 第一次提交](#%C2%A03.1.7%20%E7%AC%AC%E4%B8%80%E6%AC%A1%E6%8F%90%E4%BA%A4)

[ 3.1.8 需求变更](#%C2%A03.1.8%20%E9%9C%80%E6%B1%82%E5%8F%98%E6%9B%B4)

[ 3.1.9 需求撤销](#%C2%A03.1.9%20%E9%9C%80%E6%B1%82%E6%92%A4%E9%94%80)

[ 3.1.10 第二天正式需求](#%C2%A03.1.10%20%E7%AC%AC%E4%BA%8C%E5%A4%A9%E6%AD%A3%E5%BC%8F%E9%9C%80%E6%B1%82)

[3.1.11 第二天的需求提交到git仓库](#3.1.11%20%E7%AC%AC%E4%BA%8C%E5%A4%A9%E7%9A%84%E9%9C%80%E6%B1%82%E6%8F%90%E4%BA%A4%E5%88%B0git%E4%BB%93%E5%BA%93)

[3.1.12 第三天撤销需求](#3.1.12%20%E7%AC%AC%E4%B8%89%E5%A4%A9%E6%92%A4%E9%94%80%E9%9C%80%E6%B1%82)

[ 3.1.13 项目不需要了](#%C2%A03.1.13%20%E9%A1%B9%E7%9B%AE%E4%B8%8D%E9%9C%80%E8%A6%81%E4%BA%86)

[3.2 命令行界面](#3.2%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2)

[3.2.1 先有一个空目录](#3.2.1%20%E5%85%88%E6%9C%89%E4%B8%80%E4%B8%AA%E7%A9%BA%E7%9B%AE%E5%BD%95)

[3.2.2 在该空目录下打开git_bush](#3.2.2%20%E5%9C%A8%E8%AF%A5%E7%A9%BA%E7%9B%AE%E5%BD%95%E4%B8%8B%E6%89%93%E5%BC%80git_bush)

[ 3.2.3 产品经理临时变更需求](#%C2%A03.2.3%20%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E4%B8%B4%E6%97%B6%E5%8F%98%E6%9B%B4%E9%9C%80%E6%B1%82)

[3.2.4 将变更后的需求提交到暂存区](#3.2.4%20%E5%B0%86%E5%8F%98%E6%9B%B4%E5%90%8E%E7%9A%84%E9%9C%80%E6%B1%82%E6%8F%90%E4%BA%A4%E5%88%B0%E6%9A%82%E5%AD%98%E5%8C%BA)

[ 3.2.5 第二天上班之后，被产品经理告知该需求不需要](#%C2%A03.2.5%20%E7%AC%AC%E4%BA%8C%E5%A4%A9%E4%B8%8A%E7%8F%AD%E4%B9%8B%E5%90%8E%EF%BC%8C%E8%A2%AB%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E5%91%8A%E7%9F%A5%E8%AF%A5%E9%9C%80%E6%B1%82%E4%B8%8D%E9%9C%80%E8%A6%81)

[ 3.2.6 第二天结束](#%C2%A03.2.6%20%E7%AC%AC%E4%BA%8C%E5%A4%A9%E7%BB%93%E6%9D%9F)

[ 3.2.7 将第二天的工作内容提交到仓库](#%C2%A03.2.7%20%E5%B0%86%E7%AC%AC%E4%BA%8C%E5%A4%A9%E7%9A%84%E5%B7%A5%E4%BD%9C%E5%86%85%E5%AE%B9%E6%8F%90%E4%BA%A4%E5%88%B0%E4%BB%93%E5%BA%93)

[ 3.2.8 产品经理突然告知这个需求不要了](#%C2%A03.2.8%20%E4%BA%A7%E5%93%81%E7%BB%8F%E7%90%86%E7%AA%81%E7%84%B6%E5%91%8A%E7%9F%A5%E8%BF%99%E4%B8%AA%E9%9C%80%E6%B1%82%E4%B8%8D%E8%A6%81%E4%BA%86)

[ 3.2.9 这个项目都不需要了](#%C2%A03.2.9%20%E8%BF%99%E4%B8%AA%E9%A1%B9%E7%9B%AE%E9%83%BD%E4%B8%8D%E9%9C%80%E8%A6%81%E4%BA%86)

[ 3.3 总结](#%C2%A03.3%20%E6%80%BB%E7%BB%93)

[ 四、远程仓库](#%C2%A0%E5%9B%9B%E3%80%81%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93)

[4.1 github密钥生成](#4.1%20github%E5%AF%86%E9%92%A5%E7%94%9F%E6%88%90)

[4.2 添加远程仓库](#4.2%20%E6%B7%BB%E5%8A%A0%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93)

[ 4.2.1 命令行界面](#%C2%A04.2.1%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2)

[4.2.2 图形化界面](#4.2.2%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%95%8C%E9%9D%A2)

[ 五、克隆仓库](#%C2%A0%E4%BA%94%E3%80%81%E5%85%8B%E9%9A%86%E4%BB%93%E5%BA%93)

[5.1 命令行操作](#5.1%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%93%8D%E4%BD%9C)

[5.2 图形化操作](#5.2%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E6%93%8D%E4%BD%9C)

[ 六、标签管理](#%C2%A0%E5%85%AD%E3%80%81%E6%A0%87%E7%AD%BE%E7%AE%A1%E7%90%86)

[6.1 标签命令](#6.1%20%E6%A0%87%E7%AD%BE%E5%91%BD%E4%BB%A4)

[6.2 命令行方式实现](#6.2%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%96%B9%E5%BC%8F%E5%AE%9E%E7%8E%B0)

[6.3 图形化方式实现](#6.3%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E6%96%B9%E5%BC%8F%E5%AE%9E%E7%8E%B0)

[七、分支管理](#%E4%B8%83%E3%80%81%E5%88%86%E6%94%AF%E7%AE%A1%E7%90%86)

[7.1 命令行方式](#7.1%20%E5%91%BD%E4%BB%A4%E8%A1%8C%E6%96%B9%E5%BC%8F)

[7.1.1 提交到本地仓库](#7.1.1%20%E6%8F%90%E4%BA%A4%E5%88%B0%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93)

[ 7.1.2 创建分支](#%C2%A07.1.2%20%E5%88%9B%E5%BB%BA%E5%88%86%E6%94%AF)

[ 7.1.2 删除分支](#%C2%A07.1.2%20%E5%88%A0%E9%99%A4%E5%88%86%E6%94%AF)

[7.2 图形化界面](#7.2%20%E5%9B%BE%E5%BD%A2%E5%8C%96%E7%95%8C%E9%9D%A2)

[7.2.1 首先需要有一个本地目录，里面有一个文件，文件中有内容](#7.2.1%20%E9%A6%96%E5%85%88%E9%9C%80%E8%A6%81%E6%9C%89%E4%B8%80%E4%B8%AA%E6%9C%AC%E5%9C%B0%E7%9B%AE%E5%BD%95%EF%BC%8C%E9%87%8C%E9%9D%A2%E6%9C%89%E4%B8%80%E4%B8%AA%E6%96%87%E4%BB%B6%EF%BC%8C%E6%96%87%E4%BB%B6%E4%B8%AD%E6%9C%89%E5%86%85%E5%AE%B9)

[ 7.2.2 打开SourceTree创建本地仓库，并将代码提交到本地仓库](#%C2%A07.2.2%20%E6%89%93%E5%BC%80SourceTree%E5%88%9B%E5%BB%BA%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93%EF%BC%8C%E5%B9%B6%E5%B0%86%E4%BB%A3%E7%A0%81%E6%8F%90%E4%BA%A4%E5%88%B0%E6%9C%AC%E5%9C%B0%E4%BB%93%E5%BA%93)

[7.2.3 新建分支](#7.2.3%20%E6%96%B0%E5%BB%BA%E5%88%86%E6%94%AF)

[7.2.4 删除分支](#7.2.4%20%E5%88%A0%E9%99%A4%E5%88%86%E6%94%AF)

[ 八、问题归纳总结](#%C2%A0%E5%85%AB%E3%80%81%E9%97%AE%E9%A2%98%E5%BD%92%E7%BA%B3%E6%80%BB%E7%BB%93)

[8.1 报错](#8.1%20%E6%8A%A5%E9%94%99)

[8.1.1 如果你本地有远程仓库的ssh的话，按照下方步骤来添加](#8.1.1%20%E5%A6%82%E6%9E%9C%E4%BD%A0%E6%9C%AC%E5%9C%B0%E6%9C%89%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93%E7%9A%84ssh%E7%9A%84%E8%AF%9D%EF%BC%8C%E6%8C%89%E7%85%A7%E4%B8%8B%E6%96%B9%E6%AD%A5%E9%AA%A4%E6%9D%A5%E6%B7%BB%E5%8A%A0)

[8.1.2 如果你本地没有远程仓库的ssh的话，先来添加](#8.1.2%20%E5%A6%82%E6%9E%9C%E4%BD%A0%E6%9C%AC%E5%9C%B0%E6%B2%A1%E6%9C%89%E8%BF%9C%E7%A8%8B%E4%BB%93%E5%BA%93%E7%9A%84ssh%E7%9A%84%E8%AF%9D%EF%BC%8C%E5%85%88%E6%9D%A5%E6%B7%BB%E5%8A%A0)

# 一、Git的安装

## 1.1 图形化界面

**https://pan.baidu.com/s/1oAf6Eu9iha6TPzaGHNsADQ**

安装过程：

安装完成之后,在**C:\Users\Administrator\AppData\Local\Atlassian\SourceTree**目录下创建**accounts.json**文件，里面内容如下：
<li>
   
    
   
   
    
     [
    
   </li><li>
   
    
   
   
    
       {
    
   </li><li>
   
    
   
   
        
     "$id": 
     "1",
    
   </li><li>
   
    
   
   
        
     "$type": 
     "SourceTree.Api.Host.Identity.Model.IdentityAccount, SourceTree.Api.Host.Identity",
    
   </li><li>
   
    
   
   
        
     "Authenticate": 
     true,
    
   </li><li>
   
    
   
   
        
     "HostInstance": {
    
   </li><li>
   
    
   
   
          
     "$id": 
     "2",
    
   </li><li>
   
    
   
   
          
     "$type": 
     "SourceTree.Host.Atlassianaccount.AtlassianAccountInstance, SourceTree.Host.AtlassianAccount",
    
   </li><li>
   
    
   
   
          
     "Host": {
    
   </li><li>
   
    
   
   
            
     "$id": 
     "3",
    
   </li><li>
   
    
   
   
            
     "$type": 
     "SourceTree.Host.Atlassianaccount.AtlassianAccountHost, SourceTree.Host.AtlassianAccount",
    
   </li><li>
   
    
   
   
            
     "Id": 
     "atlassian account"
    
   </li><li>
   
    
   
   
    
           },
    
   </li><li>
   
    
   
   
          
     "BaseUrl": 
     "https://id.atlassian.com/"
    
   </li><li>
   
    
   
   
    
         },
    
   </li><li>
   
    
   
   
        
     "Credentials": {
    
   </li><li>
   
    
   
   
          
     "$id": 
     "4",
    
   </li><li>
   
    
   
   
          
     "$type": 
     "SourceTree.Model.BasicAuthCredentials, SourceTree.Api.Account",
    
   </li><li>
   
    
   
   
          
     "Username": 
     "username@email.com"
    
   </li><li>
   
    
   
   
    
         },
    
   </li><li>
   
    
   
   
        
     "IsDefault": 
     false
    
   </li><li>
   
    
   
   
    
       }
    
   </li><li>
   
    
   
   
    
     ]
    
   </li>
再次打开SourceTree下载只被SourceTree识别的Git，不需要moun...(会有提示，没有则不用管)

## 1.2 命令行界面

**https://pan.baidu.com/s/1SPqrbKJLRkzzz2c0jHkuJA**

# 二、本地仓库的创建与提交

## 2.1 图形化界面

### 2.1.1 首先在电脑上有一个空白目录

![20191204085509710.png](https://img-blog.csdnimg.cn/20191204085509710.png)

### 2.1.2 打开SourceTree

![20191204085610526.png](https://img-blog.csdnimg.cn/20191204085610526.png)

###  2.1.3 点击左边"克隆/新建",创建本地仓库

![20191204085642473.png](https://img-blog.csdnimg.cn/20191204085642473.png)

###  2.1.4 选择第一步中的空白目录，点击"创建"按钮

![20191204085708371.png](https://img-blog.csdnimg.cn/20191204085708371.png)

###  2.1.5 此时左边会出现这个，代表本地仓库创建完成

![20191204085732705.png](https://img-blog.csdnimg.cn/20191204085732705.png)



###  2.1.6 打开空白目录，在空白目录下新建文件，文件(内容/名称)随便输入

![2019120408580358.png](https://img-blog.csdnimg.cn/2019120408580358.png)

###  2.1.7 返回SourceTree，会发现未暂存文件中有你刚才修改或增加的文件

![20191204085936373.png](https://img-blog.csdnimg.cn/20191204085936373.png)

###  2.1.8 右键“未暂存文件”中的文件，点击添加

![2019120409000484.png](https://img-blog.csdnimg.cn/2019120409000484.png)

###  2.1.9 会发现“未暂存文件”中的文件进入了“已暂存文件”中

![20191204090035496.png](https://img-blog.csdnimg.cn/20191204090035496.png)

###  2.1.10 在下方输入“本次提交的描述”，点击“提交按钮”

![20191204090058115.png](https://img-blog.csdnimg.cn/20191204090058115.png)

###  2.1.11 点击master分支，会显示本次提交的详细信息

![20191204090124745.png](https://img-blog.csdnimg.cn/20191204090124745.png)



## 2.2 命令行界面

### 2.2.1 点击SourceTree右上角的“命令行模式”即可打开命令行窗口

![20191204090159319.png](https://img-blog.csdnimg.cn/20191204090159319.png)

![20191204090210498.png](https://img-blog.csdnimg.cn/20191204090210498.png) 



###  2.2.2 命令识别
<li>
   
    
   
   
    
     pwd  查看当前目录
    
   </li><li>
   
    
   
   
    
     cd .. 返回上一级目录
    
   </li><li>
   
    
   
   
    
     mkdir demo2  新建目录demo2
    
   </li><li>
   
    
   
   
    
     cd demo2  进入目录
    
   </li><li>
   
    
   
   
    
     ll  展示目录文件
    
   </li><li>
   
    
   
   
    
     ls -a 展示所有文件
    
   </li><li>
   
    
   
   
    
     echo 
     "git repo2" &gt;&gt; test.txt  给test.txt追加git repo2
    
   </li><li>
   
    
   
   
    
     cat test.txt   展示当前文件内容
    
   </li><li>
   
    
   
   
    
     git add test.txt  添加
    
   </li><li>
   
    
   
   
    
     git commit -m 
     "repo2 first commit"  提交
    
   </li><li>
   
    
   
   
    
     git status   查看当前仓库状态
    
   </li>
 ![20191204090259541.png](https://img-blog.csdnimg.cn/20191204090259541.png)

# 三、工作流

## 3.1 图形化界面

### 3.1.1 首先在电脑上有一个空白目录

![20191204090330298.png](https://img-blog.csdnimg.cn/20191204090330298.png)

###  3.1.2 打开SourceTree

![20191204090354545.png](https://img-blog.csdnimg.cn/20191204090354545.png)

### 3.1.3 点击左边"克隆/新建",创建本地仓库

![20191204090418820.png](https://img-blog.csdnimg.cn/20191204090418820.png)

###  3.1.4 选择第一步中的空白目录，点击"创建"按钮

![20191204090434772.png](https://img-blog.csdnimg.cn/20191204090434772.png)



###  3.1.5 打开刚才创建的demo2目录，在里面添加一个文件(内容自定)

![20191204090458269.png](https://img-blog.csdnimg.cn/20191204090458269.png)

### 3.1.6 打开SourceTree，将刚才修改的文件添加进暂存区

![20191204090519861.png](https://img-blog.csdnimg.cn/20191204090519861.png)

###  3.1.7 第一次提交

![20191204090542741.png](https://img-blog.csdnimg.cn/20191204090542741.png)



###  3.1.8 需求变更

>  
 背景：开发完成，要下班了，但是临时有个需求变更，将变更后的文件提交的暂存区 




 修改内容，添加“需求变更”

![20191204090711553.png](https://img-blog.csdnimg.cn/20191204090711553.png)

 将修改后的文件添加到暂存区

![20191204090728248.png](https://img-blog.csdnimg.cn/20191204090728248.png)

###  3.1.9 需求撤销

>  
 背景：第二天上班之后，产品经理说，昨天的需求不需要了 


 直接丢弃掉暂存区的文件

![2019120409081420.png](https://img-blog.csdnimg.cn/2019120409081420.png)

此时的需求变更已撤销

 ![20191204090834438.png](https://img-blog.csdnimg.cn/20191204090834438.png)

###  3.1.10 第二天正式需求

>  
 背景：第二天下班之后，当天的需求已经完成，准备提交到git仓库 


 ![20191204090907542.png](https://img-blog.csdnimg.cn/20191204090907542.png)

### 3.1.11 第二天的需求提交到git仓库

![20191204090930595.png](https://img-blog.csdnimg.cn/20191204090930595.png)

 ![20191204090940109.png](https://img-blog.csdnimg.cn/20191204090940109.png)

### 3.1.12 第三天撤销需求

>  
 背景：第三天上班，发现第二天的需求没用，但是已经提交到线上仓库，可以通过重置当前分支到此次提交 


![20191204091010217.png](https://img-blog.csdnimg.cn/20191204091010217.png)

 ![20191204091105989.png](https://img-blog.csdnimg.cn/20191204091105989.png)

###  3.1.13 项目不需要了

在工作区直接删除该文件，打开sourceTree，虽然在本地删除了，但是线上仓库还有遗留。

再次打开SourceTree，将动作提交至暂存区，然后再次提交到仓库

![20191204091135761.png](https://img-blog.csdnimg.cn/20191204091135761.png)

![20191204091149620.png](https://img-blog.csdnimg.cn/20191204091149620.png)

到此，仓库才算干净

## 3.2 命令行界面

### 3.2.1 先有一个空目录

### 3.2.2 在该空目录下打开git_bush

![20191204091235981.png](https://img-blog.csdnimg.cn/20191204091235981.png)

###  3.2.3 产品经理临时变更需求

![20191204091258396.png](https://img-blog.csdnimg.cn/20191204091258396.png)

### 3.2.4 将变更后的需求提交到暂存区

![20191204091325297.png](https://img-blog.csdnimg.cn/20191204091325297.png)

###  3.2.5 第二天上班之后，被产品经理告知该需求不需要

![20191204091345923.png](https://img-blog.csdnimg.cn/20191204091345923.png)

 此时的工作区已经干净

![20191204091421824.png](https://img-blog.csdnimg.cn/20191204091421824.png)

###  3.2.6 第二天结束

![20191204091443347.png](https://img-blog.csdnimg.cn/20191204091443347.png)

###  3.2.7 将第二天的工作内容提交到仓库

![20191204091510304.png](https://img-blog.csdnimg.cn/20191204091510304.png)

###  3.2.8 产品经理突然告知这个需求不要了

![20191204091530463.png](https://img-blog.csdnimg.cn/20191204091530463.png)

此时的工作区只有第一次提交的信息

 ![2019120409155284.png](https://img-blog.csdnimg.cn/2019120409155284.png)

###  3.2.9 这个项目都不需要了

![2019120409161061.png](https://img-blog.csdnimg.cn/2019120409161061.png)

##  3.3 总结

 ![20191204091630292.png](https://img-blog.csdnimg.cn/20191204091630292.png)

#  四、远程仓库

## 4.1 github密钥生成

**https://www.cnblogs.com/xue-shuai/p/11555150.html**

## 4.2 添加远程仓库

![20191204091840136.png](https://img-blog.csdnimg.cn/20191204091840136.png)

###  4.2.1 命令行界面
<li>
   
    
   
   
    
     首先添加到本地仓库
    
   </li><li>
   
    
   
   
    
     使用 
     git 
     remote 
     add 
     origin 
     git@/**********.
     git  本地仓库关联远程GitHub仓库
    
   </li><li>
   
    
   
   
    
     使用 git push -u origin master    将本地仓库推送到GitHub仓库master分支(-u已经默认将master分支关联)
    
   </li>
### 4.2.2 图形化界面

**1）首先先提交到本地仓库**

![20191204091954970.png](https://img-blog.csdnimg.cn/20191204091954970.png)

** 2）将本地仓库与远程仓库关联，右键master分支，点击“创建拉去请求”**

![20191204092018821.png](https://img-blog.csdnimg.cn/20191204092018821.png)

 添加远程仓库地址

![2019120409203531.png](https://img-blog.csdnimg.cn/2019120409203531.png)





 ![20191204092047700.png](https://img-blog.csdnimg.cn/20191204092047700.png)

 点击确定

**3）出现origin说明本地仓库与远程仓库关联成功**

![20191204092126701.png](https://img-blog.csdnimg.cn/20191204092126701.png)

**4）推送到远程仓库**

右键master，点击推送到origin

![20191204092146665.png](https://img-blog.csdnimg.cn/20191204092146665.png)

 直接推送即可

![20191204092208210.png](https://img-blog.csdnimg.cn/20191204092208210.png)



#  五、克隆仓库

## 5.1 命令行操作

找一个空目录，输入

克隆远程仓库到本地

## 5.2 图形化操作

点击克隆，输入远程仓库地址，找到放置的目录，点击克隆即可

![2019120409231227.png](https://img-blog.csdnimg.cn/2019120409231227.png)

#  六、标签管理

## 6.1 标签命令
<li>
   
    
   
   
    
     git tag     查看所有标签
    
   </li><li>
   
    
   
   
    
     git tag name    创建标签
    
   </li><li>
   
    
   
   
    
     git tag -a name -
     m 
     "comment"    指定提交信息
    
   </li><li>
   
    
   
   
    
     git tag -d name    删除标签
    
   </li><li>
   
    
   
   
    
     git 
     push origin name    标签发布
    
   </li>
## 6.2 命令行方式实现

首先需要在远程GitHub上有一个仓库，并且克隆到本地，在该项目中执行下列命令

![20191204092403849.png](https://img-blog.csdnimg.cn/20191204092403849.png)

查看远程GitHub中的标签

![20191204092422853.png](https://img-blog.csdnimg.cn/20191204092422853.png)

 

![20191204092459117.png](https://img-blog.csdnimg.cn/20191204092459117.png)

更换Branches分支为Tags标签，即可查看拥有的标签，可进行版本的查看与切换。

** 删除远程标签**

![20191204092630219.png](https://img-blog.csdnimg.cn/20191204092630219.png)

## 6.3 图形化方式实现

>  
 首先先提交本地仓库到远程仓库，这里就不多说了，详情查看4.2.2 




 推送完成之后，点击标签

![20191204092716688.png](https://img-blog.csdnimg.cn/20191204092716688.png)



填写“标签名称”，选择“指定的提交”，勾选“推送标签”

 ![20191204092735610.png](https://img-blog.csdnimg.cn/20191204092735610.png)

选择最新的修改，点击确定

![20191204092754492.png](https://img-blog.csdnimg.cn/20191204092754492.png)



 添加标签

![2019120409281845.png](https://img-blog.csdnimg.cn/2019120409281845.png)

 添加完成之后即可在GitHub上查看添加成功的标签

 ![20191204092842256.png](https://img-blog.csdnimg.cn/20191204092842256.png)

删除标签，在sourceTree中右键所要删除的标签

 ![20191204092903466.png](https://img-blog.csdnimg.cn/20191204092903466.png)

勾选“移除所有远程标签”，即可将远程仓库中该标签删除掉

 ![20191204092932736.png](https://img-blog.csdnimg.cn/20191204092932736.png)

# 七、分支管理

>  
 假设需要实现一个功能，但是这个功能需要两周完成，第一周完成了50%，如果直接提交到远程仓库，别人的代码可能会出问题，但是如果等到全部完成在提交，可能进度上会有问题，所以只需要创建一个属于你自己的分支，自己所有的代码在该分支上完成。为保持工作树清洁，所创建的分支在合成到主分支之后，该分支便不再需要，可删除。 




 ![20191204093001498.png](https://img-blog.csdnimg.cn/20191204093001498.png)

## 7.1 命令行方式

**在一个空目录下打开git bash**

### 7.1.1 提交到本地仓库

 ![20191204093040907.png](https://img-blog.csdnimg.cn/20191204093040907.png)

###  7.1.2 创建分支

![20191204093108484.png](https://img-blog.csdnimg.cn/20191204093108484.png)



###  7.1.2 删除分支

![20191204093137477.png](https://img-blog.csdnimg.cn/20191204093137477.png)

## 7.2 图形化界面

### 7.2.1 首先需要有一个本地目录，里面有一个文件，文件中有内容

![20191204093201610.png](https://img-blog.csdnimg.cn/20191204093201610.png)

###  7.2.2 打开SourceTree创建本地仓库，并将代码提交到本地仓库

>  
 具体就不细说了，详情请看2.1 




### 7.2.3 新建分支

**点击“分支”**

![20191204093253299.png](https://img-blog.csdnimg.cn/20191204093253299.png)



** 输入新的分支名称，点击“创建分支”**

![20191204093319465.png](https://img-blog.csdnimg.cn/20191204093319465.png)

 ![2019120409334045.png](https://img-blog.csdnimg.cn/2019120409334045.png)

**右键仓库，选择“在资源管理器里打开”**

![20191204093404373.png](https://img-blog.csdnimg.cn/20191204093404373.png)

**在新的分支上添加一些内容**

![20191204093423505.png](https://img-blog.csdnimg.cn/20191204093423505.png)

 **返回sourceTree，选择“未提交的更改”，将下方的“为暂存文件”提交到本地仓库**

![20191204093450907.png](https://img-blog.csdnimg.cn/20191204093450907.png)

 **接下来合并分支。双击master分支就会切换至master分支**

![20191204093525601.png](https://img-blog.csdnimg.cn/20191204093525601.png)

**点击“合并”，选择要合并的分支，勾选“立即提交合并”，点击确定**

![20191204093549461.png](https://img-blog.csdnimg.cn/20191204093549461.png)

 **此时通过右键该仓库点击“在资源管理器中打开”，查看该文件**

![20191204093611795.png](https://img-blog.csdnimg.cn/20191204093611795.png)

** 我们发现原来futureY中修改的文件已经合并到了master分支上**

![20191204093635726.png](https://img-blog.csdnimg.cn/20191204093635726.png)

### 7.2.4 删除分支

**右键要删除的分支名，点击删除futureY**

![20191204093657474.png](https://img-blog.csdnimg.cn/20191204093657474.png)

**勾选“强制删除”，ok即可删除该分支。**

![20191204093717458.png](https://img-blog.csdnimg.cn/20191204093717458.png)

#  八、问题归纳总结

## 8.1 报错

>  
 如果出现下类问题不要慌，是因为你的git没有ssh密钥与远程仓库关联 




![20191204093759283.png](https://img-blog.csdnimg.cn/20191204093759283.png)

### 8.1.1 如果你本地有远程仓库的ssh的话，按照下方步骤来添加

![20191204093828847.png](https://img-blog.csdnimg.cn/20191204093828847.png)

 ![2019120409384427.png](https://img-blog.csdnimg.cn/2019120409384427.png)

**会自动帮你提取本地的ssh**

![20191204093904891.png](https://img-blog.csdnimg.cn/20191204093904891.png)

### 8.1.2 如果你本地没有远程仓库的ssh的话，先来添加

**https://www.cnblogs.com/xue-shuai/p/11555150.html**

 

 
