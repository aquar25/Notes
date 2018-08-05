**冯诺依曼体系**  
存储式计算机结构，由CPU和内存组成，cpu和内存之间通过总线连接，CPU中有IP（指令寄存器），16bit的CPU上叫IP，32bit的叫EIP，64bit的叫RIP。指令寄存器指向内存的某一块区域。
IP指向内存中的指令存放的位置即CS（code Segment,代码段），CPU从IP指向的地址取出一条指令进行执行，然后IP++，指向下一条指令。

**ABI**  
Application Binary Interface,程序与CPU的接口，是指令编码，规定了一条汇编代码如何编码成CPU执行的二进制指令。
指令使用的寄存器有一定的约定
指令可以直接访问内存
 
x86EIP是32bit，指向内存中指令的地址，EIP每次执行完后指向下一条指令，不一定是固定的32bit。

###### x86的寄存器
通用寄存器有：  
AX（Accumulator累加器）  
BX 基地址寄存器 base register  
CX 计数寄存器 Count register  
DX 数据寄存器 Data register  
BP 堆栈基指针 Base Pointer  
SI DI 变址寄存器 Index register  
SP 堆栈顶指针 Stack Pointer  

这些寄存器前面加E-1前缀为32位系统中的寄存器名称，如EAX，ESI

段寄存器：  
CS：代码段寄存器 Code Segment Register
DS: 数据段寄存器 Data Segment Register
ES、FS、GS：附加段寄存器 Extra Segment Register
SS: 堆栈段寄存器 Stack Segment Register

CPU在取指令时根据cs:eip来定位指令的位置。

标志寄存器，用来标识当前CPU的状态

指令后缀b,w,l,q分别表示8,16,32,64位，如  
`movl %eax, %edx    edx = eax `  register mode寄存器寻址，以%开头  
`movl $0x123, %edx  edx = 0x123 ` immediate 立即寻址，把数值放到寄存器中  
`movl 0x123, $edx   edx = *(int32_t*)0x123` direct 直接寻址，将地址0x123中的值放到edx中  
`movl (%ebx), %edx   edx = *(int32_t*)ebx` indirect 间接寻址,ebx中地址指向的值放到edx中  
`movl 4(%ebx), %edx   edx = *(int32_t*)(ebx+4)`  displaced 变址寻址，将ebx的地址先增加4后，再取出这个地址中值放入edx  

Linux使用的是AT&T的汇编格式，和Intel的汇编格式不同

`pushl %EAX `   将寄存器EAX的值压到栈顶，该指令等价于：  
`sub $4, %esp`    将esp地址进行减法操作，指向堆栈下一个位置（向下生长）
`mov %eax, (%esp)`将eax中的值放到esp地址指向的内存中

堆栈向下增长： ebp和esp一起配对，这两个看以看作两个指针，总是指向栈的一段空间，通过不断修改这两个指针的指向，形成多个逻辑的栈空间  
EBP  --> 栈基指针  函数栈帧的栈底
ESP  --> 栈顶指针  函数堆栈的栈顶

`pop %eax`    出栈等价于：  
`mov (%esp), %eax`  将esp指向的内存中的值放入eax中
`add $4, %esp`      将esp向上移动一个位置

`call 0x12345678`  equal to:
`push %eip`  将当前CPU执行的指令地址压栈，相当于函数返回点
`mov $0x12345678, %eip`  将地址0x12345678地址放入eip，让cpu执行它。

`ret`     equal to:
`pop %eip`  弹出当前栈顶放到eip中，让CPU执行，即函数调用前push到栈顶的指令。

编译汇编：
```
int g(int x)
{
      return x + 3;
}

int f(int x)
{
      return g(x);
}

int main(void)
{
      return f(8) + 1;
}
```
`gcc -S -o main.s main.c -m32`  //以32bit编译main.c，输出汇编代码到main.s中

```
g:

	pushl	%ebp  //将f的ebp保存到栈顶，esp指向下一个位置
	movl	%esp, %ebp  //将ebp指向当前esp的位置，即将esp当前所指向的地址存入ebp中，开始函数g的栈空间
	movl	8(%ebp), %eax  //将当前ebp上方两个位置处的g的参数值放入eax
	addl	$3, %eax   //将数字3和eax中的值相加，保存到eax中
	popl	%ebp      //让ebp指向保存f的ebp的地址，之后esp指向了保存的eip指令
	ret     //让eip指向进入g之前指令，即f函数中的leave指令
f:
	pushl	%ebp     // 将main的ebp值保存到栈顶，esp指向下一个位置
	movl	%esp, %ebp  //将ebp指向当前esp的位置，此时这个ebp的位置上方有上一个方法的ebp的地址和进入该方法之前保存的eip的地址，共8个字节
	subl	$4, %esp    //esp指向下一个位置
	movl	8(%ebp), %eax  //变址寻址，将ebp的地址增加8，即向上移动两个位置，也就是传入该方法的参数的值放入eax中
	movl	%eax, (%esp)  //将eax中的值放入esp指向的内存中，即准备函数g的参数
	call	g    //将当前的eip(指向leave)放入栈顶，将g地址赋给eip开始执行g
	leave
	ret

main:
	pushl	%ebp
	movl	%esp, %ebp  //ebp和esp指向同一个位置，一个空栈开始
	subl	$4, %esp    // esp向下增长一个位置
	movl	$8, (%esp)  // 把8放入esp当前指向的栈空间中
	call	f           //将当前的eip（此时eip已经指向下面addl这条指令了）放入栈頂，再将f的地址放入eip中，让eip指向f，开始执行
	addl	$1, %eax
	leave
	ret
```

64bit系统中，寄存器ebp为rbp，栈地址每次为8个字节（unsigned long）

main.s中所有以.开头的语句是连接的辅助信息，不会被执行，可以忽略。

enter指令： 因此这两条指令说明了一个函数调用的开始
`push %ebp`  把当前在执行的栈基指针压入栈顶
`mov %esp, %ebp`  新开一个空栈，将ebp指向当前esp位置。之前老的ebp的值已经保存到了栈里，因此可以开始一个新的函数调用

leave指令:
`mov %ebp, %esp`  让esp指向当前ebp的指针位置，相当于当前函数栈帧的基地址
`pop %ebp`        让ebp指向enter指令调用时，保存的ebp地址，即调用函数之前的函数的基地址

