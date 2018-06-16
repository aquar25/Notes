####ubuntu 16.04 install

1. allocate 15G empty disk for system install
2. download the live cd file from the official website(1.2G)
3. save the file in C:\ubuntu-16.04-desktop-amd64.iso
4. extract vmlinuz.efi, initrd.lz(in directory casper ) and .disk from the iso file to C:\
5. install easybcd, add new item-> NeoGrub -> install --> configure, in the opened menu.lst file, clear all content and paste following code into it.
```
title Install Ubuntu
root (hd0,0)
kernel (hd0,0)/vmlinuz.efi boot=casper iso-scan/filename=/ubuntu-16.04-desktop-amd64.iso ro quiet splash locale=zh_CN.UTF-8
initrd (hd0,0)/initrd.lz
```
6. restart the windows, select the NeoGrub menu to install ubuntu system.

####upgrade my 16.04 to 18.04 LTS

1. all the same as the above ubuntu 16.04 install steps
2. when go to the select the partition, select the old boot partition and click change, format and use as /boot, do format also on the / partition. Please do not check the format for the /home partition, I still want the old files.
3. after the install, the system is new with old /home file left.
4. boot the ubuntu system by Easybcd on windows7: add new entry, select linux-> grub (legacy) -> select the boot partition, and give a new name Ubuntu 18.04. This will generate a mbr file with name `nst_linux-245D575CFD27300E2FE9BE42BCB5805A.mbr` under `c:\NST\`
5. when the PC startup, just select the Ubuntu 18.04

####Disk Partition
add new partition  `/` for system (14326M)
add new partition  `swap` (1536M)
add new Partition `/boot` for grub (200M)

####Move /home to a new partition
1.  Create a disk partion using gparted, and format the partion to ext4. Remember the partition's dev name, mine is `/dev/sda9`. Gparted is not installed with Ubuntu by default, so we need install it first. `sudo apt-get install gparted`. 
2.  mount the new partition and copy all the /home files to it. All of the operation must using root, so we need `sudo -i` to change the shell to `#`.
    * `~#mkdir /mnt/newhome`
    * `~#mount -t ext4 /dev/sda9 /mnt/newhome`
    * Now, Copy files over: Since the `/home` directory will have hardlinks, softlinks, files and nested directories, a regular copy (cp) may not do the job completely. Therefore, we use something we learn from the Debian archiving guide:
        * `~#cd /home/`
        * `~#find . -depth -print0 | cpio --null --sparse -pvd /mnt/newhome/`
    * `~#umount /mnt/newhome`
3.  move the home.
    * `sudo mv /home /old_home`
    * create a new home: `sudo mkdir /home`
    * mount the new home: `sudo mount /dev/sda9 /home`
4.  Tell the system the new home is at /dev/sda9
    * check the uuid of the new home partition: `ls -l /dev/disk/by-uuid` note the uuid of sda9 `b7e077de-e1fe-4937-bee4-1f65b0ca1f85`
    * edit the `/etc/fstab`, and add a line for the new home
    ```
    # /home was on /dev/sda9 during installation
    UUID=b7e077de-e1fe-4937-bee4-1f65b0ca1f85 /home            ext4    nodev,nosuid    0       2
    ```
5.  restart the system and check the size of /home is now bigger. using `df -kh` to check the mount information of current system. If everything is all right, just `sudo rm -r /old_home` 

