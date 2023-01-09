+++
author = "南宫乘风"
title = "Gin编写邮件告警接口（添加优化日志记录）"
date = "2021-12-17 18:31:58"
tags=['linq', 'p2p', 'html', 'Go']
categories=['Go语言']
image = "post/4kdongman/74.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/122002534](https://blog.csdn.net/heian_99/article/details/122002534)

# [GO的WEB编程（GIN实现邮件接口报警）](https://blog.csdn.net/heian_99/article/details/121851358)

# [Gin编写邮件接口（支持多人发送）](https://blog.csdn.net/heian_99/article/details/121912558)

这个代码基于上面两个已经完成的功能上实现。

实现下面功能

**        日志分割**

**        日志记录**

效果图

        ![416e3577dc7b400c9ac06ac783863c15.png](https://img-blog.csdnimg.cn/416e3577dc7b400c9ac06ac783863c15.png)

 

![5239fc811ee94f5ea78a853eb232bb97.png](https://img-blog.csdnimg.cn/5239fc811ee94f5ea78a853eb232bb97.png)

 

因为日常范围，我们在操作系统上，需要报警时，只能采用mailx来使用。需要配置账号，密码，和邮箱认证。如果需要多台使用的话，岂不是很麻烦，要配置多台，这个导致密码很不安全，容易泄露。所以，为了安全，有效，更方便，我们可以采用接口发送邮件。

（1）构建接口

（2）传入post的json情况

（3）把相应json转换字符

（4）发送邮件



代码放在一个main。

```
package main

import (
	"fmt"
	"net/http"
	"net/smtp"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

/*
支持多人发送
curl http://10.10.10.3:7070/send -H "Content-Type:application/json" -X POST -d '{"source":"heian","contacts":["账号@qq.com","账号@qq.com"],"subject":"多人测试","content":"现在进行多人测试"}'

*/

/*
zapcore.Core需要三个配置——Encoder，WriteSyncer，LogLevel
Encoder:编码器(如何写入日志)。我们将使用开箱即用的NewJSONEncoder()
WriterSyncer ：指定日志将写到哪里去。我们使用zapcore.AddSync()
Log Level：哪种级别的日志将被写入。
*/
var sugarLogger *zap.SugaredLogger

func InitLogger() {
	writeSyncer := getLogWriter()
	encoder := getEncoder()
	core := zapcore.NewCore(encoder, writeSyncer, zapcore.DebugLevel)

	logger := zap.New(core, zap.AddCaller())
	sugarLogger = logger.Sugar()
}

func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	return zapcore.NewConsoleEncoder(encoderConfig)
}

func getLogWriter() zapcore.WriteSyncer {
	/*
		Lumberjack Logger采用以下属性作为输入:

		Filename: 日志文件的位置
		MaxSize：在进行切割之前，日志文件的最大大小（以MB为单位）
		MaxBackups：保留旧文件的最大个数
		MaxAges：保留旧文件的最大天数
		Compress：是否压缩/归档旧文件
	*/
	lumberJackLogger := &amp;lumberjack.Logger{
		Filename:   "./logs/info.log",
		MaxSize:    10,
		MaxBackups: 5,
		MaxAge:     30,
		Compress:   false,
	}
	return zapcore.AddSync(lumberJackLogger)

}

// 定义接收数据的结构体
type User struct {
	// binding:"required"修饰的字段，若接收为空值，则报错，是必须字段
	Source   string   `form:"source" json:"source" uri:"source" xml:"source" binding:"required"`
	Contacts []string `form:"contacts" json:"contacts" uri:"contacts" xml:"contacts" binding:"required"`
	Subject  string   `form:"subject" json:"subject" uri:"subject" xml:"subject" binding:"required"`
	Content  string   `form:"content" json:"content" uri:"content" xml:"content" binding:"required"`
}

func SendToMail(user, sendUserName, password, host, to, subject, body, mailtype string) error {
	hp := strings.Split(host, ":")
	//fmt.Println(hp)
	auth := smtp.PlainAuth("", user, password, hp[0])
	var content_type string
	if mailtype == "html" {
		content_type = "Content-Type: text/" + mailtype + "; charset=UTF-8"
	} else {
		content_type = "Content-Type: text/plain" + "; charset=UTF-8"
	}

	msg := []byte("To: " + to + "\r\nFrom: " + sendUserName + "&lt;" + user + "&gt;" + "\r\nSubject: " + subject + "\r\n" + content_type + "\r\n\r\n" + body)
	send_to := strings.Split(to, ";")
	err := smtp.SendMail(host, auth, user, send_to, msg)
	//fmt.Println(err)
	return err
}

//获取ip
func GetRequestIP(c *gin.Context) string {
	reqIP := c.ClientIP()
	if reqIP == "::1" {
		reqIP = "127.0.0.1"
	}
	return reqIP
}
func PostMail(c *gin.Context) {
	c_ip := GetRequestIP(c)
	//fmt.Println(c_ip)
	sugarLogger.Debugf("调用 PostMail 接口Api，调用者IP： %s ", c_ip)
	 声明接收的变量
	var json User
	 将request的body中的数据，自动按照json格式解析到结构体
	//
	if err := c.ShouldBindJSON(&amp;json); err != nil {
		//	// 返回错误信息
		//	// gin.H封装了生成json数据的工具
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		sugarLogger.Errorf("Error: %s", err.Error())
		return
	}
	//fmt.Println(json.Content, json.Contacts)
	//c.JSON(http.StatusOK, gin.H{"status": &amp;json})
	sugarLogger.Infof("info: %s", json)
	user := "账号@qq.com"
	password := "密码"
	host := "smtp.qq.com:25"
	source := json.Source
	if source != "heian" {
		fmt.Println("Send mail error!,source 认证失败")
		sugarLogger.Errorf("Send mail error!,source 认证失败")
		c.JSON(http.StatusOK, gin.H{
			"error": "Send mail error!,source 认证失败",
		})
		return
	}
	//println(json.Contacts)
	to := json.Contacts
	if to[0] == "" {
		fmt.Println("Send mail error!,发送人为空")
		sugarLogger.Errorf("Send mail error!,发送人为空")
		c.JSON(http.StatusOK, gin.H{
			"error": "Send mail error!,发送人为空",
		})
		return
	}
	subject := json.Subject
	if strings.TrimSpace(subject) == "" {
		fmt.Println("Send mail error!标题为空")
		sugarLogger.Errorf("Send mail error!标题为空")
		c.JSON(http.StatusOK, gin.H{
			"error": "Send mail error!,标题为空",
		})
		return
	}
	body := `
		&lt;!DOCTYPE html&gt;
		&lt;html lang="en"&gt;
		&lt;head&gt;
			&lt;meta charset="iso-8859-15"&gt;
			&lt;title&gt;MMOGA POWER&lt;/title&gt;
		&lt;/head&gt;
		&lt;body&gt;
			` + fmt.Sprintf(json.Content) +
		`&lt;/body&gt;
		&lt;/html&gt;`

	sendUserName := "告警平台" //发送邮件的人名称
	fmt.Println("send email")

	for _, s := range to {
		//fmt.Println(i, s)
		err := SendToMail(user, sendUserName, password, host, s, subject, body, "html")
		//log.Printf("接收人：", s+"\n"+"标题:", json.Subject+"\n", "发送内容：", json.Content+"\n")
		fmt.Printf("接收人:%s \n 标题: %s \n 内容: %s \n", s, json.Subject, json.Content)
		sugarLogger.Infof("接收人: %s ,标题: %s, 内容: %s", s, json.Subject, json.Content)
		if err != nil {
			fmt.Println("Send mail error!\n")
			sugarLogger.Errorf("Error 调用者IP: %s ,Send mail error! !", c_ip)
			c.JSON(http.StatusOK, gin.H{
				"error": "Send mail error! !\n",
			})
			//fmt.Println(err)
		} else {
			fmt.Println("Send mail success!\n")
			sugarLogger.Infof("success 调用者IP: %s ,Send mail success! !", c_ip)
			c.JSON(http.StatusOK, gin.H{
				"success": "Send mail success! !\n",
			})
		}

	}

}

func main() {
	// 1.创建路由
	// 默认使用了2个中间件Logger(), Recovery()
	InitLogger()
	defer sugarLogger.Sync()
	r := gin.Default()
	// JSON绑定
	r.POST("send", PostMail)
	sugarLogger.Infof("Success! Port is start")
	r.Run(":7070")

}

```

![ebcbd6aae9db429ead007045fd309141.png](https://img-blog.csdnimg.cn/ebcbd6aae9db429ead007045fd309141.png)

 