例子2：
```
int multi(int x)
{
      return x * 3;
}

int add(int x, int y)
{
      return multi(x) + y;
}

int main(void)
{
      return add(4, 2) + 1;
}
```
汇编代码：
```
multi:
	pushl	%ebp
	movl	%esp, %ebp
	movl	8(%ebp), %edx
	movl	%edx, %eax
	addl	%eax, %eax
	addl	%edx, %eax
	popl	%ebp
	ret
add:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$4, %esp
	movl	8(%ebp), %eax
	movl	%eax, (%esp)
	call	multi
	movl	12(%ebp), %edx
	addl	%edx, %eax
	leave
	ret
main:
	pushl	%ebp
	movl	%esp, %ebp
	subl	$8, %esp
	movl	$2, 4(%esp)
	movl	$4, (%esp)
	call	add
	addl	$1, %eax
	leave
	ret


```
##### ubuntu 64 bit gcc
`cat /proc/self/maps`访问proc的进程的map或者`cat /proc/<PID>/maps`查看某个进程具体的内存映射地址
    ```
    edison@aquarius:~$ cat /proc/9793/maps 
    00400000-00401000 r-xp 00000000 08:06 154592                             /media/edison/data/code/linux/LinuxStudy/fun_frame
    00600000-00601000 r--p 00000000 08:06 154592                             /media/edison/data/code/linux/LinuxStudy/fun_frame
    00601000-00602000 rw-p 00001000 08:06 154592                             /media/edison/data/code/linux/LinuxStudy/fun_frame
    006e4000-00705000 rw-p 00000000 00:00 0                                  [heap]
    7f64f59dc000-7f64f5b9c000 r-xp 00000000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f64f5b9c000-7f64f5d9b000 ---p 001c0000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f64f5d9b000-7f64f5d9f000 r--p 001bf000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f64f5d9f000-7f64f5da1000 rw-p 001c3000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f64f5da1000-7f64f5da5000 rw-p 00000000 00:00 0 
    7f64f5da5000-7f64f5dcb000 r-xp 00000000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f64f5fa5000-7f64f5fa8000 rw-p 00000000 00:00 0 
    7f64f5fc8000-7f64f5fca000 rw-p 00000000 00:00 0 
    7f64f5fca000-7f64f5fcb000 r--p 00025000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f64f5fcb000-7f64f5fcc000 rw-p 00026000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f64f5fcc000-7f64f5fcd000 rw-p 00000000 00:00 0 
    7ffcdc5a5000-7ffcdc5c6000 rw-p 00000000 00:00 0                          [stack]
    7ffcdc5ed000-7ffcdc5ef000 r--p 00000000 00:00 0                          [vvar]
    7ffcdc5ef000-7ffcdc5f1000 r-xp 00000000 00:00 0                          [vdso]
    ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
    ```

On Unbuntu 16.04 64bit gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.2)
`g++ -g -o fun_frame fun_frame.cpp -Wl,-Map,fun_frame.map`


```CPP
int AddFun(int x)
{
    int ret = x + 50;
    return ret;
}

void TestFun()
{
    int value = 8;
    AddFun(value);
}

int main()
{
    TestFun();
    return 0;
}
```

using GDB `disassemble <function_name>`, output:

    ```
    main
    0x0000000000400507 <+0>:	    push   %rbp
       0x0000000000400508 <+1>:	    mov    %rsp,%rbp  // rbp = rsp = 0x7fffffffdbb0
       0x000000000040050b <+4>:	    callq  0x4004eb <TestFun()>
       0x0000000000400510 <+9>:	    mov    $0x0,%eax  // 将返回值0放入eax
       0x0000000000400515 <+14>:	pop    %rbp
       0x0000000000400516 <+15>:	retq   
       
    Dump of assembler code for function TestFun():
       0x00000000004004eb <+0>:	    push   %rbp
       0x00000000004004ec <+1>:	    mov    %rsp,%rbp  // rbp = 0x7fffffffdba0
       0x00000000004004ef <+4>:	    sub    $0x10,%rsp     //开辟16个字节的空间 rsp = 0x7fffffffdb90
       0x00000000004004f3 <+8>:	    movl   $0x8,-0x4(%rbp)  // 把数字8赋值给4字节局部变量
       0x00000000004004fa <+15>:	mov    -0x4(%rbp),%eax  // 数字8放到eax中
       0x00000000004004fd <+18>:	mov    %eax,%edi  //将eax中的值放入edi中，放入8
       0x00000000004004ff <+20>:	callq  0x4004d6 <AddFun(int)> // call在执行时，先将下一条指令的地址0x0400504压栈，再将调用函数的地址0x4004d6给rip，让rip执行该函数，此时rbp的指针为0x7fffffffdba0，rsp的指针为0x7fffffffdb88
       0x0000000000400504 <+25>:	nop
       0x0000000000400505 <+26>:	leaveq   // esp指向ebp的地址，即清空函数栈帧，再将上一层函数的ebp的值放到ebp寄存器，相当有pop ebp的作用
       0x0000000000400506 <+27>:	retq   //弹出当前esp（栈顶）地址中的内容0x400510给rip执行，rsp指针+1   %rbp当前值为0x7fffffffdb0,%rsp的值为0x7fffffffdbb0

       
    Dump of assembler code for function AddFun(int):
       0x00000000004004d6 <+0>:	    push   %rbp       //当前栈顶为上一个函数的rbp的值，push函数中，先对esp指针-1（8字节位置），再将ebp的值放入新的esp指向的地址中，此时rsp指针值为0x7fffffffdb80，rbp的指针值为0x7fffffffdba0
       0x00000000004004d7 <+1>:	    mov    %rsp,%rbp    // 将当前rsp的值付给rbp寄存器，rbp = rsp = 0x7fffffffdb80，这个地址中存放的就是上个函数的ebp值
       0x00000000004004da <+4>:	    mov    %edi,-0x14(%rbp)  //将参数edi的值8放入函数栈中，开辟了20个字节的空间
    => 0x00000000004004dd <+7>:	    mov    -0x14(%rbp),%eax  //将参数放入eax，通过eax访问参数，而没有通过索引栈指针来传递参数
       0x00000000004004e0 <+10>:	add    $0x32,%eax   // 对eax的值加50
       0x00000000004004e3 <+13>:	mov    %eax,-0x4(%rbp)  //将eax的值放入rbp-4（0x7fffffffdb7c）的位置中的值为0x3a
       0x00000000004004e6 <+16>:	mov    -0x4(%rbp),%eax  //将rbp-4的值0x3a放入eax
       0x00000000004004e9 <+19>:	pop    %rbp      // 将当前esp指向的内容放入rbp中，再将esp指针+1，此时esp指向的地址为0x7fffffffdb88，该地址中存放的是调用call函数之后下一条指令的地址，即<TestFun()+25  
       0x00000000004004ea <+20>:	retq   //弹出当前esp（栈顶）地址中的内容0x400504给rip执行，rsp指针+1   %rbp当前值为0x7fffffffdba0,%rsp的值为0x7fffffffdb90

    ```
* 汇编指令单步执行 `si`

在`AddFun(int x)`的入口处断点时的调用堆栈
    ```
    (gdb) bt
    #0  AddFun (x=8) at fun_frame.cpp:4
    #1  0x0000000000400504 in TestFun () at fun_frame.cpp:11
    #2  0x0000000000400510 in main () at fun_frame.cpp:16
    (gdb) i register
    rax            0x8
    rdi            0x8
    rbp            0x7fffffffdb80
    rsp            0x7fffffffdb80   // rsp并没有随着函数中语句的执行执行而减小，始终使用rbp+偏移量来放完栈帧中的空间
    rip            0x4004dd	0x4004dd <AddFun(int)+7>
    (gdb) x 0x7fffffffdb88   // rbp上一个位置的值为call之后下一条指令地址
    0x7fffffffdb88:	0x00400504  // TestFun()的0400504 <+25>:	nop
    //完整栈空间内容
    0x7fffffffdba8:	0x400510 <main()+9>
    0x7fffffffdba0:	0xffffffffffffdbb0
    0x7fffffffdb98:	0x4003e0 <_start>
    0x7fffffffdb90:	0x400520 <__libc_csu_init>
    0x7fffffffdb88:	0x400504 <TestFun()+25>
    0x7fffffffdb80:	0xffffffffffffdba0   //esp指向地址，上一个函数AddFun(int)的ebp的地址
    
    (gdb) x 0x7fffffffdba8
    0x7fffffffdba8:	0x400510 <main()+9>
    
    (gdb) x 0x7fffffffdba0   // 函数AddFun(int)的ebp的地址存放着main()函数的ebp地址
    0x7fffffffdba0:	0xffffffffffffdbb0  // 实际值应该为0x7fffffffdbb0
    
    
    ```
