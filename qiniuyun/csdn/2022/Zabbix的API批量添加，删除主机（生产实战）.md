---
author: 南宫乘风
categories:
- Zabbix监控
date: 2022-03-16 12:50:02
description: 场景：公司业务变更，部分机器需要变更，下线重新调整相关的业务。我们机器上有和监控，下线需要清空这些监控。比较监控，可以直接使用自动注册。删除下线就很麻烦。一台就可以手动删除，但是上百台那，一个个手动吗。。。。。。。
image: ../../title_pic/60.jpg
slug: '202203161250'
tags:
- python
- 开发语言
title: Zabbix的API批量添加，删除主机（生产实战）
---

<!--more-->

# **场景：**

公司业务变更，部分机器需要变更，下线重新调整相关的业务。

我们机器上有zabbix和prometheus监控，下线需要清空这些监控。

prometheus比较监控，可以直接使用consul自动注册。

zabbix 删除下线就很麻烦。一台就可以手动删除，但是上百台那，一个个手动吗，很麻烦的。

![](../../image/5c5d840479354526b422f02688b48c41.png)

 ![](../../image/9445ceb49f6941099cd8edd4b26a108f.png)

 

 

所以直接考虑zabbix的APi来批量删除主机

## 介绍

**代码放在下方**

代码使用的是python2.0的

因为我是纯内网环境需要先在外网部署好环境 ，然后打包使用的。

```bash
Python3虚拟环境创建

/usr/local/python3/bin/python3.7 -m venv py3

加载虚拟环境

source py3/bin/activate


安装依赖

pip install -r requirements.txt


生成依赖

pip freeze > requirements.txt


python2 虚拟环境
1.安装virtualenv

pip install virtualenv

2.创建虚拟环境

virtualenv 虚拟环境名称 

3.激活虚拟环境

source 虚拟环境目录/bin/activate  （./虚拟环境目录/bin/activate）

4.退出虚拟环境

deactivate
```

我们采用python2.0创建虚拟环境

```
[root@zabbix zabbix]# virtualenv py2

[root@zabbix zabbix]# ls
py2  zbx_tool.py
[root@zabbix zabbix]# source py2/
bin/        .gitignore  include/    lib/        lib64/      pyvenv.cfg  
             python            wheel2            
[root@zabbix zabbix]# source py2/bin/activate
(py2) [root@zabbix zabbix]# ls
py2  zbx_tool.py
(py2) [root@zabbix zabbix]# pip install argparse
.........
(py2) [root@zabbix zabbix]# ls
py2  zbx_tool.py
(py2) [root@zabbix zabbix]# python


打包 上传虚拟环境
tar -zcvf zabbix.tar.gz zabbix
```

上传内网环境进行解压，然后加载就可以使用虚拟环境

```bash
 source py2/bin/activate
```

## 生产环境实战

### 删除单台主机

![](../../image/be61ea52b49f4ccc989186cb4f9bcf81.png)

###  批量删除

![](../../image/d96b8a218ab3462e99bc4746cbd9cac1.png)

### for循环删除

首先新建有一个文本，然后通过for 循环批量删除

```bash
for ip in `cat zabbixip`;do python zbx_tool.py --delete $ip ;done
```

![](../../image/2fef6a30074e49108b088690a6253452.png)

** 开始**![](../../image/3a628a3e420746d286ab394da496eeaa.png)

**批量操作**

 ![](../../image/7b2da7afbbf04244a011902ccc332c23.png)

 

## **代码**

集合脚本，包含查询主机，主机组，模板，添加开启禁用删除主机等功能

