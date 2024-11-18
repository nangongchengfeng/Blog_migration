---
author: 南宫乘风
categories:
- Python学习
date: 2023-09-22 16:13:03
description: 技术后端：可视化：前端：大屏布局大屏拆分案例项目中大屏可按版块进行拆解，会发现这里大屏主要由标题、折线图、柱状图、地图、滚动图和词云等组成，整体可切分为个版块，如下：下方为简单演示：在这里插入图片描述。。。。。。。
image: ../../title_pic/27.jpg
slug: '202309221613'
tags:
- flask
- echarts
- python
title: Flask配合Echarts写一个动态可视化大屏
---

<!--more-->

ch
## 技术
后端：flask
可视化：echarts
前端：HTML+JavaScript+css

## 大屏布局
大屏拆分
案例项目中大屏可按版块进行拆解，会发现这里大屏主要由标题、折线图、柱状图、地图、滚动图和词云等组成，整体可切分为8个版块，如下：
下方为简单演示：
![在这里插入图片描述](../../image/c2c0e7e517df4b119a95d031fe82eaf6.png)
![在这里插入图片描述](../../image/86b9b02868d444ee973650306b29f4c9.png)
### HTML
我们整体布局前，先通过简单的案例了解前端布局实现方法。

创建一个html文件，这里先调整标题的布局位置，代码如下：

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">

    <meta charset="utf-8"/>
    <title>ECharts</title>
    <!-- 引入刚刚下载的 ECharts 文件 -->
    <!-- 引入 jQuery 库 -->
    <script src="https://cdn.staticfile.org/jquery/3.6.0/jquery.min.js"></script>
    <script src="static/js/echarts.min.js"></script>
</head>

<body>
<div id="title">机器监控实时跟踪</div>
<div id="time"></div>
<!-- 为 ECharts 准备一个定义了宽高的 DOM -->
<div id="main"></div>

<div id="cpu"></div>

<div id="disk"></div>
<div id="network"></div>
</body>
<html>
```
展示
![在这里插入图片描述](../../image/8b33dd543697470cbcc5e582a30d5d60.png)
### CSS
在上面添加一些css的样式，划分相关的位置
```html
        position: absolute;
        width: 100%;
        height: 50%;
        top: 50%;
        right: 0%;
```
上面就是划分位置的参数，能够帮我们快速划分好位置。
这段代码是用于对一个元素进行定位的 CSS 样式设置。以下是对每个参数的详细介绍：

position: absolute;：将元素的定位类型设置为绝对定位，即相对于其最近的具有定位（非static）的父元素进行定位。
width: 100%;：将元素的宽度设置为父元素的100%。换句话说，元素的宽度将填充其父元素的整个宽度。
height: 50%;：将元素的高度设置为父元素高度的50%。元素将占据其父元素高度的一半。
top: 50%;：将元素的顶部边缘相对于其包含块（通常是最近的已定位祖先元素）的顶部边缘偏移50%。此设置将使元素的中心垂直居中。
right: 0%;：将元素的右侧边缘相对于其包含块的右侧边缘偏移0%。换句话说，元素将紧贴其包含块的右侧边缘。

根据以上参数设置，这段代码将使元素以绝对定位方式出现在父元素内部。元素的宽度将填满整个父元素的宽度，高度为父元素高度的一半。元素将垂直居中，且右侧紧贴父元素。请注意，此代码片段中未提及其他定位相关属性（如左侧偏移量），因此可能还需要其他样式设置来完整定义元素的位置和大小。


```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">

    <meta charset="utf-8"/>
    <title>ECharts</title>
    <!-- 引入刚刚下载的 ECharts 文件 -->
    <!-- 引入 jQuery 库 -->
    <script src="https://cdn.staticfile.org/jquery/3.6.0/jquery.min.js"></script>
    <script src="static/js/echarts.min.js"></script>
</head>
<style>
    body {
        margin: 0;
        background: #333;
    }

    #title {
        position: absolute;
        width: 40%;
        height: 10%;
        top: 0%;
        left: 30%;
        background: #666666;
        color: white;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold; /* 加粗字体 */
        border-radius: 10px; /* 增加圆润感 */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 增加一些阴影，增加科技感 */
    }

    #main {
        position: absolute;
        width: 40%;
        height: 40%;
        top: 10%;
        left: 30%;
        background: #46a9be;
        color: white;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold; /* 加粗字体 */
        border-radius: 10px; /* 增加圆润感 */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 增加一些阴影，增加科技感 */
    }

    #cpu {
        position: absolute;
        width: 30%;
        height: 40%;
        top: 10%;
        left: 0%;
        background: #48dada;
        color: white;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold; /* 加粗字体 */
        border-radius: 10px; /* 增加圆润感 */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 增加一些阴影，增加科技感 */
    }

    #time {
        position: absolute;
        /* width: 30%; */
        height: 10%;
        top: 5%;
        right: 2%;
        color: #FFFFFF;
        font-size: 20px;
        /* background: green; */
    }

    #disk {
        position: absolute;
        width: 30%;
        height: 40%;
        top: 10%;
        right: 0%;
        background: #48dada;
        color: white;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold; /* 加粗字体 */
        border-radius: 10px; /* 增加圆润感 */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 增加一些阴影，增加科技感 */

    }

    #network {
        position: absolute;
        width: 100%;
        height: 50%;
        top: 50%;
        right: 0%;
        background: #dea594;
        color: white;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold; /* 加粗字体 */
        border-radius: 10px; /* 增加圆润感 */
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 增加一些阴影，增加科技感 */

    }
