
ubuntu 14.04 install qemu

`#sudo apt-get intall qemu`

check the develop board which supported by qemu:
`#qemu-system-arm -M ?`

u-boot Release site:
ftp://ftp.denx.de/pub/u-boot/

Linux Kernel compile

####Download kernel source
https://www.kernel.org/ 

`xz -d linux-3.19.1.tar.xz`
`tar -xvf linux-3.19.1.tar`

####Config
as using qemu simulate arm versatile board, just make the versatile config, all the config file are in arch/arm/configs. In the root directory of kernel source:
`make versatile_defconfig ARCH=arm`
this will generate a .config file. 
Modify the Makefile in root dir of kernel source, change 
`ARCH ?= arm`
`CROSS_COMPILE ?=arm-linux-guneabi-`
make sure there is no space behind the word arm, then: 
`make menuconfig`
to config the compile option for the kernel. 
But it will encount an error like this:
> In file included from scripts/kconfig/mconf.c:23:0:
scripts/kconfig/lxdialog/dialog.h:38:20: fatal error: curses.h: No such file or directory
 include CURSES_LOC                   
compilation terminated.
make[1]: *** [scripts/kconfig/mconf.o] Error 1
make: *** [menuconfig] Error 2

Because Ubuntu does not have the *ncurses devel*.
`sudo apt-get install libncurses5-dev`

设置编译时增加调试信息，以便通过GDB调试内核：
```
kernel hacking-->
[*]compile the kernel with debug info
```

修改.config文件中为如下：
`CONFIG_CMDLINE="earlyprintk console=ttyAMA0 root=/dev/ram0"`
将qemu的输出到当前的提示窗口，设置根目录为/dev/ram0

execute below to compile kernel:
`make mrproper`  // 清除残留的.o文件，如果是第一次编译，就不需要该命令
`make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-`
-j12 means use 12 threads to compile  

after compile we will see:
Kernel: arch/arm/boot/zImage is ready


Use qemu to run the kernel:  
`qemu-system-arm -M versatilepb -kernel arch/arm/boot/zImage -nographic`

-M versatilepb: simulate the versatile board pb type  
-kernel : set the kernel file  
-nographic: let qemu print info into thi console  

busybox
http://www.busybox.net/
`tar jxvf busybox-1.23.1.tar.bz2` or
`bzip2 -d busybox-1.23.1.tar.bz2`
`tar -xvf busybox-1.23.1.tar`
busybox配置：
* 勾选静态编译
* 指定交叉编译器为：arm-linux-gnueabi-
* Installation Options--> Dont use /usr
* Busybox Libary Tuning--> 勾选：[\*]Username completion、[\*]Fancy shell prompts 、[\*]Query  cursor  position  from  terminal 

make defconfig
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- install
生成_install目录，里面是一个文件系统，把arm-linux-gnueabi/libc/lib/拷贝到_install/lib/中
在_install目录中执行
`mkdir proc sys dev etc etc/init.d`
创建一个新文件 _install/etc/init.d/rcS：
```
#!/bin/sh
mount -t proc none /proc
mount -t sysfs none /sys
/sbin/mdev -s
```
设置文件的属性，因为/sbin/init会执行/etc/init.d/rcS.而linux内核运行起来后会调用init
chmod +x _install/etc/init.d/rcS
制作ramdisk文件：
find . | cpio -o --format=newc > ../../../initramfs  
执行如下语句才可以运行busybox的文件系统
```
qemu-system-arm -M versatilepb -kernel arch/arm/boot/zImage -nographic -initrd ./initramfs -append "root=/dev/ram rdinit=/sbin/init console=ttyAMA0"
```
其中initrd指明init ram disk的根目录是哪个。一般分两阶段启动，先是利用initrd的内存文件系统，然后切换到硬盘文件系统继续启动。initrd文件的功能主要有两个：1、提供开机必需的但kernel文件(即vmlinuz)没有提供的驱动模块(modules) 2、负责加载硬盘上的根文件系统并执行其中的/sbin/init程序进而将开机过程持续下去

init是linux的0号进程，是第一个用户态程序

linux内核分析课程：
http://mooc.study.163.com/learn/USTC-1000029000?tid=1000037000#/learn/content?type=detail&id=1000116009&cid=1000101069

```
qemu -kernel linux-3.18.6/arch/x86/boot/bzImage -initrd rootfs.img -s -S # 关于-s和-S选项的说明：
# -S freeze CPU at startup (use ’c’ to start execution)
# -s shorthand for -gdb tcp::1234 若不想使用1234端口，则可以使用-gdb tcp:xxxx来取代-s选项
```

gdb
	（gdb）file linux-3.18.6/vmlinux # 在gdb界面中targe remote之前加载符号表
    （gdb）target remote:1234 # 建立gdb和gdbserver之间的连接,按c 让qemu上的Linux继续运行
    （gdb）break start_kernel # 断点的设置可以在target remote之前，也可以在之后

(gdb)break start_kernel  // 设置断点
(gdb)c                   // 运行程序
(gdb)list                // 显示断点附近内容



