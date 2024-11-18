
# 背景
在日常工作中，我们经常需要创建Nginx配置文件的模板，以便在不同的环境中快速部署和配置Nginx服务器。然而，这样的任务通常需要重复性高、耗时长，且容易出错。为了加快这些任务的完成，并提高工作效率，可以使用一些自动化工具来简化Nginx配置文件的生成和管理。

其中，一种常见的方法是使用基于文本替换的模板引擎，如Jinja2、Mustache等，将Nginx配置文件中的变量替换为实际的值。例如，可以将配置文件中的端口号、域名、SSL证书路径等信息作为变量，在部署时再根据实际情况进行替换，从而快速生成满足需求的Nginx配置文件。此外，还可以使用版本控制工具（如Git）来对Nginx配置文件进行管理，并利用CI/CD工具（如Jenkins）自动构建和部署Nginx服务器。

通过自动化工具的使用，可以大大提高Nginx服务器的配置效率和准确性，并更好地适应不同环境下的需求。
# 1、需求
开发部门 不定期会更新新的项目上线，会用到域名绑定服务器 进行暴露。
##  流程

 1. 开发部门提出域名订单需求，包括需要绑定的域名和相应的服务器地址。   
 2. [运维部门在DNS管理控制面板中添加DNS解析记录，将需要绑定的域名解析到相应的服务器IP地址。](https://blog.csdn.net/heian_99/article/details/129682959)   
 3. 运维部门在Nginx配置中创建新的server块，配置要绑定的域名和相应的站点信息，例如文档根目录、日志文件、SSL证书等。   
 4. 运维部门将Nginx配置文件中的变量和实际的服务器地址进行替换，例如替换$server_name变量为实际要绑定的域名。   
 5. 运维部门重载或重新启动Nginx服务，使新的配置生效。 
 6. 最终，域名解析到相应的服务器地址，并由Nginx正确地将请求路由到相应的站点。
![在这里插入图片描述](https://img-blog.csdnimg.cn/a7b17f5b94b34c36a5a59113f68438c1.png)
# 2、kubernetes+ingress实战
## 1、转发kubernetes的ingress
**kubernetes-cluster.conf**
```bash
upstream kubernetes-cluster {
  server 192.168.82.42 weight=5;
  keepalive 16;
}
```

## 2、域名配置
**ogateway-uat.xxxx.net.conf**
```bash
server {
        listen       80;
        server_name   ogateway-uat.xxxx.net;
        rewrite ^/(.*)$ https://$host/$1 permanent;
        # IP白名单
        include /usr/local/openresty/nginx/whitelist/corporation.conf;
    
}
server {
        listen       443 ssl;
        server_name   ogateway-uat.xxxx.net;


        ssl                   on;
        ssl_certificate      /usr/local/openresty/nginx/ssl/xxx.net.crt;
        ssl_certificate_key  /usr/local/openresty/nginx/ssl/xxx.net.key;
        include ssl.conf;
        # IP白名单 放开时间0920-0930
        include /usr/local/openresty/nginx/whitelist/corporation.conf;
        location / {
            proxy_pass  http://kubernetes-cluster;
        include https_proxy.conf;
        }
}

```

# 3、反向代理

```bash
server {
        listen       80;
        server_name  customer-uat.xxxxx.com;
        # IP白名单
        include /usr/local/openresty/nginx/whitelist/corporation.conf;
        
        rewrite ^/(.*)$ https://$host/$1 permanent;
}
server {
        listen       443 ssl;
        server_name  customer-uat.xxxx.com;
        # IP白名单
        include /usr/local/openresty/nginx/whitelist/corporation.conf;

        ssl                   on;
        ssl_certificate      /usr/local/openresty/nginx/ssl/xxxx.com.crt;
        ssl_certificate_key  /usr/local/openresty/nginx/ssl/xxxxx.com.key;
        include ssl.conf;

        location / {
            proxy_pass  http://192.168.102.202;
            include proxy.conf;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-HTTPS on;
            add_header Front-End-Https on;
        }
}

```

# 4、负载轮询代理
```bash
upstream xxxx-backend-uat {
     #server 192.168.99.147:1201;
     server 192.168.82.42;
}
server {
    listen 80;
    server_name inhouse-xxxx-uat.xxxx.com;
    include /usr/local/openresty/nginx/whitelist/corporation.conf;

	location / {
        proxy_pass  http://xxxx-backend-uat;
        include http_proxy.conf;
    }
}
server {
    listen 443 ssl;
    server_name xxxx-backend-uat.xxxx.com;
    include /usr/local/openresty/nginx/whitelist/corporation.conf;

    ssl                   on;
    ssl_certificate      /usr/local/openresty/nginx/ssl/xxxx.com.crt;
    ssl_certificate_key  /usr/local/openresty/nginx/ssl/xxxx.com.key;
    include ssl.conf;

    location / {
        proxy_pass  http://xxxx-backend-uat;
        include http_proxy.conf;
    }
}
```

# 5、自动化处理
**add_nginx.sh**
```bash
#!/bin/bash

#日志级别 debug-1, info-2, warn-3, error-4, always-5
LOG_LEVEL=1

#日志名称
job_name=add_nginx

#脚本目录
script_dir=/opt

#日志文件
LOG_FILE=./${job_name}.log

#调试日志
function log_debug() {
	content="[DEBUG] $(date '+%Y-%m-%d %H:%M:%S') $@"
	[ $LOG_LEVEL -le 1 ] && echo $content >>$LOG_FILE && echo -e "\033[32m" ${content} "\033[0m"
}
#信息日志
function log_info() {
	content="[INFO] $(date '+%Y-%m-%d %H:%M:%S') $@"
	[ $LOG_LEVEL -le 2 ] && echo $content >>$LOG_FILE && echo -e "\033[32m" ${content} "\033[0m"
}
#警告日志
function log_warn() {
	content="[WARN] $(date '+%Y-%m-%d %H:%M:%S') $@"
	[ $LOG_LEVEL -le 3 ] && echo $content >>$LOG_FILE && echo -e "\033[33m" ${content} "\033[0m"
}
#错误日志
function log_err() {
	content="[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $@"
	[ $LOG_LEVEL -le 4 ] && echo $content >>$LOG_FILE && echo -e "\033[31m" ${content} "\033[0m"
}
#一直都会打印的日志
function log_always() {
	content="[ALWAYS] $(date '+%Y-%m-%d %H:%M:%S') $@"
	[ $LOG_LEVEL -le 5 ] && echo $content >>$LOG_FILE && echo -e "\033[32m" ${content} "\033[0m"
}

function get_Whitelist() {
	# 提示用户输入选项
	echo "1. 使用白名单"
	echo "2. 不使用白名单"

	# 获取用户输入
	read -p "请选择要使用白名单配置：" choice_whitelist

	# 使用case语句根据用户选择设置变量
	case $choice_whitelist in
	1)
		use_whitelist=true
		;;
	2)
		use_whitelist=false
		;;
	*)
		echo "错误：请输入正确的选项" >&2
		exit 1
		;;
	esac

}

function set_whitelist() {
  if [ "$use_whitelist" = true ]; then
    log_info "已经设置IP白名单"
    sed -i -r 's/^(\s*)#(.*include\s*\/usr\/local\/openresty\/nginx\/whitelist\/corporation\.conf;.*)$/\1\2/g' "$conf_file"
  else
    log_info "不使用IP白名单"
  fi
}

function check_nginx() {
	conf_file="/chen/company_shell/$realm_name.conf"
	# 检查Nginx配置文件
	if nginx -t >/dev/null 2>&1; then
		echo "Nginx configuration test passed."
	else
		echo "Nginx configuration test failed. Please check your configuration file."
		exit 1
	fi
}

function kubernetes_nginx() {
	re_301='rewrite ^/(.*)$ https://$host/$1 permanent;'
	tld=$(echo "$realm_name" | sed -E 's/.*\.([^.]+\.[^.]+)$/\1/')
	cat >$realm_name.conf <<EOF
server {
        listen       80;
        server_name  $realm_name;
	# IP白名单
        #include /usr/local/openresty/nginx/whitelist/corporation.conf;
        $re_301
}
server {
        listen       443 ssl;
        server_name  $realm_name;
        ssl                   on;
        ssl_certificate      /usr/local/openresty/nginx/ssl/$tld.crt;
        ssl_certificate_key  /usr/local/openresty/nginx/ssl/$tld.key;
        include ssl.conf;
	# IP白名单
        #include /usr/local/openresty/nginx/whitelist/corporation.conf;

        location / {
           proxy_pass  http://kubernetes-cluster;
           include https_proxy.conf;
        }
}
EOF
}

function proxy_nginx() {
	read -p "设置反向代理（列如：http://172.18.199.115）：" proxy_ip
	re_301='rewrite ^/(.*)$ https://$host/$1 permanent;'
	tld=$(echo "$realm_name" | sed -E 's/.*\.([^.]+\.[^.]+)$/\1/')
	cat >$realm_name.conf <<EOF
server {
        listen       80;
        server_name  $realm_name;
	    $re_301
	
	# IP白名单
        #include /usr/local/openresty/nginx/whitelist/corporation.conf;
}
server {
        listen       443 ssl;
        server_name  $realm_name;

	# IP白名单
        #include /usr/local/openresty/nginx/whitelist/corporation.conf;

        ssl                   on;
        ssl_certificate      /usr/local/openresty/nginx/ssl/$tld.crt;
        ssl_certificate_key  /usr/local/openresty/nginx/ssl/$tld.key;
        include ssl.conf;

        location / {
        	proxy_pass  $proxy_ip;
		include https_proxy.conf;
        }
}
EOF
}

function upstream_nginx() {
	pass
}

# 定义函数：生产域名
function set_kubernetes_nginx() {
	# TODO: 在这里实现生产域名的操作
	log_info "开始配置nginx模板"
	read -p "请输您的域名:  " realm_name
	log_info "域名记录： $realm_name"
	get_Whitelist
	kubernetes_nginx
	# 输出变量值
	set_whitelist
	#配置文件校检
	check_nginx
}

function set_reverse_proxy_nginx() {
	# TODO: 在这里实现生产域名的操作
	log_info "开始配置nginx模板"
	read -p "请输您的域名:  " realm_name
	log_info "域名记录： $realm_name"
	get_Whitelist
	proxy_nginx
	# 输出变量值
	set_whitelist
	#配置文件校检
	check_nginx
}

function set_upstream_proxy_nginx() {
	# TODO: 在这里实现生产域名的操作
	log_info "开始配置nginx模板"
	read -p "请输您的域名:  " realm_name
	log_info "域名记录： $realm_name"
	get_Whitelist
	upstream_nginx
	# 输出变量值
	set_whitelist
	#配置文件校检
	check_nginx
}

# 定义主函数
function main() {
	# 显示菜单
	echo "请选择一个选项："
	echo "1. kubernetes接入"
	echo "2. 反向代理接入"
	echo "3. 负载均衡接入"

	# 读取用户输入
	read -p "请输您的选择:  " choice

	# 根据用户输入选择对应的操作
	case $choice in
	1) set_kubernetes_nginx ;;
	2) set_reverse_proxy_nginx ;;
	3) set_upstream_proxy_nginx ;;
	*) echo "无效的选项，请重新输入" ;;
	esac

}

# 调用主函数
main

```
![在这里插入图片描述](https://img-blog.csdnimg.cn/4133ca74f16e49aea444f688035065a2.png)

