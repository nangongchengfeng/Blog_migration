---
author: 南宫乘风
categories:
- Python学习
date: 2021-07-19 21:19:19
description: 调用查询机器资源利用率，导出表格背景：平常我们工作中，需要知道机器的资源利用率多少，我们可以手动查看，但是有多台改怎么办？方案：我们机器如果是监控的，我们可以直接调用的，来获取所有主机的相关信息，生成。。。。。。。
image: ../../title_pic/52.jpg
slug: '202107192119'
tags:
- Zabbix监控
- python
- zabbix
title: zabbix-api查询机器资源利用率，导出execl表格
---

<!--more-->

zabbix调用api查询机器资源利用率，导出execl表格

背景：平常我们工作中，需要知道机器的资源利用率多少，我们可以手动查看，但是有1000多台改怎么办？

方案：我们机器如果是zabbix监控的，我们可以直接调用zabbix的api，来获取所有主机的相关信息，生成execl表格并且导出

我们可以设置定时任务，每周定时导出，查看集群服务器的利用率。 

github地址：<https://github.com/nangongchengfeng/zabbix-api.git>

![](../../image/20210719210917960.png)

 

```python
if host['Number of CPUs'] == "0":
	HostItemValues.append("已停用")
if  float(host['Load average (15m avg)']) >= 10 or  float(round(float(host['CPU utilization']), 2)) >= 20 :
	HostItemValues.append("否")
else:
	HostItemValues.append("是")
```

最后面添加是否低负载机器

判断条件：CPU平均负载/15min >= 10 or CPU使用率 >=20

## Zabbix-api\_v1

Zabbix-api\_v1版本是初级版本，需要Python环境下操作

## Zabbix-api\_v2

Zabbix-api\_v2版本可以打包成exe程序，可以方便执行，不需要依赖

这里我贴版本2的代码，可以生成exe

## main.py

```python
#! /usr/bin/env python

import configparser
import os,sys
import time
from GetItems import Zabbix
from SaveToExcel  import WriteExcel
import datetime

path = os.path.dirname(os.path.abspath(__file__))
sys.intern(path)


if __name__ == "__main__":
    print("start".center(60,"*"))
    print("zabbix统计机器资源使用情况".center(60))
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'config.ini'), encoding='utf-8')
    # 实例化一个zabbix对象
    #api调用地址
    zabbix_api='http://10.190.5.237/api_jsonrpc.php'
    zabbix_user=input("请输入您zabbix的账号：")
    zabbix_passwd=input('请输入您zabbix的密码：')
    file_name='服务器资源使用情况分析'
    zabbix =  Zabbix(
        zabbix_api,
        zabbix_user,
        zabbix_passwd
    )
    starttime = datetime.datetime.now()
    # 调用GetItemValue方法获取每台监控主机的监控数据
    zabbix_data = zabbix.GetItemValue()
    if len(zabbix_data) == 2:
        print(zabbix_data['errmsg'])
        print("end".center(60, "*"))
    else:
        date_time = time.strftime('%Y-%m-%d_%H-%M')
        #print(zabbix_data)
        file_name = os.path.join(os.getcwd(), file_name + date_time + '.xlsx')
        WriteExcel(file_name, zabbix_data)
        endtime = datetime.datetime.now()
        run_time=endtime - starttime
        print(f"程序运行：{run_time.seconds} s  生成文件：{file_name}")
        print("end".center(60, "*"))
```

## GetItems.py

在这里可以定制值。切记，这里代码只适合我的环境，有些值为特定值，如有需要，需要更改值

列如：

>                                     "io.usedgen\[\*\]",        # 根目录使用率监控  
>                                     "disk\_capacity.\[disk\_all\_Usage\]",#服务器总使用率