``
####堆栈####

堆栈是C语言程序运行时必须的一个记录调用路径和参数的空间。保存函数调用地址，局部变量，函数入参。
gcc -g test.c -o test
objdump -S test -o test.S

GDB查看汇编代码 `gdb> disassemble /m main`

####中断####

CPU有几种不同的指令执行级别，高级别下，代码可以执行特权指令，访问任意物理地址，对应内核态，一般由操作系统来执行。低级别的
只能在有限的范围内执行。x86 CPU有4中不同的执行级别0-3，Linux只使用了其中的0和3级，分别表示内核态和用户态。

CS寄存器的最低两位表明了当前代码的特权级别。CPU执行的指令的读取通过CS:EIP这两个寄存器来指定。CS是代码段选择寄存器，EIP是偏移量指令寄存器。

Linux系统中0xC0000000以上的地址空间只能在内核态访问，0x00000000-0xbfffffff在两种状态下都可以访问。

2^32 = (2^10) * (2^10) * (2^10) * (2^2) = 4GB
因此32系统可以寻址4G的地址空间
编码就是对每一个物理存储单元(一个字节)分配一个唯一的地址号码，这个过程又叫做“编址”或者“地址映射”

进程的地址空间：32bit为4GB，每个进程一个。Linux系统中，3GB以上是内核空间，3GB以下是用户空间

中断：中断时需要保存CPU的执行状态，是从用户态进入内核态的主要方式，例如用户态程序通过系统调用进入了内核态，这种方式称作trap，系统调用本质上是一种中断，此时INT指令会在堆栈上保存一些寄存器的值，例如：用户态的栈顶地址、当时的状态字、CS:EIP的值等

中断开始时调用宏SAVE_ALL来保存现场，结束后调用RESTORE_ALL来恢复现场

####系统调用
#####为什么
操作系统为用户态进程提供的和硬件设备进行交互的一组接口，从而
* 提高系统的安全性，
* 用户程序不需要关心硬件编程，
* 也使得用户程序更好的移植。


#####过程
1. interrupt(ex:int 0x80):保存当前用户态的cs:eip/ss:esp/eflags到内核的栈中，然后加载一个中断信号的入口到cs:eip，将内核堆栈的指针存入ss:esp中。
2. SAVE_ALL 保存当前的CPU的状态
3. 在内核态的堆栈上执行内核代码，完成相关任务
4. RESTORE_ALL 恢复CPU的执行状态
5. iret: pop cs:eip/ss:esp/eflags //回到用户态

api(库函数)--> 中断向量(int 0x80) --> 系统内核函数

system_call是linux中所有系统调用的入口点，每个系统调用至少有一个参数即由EAX（固定使用这个寄存器）传递的系统调用号，用来区分不同的系统调用。例如：fork()接口，在执行int $0x80之前把eax的值设置为2（即_NR_fork）

寄存器参数传递：
1. 每个参数的长度不能超过寄存器的长度，即32bit
2. 除过系统调用号eax外，参数个数不能超过6个(ebx,ecx, edx, esi, edi, ebp)，可以通过将参数指针传递进来的方式来传递更多的参数信息。

内嵌汇编的方式实现系统调用：
time()接口实现：
```
time_t tt;
asm volatile(
	"mov $0, %%ebx\n\t" //传入一个参数0给ebx
    "mov $0xd, %%eax\n\t" // 设置系统调用号为0xd系统时间系统调用的号码
    "int $0x08\n\t"  //执行中断
    "mov %%eax, %0\n\t" //将系统调用返回的数据放入第一个参数中
    :"=m" (tt)
)
printf("%d\n",tt); //此时tt就是当前系统时间的值
```

系统调用的相关代码在内核的arch/x86/kernel/entry_32.S中：
```
ENTRY(system_call)
......
```


####内嵌汇编####

__asm__(
   “汇编语句模板” // 编写需要执行的语句 
   “输出部分”    // 语句中用到的输出的变量定义  
   “输入部分”    // 语句中用到的输入变量的定义 
   “破坏描述部分” // 哪些寄存的值被破坏，在这里声明
)

asm ( "statements" : output_regs : input_regs : clobbered_regs);

```
int main()
{
	// 通过嵌入汇编实现：val3 = val1 + val2;
    unsigned int val1 = 1;
    unsigned int val2 = 2;
    unsigned int val3 = 0;
    
	asm volatile (            // 不要让编译器优化 
		"movl $0, %%eax\n\t"  // %%相当于多了一个%来转义，把0放到eax中
        "addl %1, %%eax\n\t"  // %1 表示输入和输出的第二个，即下面的"c"(val1)定义的ecx
        "addl %2, %%eax\n\t"  // %2 表示输入和输出的第三个，对应于"d"(val2)，即edx中的值，即val1+val2
        "movl %%eax, %0\n\t"  // %0 表示输入和输出的第1个，即内存变量val3，将eax中值放入内存变量val3中
        :"=m" (val3)          // m表示内存变量，=表示操作数是只写的（输出操作数）
        :"c"(val1),"d"(val2)  // 将val1的值放到ecx中，val2的值放到edx中，“c”代表ecx
	);
	return 0;
}
```
PCB  process control block

###内核启动
init目录下main.c:
```
asmlinkage __visible void __init start_kernel(void)
{
	/*
	 * Need to run as early as possible, to initialize the
	 * lockdep hash:
	 */
	lockdep_init();
	set_task_stack_end_magic(&init_task); //init_task即PCB，0号进程就是最终的idle进程
	smp_setup_processor_id();
	debug_objects_early_init();

	cgroup_init_early();

	local_irq_disable();
	early_boot_irqs_disabled = true;
	......
	ftrace_init();

	/* Do the rest non-__init'ed, we're now alive */
	rest_init();
}
```

####进程管理
进程管理task_struct、内存管理、文件系统fs_struct
struct task_struct; // 进程描述结构
http://codelab.shiyanlou.com/xref/linux-3.18.6/include/linux/sched.h#task_struct

fork()-->Task_RUNNING(就绪，并没运行)-schedule()->Task_RUNNING(获得调度，真正执行)-do_exit()->Task_Zombie
Task_Interruptable(阻塞)

双向循环列表
list_head  //非常好的一个双向列表实现
使用 `struct list_head children;	/* list of my children */`

