### shadowsocksR

网上下载的windows程序运行时会提示“Fatal Error Can't bind to 127.0.0.1:xxxx (error number 10106)”,经过在stackoverflow上查，原因是winsock的错误

```
Service provider failed to initialize. This error is returned if either a service provider's DLL could not be loaded(LoadLibrary failed)or the provider's WSPStartup or NSPStartup function failed.
```
To fix it, open cmd as admin, type the following and hit Enter. `netsh winsock reset`



### GCP SSR

#### 创建服务器

进入GCP的Console界面后，选择Compute Engine，进入VM instances，选择Create instance 

选择最低配置0.6G Cpu，选择一个地区后，Allow https/http traffic都勾选。

boot disk选择Centos 7

#### 配置服务器firewall

进入GCP的Console界面后，`networking` -- `VPC network` -- `External IP addresses`设置网络类型为静态

`networking` -- `VPC network` -- `firewall rules` 创建两个规则

Direction: Egress和Ingress各创建一个

Action on match : allow

Targets : All instances in the network

Destination filter : IP ranges

IP ranges: 0.0.0.0/0

Protocols and ports: Allow all

其他保持默认配置

#### 登录服务器

在创建的VM instance上的SSH列选择Open in Browser Window，可以自动以SSH方式登录，这种方式不需要密码，如果要用客户端在本地SSH登录，需要先通过网页的配置一下。

```bash
#sudo su // get the root 
#sudo passwd root // reset the password of root

// configure ssh using root and password login
#vi /etc/ssh/sshd_config // change he content as below

PermitRootLogin yes   // allow root ssh login
PasswordAuthentication yes // using password

#service sshd restart // restart the ssh service
```

* using XShell to login

new session with ssh and the VM instance ip. User name is root and password is just set.

* install BBR

  ```bash
  #yum install -y wget
  #wget --no-check-certificate https://github.com/teddysun/across/raw/master/bbr.sh
  #chmod +x bbr.sh
  #./bbr.sh
  // reboot the vm
  // check the version
  #uname -r // if the version is > 4.13 is ok
  // check 
  #sysctl net.ipv4.tcp_available_congestion_control
  // show follow info is right
  //net.ipv4.tcp_available_congestion_control = bbr cubic reno
  ```

  

  #### Install SSR

`wget -N --no-check-certificate https://softs.fun/Bash/ssrmu.sh && chmod +x ssrmu.sh && bash ssrmu.sh`

或者

`wget -N –no-checkcertificate https://raw.githubusercontent.com/ToyoDAdoubi/doubi/master/ssr.sh && chmod +x ssr.sh && bash ssr.sh`    

执行以上命令后，会进入配置模式，可以设置端口为17502，

加密选chacha20 

协议选auth_aes128_sha1

混淆选tls1.2_ticket_auth

配置完后，会自动进行安装。

使用`bash ./ssr.sh`查看状态和修改配置

如果使用了chacha20加密，还需要`bash ./ssr.sh`进入配置界面，安装libssodium，否则启动不成功。

在启动成功后，可以看到自动生成的服务地址。

