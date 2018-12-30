## Caddy Web Server

Caddy是一个go实现的Web服务器，可以很好的支持Http2和Https

[下载地址](https://caddyserver.com/download)

在下载页面可以选择运行的系统和需要的插件，可以把几乎所有的默认插件都勾选了，实际编译出来的二进制文件也不到50M，官网根据选择的插件编译一个版本给用户下载。服务器只有一个可执行文件`Caddy.exe`

如果官方的服务器维护无法下载时，需要到[Github](https://github.com/mholt/caddy)上下载release版本，但是没有插件。

### 基本使用

* 在命令行下执行`caddy.exe`后以当前目录为服务器的根目录
* 服务器的默认端口为2015，访问http://127.0.0.1:2015 返回404文字（因为没有服务默认的index网页），说明服务器启动成功

### 基本配置

当第一次使用域名启动caddy时，它会提示输入一个邮箱地址，Caddy用来验证你拥有这个域名并把证书安全的存储在磁盘上。

默认的配置文件名称为**Caddyfile** ，也可以使用`caddy -conf C:\path\to\Caddyfile `指定一个配置文件

```json
localhost:8080
gzip
log ./access.log  # log file
markdown /blog {
    css /blog.css
    js  /scripts.js
}
```

### 指令

在一个站点地址下方的内容以一个指令开始，指令是Caddy识别的关键字，例如gzip是一个HTTP指令。

一个指令可以有一个或多个参数。如果一个指令需要更多的配置，可以把这些配置使用`{ }`包成一个块，大括号的对齐必须使用行尾和结束的右括号独占一行的规则。

参数中如果有空格，参数需要使用`" "`包起来, `#`标识一个行注释

如果要在一个配置文件中配置多个站点，每个站点都要用`{ }`定义一个块，站点名称可以使用路径或者通配符的方式定义。站点地址格式`scheme://host:port/path `，如果不指定scheme，系统默认为https和443端口，如果要使用http，则必须指定scheme为http.

```json
# 多个站点使用相同的配置
localhost:8080, https://site.com, http://mysite.com { 
    root /www/mysite.com
}

example.com/static, *.example.com { # 一个独立的配置
    root /www/sub.mysite.com
    gzip
    log ./access.log
}
```

配置文件中的地址和参数可以使用系统的环境变量，环境变量使用`{ }`包起来就行

```json
localhost:{$PORT} # for *nix 
root {%SITE_ROOT%} # for windows
```

所有的配置不支持继承，一个站点只能配置一次，如果需要需要复用一些公共配置，可以使用`import`指令

#### 占位符

部分指令支持使用`{var}`格式的占位符，这样可以动态获取请求的数据或响应数据，例如`{host}`表示了请求的主机名

#### 代理 proxy

Caddy可以支持服务器反向代理和负载均衡。这个中间件提供一个 **{upstream}**  占位符，可以用在log中间件中。

```json
proxy from to... { # from 被代理的请求地址 to 被代理的端点服务，可以有多个，默认为http服务，可以设置为srv+https://
	policy name [value] # 负载均衡策略
	fail_timeout duration # 值为10s或1m格式的时间长度，用来判断一个后端服务是否响应超时，默认为0
	max_fails integer # 如果一个后端响应超时的次数超过这个值，则认为这个后端挂了，后续不会给他请求了
	max_conns integer # 每个后端的最大连接数，默认为0，没有限制
	try_duration duration
	try_interval duration
	health_check path
	health_check_port port
	health_check_interval interval_duration
	health_check_timeout timeout_duration
	fallback_delay delay_duration
	header_upstream name value
	header_downstream name value
	keepalive number
	timeout duration
	without prefix
	except ignored_paths...
	upstream to # 指定另一个后端服务，可以设置多次，这个子指令无法使用to为服务
	insecure_skip_verify
	preset #预设值，可以简化配置。例如transparent可以代替header_upstream Host {host} header_upstream X-Real-IP {remote} header_upstream X-Forwarded-For {remote} header_upstream X-Forwarded-Proto {scheme}
}
```

* 举例 

创建4个服务实例，端口分别为8085 8086 8087 8088，并在hosts文件中增加一行`127.0.0.1 memorywalker.com`,使浏览器可以以域名方式访问服务。 配置8085的根目录访问的后端节点为8086和8087，且负载均衡的策略为循环，当访问8085时，`ctrl+F5`强制刷新，会在8086和8087之间循环。8088则指向了baidu

```json
http://memorywalker.com:8085 {
    gzip
	log ./memorywalker.log  # log file
	proxy / http://memorywalker.com:8086 http://memorywalker.com:8087 {
		policy round_robin  #load balance for each round
		health_check / # 使用后端的根目录作为检查后端是否可用的路径
		transparent
	}	
}

http://memorywalker.com:8086 {
    gzip
	log ./memorywalker8086.log  # log file	
	index index8086.html	
}

http://memorywalker.com:8087 {
    gzip
	log ./memorywalker8087.log  # log file
	index index8087.html
}

http://memorywalker.com:8088 {
	proxy / http://www.baidu.com
}
```

#### steam本地反向代理

1. 修改hosts `127.0.0.1 steamcommunity.com`
2. 配置本地代理服务，把社区的请求转到商店
3. 自签CA证书

```json
steamcommunity.com:443 {
    gzip
	tls ./steamcommunity.crt ./steamcommunity.key
    proxy / https://store.steampowered.com/ {
        transparent
		header_upstream Host steamcommunity.com
    }
}

https://:9581 {
#tls self_signed
	tls steamcommunity.crt steamcommunity.key
    # default/catchall
    proxy / https://playartifact.com https://steamcdn-a.akamaihd.net https://steamstore-a.akamaihd.net https://steamcommunity-a.akamaihd.net https://steampipe.akamaized.net https://origin-a.akamaihd.net https://blzddist1-a.akamaihd.net https://blzddistkr1-a.akamaihd.net https://eaassets-a.akamaihd.net https://humblebundle-a.akamaihd.net https://store.steampowered.com {
    policy random
    fail_timeout 5s
    timeout 30s
    transparent
    header_upstream Host steamcommunity.com
    #header_downstream Host steamcommunity.com
    #insecure_skip_verify
    }
}
```



#### Markdown支持

```json
markdown [basepath] {
	ext         extensions...
	[css|js]    file
	template    [name] path
	templatedir defaultpath # 默认的模板文件路径
}
```

* `basepath` 只有请求的URL以此为前缀时才会启用markdown指令，默认为根目录
* `extensions`空格分隔的文件扩展名列表，例如`md mdown`，如果不设置默认为md
* `[css|js]` 指出页面渲染使用的css和js文件，可以写多个这个指令来使用多个文件
* `[name] path` 指出使用的模板文件名和模板文件的路径，如果使用默认模板，name为空

Markdown格式的文件可以在文件开头增加Front Matter（扉页）用来说明这个文档中的一些元变量。这个信息可以使用TOML、YAML或JSON格式。例如有Markdown文件如下.其中说明了渲染使用的模板，以及模板可以使用的metadata

```markdown
{
	"template": "blog",
	"title": "Blog Homepage",
	"sitename": "Live site"
}

### live

* go
```

* 模板文件 模板可以使用`{{.Doc.variable}}`格式使用变量，可以是Markdown文件头定义的，也可是Caddy支持的Template Actions。

```html
<!DOCTYPE html>
<html>
	<head>
		<title>{{.Doc.title}}</title>
	</head>
	<body>
		Welcome to {{.Doc.sitename}}!
		<br><br>
		{{.Doc.body}}
		
		<p>My IP is {{.ServerIP}} your IP is {{.IP}}</p>
		<p>Request URI is {{.URI}}</p>
		file list of mdfiles/
		<p>
		{{.Context.Files "./mdfiles/"}}
		</p>
	</body>
</html>
```

* 服务器配置文件

```json
http://memorywalker.com:8085 {
    gzip
	log ./memorywalker.log  # log file
	markdown /mdfiles { #当访问这个路径下的文件时，以markdown模式解析
		css /mdfiles/blog.css
		js  /mdfiles/scripts.js
		template /mdfiles/default.html
		template blog /mdfiles/blog.html # 定义一个名称为blog的模板
	}
}
```

### 插件

#### forwardproxy

使Caddy作为一个转发代理服务器。这个插件支持Access Control Lists and authentication 。特色功能如防止探测，可以让你的服务器作为一个转发代理工作，而不被探测到。

地址https://github.com/caddyserver/forwardproxy

使用举例 https://medium.com/@mattholt/private-browsing-without-a-vpn-e91027552700

```
http://memorywalker.com:8095 {
	gzip
	log ./caddy8095.log  # log file
    forwardproxy {
		basicauth mem 123456  # 代理服务器的用户名为mem，密码为123456
		probe_resistance secret.localhost
		hide_ip
	}
}
```

如果提示` [ERROR 0 ] Proxy-Authorization is required! Expected format: <type> <credentials>`，可以试下把用户登录认证去掉，再访问是否可行。

另外参考[issue #24](https://github.com/caddyserver/forwardproxy/issues/24) 需要在浏览器中访问"<http://secret.localhost/>"  

I highly recommend to choose unique secret link, so that censor could not possibly probe your server

```
probe_resistance myownlink123.localhost
```

### 其他

#### Chrome

chrome的网络配置入口`chrome://net-internals/`其中`chrome://net-internals/#dns`可以查看dns的数据

#### DNS

如果在hosts中添加一行`127.0.0.1 memorywalker.com`，且服务器配置为默认的80端口，在浏览器中无法打开`http://memorywalker.com`，需要把host中的地址设置为具体的ip地址例如`192.168.43.201 memorywalker.com`才行。实际上在浏览器中直接输入`127.0.0.1:80`也无法打开页面，是因为使用的steam302工具默认已经使用了127.0.0.1的80端口，如果关闭steam社区工具，就可以正常打开自己的服务器页面了。Caddy在端口冲突时居然没有提示。

配置自己的测试服务器的端口为8085后，访问`http://memorywalker.com:8085/`就可以，可以在浏览器的请求头中看到`Remote Address: 127.0.0.1:8085`

```json
# 
http://memorywalker.com {
    gzip
	log ./memorywalker.log  # log file
}

# 当80端口被占用后，127.0.0.1：8085可以打开，默认的80端口无法打开
http://memorywalker.com:8085 {
    gzip
	log ./memorywalker.log  # log file
}
```