```
struct list {
	struct list *next, *prev;
};

static inline void
list_init(struct list *list)
{
	list->next = list;
	list->prev = list;
}

static inline int
list_empty(struct list *list)
{
	return list->next == list;
}

static inline void
list_insert(struct list *link, struct list *new_link)
{
	new_link->prev		= link->prev;
	new_link->next		= link;
	new_link->prev->next	= new_link;
	new_link->next->prev	= new_link;
}

static inline void
list_append(struct list *list, struct list *new_link)
{
	list_insert((struct list *)list, new_link);
}

static inline void
list_prepend(struct list *list, struct list *new_link)
{
	list_insert(list->next, new_link);
}

static inline void
list_remove(struct list *link)
{
	link->prev->next = link->next;
	link->next->prev = link->prev;
}

#define list_entry(link, type, member) \
	((type *)((char *)(link)-(unsigned long)(&((type *)0)->member)))

#define list_head(list, type, member)		\
	list_entry((list)->next, type, member)

#define list_tail(list, type, member)		\
	list_entry((list)->prev, type, member)

#define list_next(elm, member)					\
	list_entry((elm)->member.next, typeof(*elm), member)

#define list_for_each_entry(pos, list, member)			\
	for (pos = list_head(list, typeof(*pos), member);	\
	     &pos->member != (list);				\
	     pos = list_next(pos, member))
```

####进程创建
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc, char * argv[])
{
    int pid;
    /* fork another process */
    pid = fork();
    if (pid < 0) 
    { 
        /* error occurred */
        fprintf(stderr,"Fork Failed!");
        exit(-1);
    } 
    else if (pid == 0) 
    {
        /* child process */
        printf("This is Child Process!\n");
    } 
    else //父进程中返回时，pid为子进程的id，fork会返回两次，因此这个分支也会被执行
    {  
        /* parent process  */
        printf("This is Parent Process!\n");
        /* parent will wait for the child to complete*/
        wait(NULL);
        printf("Child Complete!\n");
    }
}
```

#####创建新进程过程
fork、vfork和clone三个系统调用都可以创建一个新进程，而且都是通过调用*do_fork*来实现进程的创建；
Linux通过复制父进程来创建一个新进程，那么这就给我们理解这一个过程提供一个想象的框架：
* 复制一个PCB——task_struct
	`err = arch_dup_task_struct(tsk, orig);`
* 要给新进程分配一个新的内核堆栈
```
ti = alloc_thread_info_node(tsk, node);
tsk->stack = ti;
setup_thread_stack(tsk, orig); //这里只是复制thread_info，而非复制内核堆栈
```
* 要修改复制过来的进程数据，比如pid、进程链表等等都要改改吧，见copy_process内部。


从用户态的代码看fork();函数返回了两次，即在父子进程中各返回一次，父进程从系统调用中返回比较容易理解，子进程从系统调用中返回，那它在系统调用处理过程中的哪里开始执行的呢？这就涉及子进程的内核堆栈数据状态和task_struct中thread记录的sp和ip的一致性问题，这是在哪里设定的？copy_thread in copy_process
```
*childregs = *current_pt_regs(); //复制当前内核堆栈给子进程，即父进程进入系统调用时保存的堆栈信息
childregs->ax = 0; //为什么子进程的fork返回0，这里就是原因！ 
p->thread.sp = (unsigned long) childregs; //调度到子进程时的内核栈顶
p->thread.ip = (unsigned long) ret_from_fork; //调度到子进程时的第一条指令地址，因此如果子进程得到调度，通过子进程的内核堆栈从内核态返回到用户态，因为ret_from_fork最终执行了syscall_exit
```
0号进程的PCB是在代码中写好的，而1号进程通过在0号进程中复制了一份，并作修改从而创建出来。Linux中，1号进程是所有用户态进程的祖先，0号进程是所有内核线程的祖先

fofork()也是一个系统调用，在它的系统调用函数中，在它内核处理函数中创建了一个子进程

kernel/fork.c
do_fork

####可执行程序
.c---GCC--->.asm---GAS--->.o---ld--->a.out
最终可执行文件a.out被加载到内存中执行

gcc -E -o hello.cpp hello.c -m32 // 对hello.c进行预处理 包括扩展include的头文件以及宏定义
```
gcc -x cpp-output -S -o hello.s hello.cpp -m32 // 将hello.cpp编译成汇编代码

gcc -x assembler -c hello.s -o hello.o -m32 //将hello.s编译成目标文件

gcc -o hello hello.o -m32 //动态链接生成hello可执行文件

gcc -o hello.static hello.o -m32 -static //静态链接,生成文件比较大
```
* ELF:Executable and linkable format
* ABI:application binary interface

ELF文件有三种：
1. 可重定位文件(relocatable):保存着代码和适当的数据用来和其他的obj文件一起创建一个可执行文件或者共享文件， 如.o文件
2. 可执行文件(executable):指出系统调用exec(BA_OS)如何创建程序的进程映像，如.exe
3. 共享目标文件:保存着代码和合适的数据用来被下面的两种链接器链接：
	* 链接编辑器ld(SD_CMD),可以和可重定位文件或共享目标文件来创建其他的目标文件
	* 动态链接器，联合一个可执行文件和其他的共享目标文件来创建一个进程映像。

查看一个一个可执行文件的ELF头
`readelf -h hello`

一个可执行程序的组成：
```
offset		File
0			ELF HEADER
0x100		.Text segment   // 代码段
0xf00		.Data segment   // 数据段
0x1f00		other info
```
代码段和数据段的内容会根据偏移地址映射到虚拟的内存地址空间，而在elf头信息中，给出了程序入口点的地址，这是程序被加载到内存后的第一个个指令。

编译生成共享库文件
`$ gcc -shared libexample.c -o libexample.so -m32`

*动态链接分为可执行程序装载时动态链接和运行时动态链接*，后者很少用到

```
int main()
{
    printf("This is a Main program!\n");
    /* Use Shared Lib */
    printf("Calling SharedLibApi() function of libshlibexample.so!\n");
    SharedLibApi();
    /* Use Dynamical Loading Lib */
    void * handle = dlopen("libdllibexample.so",RTLD_NOW); //动态加载
    if(handle == NULL)
    {
        printf("Open Lib libdllibexample.so Error:%s\n",dlerror());
        return   FAILURE;
    }
    int (*func)(void);
    char * error;
    func = dlsym(handle,"DynamicalLoadingLibApi");
    if((error = dlerror()) != NULL)
    {
        printf("DynamicalLoadingLibApi not found:%s\n",error);
        return   FAILURE;
    }    
    printf("Calling DynamicalLoadingLibApi() function of libdllibexample.so!\n");
    func();  
    dlclose(handle);       
    return SUCCESS;
}

```

注意这里只提供libexample的-L（库对应的接口头文件所在目录）和-l（库名，如libexample.so去掉lib和.so的部分），并没有提供libexample的相关信息，只是指明了-ldl(动态加载共享库)
`$ gcc main.c -o main -L/path/to/your/dir -lexample -ldl -m32`
还需要设置库文件的搜索目录
`export LD_LIBRARY_PATH=$PWD #将当前目录加入默认路径，否则main找不到依赖的库文件，当然也可以将库文件copy到默认路径/usr/lib下。`

####启动一个程序
命令行参数和shell环境，一般我们执行一个程序的Shell环境，我们的实验直接使用execve系统调用。
* Shell本身不限制命令行参数的个数，命令行参数的个数受限于命令自身
* 例如，int main(int argc, char *argv[])
* 又如， int main(int argc, char *argv[], char *envp[]) // envp包含shell的环境变量信息
* Shell会调用execve将命令行参数和环境参数传递给可执行程序的main函数
`int execve(const char * filename,char * const argv[ ],char * const envp[ ]);`
* 库函数exec*都是execve的封装例程

