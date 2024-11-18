---
author: 南宫乘风
categories:
- Nginx
- 项目实战
date: 2024-07-15 16:47:03
description: 、引言在当今数字化时代，网络安全已成为企业和个人用户关注的焦点。黑白名单作为一种有效的网络安全策略，允许我们精确控制对资源的访问权限。通过白名单，我们可以确保只有可信的地址能够访问敏感资源；而黑名单则。。。。。。。
image: ../../title_pic/18.jpg
slug: '202407151647'
tags:
- nginx
- openresty
- redis
title: 使用Nginx OpenResty与Redis实现高效IP黑白名单管理
---

<!--more-->

## 1、引言

在当今数字化时代，网络安全已成为企业和个人用户关注的焦点。IP黑白名单作为一种有效的网络安全策略，允许我们精确控制对Web资源的访问权限。通过白名单，我们可以确保只有可信的IP地址能够访问敏感资源；而黑名单则可以阻止恶意IP的访问，从而减少安全风险。

选择Nginx OpenResty与Redis作为实现黑白名单的解决方案，是基于以下几个原因：

- **高性能**：Nginx以其轻量级和高性能著称，适合处理高并发请求。
- **灵活性**：OpenResty通过集成Lua脚本，提供了强大的定制能力。
- **可扩展性**：Redis作为一个内存数据结构存储，支持数据的快速读写，适合实现动态的黑白名单管理。
## 2、简介
### 1、什么是OpenResty？
OpenResty是一个基于Nginx的全功能Web平台，它集成了一系列精心设计的Lua库、第三方模块和一个基于LuaJIT的轻量级Web框架。OpenResty的核心是Nginx，但它通过Lua语言扩展了Nginx的功能，使其能够构建能够处理超高并发的动态Web应用。

### 2、OpenResty与Nginx的关系
OpenResty是在Nginx的基础上构建的，它保留了Nginx的所有功能，并通过Lua语言扩展了其能力。这意味着你可以使用OpenResty来实现Nginx的所有功能，同时还能够利用Lua脚本来实现更复杂的业务逻辑。

## 3、环境安装
### 1、环境版本
```bash
centos 7 
redis 7.2
nginx version: openresty/1.25.3.1
```
### 2、环境安装
1、添加OpenResty仓库

```bash
# 由于公共库中找不到openresty，所以需要添加openresty的源仓库
yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo

# 注意，如果上面命令提示不存在,那就先安装一下
yum install -y yum-utils
```
2. 安装OpenResty

```bash
# 安装openresty
yum install -y openresty
# 安装OpenResty管理工具，帮助我们安装第三方的Lua模块
yum install -y openresty-opm
```
3、目录结构
​ 默认安装在/usr/local/openresty
![在这里插入图片描述](../../image/527f59876e9a41f0b055f08da40ff9d2.png)
看到里面有一个nginx目录，进去可以看到跟我们平常用的nginx是一模一样的，OpenResty就是在Nginx基础上集成了一些Lua模块

到这里我们就安装好了

4、启动和运行
OpenResty底层是基于Nginx的，查看OpenResty目录的nginx目录，结构与windows中安装的nginx基本一致

5、安装配置redis

```bash
sudo yum install redis -y
```

Redis配置主要包括设置持久化选项、网络配置、安全性设置等。以下是一个基本的配置示例：

```bash
# redis.conf
port 6379
bind 127.0.0.1
protected-mode yes
requirepass "yourpassword"
```
## 4、白名单实现

![在这里插入图片描述](../../image/8454272694fe4cbf98d5e3c36d3524ff.png)
### 图例说明：

- **客户端**：发送HTTP请求的用户或应用。
- **Nginx (OpenResty)**：处理和管理HTTP请求，执行Lua脚本进行访问控制。
- **Lua脚本**：在Nginx中运行，负责从Redis获取白名单并进行IP检查。
- **Redis**：存储白名单数据，用于快速查询。

#### 交互流程：

1. 客户端发送请求到Nginx。
2. Nginx调用Lua脚本进行访问控制。
3. Lua脚本连接Redis，并查询IP是否在白名单中。
4. Lua脚本返回查询结果给Nginx。
5. Nginx根据结果决定是否允许请求，并返回响应给客户端
### 定义白名单的作用与重要性

白名单是一种安全策略，用于定义一组被信任的IP地址或实体，它们被允许访问特定的资源或服务。在Web应用中，白名单的作用尤为显著：

