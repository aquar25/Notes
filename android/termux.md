##Termux



###SSH

pkg install openssh

使用**ssh-keygen**生成密钥，如果用windows下的**puttygen.exe**生成的key文件会有注释，需要自己删除，并修改为ssh-rsa开始，且中间不能有任何换行。我自己使用了git安装时自带的ssh-keygen

其中id_rsa.pub的公钥放到手机~里面

执行cat  id_rsa.pub > ./.ssh/authorized_keys

chmod 700 .ssh

chmod 600 ./.ssh/authorized_keys

sshd &



PC client

xshell选择用户私钥为之前生成的没有扩展名的文件

ssh的地址192.168.43.1 端口为8022

192.168.43.1是手机作为热点的ip地址

 用户名可以不用输入即可连接到手机

可以在Xshell的设置中配置sftp的默认目录，点击工具栏的new file transfer，就可以建立一个sftp连接。默认会弹出提示安装xftp插件，选择取消，使用sftp命令就足够了。 

在`sftp>`下，get xxx从PC上获取文件到服务器。put为下载手机文件到电脑中配置的sftp目录

`cp -u src dst`只拷贝更新的文件，增量拷贝。



### 存储卡

存储卡目录`/storage/emulated/0/`

获取存储卡权限`termux-setup-storage`，执行后会在home目录创建`storage`的符号链接，其中有其他几个子目录

```bash
$ ls -l storage/
total 0
dcim -> /storage/emulated/0/DCIM
downloads -> /storage/emulated/0/Download
movies -> /storage/emulated/0/Movies
music -> /storage/emulated/0/Music
pictures -> /storage/emulated/0/Pictures
shared -> /storage/emulated/0
```

给UC的下载目录设置符号链接，注意必须是完整的路径

`$ ln -s /data/data/com.termux/files/home/storage/shared/UCDownloads uc`