####Video Card Driver
* install nvidia driver `sudo apt-get install nvidia-390 nvidia-prime`
* reboot the system, but we cant login with x-window
* cmd+alt+F1, login system with tty1
* check the system's default card `prime-select query`, this will output `nvidia`
* switch to intel video card, `prime-select intel`
* restart
* But there is just a wallpaper after I login the system successfully~. I can't see the status bar and laucher on the left side of desktop
* solution: Turn the Unity plugin back on [ref](http://askubuntu.com/questions/17381/unity-doesnt-load-no-launcher-no-dash-appears/)
  * cmd+alt+T open a terminal / or right click the desktop ->`Open terminal here`
  * Install compizconfig-settings-manager, `sudo apt-get install compizconfig-settings-manager`
  * Then run it with this: `DISPLAY=: ccsm` (The first part tells the terminal which display you want it to load on)
  * In the compizconfig-settings-manager, find the Unity plugin. Enable it.
  * If the desktop is still not work well, reboot the system


####GCC
`sudo apt-get install build-essential`

####Java Install
1. Download jdk from oracle website [Linux x64](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html).
2. `sudo mkdir /usr/local/java`
3. `sudo cp jdk-8u92-linux-x64.tar.gz /usr/local/java`
4. `cd /usr/local/java`
5. `sudo tar xvf jdk-8u92-linux-x64.tar.gz`
6. `sudo rm jdk-8u92-linux-x64.tar.gz`
7. Set the path `sudo gedit ~/.bashrc` add following code at the end of the file
    ```
    export JAVA_HOME=/usr/local/java/jdk1.8.0_92
    export JRE_HOME=${JAVA_HOME}/jre
    export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
    export PATH=${JAVA_HOME}/bin:$PATH
    ```
8. open a new terminal and check `java -version`

####Clang Install
1. Download pre-built binary file [Clang for x86_64 Ubuntu 16.04](http://llvm.org/releases/download.html)
2. `tar xvf clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz`
3. `cd clang+llvm-3.8.0-x86_64-linux-gnu-ubuntu-16.04`
4. `sudo cp -r * /usr/local`
5. `clang -v` check the verison 

####Install eclipse
1. Download eclipse-cpp-mars-2-linux-gtk-x86_64.tar.gz
2. 将 Eclipse 解压到 /opt/ 目录以供全局使用 `cd /opt/ && sudo tar -zxvf ~/Downloads/eclipse-*.tar.gz`
3. 创建快捷方式`sudo gedit /usr/share/applications/eclipse.desktop` add following code
```
[Desktop Entry]
Name=Eclipse
Type=Application
Exec=/opt/eclipse/eclipse
Terminal=false
Icon=/opt/eclipse/icon.xpm
Comment=Integrated Development Environment
NoDisplay=false
Categories=Development;IDE;
Name[en]=Eclipse
```

####Foxit Reader
1. Download from http://www.foxitsoftware.cn/downloads/
2. tar -zxvf Foxit*.gz to any tmp dir
3. sudo ./Foxit*.run and follow the intallation
4. intall the application to /opt/foxitsoftware/

#### SublimeText3

* 离线安装插件

  插件目录 /home/edison/.config/sublime-text-3/Packages/，将下载的zip文件内容解压到插件名称的文件中

####Code::Blocks

* The newest 16.01 is worked on ubuntu 16.04.1. ~~Xenial dumped wxWidgets 2.8, it's not even in repositories. code::blocks won't work on it, unless a version compiled with 3.0 is made available (and Jen's version won't work, it requires more recent libs than those available on hte repositories) or 2.8 is added back.---[link](http://askubuntu.com/questions/761159/codeblocks-in-a-xenial)~~
1. `sudo add-apt-repository ppa:damien-moore/codeblocks-stable`
2. `sudo apt-get update`
3. `sudo apt-get install codeblocks`

####Clion
1. Download from [here](http://www.jetbrains.com/clion/download/#section=linux-version)
2. `cd ~/program/ && sudo tar -zxvf /media/edison/other/downloads/CLion-2016.1.1.tar.gz`
3. Run CLion.sh from the bin subdirectory
4. Follows the Install-Linux-tar.txt in the CLion-2016.1.1 directory
5. License server http://idea.qinxi1992.cn/
6. cmake -D CMAKE_C_COMPILER=/usr/local/bin/clang -D CMAKE_CXX_COMPILER=/usr/local/bin/clang++

http://www.jetbrains.com/help/clion/2016.1/quick-cmake-tutorial.html?origin=old_help&search=clang
If, on the other hand, you want to explicitly specify the compiler to use, you can open up the options under File | Settings | Build, Execution, Deployment | CMake (or CLion | Preferences | Build, Execution, Deployment | CMake for OS X users) and specify the desired compiler by passing in the following string:
`-D CMAKE_<LANG>_COMPILER=[fully qualified compiler name]`
The LANG part specifies the language to compile (C for C and CXX for C++). You need to provide the full path to the compiler, for example:
`-D CMAKE_CXX_COMPILER=C:\MinGW\bin\g++`

clang cant support gdb debug in clion. In the cmake window, change the compiler and save.

```
(gdb) p x
$1 = (int &) @0x618c20: 9
(gdb) x /1ih 0x618c20
   0x618c20:	or     %eax,(%rax)
(gdb) x /1h 0x618c20
0x618c20:	0x0009
(gdb) x /10w 0x618c20
0x618c20:	0x00000009	0x00000008	0x00000007	0x00000006
0x618c30:	0x00000005	0x00000004	0x00000003	0x00000002
0x618c40:	0x00000001	0x00000000
(gdb) x /10b 0x618c20
0x618c20:	0x09	0x00	0x00	0x00	0x08	0x00	0x00	0x00
0x618c28:	0x07	0x00
```

####git
* git使用ssh方式的话每次pull或push就不用输入用户名和密码
* generate new ssh keys `ssh-keygen -t rsa -C "xxx@mail.com"`，默认会在~/.ssh/生成名称为`id_rsa`的私钥和`id_rsa.pub`的公钥
* add pub key to github: copy the content of id_rsa.pub to the SSH Keys of github setting
* `ssh -T git@github.com` test the key is set right.
* git同时支持多个服务器的方法
  windows `C:\Users\<username>\.ssh`
  Linux `~\.ssh`
  ssh目录下有使用ssh工具生成的公钥和私钥组合，和一个配置文件
```
coding_rsa      config      github_rsa.pub  id_rsa.pub
coding_rsa.pub  github_rsa  id_rsa          known_hosts
```
其中coding_rsa对应我在coding.net上的私钥，github_rsa对应我在github上的私钥，配置文件config的内容如下
```ini

#github
Host github.com
    HostName     github.com
    User         memorywalker
    IdentityFile ~/.ssh/github_rsa

Host git.coding.net
    HostName     git.coding.net
    User         memorywalker
    IdentityFile ~/.ssh/coding_rsa

```
通过这个配置文件不同域名指向不同的私钥文件，就可以自动选择正确的私钥进行链接了

https://coding.net/u/memwalker/p/LinuxStudy/git

* clone one repository from github 
  `git clone git@github.com:aquar25/Tickeys-linux.git`
* commit changes
  `git commit -m "message"`
* push the local repo to the server
  `git push`
* check the log on the server
  `git log`
* Commit the changes, -a will commit changes for modified files, but will not add automatically new files
  `git commit -a -m ""`
* check the current status`git status`, and it will show as follow:
```
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)
nothing to commit, working directory clean
```

* git branch

`git branch`列出本地所有branch  
`git branch -r`列出远端所有分支  
`git branch -a`列出本地和远端所有分支  
`git branch <branchname>`创建一个名为branchname的分支，但是不切换到该分支  
`git branch -m | -M oldbranch newbranch`重命名分支，如果newbranch名字分支已经存在，则需要使用-M强制重命名，否则，使用-m进行重命名  
`git branch -d | -D branchname`删除branchname分支  
`git branch -d -r branchname`删除远程branchname分支
`git checkout testing`切换到分支testing  

* Git GUI: use command `git gui`. 
  Installation: `sudo apt-get install git-gui`. graphical commit tool, in Tcl/Tk, distributed with Git (usually in git-gui package). The tool is same on windows system.

* 同一个project可以push到多个server上
  编辑代码库中的`.git/config`文件，在需要的romote下添加新的url即可例如：  
```ini
[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
[remote "origin"]
	url = git@git.oschina.net:aquar/Notes.git	
	fetch = +refs/heads/*:refs/remotes/origin/*
	url = git@github.com:aquar25/Notes.git
[branch "master"]
	remote = origin
	merge = refs/heads/master
[gui]
	wmstate = normal
	geometry = 1099x491+337+341 219 227
```

#### 安装openssh

电脑中只有Ubuntu11.04，且系统中默认自带的只有ssh的客户端，而没有服务端。但是想体验下ssh登录Linux功能，只好自己编译安装虚拟机里面的openssh。查看系统中是否有ssh服务端运行`ps -e | grep ssh`

```shell
  30 ?        00:00:00 sshd
  373 ?       00:00:00 ssh-agent
```

其中ssh-agent是ssh的客户端，而sshd才是后台服务，桌面版本系统一般都没有，需要自行安装

在Ubuntu中编译安装程序需要`build-essential`，常用的gcc编译工具系统已经自带，缺少的只是autoconf和automake，编译autoconf需要m4，因此需要先安m4，直接到官网上下载最新的m4、autoconf和automake，使用`tar -xzvf xxx.tar.gz`解压后，进入目录，参考readme和Install两个文件编译，`make install`需要root权限，因为安装时一般需要安装到`/usr/local/`目录下，而普通用户没有写权限

```
./configure 
make
make test
sudo make install
```

安装完编译环境后，准备安装openssh，在它的说明文档中写了依赖3个库，autoconf、zlib和openssl，安装时需要注意版本的匹配，不一定用最新的版本。我在ubuntu上zlib使用的最新版本，openssl使用的1.0.2m版本，openssh下载的时7.6版本。

安装方法还是一样的make一套，只是openssl用的时`./config`，它里面根据系统的差异再去调用`./Configure`。需要注意的地方：

* 不能在虚拟机vmware的共享目录下直接执行config编译openssl，需要拷贝到linux内部的目录中，否则在中间创建符号链接时会失败，make时提示`No rule to make target `../include/openssl/bio.h', needed by `cryptlib.o'. Stop.MAKE`
* openssl编译时必须设置为动态库方式编译，否则openssh编译不了。`./config --shared`
* 编译完成openssl后需要确认当前系统默认的openssl为自己刚刚编译的版本，如果系统之前自带了openssl，会导致openssh在configure时提示`checking OpenSSL header version... not found`错误。查看当前系统openssl版本`openssl version -a`。正常自己编译安装的程序如果在configure时不指定`--prefix=dir`安装目录的话，一般会安装在`/usr/local/ssl`，而系统默认的目录为`/usr/bin/openssl`以及`/usr/include/openssl`，因此需要创建符号链接，将刚编译的openssl作为默认，具体路径需要参考安装说明中的路径。

```
sudo mv /usr/bin/openssl /usr/bin/openssl.old
sudo ln -s /usr/local/ssl /usr/bin/openssl
sudo ln -s /usr/local/include/openssl /usr/include/openssl
# 动态库目录设置,这个命令执行时提示没有权限，失败
sudo echo "/usr/local/ssl/lib" >> /etc/ld.so.conf
```

在ubuntu中`/etc/ld.so.conf`指明了系统当前动态库的查找目录其中只有一句话

```sh
include /etc/ld.so.conf.d/*.conf
```

本质上就是包含了`ld.so.conf.d`这个目录下的所有动态库配置，例如其中就有一个libc.conf指明了c库的默认位置为`/usr/local/lib`，同理可以在这个目录下新建一个openssl.conf的文件，在其中加一句话`/usr/local/ssl/lib`即可。在设置库目录后，需要执行一次`sudo ldconfig`来让系统更新一下库目录缓存`/etc/ld.so.cache`文件

至此，openssh的make已经没有问题，但是在install时会提示`Privilege separation user sshd does not exist`，这个和openssh的分权用户有关，

> 所谓特权分离(Privilege Separation)实际上是一种 OpenSSH 的安全机制，该特性默认开启，可通过配置文件中的 UsePrivilegeSeparation 指令开启或关闭。

需要执行以下操作后，再`sudo make install`

```shell
sudo mkdir -p  /var/empty #设置一个空目录
sudo chown 0:0 /var/empty #所有者和组，0代表"root"
sudo chmod 000 /var/empty #目录权限设置为"000"
sudo groupadd sshd #建立sshd组
sudo useradd -g sshd -c 'sshd privsep' -d /var/empty -s /bin/false sshd #用于特权分离的非特权用户"sshd"
```

* 启动openssh服务

编译安装的ssh不会创建`/etc/init.d/sshd`服务启动脚本，只有使用安装包安装的才有。因此要启动sshd服务，需要直接执行`sudo /usr/local/sbin/sshd`，注意此处不能直接执行`sudo sshd`，系统会提示要用绝对路径执行，网上有讲这个是因为sbin属于root用户，普通用户下是不能直接执行sbin下的命令。

* 自动启动sshd

  1. 在`/etc/rc.local`中的exit 0之前添加`/usr/local/sbin/sshd & `，让系统在初始化时执行

  2. 自己手动创建一个sshd的shell脚本文件放在`/etc/init.d/`目录下，并给文件增加执行权限`chmod +x sshd`，文件的内容为

     ```shell
     #!/bin/bash 
     cd /usr/local/sbin 
     ./sshd & 
     ```

  3. 然后到/etc/rc3.d/目录下建立一个链接到刚刚的sshd文件，标识系统在3级运行时就启动这个服务

     ```shell
     # cd /etc/rc3.d 
     # ln -s ../init.d/sshd S13sshd
     ```
     ​

* `/etc/rcN.d/`简要说明

init.d 目录下放了系统安装程序时对应的服务启动或停止的脚本，但是系统不是直接从这个目录中直接执行脚本文件，而是根据当前系统的运行级别来决定指定哪些脚本。
init进程上来首先做的事是去读取/etc/目录下inittab文件中initdefault id值，这个值称为运行级别(run-level)。它决定了系统启动之后运行于什么级别。运行级别决定了系统启动的绝大部分行为和目的。这个级别从0到6 ，具有不同的功能。不同的运行级定义如下： 

* 0 - 停机（千万别把initdefault设置为0，否则系统永远无法启动）
* 1 - 单用户模式
* 2 - 多用户，没有 NFS
* 3 - 完全多用户模式(标准的运行级)
* 4 – 系统保留的
* 5 - X11 （x window)
* 6 - 重新启动 （千万不要把initdefault 设置为6，否则将一直在重启 ）

`/etc/rcN.d/`中的数字N就代表了对应的运行级别要执行的脚本的目录，通过这些目录将不同级别执行的服务区分。而所有的服务脚本本质都在init.d这个目录中，而rcN.d中则是软链接到了实际的脚本文件。例如级别3要启动的服务都放在rc3.d这个目录下。这个目录下文件名又以Sxx或Kxx开头，其中S表示启动一个服务，K标识停止一个服务，而xx标识执行的顺序，数字越小，越早执行，这样可以处理服务之间的相互依赖关系。

​        

####deb

deb是debian linus的安装格式，跟red hat的rpm非常相似，最基本的安装命令是：dpkg -i file.deb 
dpkg 是Debian Package的简写，是为Debian 专门开发的套件管理系统，方便软件的安装、更新及移除。所有源自Debian的Linux发行版都使用dpkg，例如Ubuntu、Knoppix 等。
以下是一些 Dpkg 的普通用法：
1、dpkg -i <package.deb>
安装一个 Debian 软件包，如你手动下载的文件。
2、dpkg -c <package.deb>
列出 <package.deb> 的内容。
3、dpkg -I <package.deb>
从 <package.deb> 中提取包裹信息。
4、dpkg -r <package>
移除一个已安装的包裹。
5、dpkg -P <package>
完全清除一个已安装的包裹。和 remove 不同的是，remove 只是删掉数据和可执行文件，purge 另外还删除所有的配制文件。
6、dpkg -L <package>
列出 <package> 安装的所有文件清单。同时请看 dpkg -c 来检查一个 .deb 文件的内容。
7、dpkg -s <package>
显示已安装包裹的信息。同时请看 apt-cache 显示 Debian 存档中的包裹信息，以及 dpkg -I 来显示从一个 .deb 文件中提取的包裹信息。
8、dpkg-reconfigure <package>
重新配制一个已经安装的包裹，如果它使用的是 debconf (debconf 为包裹安装提供了一个统一的配制界面)。

####Ubuntu Tips
1. show hiden files `ctrl+h`

2. Menu of top bar disappeared, chrome's menu shows, but terminal, gedit and some other applications' menu bar missing.
   run `restart unity-panel-service`

3. Software recomendation list:

   **Typora**

   **Haroopad(markdown)** 
    **Clion(C++IDE)** 
    **meld(compare files)** 
    **uGet+aria2(download)**
    **Chrome(without install flash)**
    **FoxitReader(pdf)**

4. upgrade failed with info:"failed for /boot/initrd.img-4.4.0-24-generic with 1."
   This because the /boot is not enough for upgrade the newly linux kernel. Using `df -h /boot` check the available space, and you may need run `sudo apt autoremove linux-image-4.4.0-24-generic` to remove useless linux kernel. `uname -a` to see which is current kernel. `dpkg --get-selections|grep linux`check all the kernel on the disk.

####Python
Ubuntu16.04默认安装了python2.7.11和python3.5,系统目录下
/usr/bin/python ---2.7
/usr/bin/python3 ---3.5
安装pip
`$ sudo apt-get install python-pip`
但是使用pip 安装依赖包时，此时pip命令默认使用的时3.5的pip因此安装的依赖包都是3.5的，为了避免混乱还是最好使用virtualenv创建独立的python环境。
`$ sudo pip install virtualenv` 
此时由于pip时3.5的因此virtualenv默认创建的也是3.5版本的环境，这个信息可以通过
`virtualenv -h`
查看-p参数的描述
因此如果要创建一个2.7的环境，则可以使用`virtualenv -p=python2.7 virPy27`
激活虚拟环境使用
`~$ source virPy27/bin/activate`
此时终端状态变成了
`(virPy27) xxx@aquarius:~$ `
再次查看pip -V就可以看到pip的版本信息了。退出这个虚拟环境使用
`~$ deactivate`
卸载virtualenv
`$ sudo pip uninstall virtualenv`
卸载pip 
`$ sudo apt-get remove python-pip`

####SDL2
* Installation
  `sudo apt-get intall libsdl2-dev`
    ```
    #include <SDL2/SDL.h>
    ```

####添加字体
拷贝字体文件TTF或OTF字体文件
* `sudo cp * /usr/share/fonts/`
* `sudo cp * /usr/local/share/fonts/`


####使用Fiddler
1. 安装mono环境,[website](http://fiddler.wikidot.com/mono),参考Ubuntu 12.04的说明
   `sudo apt-get install libmono-system-windows-forms4.0-cil`
   `sudo apt-get install libmono-windowsbase4.0-cil`
   `sudo apt-get install libmono-system-web4.0-cil`
   `sudo apt-get install mono-mcs`
2. 下载最新版本4.4.8.4 `/media/edison/data/code/fiddler/app`
3. 进入解压目录执行 `mono Fiddler.exe`
4. `tools-fiddler options-connections-port:8085`
5. 在浏览器中设置代理为127.0.0.1 端口为8085

####使用shadowsocks
1. install shadowsocks
   `sudo pip install shadowsocks`
2. create a new file in `/etc/shadowsocks.json` with following content:
```
{
 "server":"23.83.250.158", 
 "server_port":11751, 
 "local_port":10808, 
 "password":"Q3x0MQgP", 
 "timeout":600, 
 "method":"aes-256-cfb" 
 }
```
server and server port is supplied by the service online, some are free. mostly are are fees. Each supplier will give you a password. The local port is used in your computer. 
3. start the shadowsocks with `sslocal -c /etc/shadowsocks.json`
4. set the global network proxy. System setting->Network->Network proxy, set method with manual, and socks host with 127.0.0.1 and port is 10808 as the config file. Leave Http Proxy empty, otherwise the chrome will use it.
   Then when you update component of chrome, it will use this proxy as follow:

```
INFO: loading config from /etc/shadowsocks.json
2016-10-26 23:22:08 INFO     loading libcrypto from libcrypto.so.1.0.0
2016-10-26 23:22:08 INFO     starting local at 127.0.0.1:10808
2016-10-26 23:22:44 INFO     connecting clients1.google.com:443 from 127.0.0.1:53382
2016-10-26 23:22:46 INFO     connecting safebrowsing.google.com:443 from 127.0.0.1:53386
2016-10-26 23:22:47 INFO     connecting safebrowsing-cache.google.com:443 from 127.0.0.1:53390
```

* a suggest website 
  `https://www.laodi.pw/user`
  `http://51.ruyo.net/shadowsocks/`  
  `http://170434.vhost251.cloudvhost.cn/user/index.php` 
  `http://ordshadowsocks.sunnywell.top/user/index.php`

* generate local PAC file

Only the dev version support python3
`pip install https://github.com/JinnLynn/genpac/archive/master.zip`

Go to any directory such as `/home/xxx/network/` and execute:

`genpac --proxy="SOCKS5 127.0.0.1:1080" --gfwlist-proxy="SOCKS5 127.0.0.1:1080" -o autoproxy.pac --gfwlist-url="https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt"`

* use the pac file global
1. check proxy address and port in the pac file, the default is SOCKS5 127.0.0.1:1080
2. System setting->Network->Network proxy, set method with automatic, in the configuration URL input the pac file, here is `/home/xxx/network/autoproxy.pac`


#####ShadowasocksR
1. edit the `user-config.json` in shadowsocksr directory  with the server information  
2. cd into the shadowsocks directory, and run `python local.py` 

####chrome adobe flash is out of date
open `chrome://components/`, and check for update of Adobe Flash Player. This operation need a global proxy of system. Because we cant access google's server.



#### Typora markdown editor

[website](http://www.typora.io/)



#### ffmpeg

* 给mp4文件增加字幕

  从youtube上下载的视频文件是mp4文件，但是字幕时单独的srt文件，因此需要将两个文件压缩到一起。

  视频文件和字幕文件压缩到一起，这种是软压缩，不同于直接把字幕加在视频上（hard burn），即视频播放器支持的话就可以控制字幕大小，是否显示字幕等

  `ffmpeg -i infile.mp4 -i infile.srt -c:v copy -c:a copy -c:s mov_text outfile.mp4`

  其中`-c:v copy -c:a copy -c:s mov_text`分别标识视频不变，音频不变，字幕使用文本文件

  如果写成`-c copy -c:s mov_text`，则表示视频和音频保留不变，字幕使用输入的文本

* 视频分割


  `ffmpeg -ss 00:00:00 -i input.mp4 -c:v copy -c:a copy -c:s copy -t 00:10:44 output.mp4`

  -ss 标识分割的开始时间

  -t 标识分割的结束时间

#### ProjectLibre

微软的MS Project替代软件

https://sourceforge.net/projects/projectlibre/files/ProjectLibre/

选择需要的版本，在其中下载对应系统的安装包

#### 查看二进制文件
`hexdump filename | more`




