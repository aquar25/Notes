##Termux



###SSH

pkg install openssh

使用**ssh-keygen**生成密钥，其中id_rsa.pub的公钥放到手机~里面

执行cat  id_rsa.pub > ./.ssh/authorized_keys

chmod 700 .ssh

chmod 600 ./.ssh/authorized_keys

sshd &



PC client

xshell选择用户私钥为之前生成的没有扩展名的文件

ssh的地址192.168.43.1 端口为8022

192.168.43.1是手机作为热点的ip地址

 用户名可以不用输入即可连接到手机



存储卡目录`/storage/emulated/0`

