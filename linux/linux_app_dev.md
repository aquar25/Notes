###Linux Application development

####Linux 文件
#####文件结构
* 目录

文件的属性信息保存在文件的inode(节点)中，它是文件系统中的一个特殊的数据块，系统使用的时文件的inode编号，目录结构为文件名只是便于使用。

目录时用于保存其他文件的节点号和名字的文件。目录文件中每个数据项都是指向某个文件节点的链接，删除文件名称就等于删除与之对应的链接，指向该文件的链接数减1,当指向某个文件的链接数为0时，表示该节点以及其指向的数据不再被使用，磁盘上相应的位置会被标记为可用空间。可以使用ln来在不同的目录中创建指向同一个文件的链接。

* 常用设备文件
1. /dev/console 代表系统控制台，只有一个
2. /dev/tty 如果一个进程有控制终端的话，这个文件就是这个控制终端（键盘/显示屏/键盘/窗口）的别名（逻辑设备）。这个文件允许程序直接向用户输出信息，而不用管用户具体使用的是那种类型的伪终端或硬件终端。`ls -R | more`显示一个长文件列表为例，more程序需要提示用户进行键盘操作之后才能显示下一页的内容。
3. /dev/null 空设备。所有写向这个设备的输出都将被丢弃，读这个设备会立刻返回一个文件结束标志。可以使用`cp /dev/null empty_file`来创建一个空文件，也可以使用`touch empty_file`来创建一个文件，touch命令的用来修改文件的时间，如果文件文件不存在，就创建，但是不会修改文件原有的内容。

设备分为**字符设备**和**块设备**，两者区别在于访问设备时是否一次读写一整块。

* 驱动程序：是一组对系统硬件进行控制的底层接口。驱动程序提供的系统调用有：
1. open 打开文件或设备
2. read 从打开的文件或设备中读数据
3. write 向文件或设备写数据
4. close 关闭文件或设备
5. ioctl 把控制信息传递给设备驱动程序，提供设备相关的控制，不同的设备有自己的一组ioctl命令

* 直接使用系统调用的效率非常低：
1. 系统调用从用户态切换到内核态，再切回用户态，需要保存各种状态，因此尽量在一次系统调用中完成尽可能多的工作
2. 硬件会限制对底层系统调用一次所能读写的数据块大小，例如块设备的读写单位时10k，即使每次只写了5k，系统还是会用10k来写。

* Linux系统提供了标准函数库，对系统调用进行封装，可以更高效的安排执行底层的系统调用。
1. 用户程序和库：用户空间  
2. 系统调用和驱动（内核）：内核空间  
3. 硬件设备在最底层

* 一个进程会有一些与之关联的文件描述符，这些描述符一般都是一些小值整数，例如0代表标准输入 1代表标准输出 2标准错误。可用通过系统调用open把其他文件描述符与文件和设备相关联。

* write系统调用  
把缓冲区buf中的前n个字节写入与文件描述符fd关联的文件中，返回写入的实际字节数。如果范围-1就表示出现了错误，错误代码保存在全局变量errno中。
`size_t write(int fd, const void *buf, size_t nbytes);`
程序举例：
    ```
    #include <unistd.h>
    #include <stdlib.h>


    int main(int argc, char const *argv[])
    {

	    if ((write(1, "write sth to std out\n", 21))!=20)
	    {
		    write(2, "write error\n", 12);
	    }
	    return 0;
    }
    ```
对于所有已经打开的文件描述符在程序退出时，都会自动关闭，所以不需要明确的关闭它们。

* read系统调用，和write一致，只是读入n个字节到buff中  
`size_t read(int fd, const void *buf, size_t nbytes);`
编译如下程序，在终端执行`echo hello man | ./linux_app`，程序先从标准输入中读入echo输出的hello man，并将这个信息再显示到标准输出中。
    ```
    #include <unistd.h> //这个头文件必须放到前面，因为它定义的与POSIX规范相关的标志会影响到其他头文件
    #include <stdlib.h>

    int main(int argc, char const *argv[])
    {
	    char buffer[128]={0};
	    int nread = -1;
	    nread = read(0, buffer, 128);
	    if (nread == -1)
	    {
		    write(2, "Read error\n", 11);
	    }

	    if ((write(1,buffer,nread))!=nread)
	    {
		    write(2, "write error\n", 12);
	    }
	
	    return 0;
    }
    ```

* open 系统调用  
创建一个新的文件描述符，这个文件描述符不能与其他运行中的进程共享，如果两个进程同时打开一个文件，它们会分别得到两个不同的文件描述符，各自接着各自上次的位置写文件，因此二者之间会覆盖另个程序写的内容（与当前各自的偏移位置相关）。打开失败返回-1,新的文件描述符总是使用未使用的描述符的最小值，如果一个程序关闭了它的标准输出，再次调用open，文件描述符1就会被重新使用，并且标准输出将被有效的重定向到另一个文件或设备。
在某些unix系统上需要include`sys/types.h`和`sys/stat.h`
    ```cpp
    int open(const char *path, int oflags);
    int open(const char *path, int oflags, mode_t mode);
    ```
其中，oflags必须指定文件的必填访问方式
1. `O_RDONLY` 只读
2. `O_WDONLY` 只写
3. `O_RDWR` 读写
或者以下几种可选模式
1. `O_APPEND` 把写入数据追加在文件末尾
2. `O_TRUNC` 把文件长度设置为0,丢弃已有的内容
3. `O_CREAT` 如果需要，就按照参数mode中给出的访问模式创建文件
4. `O_EXCL` 与`O_CREAT`一起使用，确保调用者创建出文件。open调用是一个原子操作，它只执行一个函数调用，使用这个模式可以防止两个程序同时创建同一个文件，如果文件已经存在，open调用将失败

