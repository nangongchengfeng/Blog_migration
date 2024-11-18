---
author: 南宫乘风
categories:
- Go语言
date: 2021-12-30 16:43:23
description: 是一个的微框架，封装比较优雅，友好，源码注释比较明确，已经发布了版本。具有快速灵活，容错方便等特点。其实对于而言，框架的依赖要远比，之类的要小。自身的足够简单，性能也非常不错。框架更像是一些常用函数或。。。。。。。
image: http://image.ownit.top/4kdongman/31.jpg
tags:
- golang
- 开发语言
- 后端
title: Gin框架组合（Zap、lumberjack、ini）使用手册
---

<!--more-->

## Gin

Gin是一个golang的微框架，封装比较优雅，API友好，源码注释比较明确，已经发布了1.0版本。具有快速灵活，容错方便等特点。其实对于golang而言，web框架的依赖要远比Python，Java之类的要小。自身的net/http足够简单，性能也非常不错。框架更像是一些常用函数或者工具的集合。借助框架开发，不仅可以省去很多常用的封装带来的时间，也有助于团队的编码风格和形成规范。

下面就Gin的用法做一个简单的介绍。

首先需要安装，安装比较简单，使用go get即可：

```Go
go get gopkg.in/gin-gonic/gin.v1
```

```Go
import (
    "gopkg.in/gin-gonic/gin.v1"
    "net/http"
)

func main(){
    
    router := gin.Default()

    router.GET("/", func(c *gin.Context) {
        c.String(http.StatusOK, "Hello World")
    })
    router.Run(":8000")
}
```

日常我们是使用Gin框架编写接口等等，可能会使用到一下几种组件。

**Zap 日志记录**

**lumberjack 日志切割**

**ini 配置文件读取**

## ini配置读取

下载

```Go
go get github.com/go-ini/ini
```

因为项目中要是到配置文件，我们可以采用ini模块来实现

首先，创建一个`config.ini`配置文件：

