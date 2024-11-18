---
author: 南宫乘风
categories:
- Go语言
date: 2022-01-12 10:43:15
description: 日常我们会使用到到图床来存放图片，但是大致流程是什么样子的来？？图床原理实现一个服务器用这个服务器存储图片针对每个图片提供一个唯一的借助这个就可以将图片展示到其他网页上后端代码实现项目接口首先，我们需。。。。。。。
image: http://image.ownit.top/4kdongman/13.jpg
tags:
- 后端
- Go
- Gin
title: Gin编写图床后端-上传图片代码实现
---

<!--more-->

日常我们会使用到到图床来存放图片，但是大致流程是什么样子的来？？

![](http://image.ownit.top/csdn/aff15eb735a74259bfa1bd9ca3385e3f.png)

 ![](http://image.ownit.top/csdn/fa0baa835e34495bb28f4ac30bba72cf.png)

 ![](http://image.ownit.top/csdn/c2ccb53d36dc41bfab2a57da071d0111.png)

 

## 图床原理

实现一个HTTP服务器,用这个服务器存储图片,针对每个图片提供一个唯一的url,借助这个url就可以将图片展示到其他网页上

![](http://image.ownit.top/csdn/326f45711ced4e9a98f69f1a73c82d45.png)

## 后端代码实现

![](http://image.ownit.top/csdn/c3eb722b525840ba96312ecf7df883a6.png)

###  项目接口

![](http://image.ownit.top/csdn/7696758e0e67412db0a967eb3bbbd498.png)

首先，我们需要建立Gin框架 post请求访问，上传图片，判断图片是否符合，在上传图片，返回Url地址，浏览器就可以正常访问

###  app.ini

```Go
[app]
HttpPort = 8000

RuntimeRootPath = runtime/

ImagePrefixUrl = http://127.0.0.1:8000
ImageSavePath = upload/images/
# MB
ImageMaxSize = 5
ImageAllowExts = .jpg,.jpeg,.png,.gif

LogSavePath = logs/
LogSaveName = log
LogFileExt = log
TimeFormat = 20060102


```

### app/upload.go

```Go
package app

import (
	"ImagesUpload/pkg/e"
	"ImagesUpload/pkg/logging"
	"ImagesUpload/pkg/upload"
	"fmt"
	"github.com/gin-gonic/gin"
	"net/http"
	"strconv"
	"time"
)
//获取ip
func GetRequestIP(c *gin.Context) string {
	reqIP := c.ClientIP()
	if reqIP == "::1" {
		reqIP = "127.0.0.1"
	}
	return reqIP
}

func UploadImage(c *gin.Context) {
	code := e.SUCCESS
	data := make(map[string]string)
	t := time.Now()
	year := t.Year()   // type int
	month := t.Month() // type time.Month
	file, image, err := c.Request.FormFile("image")
	if err != nil {
		logging.Warn(err)
		code = e.ERROR
		c.JSON(http.StatusOK, gin.H{
			"code": code,
			"msg":  e.GetMsg(code),
			"data": data,
		})
	}

	if image == nil {
		code = e.INVALID_PARAMS
	} else {
		imageName := upload.GetImageName(image.Filename)
		fullPath := upload.GetImageFullPath() + strconv.Itoa(year) + strconv.Itoa(int(month))
		savePath := upload.GetImagePath() + strconv.Itoa(year) + strconv.Itoa(int(month))
		src := fullPath + "/" + imageName
		fmt.Println(imageName, fullPath, savePath, src)
		if !upload.CheckImageExt(imageName) || !upload.CheckImageSize(file) {
			code = e.ERROR_UPLOAD_CHECK_IMAGE_FORMAT
			fmt.Println(e.GetMsg(code))
		} else {
			err := upload.CheckImage(fullPath)
			if err != nil {
				logging.Warn(err)
				code = e.ERROR_UPLOAD_CHECK_IMAGE_FAIL
			} else if err := c.SaveUploadedFile(image, src); err != nil {
				logging.Warn(err)
				code = e.ERROR_UPLOAD_SAVE_IMAGE_FAIL
			} else {
				logging.Info("访问者IP:",GetRequestIP(c),"上传地址连接:",upload.GetImageFullUrl(imageName))
				data["image_url"] = upload.GetImageFullUrl(imageName)
				data["image_save_url"] = savePath + "/" + imageName
			}
		}
	}
	c.JSON(http.StatusOK, gin.H{
		"code": code,
		"msg":  e.GetMsg(code),
		"data": data,
	})
}

```

### pkg

![](http://image.ownit.top/csdn/9bd502a205f0453ba404526c8d4bde0b.png)

###  pkg/e/code.go

```Go
package e

const  (
	SUCCESS        = 200
	ERROR          = 500
	INVALID_PARAMS = 400
	// 保存图片失败
	ERROR_UPLOAD_SAVE_IMAGE_FAIL = 30001
	// 检查图片失败
	ERROR_UPLOAD_CHECK_IMAGE_FAIL = 30002
	// 校验图片错误，图片格式或大小有问题
	ERROR_UPLOAD_CHECK_IMAGE_FORMAT = 30003
)
```

### pkg/e/msg.go

```Go
package e

var MsgFlags = map[int]string {
	SUCCESS:                        "ok",
	ERROR:                          "fail",
	INVALID_PARAMS:                 "请求参数错误",
	// 保存图片失败
	ERROR_UPLOAD_SAVE_IMAGE_FAIL: "保存图片失败",
	// 检查图片失败
	ERROR_UPLOAD_CHECK_IMAGE_FAIL: "检查图片失败",
	// 校验图片错误，图片格式或大小有问题
	ERROR_UPLOAD_CHECK_IMAGE_FORMAT: "校验图片错误，图片格式或大小有问题",
}

func GetMsg(code int) string {
	msg ,ok := MsgFlags[code]
	if ok{
		return msg
	}
	return MsgFlags[ERROR]
}
```

### pkg/file/file.go

```Go
package file

import (
	"io/ioutil"
	"mime/multipart"
	"os"
	"path"
)

/*
GetSize：获取文件大小
GetExt：获取文件后缀
CheckNotExist：检查文件是否存在
CheckPermission：检查文件权限
IsNotExistMkDir：如果不存在则新建文件夹
MkDir：新建文件夹
Open：打开文件
*/
//GetSize：获取文件大小
func GetSize(f multipart.File) (int, error) {
	content, err := ioutil.ReadAll(f)

	return len(content), err
}

//GetExt：获取文件后缀
func GetExt(fileName string) string {
	return path.Ext(fileName)
}

//CheckNotExist：检查文件是否存在
func CheckNotExist(src string) bool {
	_, err := os.Stat(src)

	return os.IsNotExist(err)
}

//CheckPermission：检查文件权限
func CheckPermission(src string) bool {
	_, err := os.Stat(src)

	return os.IsPermission(err)
}

//IsNotExistMkDir：如果不存在则新建文件夹
func IsNotExistMkDir(src string) error {
	if notExist := CheckNotExist(src); notExist == true {
		if err := MkDir(src); err != nil {
			return err
		}
	}

	return nil
}

//MkDir：新建文件夹
func MkDir(src string) error {
	err := os.MkdirAll(src, os.ModePerm)
	if err != nil {
		return err
	}

	return nil
}

//Open：打开文件
func Open(name string, flag int, perm os.FileMode) (*os.File, error) {
	f, err := os.OpenFile(name, flag, perm)
	if err != nil {
		return nil, err
	}

	return f, nil
}
```

### pkg/logging/file.go

```Go
package logging

import (
	"ImagesUpload/pkg/file"
	"ImagesUpload/setting"
	"fmt"
	"os"
	"time"
)

func getLogFilePath() string {
	return fmt.Sprintf("%s%s", setting.AppSetting.RuntimeRootPath, setting.AppSetting.LogSavePath)
}

func getLogFileName() string {
	return fmt.Sprintf("%s%s.%s",
		setting.AppSetting.LogSaveName,
		time.Now().Format(setting.AppSetting.TimeFormat),
		setting.AppSetting.LogFileExt,
	)
}

func openLogFile(fileName, filePath string) (*os.File, error) {
	dir, err := os.Getwd()
	if err != nil {
		return nil, fmt.Errorf("os.Getwd err: %v", err)
	}

	src := dir + "/" + filePath
	perm := file.CheckPermission(src)
	if perm == true {
		return nil, fmt.Errorf("file.CheckPermission Permission denied src: %s", src)
	}

	err = file.IsNotExistMkDir(src)
	if err != nil {
		return nil, fmt.Errorf("file.IsNotExistMkDir src: %s, err: %v", src, err)
	}

	f, err := file.Open(src+fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return nil, fmt.Errorf("Fail to OpenFile :%v", err)
	}

	return f, nil
}
```

### pkg/logging/log.go

```Go
package logging

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"runtime"
)


type Level int

var (
	F *os.File

	DefaultPrefix      = ""
	DefaultCallerDepth = 2

	logger     *log.Logger
	logPrefix  = ""
	levelFlags = []string{"DEBUG", "INFO", "WARN", "ERROR", "FATAL"}
)

const (
	DEBUG Level = iota
	INFO
	WARNING
	ERROR
	FATAL
)

func Setup() {
	var err error
	filePath := getLogFilePath()
	fileName := getLogFileName()
	F, err = openLogFile(fileName, filePath)
	if err != nil {
		log.Fatalln(err)
	}

	logger = log.New(F, DefaultPrefix, log.LstdFlags)
}

func Debug(v ...interface{}) {
	setPrefix(DEBUG)
	logger.Println(v)
}

func Info(v ...interface{}) {
	setPrefix(INFO)
	logger.Println(v)
}

func Warn(v ...interface{}) {
	setPrefix(WARNING)
	logger.Println(v)
}

func Error(v ...interface{}) {
	setPrefix(ERROR)
	logger.Println(v)
}

func Fatal(v ...interface{}) {
	setPrefix(FATAL)
	logger.Fatalln(v)
}

func setPrefix(level Level) {
	_, file, line, ok := runtime.Caller(DefaultCallerDepth)
	if ok {
		logPrefix = fmt.Sprintf("[%s][%s:%d]", levelFlags[level], filepath.Base(file), line)
	} else {
		logPrefix = fmt.Sprintf("[%s]", levelFlags[level])
	}

	logger.SetPrefix(logPrefix)
}
```

### pkg/logging/logrus.go

```Go
package logging

import (
	"fmt"
	"github.com/sirupsen/logrus"
)

func Logger() *logrus.Logger {
	//now := time.Now()
	//logFilePath := getLogFilePath()
	//logFileName :=  getLogFileFullPath()
	//日志文件
	//fileName := path.Join(logFilePath, logFileName)
	//if _, err := os.Stat(fileName); err != nil {
	//	if _, err := os.Create(fileName); err != nil {
	//		fmt.Println(err.Error())
	//	}
	//}
	//写入文件
	filePath := getLogFilePath()
	fileName := getLogFileName()
	F, err := openLogFile(fileName, filePath)
	if err != nil {
		fmt.Println("日志写入失败，请检查")
	}
	//实例化
	logger := logrus.New()

	//设置输出
	logger.Out = F

	//设置日志级别
	logger.SetLevel(logrus.DebugLevel)

	//设置日志格式
	logger.SetFormatter(&logrus.TextFormatter{
		TimestampFormat: "2006-01-02 15:04:05",
	})
	return logger
}
```

### pkg/upload/image.go

```Go
package upload

import (
	"ImagesUpload/pkg/file"
	"ImagesUpload/pkg/logging"
	"ImagesUpload/pkg/util"
	"ImagesUpload/setting"
	"fmt"
	"log"
	"mime/multipart"
	"os"
	"path"
	"strconv"
	"strings"
	"time"
)

/*
GetImageFullUrl：获取图片完整访问 URL
GetImageName：获取图片名称
GetImagePath：获取图片路径
GetImageFullPath：获取图片完整路径
CheckImageExt：检查图片后缀
CheckImageSize：检查图片大小
CheckImage：检查图片
*/

//GetImageFullUrl：获取图片完整访问 URL
func GetImageFullUrl(name string) string {
	t := time.Now()
	year := t.Year()   // type int
	month := t.Month() // type time.Month
	return setting.AppSetting.ImagePrefixUrl + "/" + GetImagePath() + strconv.Itoa(year) + strconv.Itoa(int(month)) + "/" + name
}

//GetImageName：获取图片名称
func GetImageName(name string) string {
	ext := path.Ext(name)
	fileName := strings.TrimSuffix(name, ext)
	fileName = util.EncodeMD5(fileName)

	return fileName + ext
}

//GetImagePath：获取图片路径
func GetImagePath() string {
	return setting.AppSetting.ImageSavePath
}

//GetImageFullPath：获取图片完整路径
func GetImageFullPath() string {
	return setting.AppSetting.RuntimeRootPath + GetImagePath()
}

//CheckImageExt：检查图片后缀
func CheckImageExt(fileName string) bool {
	ext := file.GetExt(fileName)
	for _, allowExt := range setting.AppSetting.ImageAllowExts {
		if strings.ToUpper(allowExt) == strings.ToUpper(ext) {
			return true
		}
	}

	return false
}

//CheckImageSize：检查图片大小
func CheckImageSize(f multipart.File) bool {
	size, err := file.GetSize(f)
	if err != nil {
		log.Println(err)
		logging.Warn(err)
		return false
	}

	return size <= setting.AppSetting.ImageMaxSize
}

//CheckImage：检查图片
func CheckImage(src string) error {
	dir, err := os.Getwd()
	if err != nil {
		return fmt.Errorf("os.Getwd err: %v", err)
	}

	err = file.IsNotExistMkDir(dir + "/" + src)
	if err != nil {
		return fmt.Errorf("file.IsNotExistMkDir err: %v", err)
	}

	perm := file.CheckPermission(src)
	if perm == true {
		return fmt.Errorf("file.CheckPermission Permission denied src: %s", src)
	}

	return nil
}
```

### pkg/util/md5.go

```Go
package util

import (
	"crypto/md5"
	"encoding/hex"
)

func EncodeMD5(value string) string {
	m := md5.New()
	m.Write([]byte(value))
	return hex.EncodeToString(m.Sum(nil))
}
```

### routers/router.go

```Go
package routers

import (
	"ImagesUpload/app"
	"ImagesUpload/pkg/upload"
	"github.com/gin-gonic/gin"
	"net/http"
)

func InitRouter() *gin.Engine {
	r := gin.New()

	r.Use(gin.Logger())

	r.Use(gin.Recovery())
	r.StaticFS("/upload/images", http.Dir(upload.GetImageFullPath()))
	r.POST("upload", app.UploadImage)
	return r
}
```

### setting/setting.go

```Go
package setting

import (
	"github.com/go-ini/ini"
	"log"
)

type App struct {
	HttpPort int
	RuntimeRootPath string

	ImagePrefixUrl string
	ImageSavePath  string
	ImageMaxSize   int
	ImageAllowExts []string

	LogSavePath string
	LogSaveName string
	LogFileExt  string
	TimeFormat  string
}

var AppSetting = &App{}

func Setup() {
	Cfg, err := ini.Load("conf/app.ini")
	if err != nil {
		log.Fatalf("Fail to parse 'conf/app.ini': %v", err)
	}

	err = Cfg.Section("app").MapTo(AppSetting)
	if err != nil {
		log.Fatalf("Cfg.MapTo AppSetting err: %v", err)
	}
	AppSetting.ImageMaxSize = AppSetting.ImageMaxSize * 1024 * 1024
}
```

### main.go

```Go
package main

import (
	"ImagesUpload/pkg/logging"
	"ImagesUpload/routers"
	"ImagesUpload/setting"
	"fmt"
	"log"
	"net/http"
)

func main() {
	setting.Setup()
	logging.Setup()
	router := routers.InitRouter()
	fmt.Println("启动端口：", setting.AppSetting.HttpPort)
	s := &http.Server{
		Addr:           fmt.Sprintf(":%d", setting.AppSetting.HttpPort),
		Handler:        router,
	}
	if err := s.ListenAndServe(); err != nil {
		log.Printf("Listen: %s\n", err)
	}
}
```