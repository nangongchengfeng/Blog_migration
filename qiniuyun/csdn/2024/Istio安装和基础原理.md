---
author: 南宫乘风
categories:
- Kubernetes项目实战
date: 2024-01-12 17:19:48
description: 、简介是一个开源服务网格，它透明地分层到现有的分布式应用程序上。强大的特性提供了一种统一和更有效的方式来保护、连接和监视服务。是实现负载平衡、服务到服务身份验证和监视的路径只需要很少或不需要更改服务代。。。。。。。
image: ../../title_pic/32.jpg
slug: '202401121719'
tags:
- istio
- 云原生
title: Istio安装和基础原理
---

<!--more-->


## 1、Istio简介
Istio 是一个开源服务网格，它透明地分层到现有的分布式应用程序上。 Istio 强大的特性提供了一种统一和更有效的方式来保护、连接和监视服务。 Istio 是实现负载平衡、服务到服务身份验证和监视的路径——只需要很少或不需要更改服务代码。它强大的控制平面带来了重要的特点，包括：

- 使用 TLS 加密、强身份认证和授权的集群内服务到服务的安全通信
- 自动负载均衡的 HTTP, gRPC, WebSocket，和 TCP 流量
- 通过丰富的路由规则、重试、故障转移和故障注入对流量行为进行细粒度控制
- 一个可插入的策略层和配置 API，支持访问控制、速率限制和配额
- 对集群内的所有流量(包括集群入口和出口)进行自动度量、日志和跟踪

![在这里插入图片描述](../../image/2f1a38df2ec84e9db975a1a4ec548270.png)

Istio 主要由两部分组成，分别是数据平面和控制平面。