- **安全性增强**：限制访问权限，仅允许特定的IP地址访问敏感资源。
- **防止滥用**：减少恶意用户或爬虫对服务的滥用。
- **流量管理**：通过控制访问源，更有效地管理网络流量。

### 通过OpenResty Lua脚本实现白名单逻辑

在OpenResty中，我们可以使用Lua脚本来实现白名单逻辑。Lua脚本可以在Nginx的配置文件中直接编写，或者存储在外部文件中，并在配置文件中引用。

### Lua脚本实现步骤：

1. **定义白名单**：在Redis中存储白名单IP地址。
2. **访问控制**：在Nginx配置中使用`access_by_lua_block`或`access_by_lua_file`指令调用Lua脚本。
3. **脚本逻辑**：检查请求的IP地址是否在白名单中，如果不在，则拒绝访问。

### 案例演示
`jenkins.ownit.top.conf `
这个是nginx的配置文件
最主要内容:`access_by_lua_file /opt/nginx/lua_script/white.lua;`
```bash
upstream jenkins-uat {
        server 192.168.102.20:91;
}
server {
        listen       80;
        server_name  jenkins.ownit.top;
        #白名单 或者 黑名单
        #include /opt/nginx/whitelist/corporation.conf;

        location / {
            rewrite ^/(.*)$ https://$host/$1 permanent;
        }

    access_log  /www/wwwlogs/dns.ownit.top.log;
    error_log  /www/wwwlogs/dns.ownit.top.error.log;

}
server {
        listen       443 ssl;
        server_name  jenkins.ownit.top;
         #白名单 或者 黑名单
        #include /opt/nginx/whitelist/corporation.conf;

        #ssl                   on;
        ssl_certificate      /opt/nginx/ssl/ownit.top.crt;
        ssl_certificate_key  /opt/nginx/ssl/ownit.top.key;
        include ssl.conf;

        location / {
            access_by_lua_file /opt/nginx/lua_script/white.lua; # nginx的lua脚本
            proxy_pass  http://jenkins-uat;
            include https_proxy.conf;
        }
    access_log  /www/wwwlogs/dns.ownit.top.log;
    error_log  /www/wwwlogs/dns.ownit.top.error.log;

}


```

`white.lua`文件

通过使用Lua脚本，在接收到HTTP请求时检查请求的IP地址是否在Redis存储的白名单中。如果IP不在白名单中，则拒绝访问。
### 思路

1. **获取客户端IP和请求路径**：在Lua脚本中获取客户端的IP地址和请求路径。
2. **连接Redis**：使用`resty.redis`模块连接Redis数据库。
3. **权限校验**：对连接的Redis进行认证。
4. **检查IP是否在白名单中**：从Redis中检查IP是否存在于白名单集合中。
5. **返回结果**：如果IP在白名单中，允许访问；否则，返回403 Forbidden状态码，拒绝访问。
6. **释放Redis连接**：将Redis连接返回到连接池中，以便复用。

```bash
-- 获取客户端IP和请求路径
local client_ip = ngx.var.remote_addr
local path = ngx.var.uri

-- Redis相关配置
local redis_key_white_list = "map_request_white_list"

-- 连接Redis
local redis = require "resty.redis"
local red = redis:new()
red:set_timeout(1000) -- 设置超时（毫秒）
local ok, err = red:connect("127.0.0.1", 6379)
if not ok then
    ngx.log(ngx.ERR, "Redis连接失败: ", err)
    return ngx.exit(500)
end

-- 权限校验
local res, err = red:auth("123456")
if not res then
    ngx.say("failed to authenticate: ", err)
    return
end

-- 检查IP是否在白名单中
local is_in_whitelist, err = red:sismember(redis_key_white_list, client_ip)
if is_in_whitelist == 1 then
    ngx.log(ngx.INFO, "IP在白名单中: ", client_ip)
else
    ngx.status = ngx.HTTP_FORBIDDEN
    ngx.say("Access Denied")
    return ngx.exit(ngx.HTTP_FORBIDDEN)
end

-- 返还redis连接到连接池
local ok, err = red:set_keepalive(10000, 100)
if not ok then
    ngx.log(ngx.ERR, "设置keepalive失败: ", err)
end

```

### 详细解释