```python
#! /usr/bin/env python
# _*_ coding: utf-8 _*_

# @Desc   :调用zabbix api接口，获取监控数据，zabbix-版本为5.0以上


import requests
import json
import re

class Zabbix(object):
    def __init__(self, ApiUrl, User, Pwd):
        self.ApiUrl = ApiUrl
        self.User = User
        self.Pwd = Pwd
        self.__Headers = {
            'Content-Type': 'application/json-rpc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }
        self.Message = {
            1001: {"errcode": "1001", "errmsg": "请求路径错误，请检查API接口路径是否正确."},
            1002: {"errcode": "1002", "errmsg": "Login name or password is incorrect."},
            1003: {"errcode": "1003", "errmsg": "未获取到监控主机，请检查server端是否监控有主机."},
            1004: {"errcode": "1004", "errmsg": "未知错误."},
        }


    def __Login(self):
        '''
        登陆zabbix，获取认证的秘钥
        Returns: 返回认证秘钥

        '''
        # 登陆zabbix,接口的请求数据
        LoginApiData = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.User,
                "password": self.Pwd
            },
            "id": 1
        }
        # 向登陆接口发送post请求，获取result
        LoginRet = requests.post(url=self.ApiUrl, data=json.dumps(LoginApiData), headers=self.__Headers)
        # 判断请求是否为200
        if LoginRet.status_code is not 200:
            return 1001
        else:
            # 如果是200状态，则进行数据格式化
            try:
                LoginRet = LoginRet.json()
            except:
                return 1001
            # 如果result在返回数据中，那么表示请求成功，则获取认证key
            if 'result' in LoginRet:
                Result = LoginRet['result']
                return Result
            # 否则返回用户或密码错误
            else:
                return 1002


    def __GetMonitorHost(self):
        # 调用登陆函数，获取auth，并判断是否登陆成功
        Auth = self.__Login()
        if Auth == 1001:
            return 1001
        elif Auth == 1002:
            return 1002
        else:
            HostApiData = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["hostid", "host", "name"],
                    "selectInterfaces": ["interfaces", "ip"],
                },
                "auth": Auth,
                "id": 1
            }
            # 向host.get接口发起请求，获取所有监控主机
            HostRet = requests.post(url=self.ApiUrl, data=json.dumps(HostApiData), headers=self.__Headers).json()

            if 'result' in HostRet:
                if len(HostRet['result']) != 0:
                    # 循环处理每一条记录，进行结构化,最终将所有主机加入到all_host字典中
                    Allhost = {}
                    for host in HostRet['result']:
                        # host = {'hostid': '10331', 'host': '172.24.125.24', 'name': 'TBDS测试版172.24.125.24', 'interfaces': [{'ip': '172.24.125.24'}]}
                        # 进行结构化，提取需要的信息
                        HostInfo = {'host': host['host'], 'hostid': host['hostid'], 'ip': host['interfaces'][0]['ip'],
                                     'name': host['name']}
                        # host_info = {'host': '172.24.125.24', 'hostid': '10331', 'ip': '172.24.125.24', 'name': 'TBDS测试版172.24.125.24'}
                        # 加入到all_host中
                        Allhost[host['hostid']] = HostInfo
                    #print(Allhost)主机结构化列表
                    return {"Auth":Auth, "Allhost":Allhost}
                else:
                    return 1003
            else:
                return 1001


    def GetItemValue(self):
        '''
        # 调用item.get接口，获取监控项（监控项中带有每个监控项的最新监控数据） 接口说明文档：https://www.zabbix.com/documentation/4.0/zh/manual/api/reference/item/get
        Returns: 返回所有监控主机监控信息，
        '''
        # 获取所有的主机
        HostRet = self.__GetMonitorHost()
        # 判断HostRet是否有主机和认证key存在，这里如果是类型如果是字段，那边表示一定获取到的有主机信息，如果不是，则表示没有获取到值

        if type(HostRet) is dict:
            # 首先拿到认证文件和所有主机信息
            Auth, AllHost = HostRet['Auth'], HostRet['Allhost']
            # 定义一个新的allhost，存放所有主机新的信息
            NewAllHost = {}
            # 循环向每个主机发起请求，获取监控项的值
            for k in AllHost:
                ItemData = {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": ["extend", "name", "key_", "lastvalue"],
                        "hostids": str(k),
                        "search": {
                            "key_":
                                [
                                    "system.hostname",    # 主机名
                                    "system.uptime",      # 系统开机时长
                                    "io.usedgen[*]",        # 根目录使用率监控
                                    "disk_capacity.[disk_all_Usage]",#服务器总使用率
                                    "system.cpu.util",    # cpu使用率
                                    "system.cpu.num",     # cpu核数
                                    "system.cpu.load",    # cpu平均负载
                                    "system.cpu.util[,idle]",     # cpu空闲时间
                                    "vm.memory.utilization",      # 内存使用率
                                    "vm.memory.size[total]",      # 内存总大小
                                    "vm.memory.size[available]",  # 可用内存
                                    "net.if.in",  # 网卡每秒流入的比特(bit)数
                                    "net.if.out"  # 网卡每秒流出的比特(bit)数
                                ]
                        },
                        "searchByAny": "true",
                        "sortfield": "name"
                    },
                    "auth": Auth,
                    "id": 1
                }
                # 向每一台主机发起请求，获取监控项
                Ret = requests.post(url=self.ApiUrl, data=json.dumps(ItemData), headers=self.__Headers).json()
                #print(Ret)
                if 'result' in Ret:
                    # 判断每台主机是否有获取到监控项，如果不等于0表示获取到有监控项
                    if len(Ret['result']) != 0:
                        # 从所有主机信息中取出目前获取信息的这台主机信息存在host_info中
                        HostInfo = AllHost[k]
                        #{'host': 'Zabbix server', 'hostid': '10084', 'ip': '127.0.0.1', 'name': 'Zabbix server'}
                        # 循环处理每一台主机的所有监控项
                        #print(HostInfo)
                        for host in Ret['result']:
                            #print(str(host.values()))
                            # 匹配所有分区挂载目录使用率的正则表达式
                            DiskUtilization = re.findall(r'根目录使用率监控', str(host.values()))
                            #print(DiskUtilization)
                            if len(DiskUtilization) == 1:   #如果匹配到了分区目录，进行保存
                                HostInfo[host['name']] = host['lastvalue']

                            # 匹配网卡进出流量的正则表达式
                            NetworkBits = re.findall(r'Interface.*: Bits [a-z]{4,8}', str(host.values()))
                            #print(host.values())
                            if  len(NetworkBits) == 1:
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'System name' in host.values():      # 匹配主机名，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'System uptime' in host.values():  # 匹配系统开机运行时长，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Number of CPUs' in host.values(): # 匹配CPU核数，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Total memory' in host.values():   # 匹配内存总大小，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif '/: Total space' in host.values(): # 匹配根目录总量，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif '/: Used space' in host.values():  # 匹配根目录使用量，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif '/: Space utilization' in host.values():  # 匹配根目录使用量，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Load average (1m avg)' in host.values():  # 匹配CPU平均1分钟负载，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Load average (5m avg)' in host.values():  # 匹配CPU平均5分钟负载，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Load average (15m avg)' in host.values():  # 匹配CPU平均15分钟负载，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'idle time' in host.values():  # 匹配CPU空闲时间，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'CPU utilization' in host.values(): # 匹配CPU使用率，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Memory utilization' in host.values(): # 匹配内存使用率，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif 'Available memory' in host.values():   # 匹配可用内存大小，进行保存
                                HostInfo[host['name']] = host['lastvalue']
                            elif '服务器硬盘总使用率' in host.values():
                                HostInfo[host['name']] = host['lastvalue']
                        #print(HostInfo)
                        NewAllHost[HostInfo['hostid']] = HostInfo
                        #print(NewAllHost)
                else:
                    return {"errcode": "1001", "errmess": "Login name or password is incorrect."}
            return NewAllHost
            #print(NewAllHost)

        elif HostRet == 1001:
            return self.Message[1001]
        elif HostRet == 1002:
            return self.Message[1002]
        elif HostRet == 1003:
            return self.Message[1003]
        else:
            return self.Message[1004]
```

