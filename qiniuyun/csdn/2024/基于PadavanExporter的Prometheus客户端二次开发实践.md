---
author: 南宫乘风
categories:
- Prometheus监控
date: 2024-07-09 10:24:28
description: 、简介在现代的微服务架构中，对系统的实时监控变得尤为重要。作为一款开源的系统监控与报警工具，以其强大的数据模型和灵活的查询语言，成为了监控领域的佼佼者。然而，对于特定的硬件设备，如基于固件的路由器，直。。。。。。。
image: ../../title_pic/27.jpg
slug: '202407091024'
tags:
- prometheus
title: 基于Padavan Exporter的Prometheus客户端二次开发实践
---

<!--more-->

## 1、简介
在现代的微服务架构中，对系统的实时监控变得尤为重要。Prometheus作为一款开源的系统监控与报警工具，以其强大的数据模型和灵活的查询语言，成为了监控领域的佼佼者。然而，对于特定的硬件设备，如基于Padavan固件的路由器，直接集成Prometheus可能并非易事。因此，开发一个针对Padavan设备的Prometheus exporter，能够极大地简化监控集成过程，提升运维效率。

本文将以[padavan_exporter](https://github.com/Bpazy/padavan_exporter)项目为例，探讨如何基于此项目进行二次开发，以适应更广泛的监控需求。我们将深入分析代码结构，了解其工作原理，并探索如何扩展其功能。
项目地址：[https://github.com/Bpazy/padavan_exporter](https://github.com/Bpazy/padavan_exporter)
![在这里插入图片描述](../../image/2f734ca98f5f43f1b0b6551ea57535f6.png)

## 2、项目背景
padavan_exporter是一个专门为基于Padavan固件的路由器设计的Prometheus exporter。它通过SSH连接至路由器，收集包括CPU使用率、内存状态、网络接口状态、网络连接统计在内的关键指标，然后以Prometheus兼容的格式暴露这些指标，供Prometheus服务器抓取。

## 3、环境介绍
在开始之前，我们需要确保开发环境的正确配置。以下是开发此项目所需的环境和工具：

- Go 语言：Padavan Exporter 是用 Go 语言编写的，因此我们需要安装 Go 语言环境。
- Prometheus：用于采集和存储来自 Exporter 的指标数据。
- Grafana：用于可视化 Prometheus 存储的数据（可选，但推荐）。
- Padavan 固件设备：实际运行的 Padavan 固件设备，用于测试和验证。

## 4、设计思路

项目主要包括以下几个部分：

1. **命令行参数解析**：使用 `kingpin` 库解析命令行参数，获取 SSH 连接信息和 Web 服务监听地址。
2. **SSH 客户端初始化**：使用 `golang.org/x/crypto/ssh` 库建立 SSH 连接，获取 Padavan 设备的性能数据。
3. **Prometheus 收集器**：实现 Prometheus 收集器，用于从 SSH 客户端获取数据并提供给 Prometheus 服务器。
4. **HTTP 服务器**：启动一个 HTTP 服务器，提供 `/metrics` 接口供 Prometheus 服务器抓取数据。


## 5、main.go
![在这里插入图片描述](../../image/6a9036089a4c4ef08cd98893abaafb59.png)

### 1. 命令行参数解析

在 `init` 函数中，使用 `kingpin` 库解析命令行参数。定义了四个命令行参数：

- `web.listen-address`：监听的 HTTP 服务地址，默认为 `:9100`。
- `padavan.ssh.host`：Padavan 设备的 SSH 主机地址，默认为 `127.0.0.1:22`。
- `padavan.ssh.username`：SSH 登录的用户名，默认为 `admin`。
- `padavan.ssh.password`：SSH 登录的密码，默认为 `admin`。
- `debug`：是否开启调试模式。

通过解析这些参数，设置日志级别为 `Debug`，并输出解析后的参数值。

```go
func init() {
    // 定义命令行参数
    la = kingpin.Flag("web.listen-address", "Address on which to expose metrics and web interface").Default(":9100").String()
    ph = kingpin.Flag("padavan.ssh.host", "Padavan ssh host").Default("127.0.0.1:22").String()
    pu = kingpin.Flag("padavan.ssh.username", "Padavan ssh username").Default("admin").String()
    pp = kingpin.Flag("padavan.ssh.password", "Padavan ssh password").Default("admin").String()
    isDebug := kingpin.Flag("debug", "Debug mode").Bool()
    kingpin.Parse()

    if *isDebug {
        log.SetLevel(log.DebugLevel)
    }

    log.Debugf("web.listen-address(%s) padavan.ssh.host(%s) padavan.ssh.username(%s) padavan.ssh.password(%s)", *la, *ph, *pu, *pp)
}

```
### 2. 初始化 SSH 客户端

`initSshClient` 函数用于创建和返回一个 SSH 客户端。该客户端用于与 Padavan 设备进行 SSH 连接，以收集监控数据。

```go
func initSshClient() *ssh.Client {
    sshConfig := ssh.ClientConfig{
        User:            *pu,
        Auth:            []ssh.AuthMethod{ssh.Password(*pp)},
        Timeout:         5 * time.Second,
        HostKeyCallback: ssh.InsecureIgnoreHostKey(),
    }
    log.Printf("Connecting to %s", *ph)
    sshClient, err := ssh.Dial("tcp", *ph, &sshConfig)
    if err != nil {
        log.Fatalf("create ssh client failed: %+v", err)
    }
    return sshClient
}

```

### 3. 初始化 Prometheus 注册表和收集器

在 `main` 函数中，初始化 Prometheus 注册表（`pedantic registry`）和 SSH 客户端。然后注册各种收集器到 Prometheus 注册表。这些收集器将从 Padavan 设备获取不同类型的性能数据。

```go
func main() {
    reg := prometheus.NewPedanticRegistry()
    sc := initSshClient()
    reg.MustRegister(collector.NewLoadAverageCollector(sc))
    reg.MustRegister(collector.NewNetDevController(sc))
    reg.MustRegister(collector.NewCpuCollector(sc))
    reg.MustRegister(collector.NewMemoryCollector(sc))
    reg.MustRegister(collector.NewNetconnCollector(sc))

    gatherers := prometheus.Gatherers{reg}
    h := promhttp.HandlerFor(gatherers, promhttp.HandlerOpts{
        ErrorLog:      log.StandardLogger(),
        ErrorHandling: promhttp.ContinueOnError,
    })
    http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
        h.ServeHTTP(w, r)
    })
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        _, _ = fmt.Fprintln(w, homePage())
    })

    log.Printf("Start server at %s", *la)
    log.Fatal(http.ListenAndServe(*la, nil))
}

```
### 4. 启动 HTTP 服务器

在 `main` 函数中，启动一个 HTTP 服务器，提供 `/metrics` 接口供 Prometheus 服务器抓取数据。同时提供一个简单的首页，通过 `/` 路径访问，显示一些基本信息和有用的链接。

```go
func homePage() string {
    return `
<html>
 <head> 
  <title>padavan_exporter</title> 
 </head> 
 <body> 
  <h2>padavan_exporter</h2> 
  <span>See docs at <a href="https://github.com/Bpazy/padavan_exporter">https://github.com/Bpazy/padavan_exporter</a></span>  
  <br>
  <br>
  <span> Useful endpoints: </span>
  <br>
  <span> <a href="/metrics">metrics</a> <span> - available service metrics </span>
 </body>
</html>`
}

```


### 5、整体代码

```go

import (
	"fmt"
	"github.com/Bpazy/padavan_exporter/collector"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	log "github.com/sirupsen/logrus"
	"golang.org/x/crypto/ssh"
	"gopkg.in/alecthomas/kingpin.v2"
	"net/http"
	"time"
)

var (
	ph *string // Padavan address
	pu *string // Padavan username
	pp *string // Padavan password
	la *string // Address on which to expose metrics and web interface
)

// init 函数用于初始化命令行参数。
// 通过 kingpin 解析命令行参数，包括 web 服务监听地址、Padavan SSH 主机地址、用户名、密码等。
// 并根据是否开启 debug 模式设置日志级别。
func init() {
	// 定义命令行参数
	la = kingpin.Flag("web.listen-address", "Address on which to expose metrics and web interface").Default(":9100").String()
	ph = kingpin.Flag("padavan.ssh.host", "Padavan ssh host").Default("127.0.0.1:22").String()
	pu = kingpin.Flag("padavan.ssh.username", "Padavan ssh username").Default("admin").String()
	pp = kingpin.Flag("padavan.ssh.password", "Padavan ssh password").Default("admin").String()
	// 解析命令行参数，并在 debug 模式下设置日志级别
	isDebug := kingpin.Flag("debug", "Debug mode").Bool()
	kingpin.Parse()

	if *isDebug {
		log.SetLevel(log.DebugLevel)
	}

	log.Debugf("web.listen-address(%s) padavan.ssh.host(%s) padavan.ssh.username(%s) padavan.ssh.password(%s)", *la, *ph, *pu, *pp)
}

// main 函数作为程序入口点，负责初始化 Prometheus 监控数据收集器、SSH 客户端，并启动 HTTP 服务提供监控数据。
func main() {
	// 初始化 Prometheus 注册表和 SSH 客户端
	reg := prometheus.NewPedanticRegistry()
	sc := initSshClient()
	// 注册各种收集器到 Prometheus
	reg.MustRegister(collector.NewLoadAverageCollector(sc))
	reg.MustRegister(collector.NewNetDevController(sc))
	reg.MustRegister(collector.NewCpuCollector(sc))
	reg.MustRegister(collector.NewMemoryCollector(sc))
	reg.MustRegister(collector.NewNetconnCollector(sc))

	gatherers := prometheus.Gatherers{reg}
	h := promhttp.HandlerFor(gatherers, promhttp.HandlerOpts{
		ErrorLog:      log.StandardLogger(),
		ErrorHandling: promhttp.ContinueOnError,
	})
	// 处理 /metrics 请求以提供监控数据
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		h.ServeHTTP(w, r)
	})
	// 处理根路径请求，提供简单信息页面
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		_, _ = fmt.Fprintln(w, homePage())
	})

	log.Printf("Start server at %s", *la)
	// 启动 HTTP 服务
	log.Fatal(http.ListenAndServe(*la, nil))
}

func homePage() string {
	return `
<html>
 <head> 
  <title>padavan_exporter</title> 
 </head> 
 <body> 
  <h2>padavan_exporter</h2> 
  <span>See docs at <a href="https://github.com/Bpazy/padavan_exporter">https://github.com/Bpazy/padavan_exporter</a></span>  
  <br>
  <br>
  <span> Useful endpoints: </span>
  <br>
  <span> <a href="/metrics">metrics</a> <span> - available service metrics </span>
 </body>
</html>`
}

// initSshClient 函数用于初始化并返回一个 SSH 客户端。
// 该客户端用于与 Padavan 设备进行 SSH 连接以收集监控数据。
func initSshClient() *ssh.Client {
	// 创建 SSH 客户端配置，包括用户名、密码和一些连接选项
	sshConfig := ssh.ClientConfig{
		User:            *pu,
		Auth:            []ssh.AuthMethod{ssh.Password(*pp)},
		Timeout:         5 * time.Second,
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}
	log.Printf("Connecting to %s", *ph)
	// 尝试建立 SSH 连接
	sshClient, err := ssh.Dial("tcp", *ph, &sshConfig)
	if err != nil {
		log.Fatalf("create ssh client failed: %+v", err)
	}
	return sshClient
}

```

## 6、collector.go

### 1、整体思路

1. **建立 SSH 会话并执行命令**：通过 SSH 客户端连接到远程设备并执行命令，获取命令的输出结果。
2. **获取文件内容**：通过执行 `cat` 命令获取远程设备上指定文件的内容。
3. **解析浮点数**：将字符串形式的数字解析为浮点数。

### 2、功能解释

1. **import 部分**

   ```go
   import (
       "fmt"
       log "github.com/sirupsen/logrus"
       "golang.org/x/crypto/ssh"
       "strconv"
   )
   ```

   这部分代码导入了所需的包。`fmt` 用于格式化输出，`log` 用于日志记录，`ssh` 用于 SSH 连接，`strconv` 用于字符串和数值之间的转换。

2. **mustGetContent 函数**

   ```go
   func mustGetContent(sshClient *ssh.Client, path string) string {
       rsp, err := execCommand(sshClient, "cat "+path)
       if err != nil {
           panic(err)
       }
       return rsp
   }
   ```

   这个函数接受一个 SSH 客户端和一个文件路径，通过调用 `execCommand` 函数执行 `cat` 命令获取文件内容。如果执行命令失败，会引发 panic。成功执行后，返回文件内容作为字符串。

3. **execCommand 函数**

   ```go
   func execCommand(sshClient *ssh.Client, command string) (string, error) {
       session, err := sshClient.NewSession()
       if err != nil {
           return "", fmt.Errorf("create ssh session failed: %+v", err)
       }
       defer session.Close()
   
       rsp, err := session.CombinedOutput(command)
       if err != nil {
           return "", fmt.Errorf("execute ssh command failed: %+v", err)
       }
       return string(rsp), nil
   }
   ```

   这个函数接受一个 SSH 客户端和一个命令，创建一个新的 SSH 会话并执行命令，获取命令的输出结果。如果创建会话或执行命令失败，返回相应的错误信息。成功执行后，返回命令输出结果作为字符串。

4. **mustParseFloat 函数**

   ```go
   func mustParseFloat(fs string) float64 {
       float, err := strconv.ParseFloat(fs, 32)
       if err != nil {
           log.Printf("%+v", err)
           return 0
       }
       return float
   }
   ```

   这个函数接受一个字符串，尝试将其解析为浮点数。如果解析失败，记录错误信息并返回 0。成功解析后，返回浮点数。

### 3、整体代码
```go
import (
	"fmt"
	log "github.com/sirupsen/logrus"
	"golang.org/x/crypto/ssh"
	"strconv"
)

// mustGetContent 从指定路径读取文件内容
func mustGetContent(sshClient *ssh.Client, path string) string {
	// 执行SSH命令读取文件内容
	rsp, err := execCommand(sshClient, "cat "+path)
	if err != nil {
		// 如果发生错误，panic
		panic(err)
	}
	// 返回文件内容
	return rsp
}

// execCommand 执行SSH命令并返回结果
func execCommand(sshClient *ssh.Client, command string) (string, error) {
	// 创建一个新的SSH会话
	session, err := sshClient.NewSession()
	if err != nil {
		// 如果创建会话失败，返回错误
		return "", fmt.Errorf("create ssh session failed: %+v", err)
	}
	// 确保会话在函数结束时关闭
	defer session.Close()

	// 执行命令并获取结果
	rsp, err := session.CombinedOutput(command)
	if err != nil {
		// 如果执行命令失败，返回错误
		return "", fmt.Errorf("execute ssh command failed: %+v", err)
	}
	// 返回命令执行结果
	return string(rsp), nil
}

// mustParseFloat 解析字符串为浮点数
func mustParseFloat(fs string) float64 {
	// 尝试解析字符串为浮点数
	float, err := strconv.ParseFloat(fs, 32)
	if err != nil {
		// 如果解析失败，记录错误并返回0
		log.Printf("%+v", err)
		return 0
	}
	// 返回解析后的浮点数
	return float
}

```

## 7、memory.go
### 1、整体思路

这个代码片段的目的是通过 Prometheus 采集远程设备的内存指标。通过 SSH 连接远程设备，读取 `/proc/meminfo` 文件的内容，然后解析出相关的内存信息，最后将这些信息作为 Prometheus 指标发送。

### 2、功能解释

1. **正则表达式**

   ```go
   var (
       meminfoReg = regexp.MustCompile(`(\w+):\s+(\d+) kB`)
   )
   ```

   这个正则表达式用于匹配 `/proc/meminfo` 文件中的每一行，捕获内存指标的名称和数值。

2. **memoryCollector 结构体**

   ```go
   type memoryCollector struct {
       metrics map[string]*prometheus.Desc // 存储指标描述信息
       sc      *ssh.Client                 // SSH客户端，用于远程收集指标信息
   }
   ```

   `memoryCollector` 结构体包含两个字段：一个用于存储 Prometheus 指标描述信息的字典 `metrics`，另一个是 SSH 客户端 `sc`，用于连接远程设备。

3. **Describe 方法**

   ```go
   func (m *memoryCollector) Describe(ch chan<- *prometheus.Desc) {
       // metrics created when Collect
   }
   ```

   这个方法是 Prometheus 采集器接口的一部分，用于描述指标。但在这个实现中，指标是在 `Collect` 方法中动态创建的，所以这里没有具体实现。

4. **Collect 方法**

   ```go
   func (m *memoryCollector) Collect(ch chan<- prometheus.Metric) {
       // 通过SSH客户端获取远程机器的/proc/meminfo文件内容
       content := mustGetContent(m.sc, "/proc/meminfo")
       // 创建Scanner用于逐行读取内容
       scanner := bufio.NewScanner(strings.NewReader(content))
       // 使用正则表达式匹配行内容，获取指标名和值
       for scanner.Scan() {
           parts := meminfoReg.FindStringSubmatch(scanner.Text())
   
           if len(parts) != 3 {
               // 如果匹配不成功，则跳过当前行
               continue
           }
           // 指标名
           key := parts[1]
           // 解析指标值
           value, err := strconv.ParseFloat(parts[2], 64)
           if err != nil {
               continue
               // 如果解析失败，则跳过当前行
           }
           value *= 1024 // 将值从kB转换为B
   
           var desc *prometheus.Desc
           var ok bool
           // 根据指标名，获取或创建对应的Desc对象
           switch key {
           case "MemTotal":
               desc, ok = m.metrics["MemTotal"]
               if !ok {
                   desc = prometheus.NewDesc("node_memory_total_bytes", "Total memory in bytes.", nil, nil)
                   m.metrics["MemTotal"] = desc
               }
           case "MemFree":
               desc, ok = m.metrics["MemFree"]
               if !ok {
                   desc = prometheus.NewDesc("node_memory_free_bytes", "Free memory in bytes.", nil, nil)
                   m.metrics["MemFree"] = desc
               }
           case "Buffers":
               desc, ok = m.metrics["Buffers"]
               if !ok {
                   desc = prometheus.NewDesc("node_memory_buffers_bytes", "Buffers memory in bytes.", nil, nil)
                   m.metrics["Buffers"] = desc
               }
           case "Cached":
               desc, ok = m.metrics["Cached"]
               if (!ok) {
                   desc = prometheus.NewDesc("node_memory_cached_bytes", "Cached memory in bytes.", nil, nil)
                   m.metrics["Cached"] = desc
               }
           default:
               continue // 如果不是我们关心的指标，则跳过当前行
           }
           // 向通道发送指标
           ch <- prometheus.MustNewConstMetric(desc, prometheus.GaugeValue, value)
       }
   }
   ```

   这个方法是 Prometheus 采集器接口的另一部分，用于收集指标数据并向 Prometheus 发送。具体步骤如下：

   - 通过 `mustGetContent` 函数获取远程设备上 `/proc/meminfo` 文件的内容。
   - 使用 `bufio.Scanner` 逐行读取文件内容。
   - 使用正则表达式匹配每一行，提取内存指标名称和值。
   - 根据指标名称创建或获取对应的 `prometheus.Desc` 对象。
   - 将解析后的指标值乘以 1024，从 kB 转换为字节。
   - 使用 `prometheus.MustNewConstMetric` 函数创建 Prometheus 指标并发送到通道 `ch`。

5. **NewMemoryCollector 函数**

   ```go
   func NewMemoryCollector(sc *ssh.Client) *memoryCollector {
       return &memoryCollector{
           sc:      sc,
           metrics: map[string]*prometheus.Desc{},
       }
   }
   ```

   这个函数用于创建一个新的 `memoryCollector` 实例，初始化 SSH 客户端和指标描述信息的字典。

### 3、整体流程

1. **初始化**：通过 `NewMemoryCollector` 函数创建一个 `memoryCollector` 实例，传入 SSH 客户端。

2. 收集指标：
   - `Collect` 方法通过 SSH 客户端获取远程设备上的 `/proc/meminfo` 文件内容。
   - 使用正则表达式解析文件内容，提取内存指标。
   - 将解析后的指标转换为 Prometheus 格式并发送到通道 `ch`。

3. **描述指标**：`Describe` 方法用于向 Prometheus 描述指标，但具体实现中是在 `Collect` 方法中动态创建指标。

### 4、整体代码

```go
package collector

import (
	"bufio"
	"github.com/prometheus/client_golang/prometheus"
	"golang.org/x/crypto/ssh"
	"regexp"
	"strconv"
	"strings"
)

/**
 * @Author: 南宫乘风
 * @Description:
 * @File:  memory.go
 * @Email: 1794748404@qq.com
 * @Date: 2024-05-22 15:05
 */

var (
	meminfoReg = regexp.MustCompile(`(\w+):\s+(\d+) kB`)
)

// memoryCollector 收集内存相关指标信息
type memoryCollector struct {
	metrics map[string]*prometheus.Desc // 存储指标描述信息
	sc      *ssh.Client                 // SSH客户端，用于远程收集指标信息
}

// Describe 向通道发送描述指标的Desc对象
// 这个方法不具体实现，因为metrics在Collect方法中动态创建。
func (m *memoryCollector) Describe(ch chan<- *prometheus.Desc) {
	// metrics created when Collect
}

// Collect 向通道发送内存指标数据
// @param ch 用于发送指标的通道
func (m *memoryCollector) Collect(ch chan<- prometheus.Metric) {
	// 通过SSH客户端获取远程机器的/proc/meminfo文件内容
	content := mustGetContent(m.sc, "/proc/meminfo")
	// 创建Scanner用于逐行读取内容
	scanner := bufio.NewScanner(strings.NewReader(content))
	// 使用正则表达式匹配行内容，获取指标名和值
	for scanner.Scan() {
		parts := meminfoReg.FindStringSubmatch(scanner.Text())

		if len(parts) != 3 {
			// 如果匹配不成功，则跳过当前行
			continue
		}
		// 指标名
		key := parts[1]
		// 解析指标值
		value, err := strconv.ParseFloat(parts[2], 64)
		if err != nil {
			continue
			// 如果解析失败，则跳过当前行
		}
		value *= 1024 // 将值从kB转换为B

		var desc *prometheus.Desc
		var ok bool
		// 根据指标名，获取或创建对应的Desc对象
		switch key {
		case "MemTotal":
			desc, ok = m.metrics["MemTotal"]
			if !ok {
				desc = prometheus.NewDesc("node_memory_total_bytes", "Total memory in bytes.", nil, nil)
				m.metrics["MemTotal"] = desc
			}
		case "MemFree":
			desc, ok = m.metrics["MemFree"]
			if !ok {
				desc = prometheus.NewDesc("node_memory_free_bytes", "Free memory in bytes.", nil, nil)
				m.metrics["MemFree"] = desc
			}
		case "Buffers":
			desc, ok = m.metrics["Buffers"]
			if !ok {
				desc = prometheus.NewDesc("node_memory_buffers_bytes", "Buffers memory in bytes.", nil, nil)
				m.metrics["Buffers"] = desc
			}
		case "Cached":
			desc, ok = m.metrics["Cached"]
			if !ok {
				desc = prometheus.NewDesc("node_memory_cached_bytes", "Cached memory in bytes.", nil, nil)
				m.metrics["Cached"] = desc
			}
		default:
			continue // 如果不是我们关心的指标，则跳过当前行
		}
		// 向通道发送指标
		ch <- prometheus.MustNewConstMetric(desc, prometheus.GaugeValue, value)
	}
}

// NewMemoryCollector 创建一个新的memoryCollector实例
// @param sc SSH客户端
// @return 返回memoryCollector实例的指针
func NewMemoryCollector(sc *ssh.Client) *memoryCollector {
	return &memoryCollector{
		sc:      sc,
		metrics: map[string]*prometheus.Desc{},
	}
}

```

## 8、调用 NewMemoryCollector 的原理

`NewMemoryCollector` 函数用于创建一个新的 `memoryCollector` 实例。这个实例负责从 Padavan 设备中收集内存相关的指标信息。调用 `NewMemoryCollector` 的过程和原理如下：

### 1、`NewMemoryCollector` 函数的定义

`NewMemoryCollector` 函数接收一个 `*ssh.Client` 作为参数并返回一个 `*memoryCollector` 实例。

```go
func NewMemoryCollector(sc *ssh.Client) *memoryCollector {
    return &memoryCollector{
        sc:      sc,
        metrics: map[string]*prometheus.Desc{},
    }
}
```

### 2、`memoryCollector` 的定义

`memoryCollector` 结构体包含两个字段：

- `metrics`：一个 `map[string]*prometheus.Desc`，用于存储指标的描述信息。
- `sc`：一个 `*ssh.Client`，用于通过 SSH 连接到 Padavan 设备以收集监控数据。

```go
type memoryCollector struct {
    metrics map[string]*prometheus.Desc // 存储指标描述信息
    sc      *ssh.Client                 // SSH客户端，用于远程收集指标信息
}
```

### 3、在 `main` 函数中调用 `NewMemoryCollector`

在 `main` 函数中，首先初始化 Prometheus 注册表和 SSH 客户端，然后调用 `NewMemoryCollector` 函数创建一个 `memoryCollector` 实例，并将其注册到 Prometheus 注册表中。

```go
 reg.MustRegister(collector.NewMemoryCollector(sc))
```

###  4、`memoryCollector` 的工作原理

1. **初始化 SSH 客户端**： `initSshClient` 函数创建一个 SSH 客户端，用于连接到 Padavan 设备。
2. **创建 `memoryCollector` 实例**： 调用 `NewMemoryCollector(sc)`，传入 SSH 客户端，返回一个 `memoryCollector` 实例。
3. **注册收集器**： 使用 `reg.MustRegister(collector.NewMemoryCollector(sc))` 将 `memoryCollector` 注册到 Prometheus 注册表中。这样 Prometheus 就可以通过 `/metrics` 接口调用 `memoryCollector` 的 `Collect` 方法收集内存指标数据。
4. **收集指标数据**： `memoryCollector` 的 `Collect` 方法通过 SSH 客户端连接到 Padavan 设备，读取 `/proc/meminfo` 文件，解析文件内容并生成 Prometheus 指标，然后将指标发送到通道中供 Prometheus 收集。

```go
func (m *memoryCollector) Collect(ch chan<- prometheus.Metric) {
    // 通过SSH客户端获取远程机器的/proc/meminfo文件内容
    content := mustGetContent(m.sc, "/proc/meminfo")
    // 创建Scanner用于逐行读取内容
    scanner := bufio.NewScanner(strings.NewReader(content))
    // 使用正则表达式匹配行内容，获取指标名和值
    for scanner.Scan() {
        parts := meminfoReg.FindStringSubmatch(scanner.Text())

        if len(parts) != 3 {
            // 如果匹配不成功，则跳过当前行
            continue
        }
        // 指标名
        key := parts[1]
        // 解析指标值
        value, err := strconv.ParseFloat(parts[2], 64)
        if err != nil {
            continue
            // 如果解析失败，则跳过当前行
        }
        value *= 1024 // 将值从kB转换为B

        var desc *prometheus.Desc
        var ok bool
        // 根据指标名，获取或创建对应的Desc对象
        switch key {
        case "MemTotal":
            desc, ok = m.metrics["MemTotal"]
            if !ok {
                desc = prometheus.NewDesc("node_memory_total_bytes", "Total memory in bytes.", nil, nil)
                m.metrics["MemTotal"] = desc
            }
        case "MemFree":
            desc, ok = m.metrics["MemFree"]
            if (!ok) {
                desc = prometheus.NewDesc("node_memory_free_bytes", "Free memory in bytes.", nil, nil)
                m.metrics["MemFree"] = desc
            }
        case "Buffers":
            desc, ok = m.metrics["Buffers"]
            if (!ok) {
                desc = prometheus.NewDesc("node_memory_buffers_bytes", "Buffers memory in bytes.", nil, nil)
                m.metrics["Buffers"] = desc
            }
        case "Cached":
            desc, ok = m.metrics["Cached"]
            if (!ok) {
                desc = prometheus.NewDesc("node_memory_cached_bytes", "Cached memory in bytes.", nil, nil)
                m.metrics["Cached"] = desc
            }
        default:
            continue // 如果不是我们关心的指标，则跳过当前行
        }
        // 向通道发送指标
        ch <- prometheus.MustNewConstMetric(desc, prometheus.GaugeValue, value)
    }
}

```
![在这里插入图片描述](../../image/d278ebda91ac470ebd45e7b074f418c0.png)