1. **获取客户端IP和请求路径**

   ```lua
   local client_ip = ngx.var.remote_addr
   local path = ngx.var.uri
   ```

   这两行代码从Nginx变量中获取客户端的IP地址和请求路径，`client_ip`用于后续的白名单检查。

2. **Redis相关配置**

   ```lua
   local redis_key_white_list = "map_request_white_list"
   ```

   定义存储白名单的Redis键。

3. **连接Redis**

   ```lua
   local redis = require "resty.redis"
   local red = redis:new()
   red:set_timeout(1000) -- 设置超时（毫秒）
   local ok, err = red:connect("127.0.0.1", 6379)
   if not ok then
       ngx.log(ngx.ERR, "Redis连接失败: ", err)
       return ngx.exit(500)
   end
   ```

   使用`resty.redis`模块创建Redis连接对象，并设置连接超时时间。尝试连接到Redis服务器，如果连接失败，记录错误日志并返回500错误。

4. **权限校验**

```lua
local res, err = red:auth("123456")
if not res then
    ngx.say("failed to authenticate: ", err)
    return
end

```

   对Redis进行认证，如果认证失败，输出错误信息并停止执行。

5. **检查IP是否在白名单中**

   

```lua
local is_in_whitelist, err = red:sismember(redis_key_white_list, client_ip)
if is_in_whitelist == 1 then
    ngx.log(ngx.INFO, "IP在白名单中: ", client_ip)
else
    ngx.status = ngx.HTTP_FORBIDDEN
    ngx.say("Access Denied")
    return ngx.exit(ngx.HTTP_FORBIDDEN)
end

```

   使用`SISMEMBER`命令检查IP是否在Redis的白名单集合中。如果IP在白名单中，记录信息日志；否则，返回403 Forbidden状态码并拒绝访问。

6. **释放Redis连接**

```lua
local ok, err = red:set_keepalive(10000, 100)
if not ok then
    ngx.log(ngx.ERR, "设置keepalive失败: ", err)
end

```

   将Redis连接返回到连接池中，以便后续请求复用该连接。如果设置失败，记录错误日志。

### 在Nginx中配置Lua脚本

在Nginx的`location`配置中，使用`access_by_lua_file`指令来调用上述Lua脚本：

```
nginx复制代码http {

```lua
http {
    server {
        listen 80;
        server_name example.com;

        location / {
            access_by_lua_file /opt/nginx/lua_script/white.lua;
            proxy_pass http://backend;
        }
    }
}

```

上述配置在接收到HTTP请求时，会首先执行`/opt/nginx/lua_script/white.lua`脚本进行白名单检查。如果通过检查，则继续将请求转发到后端服务器。

![在这里插入图片描述](../../image/94ff705723444036af32efa94c21a068.png)
成功访问：
![在这里插入图片描述](../../image/502c54e94a7a4ae796a38d1530eebaf7.png)
禁止访问：
![在这里插入图片描述](../../image/8c42197780744b10b11c19a03436f08c.png)

## 5、黑名单实现
### 黑名单的作用与场景

黑名单是一种网络安全机制，用于识别并阻止恶意IP地址对服务器资源的访问。它在多种场景中发挥着重要作用：

- **防止恶意攻击**：通过封禁已知的攻击者IP，减少服务器遭受的恶意攻击。
- **打击爬虫滥用**：限制爬虫对网站资源的过度访问，保护数据不被滥用。
- **减轻服务器负载**：通过限制特定IP的访问频率，减轻服务器压力，提高服务稳定性。
- **DDoS防御**：快速响应DDoS攻击，封禁攻击源IP，保护服务可用性。

### 使用Lua脚本与Redis实现动态IP封禁
OpenResty结合Redis可以实现一个高效的动态IP封禁系统。以下是实现的关键步骤：

1. 环境配置：确保Nginx OpenResty和Redis环境准备就绪。
2. Lua脚本编写：编写Lua脚本来动态查询和更新Redis中的黑名单状态。
3. Nginx配置整合：在Nginx配置文件中集成Lua脚本，实现访问控制。

![在这里插入图片描述](../../image/b96394be65064e5fa44511998fe06e51.png)
### 案例演示

通过使用Lua脚本，在接收到HTTP请求时检查请求的IP地址是否在黑名单中，或控制IP的访问频率，并进行相应的处理。

### 思路

1. **获取客户端IP**：在Lua脚本中获取客户端的IP地址。
2. **连接Redis**：使用`resty.redis`模块连接Redis数据库。
3. **权限校验**：对连接的Redis进行认证。
4. **检查IP是否在黑名单中**：从Redis中检查IP是否存在于黑名单集合中。
5. **访问频次控制**：对每个IP的访问频次进行限制，如果超过指定的频次，则将IP加入黑名单。
6. **返回结果**：如果IP在黑名单中，返回403 Forbidden状态码，拒绝访问；否则，允许请求继续。

### Nginx 配置文件

```bash
upstream jms-uat {
    server 192.168.82.105:81;
}
server {
    listen 80;
    server_name jms.ownit.top;
    # 白名单 或者 黑名单
    # include /opt/nginx/whitelist/corporation.conf;
    rewrite ^/(.*)$ https://$host/$1 permanent;
    access_log /www/wwwlogs/dns.ownit.top.log;
    error_log /www/wwwlogs/dns.ownit.top.error.log;
}
server {
    listen 443 ssl;
    server_name jms.ownit.top;
    # 白名单 或者 黑名单
    # include /opt/nginx/whitelist/corporation.conf;
    ssl_certificate /opt/nginx/ssl/ownit.top.crt;
    ssl_certificate_key /opt/nginx/ssl/ownit.top.key;
    include ssl.conf;
    
    location = /core/auth/login/ {
        access_by_lua_file /opt/nginx/lua_script/login.lua;
        proxy_pass http://jms-uat;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        if ($request_uri !~ \.(html|htm|jpg|png|ico|js|css)$) {
            access_by_lua_file /opt/nginx/lua_script/rule.lua;
        }
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass http://jms-uat;
        include https_proxy.conf;
        client_max_body_size 0;
    }
    access_log /www/wwwlogs/dns.ownit.top.log;
    error_log /www/wwwlogs/dns.ownit.top.error.log;
}