```python
#!/usr/bin/env python
#-*- coding: utf-8 -*-
 
import json
import sys
import urllib2
import argparse
 
from urllib2 import URLError
 
reload(sys)
sys.setdefaultencoding('utf-8')
 
class zabbix_api:
    def __init__(self):
        self.url = 'http://zabbix.xxx.com/api_jsonrpc.php'
        self.header = {"Content-Type":"application/json"}
 
 
    def user_login(self):
        data = json.dumps({
                           "jsonrpc": "2.0",
                           "method": "user.login",
                           "params": {
                                      "user": "admin",
                                      "password": "zabbix"
                                      },
                           "id": 0
                           })
 
        request = urllib2.Request(self.url, data)
 
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "\033[041m 认证失败，请检查URL !\033[0m",e.code
        except KeyError as e:
            print "\033[041m 认证失败，请检查用户名密码 !\033[0m",e
        else:
            response = json.loads(result.read())
            result.close()
            #print response['result']
            self.authID = response['result']
            return self.authID
 
    def hostid_get_hostname(self, hostId=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {"hostid": hostId}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            #print response
            result.close()
 
            if not len(response['result']):
                print "hostId is not exist"
                return False
 
            #print "主机数量: \33[31m%s\33[0m" % (len(response['result']))
            host_dict=dict()
            for host in response['result']:
                status = {"0": "OK", "1": "Disabled"}
                available = {"0": "Unknown", "1": "available", "2": "Unavailable"}
                #if len(hostId) == 0:
                #    print "HostID : %s\t HostName : %s\t Status :\33[32m%s\33[0m \t Available :\33[31m%s\33[0m" % (
                #        host['hostid'], host['name'], status[host['status']], available[host['available']])
                #else:
                #    print "HostID : %s\t HostName : %s\t Status :\33[32m%s\33[0m \t Available :\33[31m%s\33[0m" % (
                #        host['hostid'], host['name'], status[host['status']], available[host['available']])
                host_dict['name']=host['name']
                host_dict['status']=status[host['status']]
                host_dict['available']=available[host['available']]
                return host_dict
 
    def hostid_get_hostip(self, hostId=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "filter": {"hostid": hostId}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            # print response
            result.close()
 
            if not len(response['result']):
                print "\033[041m hostid \033[0m is not exist"
                return False
 
            #print "主机数量: \33[31m%s\33[0m" % (len(response['result']))
            for hostip in response['result']:
                #print hostip
                #if len(hostip) == 0:
                #    print "HostID : %s\t HostIp : %s \t Port : %s " % (hostip['hostid'], hostip['ip'], hostip['port'])
                #else:
                #    print "HostID : %s\t HostIp :\33[32m%s\33[0m \t Port :\33[31m%s\33[0m" % (
                #        hostip['hostid'], hostip['ip'], hostip['port'])
                return hostip['ip']
 
    def host_get(self,hostName=''):
        data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                          "output": "extend",
                          #"filter":{"host":""}
                          "filter":{"host":hostName}
                          },
                "auth": self.user_login(),
                "id": 1
                })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            #print reqponse
            result.close()
 
            if not len(response['result']):
                print "\033[041m %s \033[0m is not exist" % hostName
                return False
 
            print "主机数量: \033[31m%s\033[0m"%(len(response['result']))
            for host in response['result']:
                status={"0":"OK","1":"Disabled"}
                available={"0":"Unknown","1":"available","2":"Unavailable"}
                #print host
                if len(hostName)==0:
                    print "HostID : %s\t HostName : %s\t HostIp : %s\t Status :%s \t Available :%s"%(host['hostid'],host['name'],self.hostid_get_hostip(hostId=host['hostid']),status[host['status']],available[host['available']])
                else:
                    print "HostID : %s\t HostName : %s\t HostIp : %s\t Status :\033[32m%s\033[0m \t Available :\033[31m%s\033[0m"%(host['hostid'],host['name'],self.hostid_get_hostip(hostId=host['hostid']),status[host['status']],available[host['available']])
                    return host['hostid']
 
    def hostip_get(self, hostIp=''):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "filter": {"ip": hostIp}
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(result.read())
            # print response
            result.close()
 
            if not len(response['result']):
                print "\033[041m hostip \033[0m is not exist"
                return False
 
            print "主机数量: \33[31m%s\33[0m" % (len(response['result']))
            for hostip in response['result']:
                host = self.hostid_get_hostname(hostip['hostid'])
                if len(hostip) == 0:
                    print "HostID : %s\t HostName : %s\t HostIp : %s\t Status :\33[32m%s\33[0m \t Available :\33[31m%s\33[0m"%(hostip['hostid'],host['name'],hostip['ip'],host['status'],host['available'])
                else:
                    print "HostID : %s\t HostName : %s\t HostIp : %s\t Status :\33[32m%s\33[0m \t Available :\33[31m%s\33[0m"%(hostip['hostid'],host['name'],hostip['ip'],host['status'],host['available'])
                    return hostip['hostid']
 
    def hostgroup_get(self, hostgroupName=''):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"hostgroup.get",
                           "params":{
                                     "output": "extend",
                                     "filter": {
                                                "name": hostgroupName
                                                }
                                     },
                           "auth":self.user_login(),
                           "id":1,
                           })
 
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            # result.read()
            response = json.loads(result.read())
            result.close()
            #print response()
            if not len(response['result']):
                print "\033[041m %s \033[0m is not exist" % hostgroupName
                return False
 
            for group in response['result']:
                if  len(hostgroupName)==0:
                    print "hostgroup:  \033[31m%s\033[0m \tgroupid : %s" %(group['name'],group['groupid'])
                else:
                    print "hostgroup:  \033[31m%s\033[0m\tgroupid : %s" %(group['name'],group['groupid'])
                    self.hostgroupID = group['groupid']
            return group['groupid']
 
    def template_get(self,templateName=''):
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method": "template.get",
                           "params": {
                                      "output": "extend",
                                      "filter": {
                                                 "name":templateName
                                                 }
                                      },
                           "auth":self.user_login(),
                           "id":1,
                           })
 
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            #print response
            if not len(response['result']):
                print "\033[041m %s \033[0m is not exist" % templateName
                return False
 
            for template in response['result']:
                if len(templateName)==0:
                    print "template : %s \t id : %s" % (template['name'], template['templateid'])
                else:
                    self.templateID = response['result'][0]['templateid']
                    print "Template Name :%s"%templateName
                    return response['result'][0]['templateid']
 
    def hostgroup_create(self,hostgroupName):
        if self.hostgroup_get(hostgroupName):
            print "hostgroup  \033[42m%s\033[0m is exist !" % hostgroupName
            sys.exit(1)
 
        data = json.dumps({
                          "jsonrpc": "2.0",
                          "method": "hostgroup.create",
                          "params": {
                          "name": hostgroupName
                          },
                          "auth": self.user_login(),
                          "id": 1
                          })
        request=urllib2.Request(self.url,data)
 
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print "添加主机组:%s  hostgroupID : %s"%(hostgroupName,self.hostgroup_get(hostgroupName))
 
    def host_create(self, hostIp, hostgroupName, templateName, hostName):
        if self.host_get(hostName) or self.hostip_get(hostIp):
            print "该主机已经添加!"
            sys.exit(1)
 
        group_list=[]
        template_list=[]
        for i in hostgroupName.split(','):
            var = {}
            var['groupid'] = self.hostgroup_get(i)
            group_list.append(var)
        for i in templateName.split(','):
            var={}
            var['templateid']=self.template_get(i)
            template_list.append(var)
 
        data = json.dumps({
                           "jsonrpc":"2.0",
                           "method":"host.create",
                           "params":{
                                     "host": hostName,
                                     "interfaces": [
                                     {
                                     "type": 1,
                                     "main": 1,
                                     "useip": 1,
                                     "ip": hostIp,
                                     "dns": "",
                                     "port": "10050"
                                      }
                                     ],
                                   "groups": group_list,
                                   "templates": template_list,
                                     },
                           "auth": self.user_login(),
                           "id":1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            print "add host : %s id :%s" % (hostIp, hostName)
        except URLError as e:
            print "Error as ", e
        except KeyError as e:
            print "\033[041m 主机添加有误，请检查模板正确性或主机是否添加重复 !\033[0m",e
            print response
 
    def host_disable(self,hostip):
        data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.update",
                "params": {
                "hostid": self.host_get(hostip),
                "status": 1
                },
                "auth": self.user_login(),
                "id": 1
                })
        request = urllib2.Request(self.url,data)
        #opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(TerminalPassword()))
        for key in self.header:
                request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            #result = opener.open(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print '------------主机现在状态------------'
            print self.host_get(hostip)
 
    def host_enable(self,hostip):
        data=json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
            "hostid": self.host_get(hostip),
            "status": 0
            },
            "auth": self.user_login(),
            "id": 1
            })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            #result = opener.open(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            print '------------主机现在状态------------'
            print self.host_get(hostip)
 
    def host_delete(self,hostNames):
        hostid_list=[]
        for hostName in hostNames.split(','):
            hostid = self.host_get(hostName=hostName)
            if not hostid:
                print "主机 \033[041m %s\033[0m  删除失败 !" % hostName
                sys.exit()
            hostid_list.append(hostid)
 
        data=json.dumps({
                "jsonrpc": "2.0",
                "method": "host.delete",
                "params": hostid_list,
                "auth": self.user_login(),
                "id": 1
                })
 
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
 
        try:
            result = urllib2.urlopen(request)
            result.close()
            print "主机 \033[041m %s\033[0m  已经删除 !" % hostName
        except Exception,e:
            print  e
 
if __name__ == "__main__":
    zabbix=zabbix_api()
    parser=argparse.ArgumentParser(description='zabbix api ',usage='%(prog)s [options]')
    parser.add_argument('-H','--host',nargs='?',dest='listhost',default='host',help='查询主机')
    parser.add_argument('-G','--group',nargs='?',dest='listgroup',default='group',help='查询主机组')
    parser.add_argument('-T','--template',nargs='?',dest='listtemp',default='template',help='查询模板信息')
    parser.add_argument('-A','--add-group',nargs=1,dest='addgroup',help='添加主机组')
    parser.add_argument('-C','--add-host',dest='addhost',nargs=4,metavar=('192.168.2.1', 'groupname', 'Template01,Template02', 'hostName'),help='添加主机,多个主机组或模板使用逗号')
    parser.add_argument('-d','--disable',dest='disablehost',nargs='+',metavar=('sh-aa-01'),help='禁用主机,填写主机名，多个主机名之间用逗号')
    parser.add_argument('-e','--enable',dest='enablehost',nargs=1,metavar=('sh-aa-01'),help='开启主机')
    parser.add_argument('-D','--delete',dest='deletehost',nargs='+',metavar=('sh-aa-01'),help='删除主机,多个主机之间用逗号')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
 
    if len(sys.argv) == 1:
        #print parser.print_help()
        #print zabbix.host_get(hostName='bbb')
        #print zabbix.hostip_get(hostIp='127.0.0.1')
        #print zabbix.hostid_get_hostname(hostId='10108')
        #print zabbix.hostid_get_hostid(hostId='10105')
        #print zabbix.hostgroup_get(hostgroupName='Linux servers')
        #print zabbix.hostgroup_get(hostgroupName='aaa')
        # ...
        print zabbix.host_delete('hz-aaa-02')
    else:
        args = parser.parse_args()
        if args.listhost != 'host':
            if args.listhost:
                zabbix.host_get(args.listhost)
            else:
                zabbix.host_get()
        if args.listgroup != 'group':
            if args.listgroup:
                zabbix.hostgroup_get(args.listgroup)
            else:
                zabbix.hostgroup_get()
        if args.listtemp != 'template':
            if args.listtemp:
                zabbix.template_get(args.listtemp)
            else:
                zabbix.template_get()
        if args.addgroup:
            zabbix.hostgroup_create(args.addgroup[0])
        if args.addhost:
            zabbix.host_create(args.addhost[0], args.addhost[1], args.addhost[2], args.addhost[3])
        if args.disablehost:
            zabbix.host_disable(args.disablehost)
        if args.deletehost:
            zabbix.host_delete(args.deletehost[0])
```