</style>

<body>
<div id="title">机器监控实时跟踪</div>
<div id="time"></div>
<!-- 为 ECharts 准备一个定义了宽高的 DOM -->
<div id="main"></div>

<div id="cpu"></div>

<div id="disk"></div>
<div id="network"></div>
</body>
<html>
```
![在这里插入图片描述](../../image/4addb3565da844f5ac1738460b15dfe8.png)
### JS
**时间显示**
```js
function showTime() {
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1; // getMonth() 返回的月份是从0开始的，所以需要+1
        var day = date.getDate();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var second = date.getSeconds();

        // 使用 'padStart' 函数来确保每个部分都是两位数
        month = month.toString().padStart(2, '0');
        day = day.toString().padStart(2, '0');
        hour = hour.toString().padStart(2, '0');
        minute = minute.toString().padStart(2, '0');
        second = second.toString().padStart(2, '0');

        var formattedDate = year + '年' + month + '月' + day + '日，' + hour + '时' + minute + '分' + second + '秒';
        document.getElementById("time").innerHTML = formattedDate;
    }

    setInterval(showTime, 1000);
```
这段代码是用 JavaScript 实现一个实时显示当前时间的页面特效,原理：
首先定义了一个 showTime() 函数，它通过创建一个新的 Date 对象来获取当前时间，并从中提取年、月、日、小时、分钟和秒的值。然后使用 padStart() 函数来确保月、日、小时、分钟和秒都是两位数（如果前缀不足，则在前面添加 '0'）。
接下来，将各个提取的时间值整合为一个字符串 formattedDate，其中各个部分之间添加了一些中文字符作为分隔符。
最后，将拼接好的时间字符串赋值给页面上带有 "time" ID 的元素，并通过调用 setInterval() 函数每隔一秒钟更新一次该元素的内容，从而实现了实时显示当前时间的效果。

这个例子比较简单，但是通过这个例子可以了解到 JavaScript 中获取和处理时间的基本方法，以及如何使用定时器来定期更新页面内容。


**echarts**

https://echarts.apache.org/examples/zh/index.html#chart-type-line

例子：https://echarts.apache.org/examples/zh/editor.html?c=gauge-simple

我们要使用 这个JS来进行大屏展示
![在这里插入图片描述](../../image/e2ea2cb47e154308926fa1a4c2a895ae.png)
**CPU**
```js
var myChart_CPU = echarts.init(document.getElementById('cpu'));
    // 指定图表的配置项和数据
    var option_cpu = {
        tooltip: {
            formatter: '{a} <br/>{b} : {c}%'
        },
        series: [
            {
                name: 'CPU',
                type: 'gauge',
                progress: {
                    show: true
                },
                detail: {
                    valueAnimation: true,
                    formatter: '{value}'
                },
                data: [
                    {
                        value: '{{ cpu_percent }} %',
                        name: 'CPU使用率'
                    }
                ]
            }
        ]
    };

    // 定义函数，发送 Ajax 请求获取内存使用率数据
    function getCPUData() {
        // 使用原生 JavaScript 发送 Ajax 请求
        // var xhr = new XMLHttpRequest();
        // xhr.onreadystatechange = function () {
        //     if (xhr.readyState === 4 && xhr.status === 200) {
        //         var cpuPercent = JSON.parse(xhr.responseText).cpu_percent;
        //         updateChart_cpu(cpuPercent); // 调用更新图表的函数
        //     }
        // };
        // xhr.open('GET', '/get_cpu_data', true);
        // xhr.send();

        // 使用 jQuery 发送 Ajax 请求
        $.ajax({
            url: '/get_cpu_data',
            dataType: 'json',
            type: 'GET',
            success: function (data) {
                var cpuPercent = data.cpu_percent;
                updateChart_cpu(cpuPercent); // 调用更新图表的函数
            },
            error: function (xhr, status, error) {
                console.log('获取数据失败');
            }
        });
    }

    // 定义函数，更新图表数据并重新渲染图表
    function updateChart_cpu(cpuPercent) {
        option_cpu.series[0].data[0].value = cpuPercent;
        myChart_CPU.setOption(option_cpu);
    }

        // 使用刚指定的配置项和数据显示图表。
    myChart_CPU.setOption(option_cpu);
    // 使用 setInterval 定时刷新数据
    setInterval(getCPUData, 5000); // 每5秒刷新一次数据