当使用带有`O_CREAT`标志的open来创建文件时，必须使用三个参数的open调用，参数mode是几个标志位按位与得到的。这些标志在`sys/stat.h`中定义。  
`S_IRUSR/S_IWUSR/S_IXUSR` 读/写/执行权限，文件属主  
`S_IRGRP/S_IWGRP/S_IXGRP` 读/写/执行权限，文件属组  
`S_IROTH/S_IWOTH/S_IXOTH` 读/写/执行权限，其他用户  
例如 `open("myfile", O_CREAT, S_IRUSR|S_IXOTH)`，创建一个文件文件属主有读权限，其他用户有执行权限，其他权限为空即`-r------x`

* umask是一个系统变量，它的作用是，当文件被创建时，为文件的访问权限设定一个掩码，执行umask命令可以修改这个变量的值，它是一个有各个八进制数字组成的值，例如777.当使用open创建文件时，参数mode将与当前的umask的值进行比较，如果mode中设置的位在umask中也被设置了，那么这个权限将会被删除，例如我当前系统的值为0002,因此当mode的值设置为`S_IWOTH`是没有效果的，其他用户权限的第二位被设置为1了。

* creat调用 不常用，相当有open的oflags标志为`O_CREAT|O_WDONLY|O_TRUNC`

任何一个进程打开的文件数量是有限的，在`limits.h`的常量`OPEN_MAX`定义，至少为16

* close 系统调用,出错时返回-1,成功返回0
`int close(int fd)`
检查close调用的返回结果非常重要，有的文件系统，特别时网络文件系统，可能不会在关闭文件之前报告文件写操作中出现的错误，只有在close的时候，才会返回错误信息。因为在执行写操作时，数据可能未被确认写入。

* ioctl系统调用  
提供控制设备及其描述符行为和配置底层服务的接口。终端/文件描述符/套接字都可以有为它们定义的ioctl
`int ioctl(int fd, int cmd, ...);`
ioctl对描述符fd引用的对象执行cmd参数中给出的操作，设备不同操作不同，可能还会有一个可选的第三参数

* time可以用来对程序执行时间进行测算，linux使用TIMEFORMAT变量来重置默认的POSIX时间输出格式（它没有cpu使用率）  
`TIMEFORMAT="" time ./linux_app`  
输出为：  
`0.00user 0.00system 0:02.37elapsed 0%CPU (0avgtext+0avgdata 1096maxresident)k0inputs+0outputs (0major+61minor)pagefaults 0swaps`  
耗时2s，cpu使用率为0

* lseek系统调用，对文件描述符的读写指针进行设置，可以设置为绝对位置或相对于当前或末尾的相对位置  
`off_t lseek(int fd, off_t offset, int whence);`
whence指定了偏移量的使用方法，`SEEK_SET/SEEK_CUR/SEEK_END`分别指定offset是绝对位置/相对当前位置/相对文件末尾

* fstat, stat, lstat系统调用返回打开的文件描述符相关的文件状态信息，该信息会写到一个stat结构中
```
int fstat(int fd, struct stat *buf);
int stat(const char *path, struct stat *buf);
int fstat(const char *path, struct stat *buf);
```
当文件是一个链接时，lstat返回的时该符号链接本身的信息，而stat返回的时该链接指向文件的信息

* dup,dup2系统调用  
dup可以赋值文件描述符，使得可以通过两个或多个不同的描述符来访问同一个文件，用于在文件的不同位置对数据读写
```
int dup(int fd);  // 返回传入参数的复制
int dup2(int fd1, int fd2);  // 将fd1复制到fd2
```

* Linux中把所有文件都当作二进制文件来看待，

* C库函数
`FILE *fopen(const char *filename, const char *mode);`  
mode的可选值：  
1. "r"或"rb"：以只读方式打开
2. "w"或"wb"：以写方式打开，并把文件长度截断为0
3. "a"或"ab"：以写方式打开，新内容追加在文件尾
4. "r+"或"rb+"：以更新方式打开（读和写）
5. "w+"或"wb+"：以更新方式打开，并把文件长度截断为0
6. "a+"或"ab+"：以更新方式打开，新内容追加在文件尾
打开的文件个数在stdio.h中`FOPEN_MAX`定义  

`size_t fread(void *ptr, size_t size, size_t nitems, FILE *stream);`
读取nitems个size大小的记录到ptr中，返回记录的个数，不是字节数

```
int fgetc(FILE *stream);  //从文件流中读一个字符
int getc(FILE *stream);  //同fgetc，但是它有可能被实现为一个宏，因此不能用getc的地址作为函数指针
int getchar(); //相当于getc(stdin),从标准输入中读入一个字符
char *fgets(char *s, int n, FILE *stream); //读入一个字符串放到s中，读入n-1个字符（还要自动加一个字符'\0'），或者到达文件末尾，返回指向字符串s的指针，如果已经到了文件尾，会设置这个文件流的EOF标识并返回一个空指针
char *gets(char *s) //gets对传入的字符个数没有限制，直到遇到换行符，因此收到的数据会超过gets自身的缓冲区大小，避免安全问题，应该禁止使用这个函数
```

