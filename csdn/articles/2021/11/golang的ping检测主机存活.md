+++
author = "南宫乘风"
title = "golang的ping检测主机存活"
date = "2021-11-30 11:17:32"
tags=['运维', 'Go', 'go语言', '编程', 'ping']
categories=['Go语言']
image = "post/4kdongman/18.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/121628241](https://blog.csdn.net/heian_99/article/details/121628241)

Go语言的协程会并发，执行，可以大大提高效率。

列如，我们通过 ping 来检测网络的主机的话。

如果使用shell的话，会检查一个IP，在检查下一个IP，速度很慢。

如果我们使用Python 的话，可以使用多线程。

我们这里使用Go的协程来操作，速度是刚刚的。



一个网段，10S中，相当于，一秒钟处理25个左右的IP，因为ping检查，有延时性 

![a37b9ebad853478a849ea442451c10f3.png](https://img-blog.csdnimg.cn/a37b9ebad853478a849ea442451c10f3.png)

此脚本，只能在Linux上执行

```
package main

import (
	"fmt"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"
)

var wg sync.WaitGroup

func main() {
	start := time.Now()
	ip := "10.10.10."
	wg.Add(254)
	for i := 1; i &lt;= 254; i++ {
		//fmt.Println(ip + strconv.Itoa(i))
		true_ip := ip + strconv.Itoa(i)
		go ping(true_ip)
	}
	wg.Wait()
	cost := time.Since(start)
	fmt.Println("执行时间:", cost)
}

func ping(ip string) {
	var beaf = "false"
	Command := fmt.Sprintf("ping -c 1 %s  &gt; /dev/null &amp;&amp; echo true || echo false", ip)
	output, err := exec.Command("/bin/sh", "-c", Command).Output()
	if err != nil {
		fmt.Println(err)
		return
	}
	real_ip := strings.TrimSpace(string(output))

	if real_ip == beaf {
		fmt.Printf("IP: %s  失败\n", ip)
	} else {

		fmt.Printf("IP: %s  成功 ping通\n", ip)
	}
	wg.Done()
}

```

不得不说，GO语言的并发，是真的香啊，