* [sys_execve](http://codelab.shiyanlou.com/xref/linux-3.18.6/fs/exec.c#1604)内部会解析可执行文件格式
	* do_execve -> do_execve_common ->  exec_binprm
search_binary_handler寻找符合elf文件格式对应的解析模块，如下：
```
   list_for_each_entry(fmt, &formats, lh) {
       if (!try_module_get(fmt->module))
           continue;
       read_unlock(&binfmt_lock);
       bprm->recursion_depth++;
       retval = fmt->load_binary(bprm);  // 实际执行load_elf_binary
       read_lock(&binfmt_lock);
       ```

* 对于ELF格式的可执行文件fmt->load_binary(bprm);执行的应该是load_elf_binary其内部是和ELF文件格式解析的部分需要和ELF文件格式标准结合起来阅读
* Linux内核是如何支持多种不同的可执行文件格式的？ 
```
static struct linux_binfmt elf_format = {
  .module     = THIS_MODULE,
  .load_binary    = load_elf_binary,  // 函数指针
  .load_shlib = load_elf_library,
  .core_dump  = elf_core_dump,
  .min_coredump   = ELF_EXEC_PAGESIZE,
};
```
```
static int __init init_elf_binfmt(void)
{
    register_binfmt(&elf_format); //将上面定义结构注册到内核中，从而可以找到该模块来解析elf格式
    return 0;
}
```
* elf_format 和 init_elf_binfmt，这里是不是就是观察者模式中的观察者？
* 可执行文件开始执行的起点在哪里？如何才能让execve系统调用返回到用户态时执行新程序？
	* 庄生梦蝶 —— 醒来迷惑是庄周梦见了蝴蝶还是蝴蝶梦见了庄周？
	* 庄周（调用execve的可执行程序）入睡（调用execve陷入内核），醒来（系统调用execve返回用户态）发现自己是蝴蝶（被execve加载的可执行程序）
	* 修改int 0x80压入内核堆栈的EIP
	* load_elf_binary ->  start_thread // 通过修改内核堆栈中EIP的值作为新程序的起点
* 动态链接的过程内核做了什么？可执行文件依赖的动态链接库（共享库）是由谁负责加载以及如何递归加载的？

#####execve执行过程
`
SYSCALL_DEFINE3(execve, 
	const char __user *, filename,
	const char __user *const __user *, argv,
	const char __user *const __user *, envp)`

`int do_execve(struct filename *filename,
	const char __user *const __user *__argv,
	const char __user *const __user *__envp)`
    
```
static int do_execve_common(struct filename *filename,
struct user_arg_ptr argv,
struct user_arg_ptr envp)
{
	file = do_open_exec(filename);
    bprm->file = file;
    retval = exec_binprm(bprm);
}
```
在load_elf_binary方法中
/* Now we do a little grungy work by mmapping the ELF image into the correct location in memory. */
ELF文件会被默认映射到0x8048000这个地址
对于需要动态链接的可执行文件先加载链接器ld，将动态链接器起点赋给elf_entry，如果是静态的程序就直接使用elf可执行文件的elf头中定义的入口点，最后在start_thread的new_ip就是这个elf_entry的值。

####进程切换
进程调度的触发：
* 中断处理过程（包括时钟中断、I/O中断、系统调用和异常）中，直接调用schedule()，或者返回用户态时根据need_resched标记调用schedule()；
* 内核线程可以直接调用schedule()进行进程切换，也可以在中断处理过程中进行调度，也就是说内核线程作为一类的特殊的进程可以主动调度，也可以被动调度；
* 用户态进程无法实现主动调度，仅能通过陷入内核态后的某个时机点进行调度，即在中断处理过程中进行调度。

进程的切换：
* 为了控制进程的执行，内核必须有能力挂起正在CPU上执行的进程，并恢复以前挂起的某个进程的执行，这叫做进程切换、任务切换、上下文切换；
* 挂起正在CPU上执行的进程，与中断时保存现场是不同的，中断前后是在同一个进程上下文中，只是由用户态转向内核态执行；

进程上下文包含了进程执行需要的所有信息：
* 用户地址空间：包括程序代码，数据，用户堆栈等
* 控制信息：进程描述符，内核堆栈等
* 硬件上下文（注意中断也要保存硬件上下文只是保存的方法不同）

[schedule()](http://codelab.shiyanlou.com/xref/linux-3.18.6/kernel/sched/core.c#2865)函数选择一个新的进程来运行，并调用context_switch进行上下文的切换，这个宏调用switch_to来进行关键上下文切换:

* next = pick_next_task(rq, prev);//[link](http://codelab.shiyanlou.com/xref/linux-3.18.6/kernel/sched/core.c#pick_next_task)进程调度算法都封装这个函数内部
* context_switch(rq, prev, next);//[link](http://codelab.shiyanlou.com/xref/linux-3.18.6/kernel/sched/core.c#context_switch)进程上下文切换
* [switch_to](http://codelab.shiyanlou.com/xref/linux-3.18.6/arch/x86/include/asm/switch_to.h#31)利用了prev和next两个参数：prev指向当前进程，next指向被调度的进程
```
#define switch_to(prev, next, last)                    \
do {                                 \
  /*                              \
   * Context-switching clobbers all registers, so we clobber  \
   * them explicitly, via unused output variables.     \
   * (EAX and EBP is not listed because EBP is saved/restored  \
   * explicitly for wchan access and EAX is the return value of   \
   * __switch_to())                     \
   */                                \
  unsigned long ebx, ecx, edx, esi, edi;                \
                                  \
  asm volatile("pushfl\n\t"      /* save    flags */   \
           "pushl %%ebp\n\t"        /* save    EBP   */ \ // 内核堆栈的切换
           "movl %%esp,%[prev_sp]\n\t"  /* save    ESP   */ \
           "movl %[next_sp],%%esp\n\t"  /* restore ESP   */ \ 
           "movl $1f,%[prev_ip]\n\t"    /* save    EIP   */ \
           "pushl %[next_ip]\n\t"   /* restore EIP   */    \
           __switch_canary                   \
           "jmp __switch_to\n"  /* regparm call  */ \
           "1:\t"                        \ //开始执行next进程的第一条指令
           "popl %%ebp\n\t"     /* restore EBP   */    \
           "popfl\n"         /* restore flags */  \
                                  \
           /* output parameters */                \
           : [prev_sp] "=m" (prev->thread.sp),     \
             [prev_ip] "=m" (prev->thread.ip),        \
             "=a" (last),                 \
                                  \
             /* clobbered output registers: */     \
             "=b" (ebx), "=c" (ecx), "=d" (edx),      \
             "=S" (esi), "=D" (edi)             \
                                       \
             __switch_canary_oparam                \
                                  \
             /* input parameters: */                \
           : [next_sp]  "m" (next->thread.sp),        \
             [next_ip]  "m" (next->thread.ip),       \
                                       \
             /* regparm parameters for __switch_to(): */  \
             [prev]     "a" (prev),              \
             [next]     "d" (next)               \
                                  \
             __switch_canary_iparam                \
                                  \
           : /* reloaded segment registers */           \
          "memory");                  \
} while (0)
```

最一般的情况：正在运行的用户态进程X切换到运行用户态进程Y的过程

1. 正在运行的用户态进程X
2. 发生中断——save cs:eip/esp/eflags(current) to kernel stack(进程X的内核堆栈),then load cs:eip(entry of a specific ISR) and ss:esp(point to kernel stack).
3. SAVE_ALL //保存现场
4. 中断处理过程中或中断返回前调用了schedule()，其中的switch_to做了关键的进程上下文切换
5. 标号1之后开始运行用户态进程Y(此时是Y的内核态堆栈，这里Y曾经通过以上步骤被切换出去过因此可以从标号1继续执行)
6. restore_all //恢复现场
7. iret - pop cs:eip/ss:esp/eflags from kernel stack（将Y被中断时保存到Y进程内核堆栈弹出，转到Y的用户态执行）
8. 继续运行用户态进程Y

X（用户态）--保存X到内核堆栈--弹出之前保存的Y的内核堆栈到用户态堆栈---在用户态执行Y的堆栈

几种特殊情况

* 通过中断处理过程中的调度时机，用户态进程与内核线程之间互相切换和内核线程之间互相切换，与最一般的情况非常类似，只是内核线程运行过程中发生中断没有进程用户态和内核态的转换；
* 内核线程主动调用schedule()，只有进程上下文的切换，没有发生中断上下文的切换，与最一般的情况简单；
* 创建子进程的系统调用在子进程中的执行起点及返回用户态，如fork；
* 加载一个新的可执行程序后返回到用户态的情况，如execve；

所有的进程在3G以上的部分是共享的，即内核态的代码段、数据段，各个进程是共享的。

内核可以看作各种中断处理过程和内核线程的集合

###线程
在一个进程中正在创建以及已经创建的线程共享相同的内存空间/文件描述(file descriptor文件句柄)以及其他系统资源，由于不存在任何资源的拷贝，因此线程的创建效率更高。如果一个线程修改了一个变量值，其他的线程将会看到修改后的值。  
Linux平台上POSIX标准线程api的实现pthreads的头文件为<pthread.h>但是标准库中没有，需要在链接时增加-lpthread选项  
每一个线程有一个唯一的线程ID标识，类型为pthread_t
####线程创建
```
/* Create a new thread, starting with execution of START-ROUTINE
   getting passed ARG.  Creation attributed come from ATTR.  The new
   handle is stored in *NEWTHREAD.  */
extern int pthread_create (pthread_t *__restrict __newthread,
			   const pthread_attr_t *__restrict __attr,
			   void *(*__start_routine) (void *),
			   void *__restrict __arg) __THROWNL __nonnull ((1, 3));
```
线程创建函数会立即返回，有4个参数: 
1. 类型为pthread_t的指针，每一个线程有一个唯一的线程ID标识，创建后返回实际的id值
2. 类型为pthread_attr_t的线程属性指针，如果传入NULL，则为默认值
3. 类型为`void* (*) (void*)`的函数指针，即返回值和参数都为`void*`，当线程创建后，会立即执行这个函数，当这个函数执行结束，线程也就自动结束
4. 类型为`void*`的线程参数，这个参数会传递线程函数

#####传递参数到线程中
通过线程创建函数的第4个参数可以将任意类型的参数传递给线程。通常定一个通用的结构体中包含线程函数想要的所有参数，并将这个结构体的指针作为参数传入。这样可以达到同一个线程函数可以被不同的线程复用，而只是数据不同。
* 需要注意传递给线程的所有的变量，都要确保在线程结束前，不会被释放，特别是使用局部变量的情况

```
// 线程函数通用参数结构
struct char_print_param
{
    // print this character
    char character;
    // print times
    int count;
};

// 通用线程函数
void* char_print(void* info)
{
    //得到需要的参数
    char_print_param* p = (char_print_param*)info;

    for (int i = 0; i < p->count; ++i) {
        cout<<p->character<<endl;
    }
    return NULL;
}

pthread_t thread_id1;
pthread_t thread_id2;
char_print_param thread_param1;
char_print_param thread_param2;

thread_param1.character = 'x';
thread_param1.count = 30000;
pthread_create(&thread_id1, NULL, &char_print, &thread_param1);

thread_param2.character = 'o';
thread_param2.count = 20000;
pthread_create(&thread_id2, NULL, &char_print, &thread_param2);
    
```

####阻塞等待线程Join
当一个线程需要等待另一个线程的结果时，就需要等待另一个线程执行完再执行后续的工作，此时要用到`pthread_join`,这个函数有两个参数，
1. 需要等待的线程id
2. 等待线程结束的返回值`void*`,如果不需要返回值，就传NULL

```
pthread_join(thread_id1, NULL);
pthread_join(thread_id2, NULL);

```
####线程退出
* 线程函数执行结束，线程函数的返回值作为线程的返回值返回
* 通过显式调用`pthread_exit`,这个函数可以在线程函数或者其他的函数中调用，这个函数的参数得到线程的返回值

####Dump正在运行进程的内存
在linux系统中可以使用dump正在运行程序的heap内存信息，方便查看异常信息。
在Linux系统中，
`cat /proc/<pid>/maps` 查看指定进程pid的内存映像关系 
例如对于测试程序,`g++ -o mytest main.cpp`，其中由于系统是64位，需要使用long类型来保存地址，不能用int
    ```
    #include <iostream>
    #include <cstdlib>
    #include <string>
    #include <memory>


    using namespace std;

    int main()
    {
        unsigned long size = 30*1024;
        char* p = new char[size];
        for(int i = 0;  i < size; i++)
        {
            *(p + i) = 'P';
        }
        long addr = (long)(p);
        cout << "addr of p: " << addr << endl;
        string name;
        cin >> name;

        return 0;
    }
    ```
在终端`./mytest`执行程序后，先使用命令`ps -e | grep mytest`查看测试程序的pid为8599
看到结果如下：
    ```
    $ cat /proc/8599/maps 
    00400000-00401000 r-xp 00000000 08:06 154834                             /code/C++/algorithm/mytest
    00601000-00602000 r--p 00001000 08:06 154834                             /code/C++/algorithm/mytest
    00602000-00603000 rw-p 00002000 08:06 154834                             /code/C++/algorithm/mytest
    00e6f000-00ea1000 rw-p 00000000 00:00 0                                  [heap]
    7f0f1dba5000-7f0f1dcad000 r-xp 00000000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f0f1dcad000-7f0f1deac000 ---p 00108000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f0f1deac000-7f0f1dead000 r--p 00107000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f0f1dead000-7f0f1deae000 rw-p 00108000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f0f1deae000-7f0f1e06e000 r-xp 00000000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f0f1e06e000-7f0f1e26d000 ---p 001c0000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f0f1e26d000-7f0f1e271000 r--p 001bf000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f0f1e271000-7f0f1e273000 rw-p 001c3000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f0f1e273000-7f0f1e277000 rw-p 00000000 00:00 0 
    7f0f1e277000-7f0f1e28d000 r-xp 00000000 08:0a 267595                     /lib/x86_64-linux-gnu/libgcc_s.so.1
    7f0f1e28d000-7f0f1e48c000 ---p 00016000 08:0a 267595                     /lib/x86_64-linux-gnu/libgcc_s.so.1
    7f0f1e48c000-7f0f1e48d000 rw-p 00015000 08:0a 267595                     /lib/x86_64-linux-gnu/libgcc_s.so.1
    7f0f1e48d000-7f0f1e5ff000 r-xp 00000000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f0f1e5ff000-7f0f1e7ff000 ---p 00172000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f0f1e7ff000-7f0f1e809000 r--p 00172000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f0f1e809000-7f0f1e80b000 rw-p 0017c000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f0f1e80b000-7f0f1e80f000 rw-p 00000000 00:00 0 
    7f0f1e80f000-7f0f1e835000 r-xp 00000000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f0f1ea0d000-7f0f1ea12000 rw-p 00000000 00:00 0 
    7f0f1ea32000-7f0f1ea34000 rw-p 00000000 00:00 0 
    7f0f1ea34000-7f0f1ea35000 r--p 00025000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f0f1ea35000-7f0f1ea36000 rw-p 00026000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f0f1ea36000-7f0f1ea37000 rw-p 00000000 00:00 0 
    7fff71cd6000-7fff71cf7000 rw-p 00000000 00:00 0                          [stack]
    7fff71deb000-7fff71ded000 r--p 00000000 00:00 0                          [vvar]
    7fff71ded000-7fff71def000 r-xp 00000000 00:00 0                          [vdso]
    ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]

    ```
其中第3行列举了当前程序在运行时的heap地址范围为：  
`00e6f000-00ea1000 rw-p 00000000 00:00 0                                  [heap]`   
可以看出系统为该程序预留的heap空间有200K，测试程序中实际使用了30K。  
实际上系统使用了`/proc/<pid>/mem`映射了进程在执行时的实际内存，因此可以通过read这个文件来将程序的内存dump出来，但是需要满足两个条件才能使用第三方程序拷贝内存信息：   
1. 目标程序可以使用`ptrace(PTRACE_ATTACH, pid, NULL, NULL) `函数attach上，因为一个进程的内存只有程序self可以访问，gdb也是这个原理
2. 使用root用户来执行访问权限

在stackoverflow上找到了下面的小程序，稍加改动，将目标程序的heap内存拷贝到一个文件中
    ```
    /*************************
    sprintf(mem_file_name, "/proc/%d/mem", pid);
    mem_fd = open(mem_file_name, O_RDONLY);
    ptrace(PTRACE_ATTACH, pid, NULL, NULL);
    waitpid(pid, NULL, 0);
    lseek(mem_fd, offset, SEEK_SET);
    read(mem_fd, buf, _SC_PAGE_SIZE);
    ptrace(PTRACE_DETACH, pid, NULL, NULL);
    ***************************/

    #include <stdio.h>
    #include <stdlib.h>
    #include <limits.h>
    #include <sys/ptrace.h>
    #include <sys/socket.h>
    #include <arpa/inet.h>

    void dump_memory_region(FILE* pMemFile, unsigned long start_address, long length, int serverSocket)
    {
        unsigned long address;
        int pageLength = 4096;
        unsigned char page[pageLength];
        fseeko(pMemFile, start_address, SEEK_SET);

        FILE *fp;
        if ((fp = fopen("dump_file", "wba")) == NULL)
        {
            return ;
        }
        
        for (address=start_address; address < start_address + length; address += pageLength)
        {
            fread(&page, 1, pageLength, pMemFile);
            if (serverSocket == -1)
            {
                // write to file
                fwrite(&page, 1, pageLength, stdout);
                fwrite(&page, 1, pageLength, fp);
            }
            else
            {
                send(serverSocket, &page, pageLength, 0);
            }
        }
        
        fclose(fp);
    }

    int main(int argc, char **argv) {

        if (argc == 2 || argc == 4)
        {
            int pid = atoi(argv[1]);
            long ptraceResult = ptrace(PTRACE_ATTACH, pid, NULL, NULL);
            if (ptraceResult < 0)
            {
                printf("Unable to attach to the pid specified\n");
                return 0;
            }
            wait(pid, NULL, NULL);

            char mapsFilename[1024];
            sprintf(mapsFilename, "/proc/%s/maps", argv[1]);
            FILE* pMapsFile = fopen(mapsFilename, "r");
            char memFilename[1024];
            sprintf(memFilename, "/proc/%s/mem", argv[1]);
            FILE* pMemFile = fopen(memFilename, "r");
            int serverSocket = -1;
            if (argc == 4)
            {   
                unsigned int port;
                int count = sscanf(argv[3], "%d", &port);
                if (count == 0)
                {
                    printf("Invalid port specified\n");
                    return 0;
                }
                serverSocket = socket(AF_INET, SOCK_STREAM, 0);
                if (serverSocket == -1)
                {
                    printf("Could not create socket\n");
                    return 0;
                }
                struct sockaddr_in serverSocketAddress;
                serverSocketAddress.sin_addr.s_addr = inet_addr(argv[2]);
                serverSocketAddress.sin_family = AF_INET;
                serverSocketAddress.sin_port = htons(port);
                if (connect(serverSocket, (struct sockaddr *) &serverSocketAddress, sizeof(serverSocketAddress)) < 0)
                {
                    printf("Could not connect to server\n");
                    return 0;
                }
            }
            char line[256];
            int i = 0;
            while (fgets(line, 256, pMapsFile) != NULL)
            {
                unsigned long start_address;
                unsigned long end_address;
                sscanf(line, "%08lx-%08lx\n", &start_address, &end_address);
                
                if(i==3)
                {
                    printf("%s: start:%08lx end:%08lx size: %d\n", line, start_address, end_address, end_address - start_address);
                    dump_memory_region(pMemFile, start_address, end_address - start_address, serverSocket);
                }
                
                i++;
            }
            fclose(pMapsFile);
            fclose(pMemFile);
            if (serverSocket != -1)
            {
                close(serverSocket);
            }

            ptrace(PTRACE_CONT, pid, NULL, NULL);
            ptrace(PTRACE_DETACH, pid, NULL, NULL);
        }
        else
        {
            printf("%s <pid>\n", argv[0]);
            printf("%s <pid> <ip-address> <port>\n", argv[0]);
            exit(0);
        }
    }
    ```

编译该程序`gcc -o dump_data dump.c`使用`$sudo ./dump_data 8599`，其中8599为执行的mytest程序的pid，执行完成后得到的`dump_file`的大小为`204,800 bytes`，与系统给测试程序分配的heap大小一致，而执行mytest程序，输出`addr of p: 15207456 `的p的地址为15207456 (0x00E80C20)，这个地址是在heap的地址范围`00e6f000-00ea1000`内。通过计算变量p的地址和heap的起始地址的差`0x00E80C20 - 0x00e6f000 = 0x00011c20`得到p在heap中的偏移位置为0x00011c20，在Dump文件中0x00011c20开始的位置开始就是测试程序中给地址p赋值的`P`字符
    ```
    .....
    00011c10: 0000 0000 0000 0000 1178 0000 0000 0000  .........x......
    00011c20: 5050 5050 5050 5050 5050 5050 5050 5050  PPPPPPPPPPPPPPPP
    00011c30: 5050 5050 5050 5050 5050 5050 5050 5050  PPPPPPPPPPPPPPPP
    00011c40: 5050 5050 5050 5050 5050 5050 5050 5050  PPPPPPPPPPPPPPPP
    .....
    ```
说明了，new的内存不一定就是从系统给程序分配的heap起始位置开始分配内存的，而是在中间的某个位置，而且不知道为什么还有个x.

修改测试程序申请30M的内存
    ```
    int main()
    {
        unsigned long size = 30*1024*1024;
        char* p = new char[size];
        for(int i = 0;  i < size; i++)
        {
            *(p + i) = 'P';
        }
        long addr = (long)(p);
        cout << "addr of p: " << addr << endl;
        string name;
        cin >> name;

        return 0;
    }
    ```
程序中输出的变量p的地址为`addr of p: 139832631033872`,即0x7F2D524D0010，此时在查看程序的proc/pid/maps的信息如下:
    ```
    00400000-00401000 r-xp 00000000 08:06 154828                             /data/code/C++/algorithm/mytest
    00601000-00602000 r--p 00001000 08:06 154828                             /data/code/C++/algorithm/mytest
    00602000-00603000 rw-p 00002000 08:06 154828                             /data/code/C++/algorithm/mytest
    0093d000-0096f000 rw-p 00000000 00:00 0                                  [heap]
    7f2d524d0000-7f2d542d1000 rw-p 00000000 00:00 0 
    7f2d542d1000-7f2d543d9000 r-xp 00000000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f2d543d9000-7f2d545d8000 ---p 00108000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f2d545d8000-7f2d545d9000 r--p 00107000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f2d545d9000-7f2d545da000 rw-p 00108000 08:0a 267627                     /lib/x86_64-linux-gnu/libm-2.23.so
    7f2d545da000-7f2d5479a000 r-xp 00000000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f2d5479a000-7f2d54999000 ---p 001c0000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f2d54999000-7f2d5499d000 r--p 001bf000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f2d5499d000-7f2d5499f000 rw-p 001c3000 08:0a 267557                     /lib/x86_64-linux-gnu/libc-2.23.so
    7f2d5499f000-7f2d549a3000 rw-p 00000000 00:00 0 
    7f2d549a3000-7f2d549b9000 r-xp 00000000 08:0a 267595                     /lib/x86_64-linux-gnu/libgcc_s.so.1
    7f2d549b9000-7f2d54bb8000 ---p 00016000 08:0a 267595                     /lib/x86_64-linux-gnu/libgcc_s.so.1
    7f2d54bb8000-7f2d54bb9000 rw-p 00015000 08:0a 267595                     /lib/x86_64-linux-gnu/libgcc_s.so.1
    7f2d54bb9000-7f2d54d2b000 r-xp 00000000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f2d54d2b000-7f2d54f2b000 ---p 00172000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f2d54f2b000-7f2d54f35000 r--p 00172000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f2d54f35000-7f2d54f37000 rw-p 0017c000 08:0a 394965                     /usr/lib/x86_64-linux-gnu/libstdc++.so.6.0.21
    7f2d54f37000-7f2d54f3b000 rw-p 00000000 00:00 0 
    7f2d54f3b000-7f2d54f61000 r-xp 00000000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f2d55139000-7f2d5513e000 rw-p 00000000 00:00 0 
    7f2d5515e000-7f2d55160000 rw-p 00000000 00:00 0 
    7f2d55160000-7f2d55161000 r--p 00025000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f2d55161000-7f2d55162000 rw-p 00026000 08:0a 267529                     /lib/x86_64-linux-gnu/ld-2.23.so
    7f2d55162000-7f2d55163000 rw-p 00000000 00:00 0 
    7ffdcd8f2000-7ffdcd913000 rw-p 00000000 00:00 0                          [stack]
    7ffdcd997000-7ffdcd999000 r--p 00000000 00:00 0                          [vvar]
    7ffdcd999000-7ffdcd99b000 r-xp 00000000 00:00 0                          [vdso]
    ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]

    ```
可以发现heap大大小还是204800字节，根本不够内存申请的30M空间，而变量p的地址存在于第5行定义的空间，这个地址空间的后面没有任何说明信息，
`7f2d524d0000-7f2d542d1000 rw-p 00000000 00:00 0 `
这个地址范围表示的大小为31461376字节，刚好满足了30M内存的申请，考虑到page对齐，实际内存大小要稍微大些.C++中，无论在哪个平台上，heap的大小总是动态扩大的，进程向OS系统执行系统调用获取足够的内存空间。而在预定义的heap段大小嫩够满足用户申请的内存大小需求时，就使用预订的heap的地址空间。在maps信息中没有描述信息的段为匿名地址映射段，它们是通过`mmap()`使用`MAP_ANONYMOUS`标记创建的，对于匿名段，可能是程序的BSS段（未初始化的静态数据段，默认值都为0），也有可能时使用malloc函数申请的内存空间。

On most Unix systems, there is a hard limit on how much total memory a process can have. This limit can be queried with the getrlimit system call. The relevant constant is RLIMIT_AS. This limit governs the maximum number of memory pages that can be assigned to a process and directly limits the amount of heap space available. Unfortunately that limit doesn't directly say how much heap you can use. Memory pages are assigned to a process as a result of mmap calls, to hold the program code itself, and for the process' stack. Additionally, this limit is frequently set well in excess of the total memory available to the whole system if you add together physical memory and swap space. So in reality your program will frequently run out of memory before this limit is reached.  
Lastly, some versions of Unix over-assign pages. They allow you to allocate a massive number of pages, but only actually find memory for those pages when you write to them. This means your program can be killed for running out of memory even if all the memory allocation calls succeed. The rationale for this is the ability to allocate huge arrays which will only ever be partially used.  
You can get the total amount of availabe memory in the sytem by :  
    ```
    cat /proc/meminfo  | grep CommitLimit 
    CommitLimit:    3475960 kB
    ```
This `CommitLimit` is caculated with following formula:  `CommitLimit = ('vm.overcommit_ratio' * Physical RAM) + Swap`  
It is more typical to fix the size of the heap in dynamic languages with GC. In C and C++, it is a simple matter to ask the OS for more memory, since it is obvious when you need it. As a consequence, the initial heap size matters very little and is just an implementation decision on the part of the allocation library.  
In both C and C++ the heap policy is event driven. The compiler does generate heap allocation calls in C++, tho not in C. When the compiler generates a call to an allocator, it is now in the hands of the library because an actual function gets called. That function attempts to allocate from the heap (perhaps something has been freed recently) but if it fails it just calls the OS to get more memory for the process as a whole, and it adds that additional memory to the heap.

If you look in `arch/mips/mm/mmap.c` you'll find there are two ways of laying our memory in Linux, which is chosen depends on the return value of `mmap_is_legacy`, which in turn depends on whether you have enabled an unlimited `stack` (forces the legacy mode) and whether your binary in compiled which the flag `PT_GNU_STACK` (not having this set forces compatibility mode). linux在2.6.7之后加入了新的内存[布局方式](http://lwn.net/Articles/90311/)
旧的内存布局方式为:  
```
| CODE ---- | HEAP ----------> | MMAP ------>  | <-------- STACK |
| 0GB       |                  | 2GB/3         |             2GB |
```
新增的内存布局方式为：  
```
| CODE ---- | HEAP ----------> | <------------- MMAP | --- STACK |
| 0GB       |                  |             2GB-8MB |       2GB |
```
新的内存布局方式不限制了heap的大小，使得程序可以申请更大的内存。



