+++
author = "南宫乘风"
title = "GO的WEB编程（GIN实现邮件接口报警）"
date = "2021-12-10 11:12:36"
tags=['golang', '前端', '开发语言']
categories=['Go语言']
image = "post/4kdongman/22.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/121851358](https://blog.csdn.net/heian_99/article/details/121851358)

为什么要写这个邮件告警接口？？？？？？

因为日常范围，我们在操作系统上，需要报警时，只能采用mailx来使用。需要配置账号，密码，和邮箱认证。如果需要多台使用的话，岂不是很麻烦，要配置多台，这个导致密码很不安全，容易泄露。所以，为了安全，有效，更方便，我们可以采用接口发送邮件。

（1）构建接口

（2）传入post的json情况

（3）把相应json转换字符

（4）发送邮件

![f82790457251415f8f747422b0c2549f.png](https://img-blog.csdnimg.cn/f82790457251415f8f747422b0c2549f.png)

![a592ffe3fae24e92a4309fe0f1fca608.png](https://img-blog.csdnimg.cn/a592ffe3fae24e92a4309fe0f1fca608.png)** 调用方式（已做脱敏）**

```
curl http://mawnit.top/send -H "Content-Type:application/json" -X POST -d '{"source":"heiassns","contacts":"17947@qq.com","subject":"geian","content":"精确吗,我很好"} '
```

 

代码很简单，实现基本功能

自定义标题，内容，发送人（只支持单个）

```
package main

import (
	"fmt"
	"net/http"
	"net/smtp"
	"strings"

	"github.com/gin-gonic/gin"
)

// 定义接收数据的结构体
type User struct {
	// binding:"required"修饰的字段，若接收为空值，则报错，是必须字段
	Source   string `form:"source" json:"source" uri:"source" xml:"source" binding:"required"`
	Contacts string `form:"contacts" json:"contacts" uri:"contacts" xml:"contacts" binding:"required"`
	Subject  string `form:"subject" json:"subject" uri:"subject" xml:"subject" binding:"required"`
	Content  string `form:"content" json:"content" uri:"content" xml:"content" binding:"required"`
}

func SendToMail(user, sendUserName, password, host, to, subject, body, mailtype string) error {
	hp := strings.Split(host, ":")
	fmt.Println(hp)
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
	fmt.Println(err)
	return err
}

func main() {
	// 1.创建路由
	// 默认使用了2个中间件Logger(), Recovery()
	r := gin.Default()
	// JSON绑定
	r.POST("send", func(c *gin.Context) {
		 声明接收的变量
		var json User
		 将request的body中的数据，自动按照json格式解析到结构体
		//
		if err := c.ShouldBindJSON(&amp;json); err != nil {
			//	// 返回错误信息
			//	// gin.H封装了生成json数据的工具
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		//fmt.Println(json.Content, json.Contacts)
		//c.JSON(http.StatusOK, gin.H{"status": &amp;json})
		user := "发件人邮箱"
		password := "密码"
		host := "smtp.qq.com:25"
		source := json.Source
		if source != "heian" {
			fmt.Println("Send mail error!,source 认证失败")
			c.JSON(http.StatusOK, gin.H{
				"error": "Send mail error!,source 认证失败",
			})
			return
		}
		to := json.Contacts
		if strings.TrimSpace(to) == "" {
			fmt.Println("Send mail error!,发送人为空")
			c.JSON(http.StatusOK, gin.H{
				"error": "Send mail error!,发送人为空",
			})
			return
		}
		subject := json.Subject
		if strings.TrimSpace(subject) == "" {
			fmt.Println("Send mail error!标题为空")
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
		//log.Printf("接收人：", json.Contacts+"\n"+"标题:", json.Subject+"\n", "发送内容：", json.Content+"\n")
		fmt.Printf("接收人:%s \n 标题: %s \n 内容: %s \n", json.Contacts, json.Subject, json.Content)
		sendUserName := "告警平台" //发送邮件的人名称
		fmt.Println("send email")
		err := SendToMail(user, sendUserName, password, host, to, subject, body, "html")
		if err != nil {
			fmt.Println("Send mail error!")
			c.JSON(http.StatusOK, gin.H{
				"error": "Send mail error! !",
			})
			//fmt.Println(err)
		} else {
			fmt.Println("Send mail success!")
			c.JSON(http.StatusOK, gin.H{
				"success": "Send mail success! !",
			})
		}

	})
	r.Run(":7070")
}


```

后续慢慢改进，把相应的发送信息，保存到数据库中，支持多人发送，支持文件发送，等等
