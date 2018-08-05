###Docker

#####DaoCloud 

添加新主机时可以选择免费胶囊主机，可以使用120min。方便用来学习Linux和docker的使用方法

创建一个胶囊主机后信息如下： 

Try_DaoCloud_1  
状态: 正常  
IP: 10.23.227.215 外网: 54.223.212.119  
主机名: ip-10-23-227-215 
Docker1.7.0: 运行正常  
连接主机: ssh ubuntu@54.223.212.119 密码: d6c9ccfdc3288284  
操作系统: Ubuntu 14.04.2 LTS  
部署标签:  

这个主机  
* ip为54.223.212.119
* 用户名：ubuntu
* 密码：d6c9ccfdc3288284 
windows下使用xshell就可以以ssh的方式登录，使用默认端口号即可。登录到主机后和使用自己的Linux系统一样，可以通过搭建ftp服务器将虚拟主机中的文件下载本地。

#####ubuntu中ftp服务
安装服务
`sudo apt-get install vsftp`
在windows下使用flashftp 使用上面的主机的用户名和密码登录ftp服务就可以访问默认的ftp目录。该目录对应主机上面的用户主目录`/home/ubuntu`

http://www.tuling123.com/openapi/api?key=54b47b9e41818baf882e0c663bdab3c6&info=hello&userid=apple; 