* **数据平面**：数据平面或者数据层是由代理服务的集合所组成的，它们会使用扩展的 [Envoy](https://www.envoyproxy.io/) 代理服务器，表现形式是每个 Kubernetes pod 中的 sidecar 容器。这些 sidecar 会协调和控制所有微服务之间的网络通信，同时还会收集和报告有用的遥测数据。
* **控制平面**：控制平面或者控制层由一个名为 *istiod* 的二进制文件组成，负责将高层级的路由规则和流量控制行为转换成 Envoy 的特定配置，然后在运行时将它们传播到 sidecar 中。除此之外，控制平面还提供安全措施，通过内置的身份标识和证书管理，实现强大的服务间和终端用户认证，同时根据服务的身份标识执行安全策略。

## 2、Istio 核心功能
![在这里插入图片描述](../../image/86a653ce40634bc797878b6c42836ca6.png)
Istio 是一个与 Kubernetes 紧密结合的服务网格(Service Mesh)，用于**服务治理**。

注意，Istio 是用于服务治理的，主要有流量管理、服务间安全、可观测性这几种功能。在微服务系统中，会碰到很多棘手的问题，Istio 只能解决其中一小部分。

服务治理有三种方式，第一种是每个项目中包含单独的治理逻辑，这样比较简单；第二种是将逻辑封装到 SDK 中，每个项目引用 SDK 即可，不增加或只需要少量配置或代码即可；第三种是下沉到基础设施层。Istio 便是第三种方式。
![在这里插入图片描述](../../image/c1c1f7ee4d4749caae149d0dab6184fe.png)
![在这里插入图片描述](../../image/a7ba4d8536644bfa8e4a07ddaa7b0875.png)
##  3、Istio 原理
Istio 可以的作用原理是拦截 Kubernetes 部署 Pod 的事件，然后从 Pod 中注入一个名为 Envoy 的容器，**这个容器会拦截外部到业务应用的流量**。由于所有流量都被 Envoy “劫持” 了，所以 Istio 可以对流量进行分析例如收集请求信息，以及一系列的流量管理操作，也可以验证授权信息。当 Envoy 拦截流量并执行一系列操作之后，如果请求没问题，就会转发流量到业务应用的 Pod 中。
![在这里插入图片描述](../../image/77ce429f7a4945fda403628a1aae4806.png)
【左：普通 Pod；Istio；右：Istio 代理了出入口流量】

当然，由于 Envoy 需要拦截流量之后转发给业务应用，这样就多了一层转发，会导致系统响应速度会有所下降，**但是增加的响应时间几乎可以忽略不计**。

每个 Pod 都有一个 Envoy 负责拦截、处理和转发进出 Pod 的所有网络流量，这种方式被称为 Sidecar。

以下是 Istio Sidecar 的一些主要功能：

* 流量管理：Envoy 代理可以根据 Istio 配置的路由规则（如 VirtualService 和 DestinationRule）实现流量的转发、分割和镜像等功能。
* 安全通信：Envoy 代理负责在服务之间建立安全的双向 TLS 连接，确保服务间通信的安全性。
* 遥测数据收集：Envoy 代理可以收集关于网络流量的详细遥测数据（如延迟、成功率等），并将这些数据上报给 Istio 的遥测组件，以便进行监控和分析。
* 策略执行：Envoy 代理可以根据 Istio 配置的策略规则（如 RateLimit 和 AuthorizationPolicy）执行限流、访问控制等策略。

由于 Pod 是通过 Envoy 暴露端口的，所有进出口流量都需要经过 Envoy 的检查，所以很容易判断访问来源，**如果请求方不是在 Istio 中的服务，那么 Envoy 便会拒绝访问。**
![在这里插入图片描述](../../image/4948196811584fb89107b9e1330fe788.png)
在 Istio 中，Envoy 这一块称为数据平面，而负责管理集群的 istiod 组件称为控制平面。

> 注意，这里是 istiod ，是 Istio 负责管理集群的一种组件。
> 
> ![在这里插入图片描述](../../image/67002026b8a34e9d94d221d236971b5d.png)

## 4、Istio 安装
```bash
istioctl(可以通过curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.20.1 sh 安装)

[root@bt ~]# istioctl profile list
Istio configuration profiles:
    ambient
    default
    demo
    empty
    external
    minimal
    openshift
    preview
    remote

或者 
安装profile=demo的 istio

istioctl manifest apply --set profile=demo \
--set cni.enabled=true --set cni.components.cni.namespace=kube-system \
--set values.gateways.istio-ingressgateway.type=ClusterIP

```
![在这里插入图片描述](../../image/2729299d0bb0415a981a8017b59c453e.png)
设置自动 istio 注入，可以通过 namespace 去做
```bash
#给ns1的命名空间添加istio标签，那么在这个标签里，所有创建的 pod 都会被自动注入 istio
kubectl label ns ns1 istio-injection=enabled

# 查看labels
kubectl get ns --show-labels
```

使用 istio 单独的注入一个pod
```bash
# 创建
istioctl kube-inject -f pod1.yaml | kubectl apply -f -

# 查看pod数量
kubectl get pods  #此时READY数为2

#这个pod新增的docker，就是 pilot，envoy


## 在创建一个 pod 测试
sed 's/pod1/pod2/' pod1.yaml | kubectl apply -f -
kubectl get pods  # 发现这个 pod2 是没有被注入的
```

安装kiali ：图形化工具，可以直观的查看流量

```bash
kubectl get pods -n istio-system

# 安装
kubectl apply -f istio-1.10.3/samples/addons/kiali.yaml
# 或者可以选择直接全部都安装上
kubectl apply -f istio-1.10.3/samples/addons/

kubectl get svc -n istio-system
# kiali 的PORT：20001，TYPE为 ClusterIP

# 修改 kiali 的 svc
kubectl edit svc kiali -n istio-system

  sessionAffinity: None
  type: LoadBalancer  #把ClusterIP修改为NodePort或者LoadBalancer
  
# 查看并验证
kubectl get svc -n istio-system 
# 查看 kiali 的 ip 和端口，使用浏览器访问
# 进入浏览器后可以测试一下，进入 Graph 页面，选择 istio-system 和 ns1 的 Namespace，可以看到我们现在环境中的拓扑图
```
![在这里插入图片描述](../../image/a88cd035f9cf4e0381de93ac69b399bd.png)
![在这里插入图片描述](../../image/f8057c5529654ac091246af54ca1351d.png)![在这里插入图片描述](../../image/1fc389afb0de4656983f3f107404f515.png)

Kiali 的 Graph 数据主要来自两个来源：Prometheus 和 Istio 本身的遥测数据。

Prometheus：Prometheus 是一个开源监控和警报工具，它用于收集和存储 Istio 服务网格中的指标数据。Istio 使用 Envoy 代理收集遥测数据，这些数据随后被 Prometheus 抓取和存储。Kiali 使用这些 Prometheus 数据来生成服务之间的流量、错误率、延迟等指标。

Istio 遥测数据：Istio 服务网格生成的遥测数据包括请求、响应、延迟以及 Envoy 代理的其他性能指标。这些数据由 Istio 组件（例如 Mixer 和 Pilot）以及 Envoy 代理本身生成。Kiali 从这些遥测数据中获取服务拓扑信息，以创建服务之间的依赖关系图。

Kiali 将这两个数据源的信息整合在一起，生成 Graph，它展示了服务网格的拓扑结构、服务之间的流量以及其他性能指标。这有助于用户更好地理解服务之间的依赖关系，发现潜在的性能问题，并优化服务网格配置。

**可能失败的原因**
如果你的 Kiali 一直显示 Empty Graph。请关注以下几种可能的情况：

集群版本低于 1.23 ，需要升级 Kubernetes 集群。
安装了 Kubesphere，说多了都是泪，Kubesphere 太重了，笔者花了一晚上时间重新安装集群。
访问的地址不正确，没有配置对 /productpage 的访问地址，请求流量没有打入集群。
Pod 没有被注入 istio-proxy。
你可以在 Kiali 的 Workloads 查看每个负载的 Pod 信息，正常情况应当如下所示：
![在这里插入图片描述](../../image/504be137206f437391cc3567807e23ba.png)
**修复 Kiali Grafana 问题**
点击右上角的消息，可能会提示配置不正确，因为 kiali 需要从 Grafana 拉取数据。
![在这里插入图片描述](../../image/81807b683c51476bae62b69a779ffe31.png)
编辑 configmap 。
```bash
 kubectl edit configmap kiali -n istio-system

 grafana:  \n    enabled: true  \n    url: \"http://grafana.istio-system.svc.cluster.local:3000\"
    \ \n    in_cluster_url: \"http://grafana.istio-system.svc.cluster.local:3000\"\n

如果上方不行，就添加下方

 grafana:  \n    enabled: true  \n    url: \"http://grafana.istio-system.svc.cluster.local:3000\"

```


![在这里插入图片描述](../../image/6ed5e168d3d8422585d8ba4fda71785c.png)
如果使用的是可视化工具，添加就简单了。
```bash
      grafana:  
        enabled: true  
        url: "http://grafana.istio-system.svc.cluster.local:3000"  
        in_cluster_url: "http://grafana.istio-system>.svc.cluster.local:3000"
```
![在这里插入图片描述](../../image/64c509b739c54ac8aa29022ac4047f56.png)
然后使用 kubectl describe configmap kiali -n istio-system 查看配置是否正确。

## 5、Istio核心资源

和Kubernetes资源一致，Istio的配置也是通过声明式自定义资源配置来加载的。常用的核心资源有VirtualService、DestinationRule、Gateway、ServiceEntry、Sidecar等。

Gateway 类似 Nginx 需要创建一个反向代理时需要绑定的域名配置。


Istio VistualService 中可以限制外部能够访问的路由地址，


DestinationRule 则可以配置访问的 Pod 策略。


可以为 Istio VistualService 绑定一个 Istio DestinationRule

通过 DestinationRule 我们还可以定义版本子集等，通过更加丰富的策略转发流量。
![在这里插入图片描述](../../image/786e56e6fe884a1e8eacaae5bb6b803b.png)

 1. **istio-ingressgateway（邮局的入口）：**  当一个请求（邮件）到达你的应用时，它首先会到达istio-ingressgateway。这就像一个邮局的入口，所有的邮件都必须先经过这里。
2. **Gateway（邮局的接收员）：**  Gateway就像是邮局的接收员，它的工作是检查每个进来的请求（邮件），看看它应该被发送到哪里。在你的例子中，Gateway会把所有的请求都发送到`bookinfo`服务。
3. **VirtualService（邮局的分拣员）：**  当请求（邮件）到达`bookinfo`服务时，VirtualService就像是一个分拣员，它会根据请求的路径或者其他属性，决定请求应该被发送到哪个服务。在你的例子中，`productpage`的VirtualService可能会把请求发送到`productpage`服务。
4. **DestinationRule（邮局的包装员）：**  当请求（邮件）被发送到一个特定的服务时，DestinationRule就像是一个包装员，它会根据规则，决定如何处理这个请求（邮件）。例如，它可能会决定请求应该被发送到哪个版本的服务，或者请求应该如何被负载均衡。
5. **Envoy（邮局的快递员）：**  当`productpage`服务需要访问其他服务（如`reviews`）时，它会发送一个请求。这个请求就像是一个新的邮件，它会被Envoy（快递员）拿到，然后根据VirtualService和DestinationRule的规则，被发送到正确的服务。


在 Istio 中，VirtualService 和 DestinationRule 是两个关键的自定义资源定义（CRD），它们用于配置和控制服务间的流量路由。

它们之间的关系可以概括为：

* VirtualService 定义了流量的路由规则，

* DestinationRule 定义了**流量到达目的地后如何进行负载分发和连接池管理**。

**VirtualService 用于定义流量的路由规则。** 当请求从一个服务到另一个服务时，VirtualService 可以指定如何将流量路由到不同的目的地（例如，不同的服务实例，版本或子集）。VirtualService 还可以根据请求的属性（如请求头、路径、来源等）对流量进行匹配和分发。此外，VirtualService 可以配置复杂的路由行为，如重试、超时和故障注入等。

**DestinationRule 被用于控制流量的分发和连接池管理。** DestinationRule 定义了服务的子集（即服务的不同版本或变体），并指定如何根据负载均衡策略（如轮询、随机、最少连接等）将流量分发到这些子集。此外，DestinationRule 还可以配置连接池设置（如最大连接数、空闲超时等）和传输层安全策略（如 TLS 设置）。

> 总之，VirtualService 和 DestinationRule 在 Istio 中共同实现了流量的精细控制。VirtualService 用于定义流量的路由规则，而 DestinationRule 则负责处理流量到达目的地后的负载分发和连接池管理。
> Istio 的做法是 Gateway 监控入口流量，
> 通过 VirtualService 设置**流量进入的策略**，并指向 Service。
> 而 DestinationRule 则定义了**流量流向 Pod 的策略**。


### VirtualService

VirtualService（虚拟服务）和Kubernetes的Service类似，但是两种并不是对等的资源类型。VirtualService基于Istio和对应平台提供的基本连通性和服务发现能力，将请求路由到对应的目标。每一个VirtualService包含一组路由规则，Istio将每个请求根据路由匹配到指定的目标地址。

和Kubernetes的Service不同的是，Kubernetes的Service只提供了最简单的服务发现和负载均衡的能力，如果想要实现更加细粒度的流量分发，比如灰度、蓝绿等流量管理，Kubernetes的Service显得比较吃力或者无法实现，而VirtualService在流量管理方面有着比较好的灵活性和有效性，可以在代码零侵入的情况下实现更加丰富的流量管理，比如灰度等。

一个典型的用例是将流量发送到被指定服务的不同版本，比如80%的流量发送给v1版本，20%的流量发送给新版本。或者将某个登录用户指定到新版本，其他用户指定到旧版本，可以实现AB测试等功能。

接下来看一个VirtualService的配置示例，根据特定用户将流量分发至不同版本：
```bash
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - reviews
  http:
  - match:
    - headers:
        end-user:
          exact: jason
    route:
    - destination:
        host: reviews
        subset: v2
  - route:
    - destination:
        host: reviews
        subset: v3
```
上面参数说明:

* apiVersion：对应的API版本
* kind：创建的资源类型，和Kubernetes的Service类似
* metadata：元数据，和Kubernetes资源类似，可以定义annotations、labels、name等
* metadata.name：VirtualService的名称
* spec：关于VirtualService的定义
* spec.hosts：VirtualService的主机，即用户指定的目标或路由规则的目标，客户端向服务端发送请求时使用的一个或多个地址，可以是IP地址、DNS名称，或者是依赖于底层平台的一个简称（比如Kubernetes的Service短名称），隐式或显式地指向一个完全限定域名（FQDN），当然也可以是一个通配符"*"
* spec.http：路由规则配置，用来指定流量的路由行为，通过该处的配置将HTTP/1.1、HTTP2和gRPC等流量发送到hosts字段指定的目标
* spec.http[].match：路由规则的条件，可以根据一些条件制定更加细粒度的路由。比如当前示例的headers，表示匹配headers里面的end-user字段，并且值为jason的请求
* route：路由规则，destination字段指定了符合此条件的流量的实际目标地址。比如该示例的请求，如果请求头包含end-user=jason字段，则该请求会被路由到reviews的v2版本。如果没有匹配到该请求头，则流量会被路由到v3版本（版本由DestinationRule划分）



**注意：VirtualService路由规则按照从上往下的顺序进行匹配，第一个规则有最高的优先级，如果不满足第一个路由规则，则流量会选择下一个规则。**

除了上述的路由匹配外，VirtualService也支持域名+路径的方式进行路由。比如后端有两个服务，一个是reviews，通过[http://](https://link.zhihu.com/?target=http%3A//bookinfo.com/reviews)​**[bookinfo.com/reviews](https://link.zhihu.com/?target=http%3A//bookinfo.com/reviews)**访问；另一个是ratings，通过[http://](https://link.zhihu.com/?target=http%3A//bookinfo.com/ratings)​**[bookinfo.com/ratings](https://link.zhihu.com/?target=http%3A//bookinfo.com/ratings)**访问。此时可以配置VirtualService如下：
```bash
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: reviews
spec:
  hosts:
  - bookinfo.com
  http:
  - match:
    - uri:
       prefix: /reviews
    route:
    - destination:
        host: reviews
  - match:
    - uri:
       prefix: /ratings
    route:
    - destination:
        host: ratings

```

### DestinationRule
将VirtualService理解为Kubernetes Service层面，DestinationRule理解为Service后端真实的目标地址，即VirtualService用于Service层面的路由管控，DestinationRule用于对后端真实的服务再做进一步的划分。比如存在一个Service名为paycenter，指向后端多个paycenter的Pod（该Pod可能是不同的Deployment创建的），而DestinationRule可以对后端的多个Pod区分新旧版本，划分成不同的subnet，之后VirtualService可以针对不同的版本进行流量管控。

在下面的示例中，目标规则为 my-svc 目标服务配置了 3 个具有不同负载均衡策略的子集：
```bash
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-destination-rule
spec:
  host: my-svc
  trafficPolicy:
    loadBalancer:
      simple: RANDOM
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
  - name: v3
    labels:
      version: v3
```
上面参数说明：

* `trafficPolicy`：这是一个用于定义流量策略的部分。在这个例子中，定义了三个子集（`subsets`）的流量策略
* `loadBalancer`：用于指定负载均衡算法的配置
* `subsets`：这里定义了三个子集（v1、v2、v3），每个子集通过 `labels` 来选择对应版本的服务实例。第一个子集 `v1` 对应版本为 `v1` 的服务实例，并使用 `simple: RANDOM` 负载均衡策略。这意味着请求将随机路由到 `v1` 子集中的服务实例；第二个子集 `v2` 对应版本为 `v2` 的服务实例，并使用 `simple: ROUND_ROBIN` 负载均衡策略。这意味着请求将以循环方式（Round Robin）路由到 `v2` 子集中的服务实例；第三个子集 `v3` 对应版本为 `v3` 的服务实例。在这里没有指定负载均衡策略，因此将使用默认的负载均衡策略。

每个子集都是基于一个或多个 `labels` 定义的，在 Kubernetes 中它是附加到像 Pod 这种对象上的键/值对。这些标签应用于 Kubernetes 服务的 Deployment 并作为 `metadata` 来识别不同的版本。

除了定义子集之外，此目标规则对于所有子集都有默认的流量策略，而对于该子集， 则有特定于子集的策略覆盖它。定义在 `subsets` 上的默认策略，为 `v1` 和 `v3` 子集设置了一个简单的随机负载均衡器。在 `v2` 策略中，轮询负载均衡器被指定在相应的子集字段上

默认情况下，Istio 使用轮询的负载均衡策略，实例池中的每个实例依次获取请求。Istio 同时支持如下的负载均衡模型， 可以在 `DestinationRule` 中为流向某个特定服务或服务子集的流量指定这些模型。

* 随机：请求以随机的方式转发到池中的实例
* 权重：请求根据指定的百分比转发到池中的实例
* 最少请求：请求被转发到最少被访问的实例

###   Gateway

Istio同样支持网关功能，可以使用Gateway在网格最外层接收HTTP/TCP流量，并将流量转发到网格内的某个服务。

在安装Istio时，可以在istio-system命名空间下安装ingressgateway的Pod，用来充当Ingress Gateway。其中Ingress Gateway为入口网关，可以将网格内的服务“暴露”出去，一般和VirtualService配置使用，并配置一个可以被外部服务访问的域名，从而外部服务可以通过该域名访问网格内的服务。

配置Gateway和Istio其他资源类似，kind指定为Gateway即可。比如配置一个VirtualService和Gateway实现对网格内的某个服务进行发布，首先创建一个Gateway，代码如下：

```text
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: httpbin-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "httpbin.example.com"
```

上面参数说明：

* selector：必选字段。选择由哪个ingressgateway的Pod发布服务，默认为istio-system命名空间下具有istio=ingressgateway标签的Pod
* servers：必选字段。表示发布的服务列表，用于描述发布服务的属性，比如代理监听的端口、协议和端口的名称等
* hosts：必选字段。Gateway发布的服务地址，也就是允许用户访问的域名，可以配置为“*”，表示任何域名都可以被代理，本示例为http://httpbin.example.com可被路由

之后配置一个VirtualService与之匹配，即可通过该域名访问VirtualService配置的服务。比如将http://httpbin.example.com的/status和/delay代理到httpbin服务的8000端口：

```text
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: httpbin
spec:
  hosts:
  - "httpbin.example.com"
  gateways:
  - httpbin-gateway
  http:
  - match:
    - uri:
       prefix: /status
    - uri:
       prefix: /delay
    route:
    - destination:
        host: httpbin
        port:
          number: 8000
```

之后将域名解析至ingressgateway Pod的Service上即可访问该域名。
