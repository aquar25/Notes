### 域名

可以在https://my.freenom.com申请免费的域名，后缀为gq ml tk每次12个月的免费，时间到前14天系统会发邮件提示，在Service--Renew Domain把之前申请的重新激活12个月即可。

##### freenom域名使用

1. 点击**Manage Freenom DNS**设置域名解析。 

   在**Name**中填写域名记录（比如**@是toyo233.cf**、**www是www.toyo233.cf**等等），**Type（类型）**根据主机空间商提供的方式选择（如果给你的是一个**独立ip**那就选**A记录**，如果是个**ipv6的ip**那就选**AAAA记录**，如果是一个**共享IP或者域名**那就选**CNAME记录**），在**Target**中填写主机空间商提供的**IP或者域名**，然后点击**Save Changes**保存。如果想要添加更多请点**More Records**按钮。 

2. 在**Management Tools——Nameserver**中可以更改DNS服务器，**Use custom nameservers (enter below)**是自定义DNS服务器，改完之后点**Change Nameservers**保存。**（切记不要短时间内多次更换dns，容易导致一些解析问题！）** 

3. 在**Management Tools——URL Forwarding**中也可以设置**URL转发**，建议选择301重定向。 



##### [使用 CloudXNS 接管 Freenom 的免费域名解析，加快国内生效速度](https://doubmirror.cf/1jg9z3mv-2.html)

1. **注册一个CloudXNS账号**，[官网](http://www.cloudxns.net/) 
2. 进入[域名控制台](https://www.cloudxns.net/Record/index.html?z_id=78887)，然后点击 **添加域名** ，输入你要添加的域名（注意是顶级域名 xxxx.xx，如图）并点 **确定** 
3. 提示你**域名未被接管**，让你去**域名管理处（Freenom）修改DNS为CloudXNS的DNS** 
4. 去[Freenom域名管理处](https://my.freenom.com/clientarea.php?action=domains)（**Domains=> My Domains**），找到你要 **接管的域名（dou-bi.ml）** ，点击最后的 **Manage Domain** 
5. **Management Tools中的 Namesevers**，**选择第二个自定义DNS服务器**，并把默认的DNS改成 **CloudXNS提醒你要修改的四个DNS服务器**。然后点**Change Nameserver保存**。 
6. 只要等**1~6个小时**CloudXNS就会提示你域名接管成功（当然如果你运气不好的话可能会多一些，DNS服务器更换**全球生效时间是48小时**，如果你超过48小时还没提示接管成功，那你肯定前面有步骤出现错误，请仔细检查！） 
7. 当你域名接管成功的时候，你就不需要去Freenom设置域名解析了，剩下所有的域名解析服务都在CloudXNS执行
8. 在我的域名--添加记录。如果是共享ip的虚拟主机，设置Host Record为二级域名文本例如mm，Type为CNAME，Recorded value 添写主机商给的域名即可

这里我再说明一次， **dou-bi.ml** 是顶级域名， **www.dou-bi.ml** 是二级域名， **www.233.dou-bi.ml** 是三级域名，**二级域名和三级域名都称为子域名**。

**主机记录** 指的是你的**子域名文本**，比如 **www.dou-bi.ml** ， **www** 就是这个子域名的主机记录。

那有人会问 **dou-bi.ml** 是怎么用的？其实 **dou-bi.ml** 的主机记录是 **@** 。

一般如果你是买的**虚拟主机**，往往他们都是给你一个**共享的IP（域名）**让你去解析，这时候你就需要 **CNAME记录类型**了。

如果你是自己买的**VPS搭建虚拟主机**，那一般都是 **独立IP**，那就是使用 **A 记录类型**，**记录值也是填的你的 VPS IP**