## **用法**

```bash
> python zbx_tool.py -h
usage: zbx_tool.py [options]
 
zabbix api
 
optional arguments:
  -h, --help            show this help message and exit
  -H [LISTHOST], --host [LISTHOST]
                        查询主机
  -G [LISTGROUP], --group [LISTGROUP]
                        查询主机组
  -T [LISTTEMP], --template [LISTTEMP]
                        查询模板信息
  -A ADDGROUP, --add-group ADDGROUP
                        添加主机组
  -C 192.168.2.1 groupname Template01,Template02 hostName, --add-host 192.168.2.1 groupname Template01,Template02 hostName
                        添加主机,多个主机组或模板使用逗号
  -d sh-aa-01 [sh-aa-01 ...], --disable sh-aa-01 [sh-aa-01 ...]
                        禁用主机,填写主机名，多个主机名之间
                        ¨逗号
  -e sh-aa-01, --enable sh-aa-01
                        开启主机
  -D sh-aa-01 [sh-aa-01 ...], --delete sh-aa-01 [sh-aa-01 ...]
                        删除主机,多个主机之间用逗号
  -v, --version         show program's version number and exit
```

 ![](../../image/be5d546dac534f03a36ebf5ac083f565.png)

 

相关博客

[利用zabbix API批量查询主机、模板、添加删除主机 \- 代码先锋网](https://www.codeleading.com/article/3026664232/ "利用zabbix API批量查询主机、模板、添加删除主机 \- 代码先锋网")