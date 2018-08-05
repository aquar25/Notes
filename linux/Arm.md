##ARM##

可以使用skyeye或qemu来模拟arm平台开发

2440 开发板，提供了外设接口

SOC System on Chip片上系统

linux系统连接串口:minicom  
minicom -s   // 先配置minicom，选择串口设置，选择连接在PC上的串口设备，从而通过串口连接到设备上，设备通过串口UART发送出的字符信息都会在minicom中显示出来

BootLoader  
Hardware

2440 外接了SDRAM(内存)和NandFlash(硬盘)

Nand Flash 前4K中有引导程序，开机时会自动拷贝到CPU的SRAM的4K存储空间中，这样系统才能启动起来，这个内容是由厂家提供。
CPU中SRAM内存的范围是0x0000---0x1000，然后才会初始化SDRAM

有些厂商在CPU中设置了ROM，里面存储了引导程序，烧不死，避免NandFalsh被覆盖，导致无法引导。

SDRAM 从30000000开始地址34000000结束，可用的范围为[30000000,33000000]，U-boot在[3300000,34000000]的区间运行。

变砖：Nand Flash中固定的前4K内容被写掉，导致无法启动

系统启动后将BootLoader拷贝到SDRAM中先运行起来，初始化各个设备的状态，然后引导系统内核。
BootLoader有U-Boot或Blob，管理硬件设备的启动和初始化，初始化内存，引导系统

U-Boot使用的是CShell语法

UART 串口 ---串口仿真--串口转USB--PC(USB)
设置U-boot Ip地址  
setenv ipaddr  192.168.1.7  
saveenv   // 保存到环境变量中
printenv  // 输出环境变量
ping PC的IP可以测试是否网络正常

在PC上建立tftp服务，从而方便通过网络将PC上的文件传输到设备上
在设备上设置tftp的服务器的ip：  
setenv serverip 192.168.1.3

tftp address  fileName  //将PC上的文件直接拷贝到地址address上
tftp 30000000 abc  

md address   //查看内存中的内容
md 30000000

在PC上编译出来的程序是x86的机器码，因此需要使用arm平台的gcc来编译来产生arm平台的机器码，即交叉编译，在PC上使用arm平台的编译器编译，再把结果烧到arm平台上执行。

安装arm-linux-gcc：
在解压的文件夹下进入bin目录，执行
arm-linux-gcc -v 查看版本信息，其中有一句--prefix 一般是这个软件的安装目录，需要把对应的程序整个目录放到这个指定的目录中。例如/usr/local/arm/4.6.1


链接器决定了程序在内存中那个地址区间执行

U-Boot中的go命令可以跳转到指定的内存地址开始执行

arm-linux-objdump 可执行程序文件  //查看程序的内存和函数信息

由于板子上一开始只装了U-boot，还没有任何系统或程序库，因此还不能使用C库函数
可以通过查看u-boot编译生成的map文件，查看U-boot中已经实现的方法的地址，从而可以调用U-boot中已经实现的方法。

	void (*show)(char*, ...);
	int main(int argc, char **argv)
	{
		show = 0x33f94aa8;
		show("hello world"); // call show supplied by U-boot
		return 0;
	}

编译 arm-linux-gcc -c test.c -o test.o
链接 arm-linux-ld -Ttext=0x30000000 test.o -o test
指定链接时程序的代码段的地址为0x30000000


arm-linux-objdump -d test // 查看程序的内存地址，可以看到main的首地址在30000000

可执行文件的组成：  
文件头:可执行文件格式信息(Aout,ELF,COFF,PE)
代码段
数据段

// 去掉可执行文件头 -I 输入文件格式信息  -O 输出文件格式
arm-linux-objcopy -I elf32-littlearm -O binary test test.bin 

由于文件有文件头，文件的开头并不是可以执行的指令，因此直接把链接出来的程序拷贝到指定的内存地址还是无法执行，需要将头去掉，再把可以直接执行的代码段开始的.bin文件拷贝到对应的内存地址，才能调用go执行

`tftp 0x30000000 test.bin` \\将二进制文件拷贝到内存地址0x30000000

go 30000000 

