### Nginx

#### Install

1. add the nginx repository key file, download it [nginx_signing.key](http://nginx.org/keys/nginx_signing.key) and run `sudo apt-key add nginx_signing.key`

2. add the sources file, edit `/etc/apt/sources.list` file with:

   ```ini
   deb http://nginx.org/packages/ubuntu/ xenial nginx
   deb-src http://nginx.org/packages/ubuntu/ xenial nginx
   ```

   ​

3. install with `sudo apt-get update` and `sudo apt-get install nginx`

4. start the service `sudo service nginx start`



#### Config

* Config file path `/etc/nginx/nginx.conf `其中使用`include /etc/nginx/conf.d/*.conf;`引用了一个默认配置`default.conf`.用户可以自己在conf.d目录下添加需要的xxx.conf文件来配置不同的server

##### Config a http file server
1. 在`/etc/nginx/conf.d/`目录下新建HttpFileServer.conf
2. 编辑文件为：
```ini
server {
        client_max_body_size 4G;        
        listen  8090;  ## listen for ipv4; this line is default and implied 
        server_name    XXX;  ##你的主机名或者是域名
	root /home/edison/nginx/fileserver;
	    location / {
		 autoindex on; ##显示索引
         autoindex_exact_size on; ##显示大小
		 autoindex_localtime on;   ##显示时间
        }
}
```

3. reload the configure `sudo /etc/init.d/nginx reload` or `sudo service nginx reload`

##### 常见问题

1. 当配置root目录为/media/xxx挂载目录时，出现403错误

   Nginx在以Linux service脚本启动时，通过start-stop-domain启动，会以root权限运行daemon进程。然后daemon进程读取/etc/nginx/nginx.conf文件中的user配置选项，默认这里的user=nginx。通过执行`ps -aux | grep nginx`也可以看到用户名为nginx。而/media/xxx目录的权限为root。因此，需要将user=nginx替换成root，然后重新启动nginx。

   其他方法也试过，比如给/home/dean/work/resources目录设置777权限，比如将nginx用户加入root组，都不行。 当开发的时候，就用user=root配置吧。至于产品环境下，resouces目录完全可以放到nginx用户目录下。