![](http://image.ownit.top/csdn/e7a104fe1c93453b82ba53147f721889.png)

```Go
port = 9000
release = false

[mysql]
user = db1
password = db1
host = 10.10.10.6
port = 3306
db = db1

[log]
level = debug
filename = ./logs/info.log
maxsize = 1
max_age = 30
max_backups = 5
```

```Go
package setting

import (
	"gopkg.in/ini.v1"
)

var Conf = new(AppConfig)

// AppConfig 应用程序配置
type AppConfig struct {
	Release      bool `ini:"release"`
	Port         int  `ini:"port"`
	*MySQLConfig `ini:"mysql"`
	*LogConfig   `ini:"log"`
}

// MySQLConfig 数据库配置
type MySQLConfig struct {
	User     string `ini:"user"`
	Password string `ini:"password"`
	DB       string `ini:"db"`
	Host     string `ini:"host"`
	Port     int    `ini:"port"`
}

type LogConfig struct {
	Level      string `ini:"level"`
	Filename   string `ini:"filename"`
	MaxSize    int    `ini:"maxsize"`
	MaxAge     int    `ini:"max_age"`
	MaxBackups int    `ini:"max_backups"`
}

//把先关初始的参数加载到全局变量，然后方便调用
func Init(file string) error {
	return ini.MapTo(Conf, file)
}
```

看一下调用方式

```Go
	// 传入配置文件路径，加载配置文件,
	if err := setting.Init("conf/config.ini"); err != nil {
		fmt.Printf("load config from file failed, err:%v\n", err)
		return
	}
	fmt.Println("config.ini配置加载成功", setting.Conf.Port)

	// 创建数据库
	// sql: CREATE DATABASE bubble;
	// 连接数据库
	err := dao.InitMySQL(setting.Conf.MySQLConfig)
	if err != nil {
		fmt.Printf("init mysql failed, err:%v\n", err)
		return
	}
	fmt.Println("数据库配置初始化加载成功", setting.Conf.MySQLConfig)
	if err := log.InitLogger(setting.Conf.LogConfig); err != nil {
		fmt.Printf("init logger failed, err:%v\n", err)
		return
	}
```

已经加载全局变量，可以正常使用

![](http://image.ownit.top/csdn/0e5409fb0f9741dab93d294b99bfb862.png)

mysql调用参数，

```Go
func InitMySQL(cfg *setting.MySQLConfig) (err error) {
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		cfg.User, cfg.Password, cfg.Host, cfg.Port, cfg.DB)

	DB, err = gorm.Open("mysql", dsn)
	if err != nil {
		return
	}
	DB.Debug()
	DB.LogMode(true)
	DB.SetLogger(&GormLogger{})
	return DB.DB().Ping()
}
```

## Zap和**lumberjack**

**Zap 日志记录**

**lumberjack 日志切割**

```Go
go get -u go.uber.org/zap
go get -u github.com/natefinch/lumberjack
```

**大家可以参考**

[golang开发:类库篇\(一\) Zap高性能日志类库的使用 \- 飞翔码农 \- 博客园](https://www.cnblogs.com/feixiangmanon/p/11109174.html "golang开发:类库篇(一) Zap高性能日志类库的使用 \- 飞翔码农 \- 博客园")[使用zap接收gin框架默认的日志并配置日志归档 \- 兰玉磊的个人博客](https://www.fdevops.com/2020/08/24/go-gin-zap "使用zap接收gin框架默认的日志并配置日志归档 \- 兰玉磊的个人博客")[golang开发:类库篇\(一\) Zap高性能日志类库的使用 \- 飞翔码农 \- 博客园](https://www.cnblogs.com/feixiangmanon/p/11109174.html "golang开发:类库篇(一) Zap高性能日志类库的使用 \- 飞翔码农 \- 博客园")

[在Go语言项目中使用Zap日志库 \- 知乎](https://zhuanlan.zhihu.com/p/88856378?utm_source=wechat_session "在Go语言项目中使用Zap日志库 \- 知乎")

日志格式

```Go
{"level":"INFO","time":"2021-12-28T15:34:50.934+0800","caller":"log/logger.go:65","msg":"/","status":200,"method":"GET","path":"/","query":"","ip":"127.0.0.1","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36","errors":"","cost":0.0010676}
{"level":"DEBUG","time":"2021-12-28T15:34:51.194+0800","caller":"dao/mysql.go:23","msg":"sql","module":"gorm","type":"sql","src":"D:/桌面/bubble/models/todo.go:24","duration":0.0504676,"sql":"SELECT * FROM `todos`  ","values":null,"rows_returned":3}
```

我们需要把它集成到Gin框架中。

![](http://image.ownit.top/csdn/1dcf8443b73045f09e0c064a4ee34c5c.png)

我这边的配置，也会读取ini的文件（看上面的代码）

```Go
[log]
level = debug
filename = ./logs/info.log
maxsize = 1
max_age = 30
max_backups = 5







type LogConfig struct {
	Level      string `ini:"level"`
	Filename   string `ini:"filename"`
	MaxSize    int    `ini:"maxsize"`
	MaxAge     int    `ini:"max_age"`
	MaxBackups int    `ini:"max_backups"`
}
```

```Go
package log

import (
	"bubble/setting"
	"github.com/gin-gonic/gin"
	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
	"net"
	"net/http"
	"net/http/httputil"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

var Logger *zap.Logger

// InitLogger 初始化Logger
func InitLogger(cfg *setting.LogConfig) (err error) {
	writeSyncer := getLogWriter(cfg.Filename, cfg.MaxSize, cfg.MaxBackups, cfg.MaxAge)
	//fmt.Println(cfg.Filename)
	encoder := getEncoder()
	var l = new(zapcore.Level)
	err = l.UnmarshalText([]byte(cfg.Level))
	if err != nil {
		return
	}
	core := zapcore.NewCore(encoder, writeSyncer, l)

	Logger = zap.New(core, zap.AddCaller())
	return
}

func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.TimeKey = "time"
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	encoderConfig.EncodeDuration = zapcore.SecondsDurationEncoder
	encoderConfig.EncodeCaller = zapcore.ShortCallerEncoder

	return zapcore.NewJSONEncoder(encoderConfig)
}

func getLogWriter(filename string, maxSize, maxBackup, maxAge int) zapcore.WriteSyncer {
	lumberJackLogger := &lumberjack.Logger{
		Filename:  filename,
		MaxSize:    maxSize,
		MaxBackups: maxBackup,
		MaxAge:     maxAge,
	}
	return zapcore.AddSync(lumberJackLogger)
}

// GinLogger 接收gin框架默认的日志
func GinLogger(logger *zap.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		query := c.Request.URL.RawQuery
		c.Next()

		cost := time.Since(start)
		logger.Info(path,
			zap.Int("status", c.Writer.Status()),
			zap.String("method", c.Request.Method),
			zap.String("path", path),
			zap.String("query", query),
			zap.String("ip", c.ClientIP()),
			zap.String("user-agent", c.Request.UserAgent()),
			zap.String("errors", c.Errors.ByType(gin.ErrorTypePrivate).String()),
			zap.Duration("cost", cost),
		)
	}
}

// GinRecovery recover掉项目可能出现的panic，并使用zap记录相关日志
func GinRecovery(logger *zap.Logger, stack bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		defer func() {
			if err := recover(); err != nil {
				// Check for a broken connection, as it is not really a
				// condition that warrants a panic stack trace.
				var brokenPipe bool
				if ne, ok := err.(*net.OpError); ok {
					if se, ok := ne.Err.(*os.SyscallError); ok {
						if strings.Contains(strings.ToLower(se.Error()), "broken pipe") || strings.Contains(strings.ToLower(se.Error()), "connection reset by peer") {
							brokenPipe = true
						}
					}
				}

				httpRequest, _ := httputil.DumpRequest(c.Request, false)
				if brokenPipe {
					logger.Error(c.Request.URL.Path,
						zap.Any("error", err),
						zap.String("request", string(httpRequest)),
					)
					// If the connection is dead, we can't write a status to it.
					c.Error(err.(error)) // nolint: errcheck
					c.Abort()
					return
				}

				if stack {
					logger.Error("[Recovery from panic]",
						zap.Any("error", err),
						zap.String("request", string(httpRequest)),
						zap.String("stack", string(debug.Stack())),
					)
				} else {
					logger.Error("[Recovery from panic]",
						zap.Any("error", err),
						zap.String("request", string(httpRequest)),
					)
				}
				c.AbortWithStatus(http.StatusInternalServerError)
			}
		}()
		c.Next()
	}
}
```

注册中间件的操作在`routes.SetupRouter()`中：

```Go
func SetupRouter() *gin.Engine {
	if setting.Conf.Release {
		gin.SetMode(gin.ReleaseMode)
	}
    #开始调用，中间件使用
	r := gin.New()
	r.Use(log.GinLogger(log.Logger), log.GinRecovery(log.Logger, true))

}
```

![](http://image.ownit.top/csdn/7a42676173a541ed96715b5dd128deca.png)

 main中调用

```Go
	log.Logger.Debug("大家好，日志展示")
	defer log.Logger.Sync()
```

```Go
{"level":"DEBUG","time":"2021-12-28T15:34:42.647+0800","caller":"bubble/main.go:39","msg":"大家好，日志展示"}
```

日志格式可以定义json格式，后期可以直接接入elk分析展示日志

## Gorm的sql日志记录到文本

Gorm 建立了对 Logger 的支持，默认模式只会在错误发生的时候打印日志。可以通过gorm SetLogger\(log logger\)方法 改变gorm 打日志的行为。

gorm 中 logger的接口：

```Go
type logger interface {
	Print(ctx context.Context, v ...interface{})
}

v 的值为：

1个参数： level，表示这个是个什么请求，可以是“sql”
2个参数：打印sql的代码行号，如/Users/yejianfeng/Documents/gopath/src/gorm-log/main.go:50, 
3个参数: 执行时间戳
4个参数: sql语句
5参数：如果有预处理，请求参数，第六个参数是这个sql影响的行数。
```

zaplog集成示例

```Go
DB.Debug()
DB.LogMode(true)
DB.SetLogger(&GormLogger{})

// GormLogger struct
type GormLogger struct{}

// Print - Log Formatter
func (*GormLogger) Print(v ...interface{}) {
	switch v[0] {
	case "sql":
		log.Debug(
			"sql",
			zap.String("module", "gorm"),
			zap.String("type", "sql"),
			zap.Any("src", v[1]),
			zap.Any("duration", v[2]),
			zap.Any("sql", v[3]),
			zap.Any("values", v[4]),
			zap.Any("rows_returned", v[5]),
		)
	case "log":
		log.Debug("log", zap.Any("gorm", v[2]))
	}
}
```

![](http://image.ownit.top/csdn/fa1ab3c8fd31455aa284eb37f1844d8b.png)

 日志格式，sql语句已经打印到日志中

```Go
{"level":"DEBUG","time":"2021-12-28T15:34:51.194+0800","caller":"dao/mysql.go:23","msg":"sql","module":"gorm","type":"sql","src":"D:/桌面/bubble/models/todo.go:24","duration":0.0504676,"sql":"SELECT * FROM `todos`  ","values":null,"rows_returned":3}
```

参考文档 [GORM自定义日志配置 \- 苍山落暮 \- 博客园](https://www.cnblogs.com/tomtellyou/p/13230163.html "GORM自定义日志配置 \- 苍山落暮 \- 博客园")