## SaveToExcel.py

```bash
#! /usr/bin/env python
# _*_ coding: utf-8 _*_



import re
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Side, Border, PatternFill


def WriteExcel(FilaPath, ZabbixData):
    WorkBook = Workbook()
    Sheet = WorkBook.active
    Sheet.title = '服务器资源使用情况'
    #  除去 :  '根目录总量/G','根目录使用量/G',
    TableTitle = ['IP','主机名','运行时长/天','CPU/核','内存/GB','根目录使用率/%','CPU平均负载/1min','CPU平均负载/5min','CPU平均负载/15min','CPU空闲时间','CPU使用率/%','内存使用率/%','可用内存/G','磁盘使用率/%','低负载（是/否）']
    TitleColumn = {} #存放每个title值所对应的列{'IP': 'A', '主机名': 'B', '运行时长': 'C', 'CPU/核': 'D', '内存/GB': 'E', '根目录总量': 'F',...}
    AllHostItemValues = [] #存放所有主机的监控项值 列表信息。

    # 维护表头，写入表头数据
    for row in range(len(TableTitle)):
        Col = row + 1
        Column = Sheet.cell(row=1, column=Col)    #获取单元格的位置
        Column.value = TableTitle[row]  #写入数据
        TitleCol = Column.coordinate.strip('1') #获取Title所在的列
        TitleColumn[TableTitle[row]] = TitleCol #加入到TitleColumn

    # 整理Zabbix 监控数据逐行写入到表格中
    #print(ZabbixData)
    for host in ZabbixData.values():
        # 1.首先要对分区目录使用率进行一个整合，将除/目录外的分区目录使用率整合为一个值
        DiskItems = ''   #定义一个空值，用于存放除根目录空间使用率外所有的分区目录使用率
        DelItems = []    #定义一个空列表，用于存放除根目录空间使用率外所有的分区目录使用率的键值
        for item in host:
            DiskItem = re.findall(r'^/[a-z0-9]{1,50}: Space utilization', item)
            if len(DiskItem) == 1:
                DiskItem = DiskItem[0]  #获取监控项的名字 /boot: Space utilization
                NewDiskItem = DiskItem.strip('Space utilization')  # 将名字格式化，/boot: Space utilization 格式化为：/boot:
                DiskItemValue = str(round(float(host[item]), 2)) + '%'  # 取出对应监控项的值，并格式化保留两位小数
                # 将所有分区目录使用率组合为一个整的磁盘使用率
                if DiskItems == '':
                    DiskItemData = str(NewDiskItem) + ' ' + str(DiskItemValue)
                else:
                    DiskItemData = '\n' + str(NewDiskItem) + ' ' + str(DiskItemValue)
                DiskItems += DiskItemData
                # 将处理完的磁盘使用率加入到DelItems列表中，供后续删除使用
                DelItems.append(DiskItem)
        #print(host)
        # 2.将已经整合过的分区目录使用率监控项在原来的主机监控项中删除
        for delitem in DelItems:
            host.pop(delitem)

        # 3.将整合好的分区目录使用率，重新加入到主机监控项的字典中
        host['Disk utilization'] = DiskItems
        #print(host)
        # 4.将每台主机监控项的值取出来组成一个列表
        # 最终得到一条一条这样的数据：
        #'IP','主机名','运行时长/天','CPU/核','内存/GB','根目录使用率/%','CPU平均负载/1min','CPU平均负载/5min','CPU平均负载/15min','CPU空闲时间','CPU使用率/%','内存使用率/%','可用内存/G','磁盘使用率/%'
        # ['172.24.125.12', 'tbds-172-24-125-12', '245.87d', '16', 64, '50G', 7.43, '14.87%', '0.1', '0.18', '0.32', 97.79, '2.21%', '35.52%', 40.45, '/boot: 14.23%\n/data: 6.24%\n/home: 0.03%']
        #print(host['System uptime'])
        if 'System uptime' in host:
            HostItemValues = [] #定义一个空列表，用于存放主机的监控项的值
            HostItemValues.append(host['ip'])
            HostItemValues.append(host['name'])
            try:
                HostItemValues.append(str(round(int(host['System uptime']) / 24 / 60 / 60, 2)) + 'd')
                # 首先将运行时长换算为天数，然后再加入到列表中
            except  IndexError as e:
                print("IndexError Details : " + str(e))
                pass

            HostItemValues.append(host['Number of CPUs'])
            TotalMemory = int(int(host['Total memory']) / 1024 / 1024 / 1024)
            if TotalMemory == 7:
                TotalMemory = 8
            elif TotalMemory == 15:
                TotalMemory = 16
            elif TotalMemory == 31:
                TotalMemory = 32
            elif TotalMemory == 62:
                TotalMemory = 64
            elif TotalMemory == 251:
                TotalMemory = 256
            elif TotalMemory == 503:
                TotalMemory = 512
            HostItemValues.append(TotalMemory)  # 内存总大小
            #HostItemValues.append(str(round(int(host['/: Total space']) / 1024 / 1024 / 1024)) + 'G')  # 根目录总共大小
            #HostItemValues.append(str(round(int(host['/: Used space']) / 1024 / 1024 / 1024, 2)) + 'G')  # 根目录使用量
            HostItemValues.append(str(round(float(host['根目录使用率监控']), 2)) + '%')  # 根目录使用率
            HostItemValues.append(host['Load average (1m avg)'])
            HostItemValues.append(host['Load average (5m avg)'])
            HostItemValues.append(host['Load average (15m avg)'])
            HostItemValues.append(round(float(host['idle time']), 2))  # CPU空闲时间
            HostItemValues.append(str(round(float(host['CPU utilization']), 2)) + '%')  # CPU使用率
            HostItemValues.append(str(round(float(host['Memory utilization']), 2)) + '%')  # 内存使用率
            HostItemValues.append(str(round(int(host['Available memory']) / 1024 / 1024 / 1024, 2)) + 'G')  # 可用内存
            HostItemValues.append(host['服务器硬盘总使用率'])  # 磁盘使用率
            if host['Number of CPUs'] == "0":
                HostItemValues.append("已停用")
            #print(type(float(host['Load average (15m avg)'])),type(float(round(float(host['CPU utilization']), 2))))
            if  float(host['Load average (15m avg)']) >= 10 or  float(round(float(host['CPU utilization']), 2)) >= 20 :
                #print("负载: 是" + host['Load average (15m avg)'])
                #print("cpu: 是" + str(round(float(host['CPU utilization']), 2)))
                HostItemValues.append("否")
            else:
                #print("负载: 否" + host['Load average (15m avg)'])
               # print("cpu: 否" + str(round(float(host['CPU utilization']), 2)))
                HostItemValues.append("是")
            # 将每一台主机的所有监控项信息添加到AllHostItems列表中
            AllHostItemValues.append(HostItemValues)
        #print(AllHostItemValues)
    # 将所有信息写入到表格中
    for HostValue in range(len(AllHostItemValues)):
        Sheet.append(AllHostItemValues[HostValue])
        #print(HostValue)
    ############ 设置单元格样式 ############
    # 字体样式
    TitleFont = Font(name="宋体", size=12, bold=True, italic=False, color="000000")
    TableFont = Font(name="宋体", size=11, bold=False, italic=False, color="000000")
    # 对齐样式
    alignment = Alignment(horizontal="center", vertical="center", text_rotation=0, wrap_text=True)
    # 边框样式
    side1 = Side(style='thin', color='000000')
    border = Border(left=side1, right=side1, top=side1, bottom=side1)
    # 填充样式
    pattern_fill = PatternFill(fill_type='solid', fgColor='99ccff')
    # 设置列宽
    column_width = {'A': 15, 'B': 30, 'C': 14, 'D': 10, 'E': 10, 'F': 16, 'G': 18, 'H': 18, 'I': 22, 'J': 22, 'K': 23,
                    'L': 15, 'M': 16, 'N': 16, 'O': 14, 'P': 16}
    for i in column_width:
        Sheet.column_dimensions[i].width = column_width[i]
    # 设置首行的高度
    Sheet.row_dimensions[1].height = 38
    # 冻结窗口
    Sheet.freeze_panes = 'A2'
    # 添加筛选器
    Sheet.auto_filter.ref = Sheet.dimensions

    # 设置单元格字体及样式
    for row in Sheet.rows:
        for cell in row:
            if cell.coordinate.endswith('1') and len(cell.coordinate) == 2:
                cell.alignment = alignment  #设置对齐样式
                cell.font = TitleFont   #设置字体
                cell.border = border    #设置边框样式
                cell.fill = pattern_fill    #设置填充样式
            else:
                cell.font = TableFont
                cell.alignment = alignment
                cell.border = border
    WorkBook.save(filename=FilaPath)
```

多文件打包。这边百度一下，很简单的

![](../../image/2021071921171411.png)