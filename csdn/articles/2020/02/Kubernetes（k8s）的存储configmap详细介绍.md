+++
author = "南宫乘风"
title = "Kubernetes（k8s）的存储configmap详细介绍"
date = "2020-02-08 16:34:52"
tags=['Kubernetes', 'k8s', 'configmap']
categories=[]
image = "post/4kdongman/10.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/104223555](https://blog.csdn.net/heian_99/article/details/104223555)

# conﬁgMap 描述信息 

**ConﬁgMap 功能在 Kubernetes1.2 版本中引入，许多应用程序会从配置文件、命令行参数或环境变量中读取配 置信息。ConﬁgMap API 给我们提供了向容器中注入配置信息的机制，ConﬁgMap 可以被用来保存单个属性，也 可以用来保存整个配置文件或者 JSON 二进制大对象 **

# ConﬁgMap 的创建 

## Ⅰ、使用目录创建<br>  

```
$ ls docs/user-guide/configmap/kubectl/
game.properties
ui.properties

$ cat docs/user-guide/configmap/kubectl/game.properties
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30

$ cat docs/user-guide/configmap/kubectl/ui.properties
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice


$ kubectl create configmap game-config --from-file=docs/user-guide/configmap/kubectl

```

—from-file 指定在目录下的所有文件都会被用在 ConﬁgMap 里面创建一个键值对，键的名字就是文件名，值就 是文件的内容<br><br>![20200208152714625.png](https://img-blog.csdnimg.cn/20200208152714625.png)

## Ⅱ、使用文件创建 

只要指定为一个文件就可以从单个文件中创建 ConﬁgMap<br>  

```
$ kubectl create configmap game-config-2 --from-file=docs/user-
guide/configmap/kubectl/game.properties 
$ kubectl get configmaps game-config-2 -o yaml

```

—from-file 这个参数可以使用多次，你可以使用两次分别指定上个实例中的那两个配置文件，效果就跟指定整个 目录是一样的<br>  

![20200208153018747.png](https://img-blog.csdnimg.cn/20200208153018747.png)

![20200208153033982.png](https://img-blog.csdnimg.cn/20200208153033982.png)

## Ⅲ、使用字面值创建 

使用文字值创建，利用 —from-literal 参数传递配置信息，该参数可以使用多次，格式如下<br>  

```
$ kubectl create configmap special-config --from-literal=special.how=very --from-
literal=special.type=charm
$ kubectl get configmaps special-config -o yaml

```

![20200208153314694.png](https://img-blog.csdnimg.cn/20200208153314694.png)

# Pod 中使用 ConﬁgMap 

## Ⅰ、使用 ConﬁgMap 来替代环境变量<br>  

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
  namespace: default
data:
  log_level: INFO

```

![2020020815390383.png](https://img-blog.csdnimg.cn/2020020815390383.png)

Pod的创建

```
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod
spec:
  containers:
    - name: test-container
      image: wangyanglinux/myapp:v1
      command: [ "/bin/sh", "-c", "env" ]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
      envFrom:
        - configMapRef:
            name: env-config
  restartPolicy: Never

```

![20200208160709427.png](https://img-blog.csdnimg.cn/20200208160709427.png)

## Ⅱ、用 ConﬁgMap 设置命令行参数 <br>  

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm

```

Pod的创建<br>  

```
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod66
spec:
  containers:
    - name: test-container
      image: wangyanglinux/myapp:v1
      command: [ "/bin/sh", "-c", "echo $(SPECIAL_LEVEL_KEY) $(SPECIAL_TYPE_KEY)" ]
      env:
        - name: SPECIAL_LEVEL_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.how
        - name: SPECIAL_TYPE_KEY
          valueFrom:
            configMapKeyRef:
              name: special-config
              key: special.type
  restartPolicy: Never

```

![2020020816124782.png](https://img-blog.csdnimg.cn/2020020816124782.png)

## Ⅲ、通过数据卷插件使用ConﬁgMap 

 

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: special-config
  namespace: default
data:
  special.how: very
  special.type: charm

```

在数据卷里面使用这个 ConﬁgMap，有不同的选项。基本的就是将文件填入数据卷，在这个文件中，键就是文 件名，键值就是文件内容<br>  

```
apiVersion: v1
kind: Pod
metadata:
  name: dapi-test-pod77
spec:
  containers:
    - name: test-container
      image: wangyanglinux/myapp:v1
      command: [ "/bin/sh", "-c", "sleep 600s" ]
      volumeMounts:
      - name: config-volume
        mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: special-config
  restartPolicy: Never

```

 

![20200208162005716.png](https://img-blog.csdnimg.cn/20200208162005716.png)

## ConﬁgMap 的热更新 

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: log-config
  namespace: default
data:
  log_level: INFO
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: my-nginx
spec:
  replicas: 1
  template:
    metadata:
      labels:
        run: my-nginx
    spec:
      containers:
      - name: my-nginx
        image: wangyanglinux/myapp:v1
        ports:
        - containerPort: 80
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
      volumes:
        - name: config-volume
          configMap:
            name: log-config

```

![20200208162855401.png](https://img-blog.csdnimg.cn/20200208162855401.png)

修改 ConﬁgMap<br>  

```
$ kubectl edit configmap log-config
```

![20200208163131606.png](https://img-blog.csdnimg.cn/20200208163131606.png)

![20200208163236166.png](https://img-blog.csdnimg.cn/20200208163236166.png)

ConﬁgMap 更新后滚动更新 Pod<br> 更新 ConﬁgMap 目前并不会触发相关 Pod 的滚动更新，可以通过修改 pod annotations 的方式强制触发滚动更新<br>  

```
$ kubectl patch deployment my-nginx --patch '{"spec": {"template": {"metadata": {"annotations": 
{"version/config": "20190411" }}}}}'

```

 

**这个例子里我们在 .spec.template.metadata.annotations 中添加 version/config ，每次通过修改 version/config 来触发滚动更新**

**！！！ 更新 ConﬁgMap 后： **

**使用该 ConﬁgMap 挂载的 Env 不会同步更新 **

**使用该 ConﬁgMap 挂载的 Volume 中的数据需要一段时间（实测大概10秒）才能同步更新 **

 

 

 

 
