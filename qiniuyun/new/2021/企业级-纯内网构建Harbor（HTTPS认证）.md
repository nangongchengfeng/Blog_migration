---
author: 南宫乘风
categories:
- Docker
date: 2021-09-16 14:18:55
description: 集群内部构建一套集群，纯内网没有公网环境，无法拉取镜像，不是很方便前期做法，本地拉去镜像，保存，上传内网，加载。这个是针对每台机器的步骤。步骤比较繁琐，和机械化。所以准备在内部构建，走域名绑定。加载配。。。。。。。
image: http://image.ownit.top/4kdongman/01.jpg
tags:
- https
- docker
title: 企业级-纯内网构建Harbor （HTTPS认证）
---

<!--more-->

集群内部构建一套Kubernetes集群，纯内网没有公网环境，无法拉取镜像，不是很方便

前期做法，本地拉去镜像，保存，上传内网，加载。这个是针对每台机器的步骤。

步骤比较繁琐，和机械化。

所以准备在内部构建harbor，走域名绑定。docker加载配置，后期可以正常使用。

# 1、环境

Docker version 20.10.7

docker-compose version 1.29.2

harbor-offline-installer-v2.3.1.tgz

内网安装，我选择离线版本的

[Release v2.3.2 · goharbor/harbor · GitHub](https://github.com/goharbor/harbor/releases/tag/v2.3.2 "Release v2.3.2 · goharbor/harbor · GitHub")

# 2、生成https证书

 docker 和 docker-compose 已经安装好下进行

```bash
cd /opt/cert
#输入密码
openssl genrsa -des3 -out server.pass.key 2048
#去除密码
openssl rsa -in server.pass.key -out server.key
#生成域名证书
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=Jiangsu/L=Nanjing/O=Company/OU=group/CN=hub.docker.com"
#生成时间多久
openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt
#生成pem的（可以跳过）
openssl x509 -in server.crt -out server.pem -outform PEM
```

![](http://image.ownit.top/csdn/20210916140855868.png)

#  3、安装harbor

解压文件

```bash
#复制新的配置
[root@hdpv3test08 harbor]# cat harbor.yml
# Configuration file of Harbor

# The IP address or hostname to access admin UI and registry service.
# DO NOT use localhost or 127.0.0.1, because Harbor needs to be accessed by external clients.
hostname: hub.docker.com

# http related config
http:
  # port for http, default is 80. If https enabled, this port will redirect to https port
  port: 80

# https related config
https:
  # https port for harbor, default is 443
  port: 443
  # The path of cert and key files for nginx
  certificate: /opt/cert/server.crt
  private_key: /opt/cert/server.key

# # Uncomment following will enable tls communication between all harbor components
# internal_tls:
#   # set enabled to true means internal tls is enabled
#   enabled: true
#   # put your cert and key files on dir
#   dir: /etc/harbor/tls/internal

# Uncomment external_url if you want to enable external proxy
# And when it enabled the hostname will no longer used
# external_url: https://reg.mydomain.com:8433

# The initial password of Harbor admin
# It only works in first time to install harbor
# Remember Change the admin password from UI after launching Harbor.
harbor_admin_password: Harbor12345

# Harbor DB configuration
database:
  # The password for the root user of Harbor DB. Change this before any production use.
  password: root123
  # The maximum number of connections in the idle connection pool. If it <=0, no idle connections are retained.
  max_idle_conns: 100
  # The maximum number of open connections to the database. If it <= 0, then there is no limit on the number of open connections.
  # Note: the default number of connections is 1024 for postgres of harbor.
  max_open_conns: 900

# The default data volume
data_volume: /data/service/harbor

# Harbor Storage settings by default is using /data dir on local filesystem
# Uncomment storage_service setting If you want to using external storage
# storage_service:
#   # ca_bundle is the path to the custom root ca certificate, which will be injected into the truststore
#   # of registry's and chart repository's containers.  This is usually needed when the user hosts a internal storage with self signed certificate.
#   ca_bundle:

#   # storage backend, default is filesystem, options include filesystem, azure, gcs, s3, swift and oss
#   # for more info about this configuration please refer https://docs.docker.com/registry/configuration/
#   filesystem:
#     maxthreads: 100
#   # set disable to true when you want to disable registry redirect
#   redirect:
#     disabled: false

# Trivy configuration
#
# Trivy DB contains vulnerability information from NVD, Red Hat, and many other upstream vulnerability databases.
# It is downloaded by Trivy from the GitHub release page https://github.com/aquasecurity/trivy-db/releases and cached
# in the local file system. In addition, the database contains the update timestamp so Trivy can detect whether it
# should download a newer version from the Internet or use the cached one. Currently, the database is updated every
# 12 hours and published as a new release to GitHub.
trivy:
  # ignoreUnfixed The flag to display only fixed vulnerabilities
  ignore_unfixed: false
  # skipUpdate The flag to enable or disable Trivy DB downloads from GitHub
  #
  # You might want to enable this flag in test or CI/CD environments to avoid GitHub rate limiting issues.
  # If the flag is enabled you have to download the `trivy-offline.tar.gz` archive manually, extract `trivy.db` and
  # `metadata.json` files and mount them in the `/home/scanner/.cache/trivy/db` path.
  skip_update: false
  #
  # insecure The flag to skip verifying registry certificate
  insecure: false
  # github_token The GitHub access token to download Trivy DB
  #
  # Anonymous downloads from GitHub are subject to the limit of 60 requests per hour. Normally such rate limit is enough
  # for production operations. If, for any reason, it's not enough, you could increase the rate limit to 5000
  # requests per hour by specifying the GitHub access token. For more details on GitHub rate limiting please consult
  # https://developer.github.com/v3/#rate-limiting
  #
  # You can create a GitHub token by following the instructions in
  # https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
  #
  # github_token: xxx

jobservice:
  # Maximum number of job workers in job service
  max_job_workers: 10

notification:
  # Maximum retry count for webhook job
  webhook_job_max_retry: 10

chart:
  # Change the value of absolute_url to enabled can enable absolute url in chart
  absolute_url: disabled

# Log configurations
log:
  # options are debug, info, warning, error, fatal
  level: info
  # configs for logs in local storage
  local:
    # Log files are rotated log_rotate_count times before being removed. If count is 0, old versions are removed rather than rotated.
    rotate_count: 50
    # Log files are rotated only if they grow bigger than log_rotate_size bytes. If size is followed by k, the size is assumed to be in kilobytes.
    # If the M is used, the size is in megabytes, and if G is used, the size is in gigabytes. So size 100, size 100k, size 100M and size 100G
    # are all valid.
    rotate_size: 200M
    # The directory on your host that store log
    location: /var/log/harbor

  # Uncomment following lines to enable external syslog endpoint.
  # external_endpoint:
  #   # protocol used to transmit log to external endpoint, options is tcp or udp
  #   protocol: tcp
  #   # The host of external endpoint
  #   host: localhost
  #   # Port of external endpoint
  #   port: 5140

#This attribute is for migrator to detect the version of the .cfg file, DO NOT MODIFY!
_version: 2.3.0

# Uncomment external_database if using external database.
# external_database:
#   harbor:
#     host: harbor_db_host
#     port: harbor_db_port
#     db_name: harbor_db_name
#     username: harbor_db_username
#     password: harbor_db_password
#     ssl_mode: disable
#     max_idle_conns: 2
#     max_open_conns: 0
#   notary_signer:
#     host: notary_signer_db_host
#     port: notary_signer_db_port
#     db_name: notary_signer_db_name
#     username: notary_signer_db_username
#     password: notary_signer_db_password
#     ssl_mode: disable
#   notary_server:
#     host: notary_server_db_host
#     port: notary_server_db_port
#     db_name: notary_server_db_name
#     username: notary_server_db_username
#     password: notary_server_db_password
#     ssl_mode: disable

# Uncomment external_redis if using external Redis server
# external_redis:
#   # support redis, redis+sentinel
#   # host for redis: <host_redis>:<port_redis>
#   # host for redis+sentinel:
#   #  <host_sentinel1>:<port_sentinel1>,<host_sentinel2>:<port_sentinel2>,<host_sentinel3>:<port_sentinel3>
#   host: redis:6379
#   password:
#   # sentinel_master_set must be set to support redis+sentinel
#   #sentinel_master_set:
#   # db_index 0 is for core, it's unchangeable
#   registry_db_index: 1
#   jobservice_db_index: 2
#   chartmuseum_db_index: 3
#   trivy_db_index: 5
#   idle_timeout_seconds: 30

# Uncomment uaa for trusting the certificate of uaa instance that is hosted via self-signed cert.
# uaa:
#   ca_file: /path/to/ca

# Global proxy
# Config http proxy for components, e.g. http://my.proxy.com:3128
# Components doesn't need to connect to each others via http proxy.
# Remove component from `components` array if want disable proxy
# for it. If you want use proxy for replication, MUST enable proxy
# for core and jobservice, and set `http_proxy` and `https_proxy`.
# Add domain to the `no_proxy` field, when you want disable proxy
# for some special registry.
proxy:
  http_proxy:
  https_proxy:
  no_proxy:
  components:
    - core
    - jobservice
    - trivy

# metric:
#   enabled: false
#   port: 9090
#   path: /metrics

```

安装

```bash
./prepare
./install.sh --with-notary --with-trivy --with-chartmuseum
```

安装完就成功

![](http://image.ownit.top/csdn/20210916141158676.png)

 ![](http://image.ownit.top/csdn/20210916141235817.png)

#  4、配置本地域名

由于是内网，我们需要写入hosts文件，配置本地域名

```bash
[root@hdpv3test08 harbor]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.17.9.47 hub.docker.com
```

# 5、配置docker

给dock添加仓库，我们自建的，需要添加到配置里面

```bash
[root@hdpv3test08 harbor]# cat /etc/docker/daemon.json 
{
    "insecure-registries":["hub.docker.com"]
}
[
```

填加完需要重启，但是由于已经容器，重启会照成影响，我们可以热加载

**热加载**

```bash
[root@hdpv3test08 harbor]# ps -ef | grep docker
root      81995      1  0 9月15 ?       00:04:03 /usr/bin/dockerd
[root@hdpv3test08 harbor]# kill -HUP 81995      
这个就是热加载
```

# 6、测试

```bash
docker login hub.docker.com -u admin -p Harbor12345
```

![](http://image.ownit.top/csdn/20210916141613296.png)