```
`location = /core/auth/login/`

```bash
location = /core/auth/login/ {
    access_by_lua_file /opt/nginx/lua_script/login.lua;
    proxy_pass http://jms-uat;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```
##### 解释

- **`location = /core/auth/login/`**：
  - 这是一个精确匹配的`location`块，仅对请求路径严格等于`/core/auth/login/`的请求生效。
- **`access_by_lua_file /opt/nginx/lua_script/login.lua;`**：
  - 使用OpenResty的Lua模块，指定在访问控制阶段执行`/opt/nginx/lua_script/login.lua`脚本。这个脚本通常用于执行认证、权限检查或其他预处理逻辑。
- **`proxy_pass http://jms-uat;`**：
  - 将匹配到的请求代理到上游服务器`http://jms-uat`。
- **`proxy_set_header Upgrade $http_upgrade;`**：
  - 设置`Upgrade`请求头，支持WebSocket等协议升级。`$http_upgrade`变量包含原始请求中的`Upgrade`头字段的值。
- **`proxy_set_header Connection "upgrade";`**：
  - 设置`Connection`请求头为`upgrade`，通常与`Upgrade`头一起使用，以确保连接升级。


`location /`

```bash
location / {
    # 如果该location 下存在静态资源文件可以做一个判断 
    if ($request_uri !~ \.(html|htm|jpg|png|ico|js|css)$) {
        access_by_lua_file /opt/nginx/lua_script/rule.lua; 加上了这条配置，则会根据 rule.lua 的规则进行限流
    }
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_pass http://jms-uat;
    include https_proxy.conf;
    client_max_body_size 0;
}
```

##### 解释

- **`location /`**：
  - 这是一个通配符匹配的`location`块，表示所有路径的请求都会匹配到这个块，除非有其他更精确的匹配块。
- **`if ($request_uri !~ \.(html|htm|jpg|png|ico|js|css)$)`**：
  - 使用`if`指令对请求路径进行检查。仅在请求路径不匹配指定的静态资源文件扩展名（如`.html`, `.htm`, `.jpg`, `.png`, `.ico`, `.js`, `.css`）时，执行后续的Lua脚本。这种检查有助于将动态资源与静态资源区分开来。
- **`access_by_lua_file /opt/nginx/lua_script/rule.lua;`**：
  - 使用OpenResty的Lua模块，指定在访问控制阶段执行`/opt/nginx/lua_script/rule.lua`脚本。这个脚本通常用于实现限流、防火墙或其他动态访问控制逻辑。
- **`proxy_set_header Upgrade $http_upgrade;`**：
  - 设置`Upgrade`请求头，支持WebSocket等协议升级。`$http_upgrade`变量包含原始请求中的`Upgrade`头字段的值。
- **`proxy_set_header Connection "upgrade";`**：
  - 设置`Connection`请求头为`upgrade`，通常与`Upgrade`头一起使用，以确保连接升级。
- **`proxy_pass http://jms-uat;`**：
  - 将匹配到的请求代理到上游服务器`http://jms-uat`。
- **`include https_proxy.conf;`**：
  - 包含额外的配置文件`https_proxy.conf`，该文件可能包含HTTPS代理相关的其他配置项。
- **`client_max_body_size 0;`**：
  - 设置客户端请求体的最大大小为0，表示不限制请求体的大小。

这两个location块主要用于处理不同路径的请求，并在访问控制阶段使用Lua脚本进行相应的逻辑处理。精确匹配的/core/auth/login/路径专用于特定的认证或预处理，而通配符匹配的/路径则处理所有其他请求，并进行动态访问控制逻辑。两者共同确保了Nginx服务器的灵活性和安全性。

### Lua脚本 (rule.lua)

```lua
-- 连接池超时回收毫秒
local pool_max_idle_time = 10000
-- 连接池大小
local pool_size = 100
-- redis 连接超时时间
local redis_connection_timeout = 100
-- redis host
local redis_host = "192.168.102.20"
-- redis port
local redis_port = "6379"
-- redis auth
local redis_auth = "123456"
-- 封禁IP时间（秒）
local ip_block_time = 120
-- 指定ip访问频率时间段（秒）
local ip_time_out = 10
-- 指定ip访问频率计数最大值（次）
local ip_max_count = 60

-- 错误日志记录
local function errlog(msg, ex)
    ngx.log(ngx.ERR, msg, ex)
end

-- 释放连接池
local function close_redis(red)
    if not red then
        return
    end
    local ok, err = red:set_keepalive(pool_max_idle_time, pool_size)
    if not ok then
        ngx.say("redis connct err:", err)
        return red:close()
    end
end

-- 连接redis
local redis = require "resty.redis"
local client = redis:new()
local ok, err = client:connect(redis_host, redis_port)
-- 连接失败返回服务器错误
if not ok then
    return
end
-- 设置超时时间
client:set_timeout(redis_connection_timeout)

-- 优化验证密码操作
local connCount, err = client:get_reused_times()
-- 新建连接，需要认证密码
if 0 == connCount then
    local ok, err = client:auth(redis_auth)
    if not ok then
        errlog("failed to auth: ", err)
        return
    end
elseif err then
    errlog("failed to get reused times: ", err)
    return
end

-- 获取请求ip
local function getIp()
    local clientIP = ngx.req.get_headers()["X-Real-IP"]
    if clientIP == nil then
        clientIP = ngx.req.get_headers()["x_forwarded_for"]
    end
    if clientIP == nil then
        clientIP = ngx.var.remote_addr
    end
    return clientIP
end

local clientIp = getIp()

local incrKey = "limit:all:count:" .. clientIp
local blockKey = "limit:all:block:" .. clientIp

-- 查询ip是否被禁止访问，如果存在则返回403错误代码
local is_block, err = client:get(blockKey)
if tonumber(is_block) == 1 then
    ngx.exit(ngx.HTTP_FORBIDDEN)
    close_redis(client)
end

local ip_count, err = client:incr(incrKey)
if tonumber(ip_count) == 1 then
    client:expire(incrKey, ip_time_out)
end
-- 如果超过单位时间限制的访问次数，则添加限制访问标识，限制时间为ip_block_time
if tonumber(ip_count) > tonumber(ip_max_count) then
    client:set(blockKey, 1)
    client:expire(blockKey, ip_block_time)
end

close_redis(client)

```

![在这里插入图片描述](../../image/79250e60c11d4c738a46b454febd8749.png)
成功访问：
![在这里插入图片描述](../../image/c7c7e1444b6b453b8a303c75b307e977.png)


失败访问：
![在这里插入图片描述](../../image/ba971e9547374129996c3a0957f020b1.png)

参考文档：
https://www.cnblogs.com/KingArmy/p/18019489
https://blog.csdn.net/qq_45503196/article/details/134648292