```

![在这里插入图片描述](../../image/53e13142d16a4ed88e48a3911f0389e2.png)
这个只是前端的JS请求后端的接口获取到数据才会显示（/get_cpu_data）

```python
@app.route('/get_cpu_data')
def get_cpu_data():
    # 获取机器的 CPU 使用率
    cpu_percent = psutil.cpu_percent()
    print(cpu_percent)
    return jsonify(cpu_percent=cpu_percent)
```
## 进击版（JS和CSS剥离）
### CSS
在static 目录 创建 CSS文件目录
cpu.css
```css
#cpu {
    position: absolute;
    width: 30%;
    height: 40%;
    top: 10%;
    left: 0%;
    background: #48dada;
    color: white;
    font-size: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold; /* 加粗字体 */
    border-radius: 10px; /* 增加圆润感 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2); /* 增加一些阴影，增加科技感 */
}
```
![在这里插入图片描述](../../image/412bd21717884ac4a100aa61e1e5413b.png)

在html页面引入相关的css
```html
		<link href="../static/css/main.css" rel="stylesheet" />
```
###  JS
**cpu.js**
```js
var myChart_CPU = echarts.init(document.getElementById('cpu'));
// 指定图表的配置项和数据
var option_cpu = {
    tooltip: {
        formatter: '{a} <br/>{b} : {c}%'
    },
    series: [
        {
            name: 'CPU',
            type: 'gauge',
            progress: {
                show: true
            },
            detail: {
                valueAnimation: true,
                formatter: '{value}'
            },
            data: [
                {
                    value: '0',
                    name: 'CPU使用率'
                }
            ]
        }
    ]
};


// 使用刚指定的配置项和数据显示图表。
myChart_CPU.setOption(option_cpu);
```
**controller.js**
```js
function getCPUData() {
    // 使用原生 JavaScript 发送 Ajax 请求
    // var xhr = new XMLHttpRequest();
    // xhr.onreadystatechange = function () {
    //     if (xhr.readyState === 4 && xhr.status === 200) {
    //         var cpuPercent = JSON.parse(xhr.responseText).cpu_percent;
    //         updateChart_cpu(cpuPercent); // 调用更新图表的函数
    //     }
    // };
    // xhr.open('GET', '/get_cpu_data', true);
    // xhr.send();

    // 使用 jQuery 发送 Ajax 请求
    $.ajax({
        url: '/get_cpu_data',
        dataType: 'json',
        type: 'GET',
        success: function (data) {
            var cpuPercent = data.cpu_percent;
            updateChart_cpu(cpuPercent); // 调用更新图表的函数
        },
        error: function (xhr, status, error) {
            console.log('获取数据失败');
        }
    });
}

// 定义函数，更新图表数据并重新渲染图表
function updateChart_cpu(cpuPercent) {
    option_cpu.series[0].data[0].value = cpuPercent;
    myChart_CPU.setOption(option_cpu);
}

getCPUData();
setInterval(getCPUData, 5000);

```
![在这里插入图片描述](../../image/cd54e717c5014ea49a9393efbf84b9fe.png)

在html页面进行引入，切记，controller.js 最好一个引入

```html
<script src="../static/js/cpu.js"></script>
<script src="../static/js/controller.js"></script>
```

![在这里插入图片描述](../../image/7fbdcbf55eb844309e7a80d872bf97c0.png)
正常显示


后续如果继续深入研究，后端框架可以换成高性能的tornado或者功能更强大的Django，可视化的组件可以换成pyecharts，前端可以使用vue，react框架等。还可以考虑加入sqlite数据库或连接db数据库，打造成一个更完整的项目。



参考文档：
[https://www.cnblogs.com/hugboy/p/15427793.html](https://www.cnblogs.com/hugboy/p/15427793.html)
[https://zhuanlan.zhihu.com/p/584796840](https://zhuanlan.zhihu.com/p/584796840)
[https://github.com/xiaokai1996/big_screen/blob/master/big_screen%E9%A1%B9%E7%9B%AE%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.md](https://github.com/xiaokai1996/big_screen/blob/master/big_screen%E9%A1%B9%E7%9B%AE%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0.md)
[https://blog.csdn.net/dwhyxjfm/article/details/127946379](https://blog.csdn.net/dwhyxjfm/article/details/127946379)
