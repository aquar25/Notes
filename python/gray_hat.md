无论是windows的dll还是linux的so库，动态库中的函数都必须通过导出的名字调用，之后再在内存中找出真正的地址。

http://www.nostarch.com/ghpython.htm

#### 调用约定

1. 函数参数传递的顺序（压栈的顺序）
2. 函数返回时，栈的平衡处理（call执行完后，是否由调用者把esp再加回去，恢复到原来的位置）

* cdecl 函数参数从右向左依次入栈，函数的调用者负责函数的平衡，call后会多执行一个`add esp,函数栈大小` C语言一般是这种
* stdcall 不负责esp的恢复

#### ctypes

cdll() dll中的函数必须使用标准的cdecl调用约定
windll() dll中的函数必须使用stdcall调用约定
oledll() 和windll类似，如果函数返回一个HRESULT的错误代码，可以使用COM函数得到具体错误信息

python调用C库函数

```python
def call_vc_dll():
    msvcrt = cdll.msvcrt
    print(cdll.msvcrt)
    message_string = "Hello world!\n"
    msvcrt.printf("Testing: %s", message_string)
```

用户模式：ring3级别的程序，平时运行用户程序的一般模式，普通的程序
内核模式：驱动程序、内核，底层组件。wireshark就是和内核的网络驱动程序交互。

### 程序执行

#### x86寄存器

CPU 的寄存器能够对少量的数据进行快速的存取访问。 在x86指令集里，一个CPU 有八个通用寄存器：EAX, EDX, ECX, ESI, EDI, EBP, ESP 和 EBX。

EAX 寄存器也叫做累加寄存器，除了用于存储函数的返回值外也用于执行计算的操作。许多优化的x86指令集都专门设计了针对EAX寄存器的读写和计算指令。从最基本的加减、比较到特殊的乘除操作都有专门的EAX优化指令。

EDX 寄存器也叫做数据寄存器，它辅助EAX完成更多复杂的计算操作像乘法和除法。

ECX 寄存器也叫做计数寄存器用于循环操作。ECX寄存器的计算是向下而不是向上的简单理解就
是用于循环操作时是由大减到小的。例如一个循环是0-10，ECX中的值从10减小到0

ESI 寄存器是源操作数指针，存储着输入的数据流的位置。 
EDI 寄存器是目的操作数指针，存储了计算结果存储的位置。 
ESI (source index)用于读，EDI(destinationindex)用于写。
用源操作数指针和目的操作数指针，极大的提高了程序处理数据的效率。

EIP 总是指向马上要执行的指令
ESP 栈指针，指着栈顶
EBP 基指针，指着栈的底端
EBX 是唯一一个没有特殊用途的寄存器。它能够作为额外的数据储存器

#### 栈

栈从内存的高地址像低地址增长

函数返回的时候，它会弹出栈里所有的参数，返回地址弹到EIP ，然后跳到返回 地址(Return address)指向的地方(父函数的代码段)继续执行

![stack](./images/stack.jpg)

栈顶到栈底依次为(地址由小到大) 
局部变量  
返回地址  
参数1  
参数2 
栈帧基地址 

#### 调试事件

调试器在调试程序的时候会一直循环等待，直到检测到一个调试事件的发生
调试器一般都能捕获的事件有断点触发、段错误、程序异常。操作系统会使用不同的方法把这些事件传递给调试器。

#### 软件断点

CPU执行到指定位置的代码时，会暂停程序执行，并将控制权转移给调试器的断点处理函数

例如一个代码反汇编后为

`0x44332211: 8BC3 MOV EAX, EBX`

其中0x44332211为这个指令的地址，8BC3是CPU的操作码opcode，`MOV EAX, EBX`则是平时我们看的汇编代码。汇编器会把汇编代码转为CPU认识的操作码。
当我们在这个地址设置断点时，为了暂停CPU，需要将2个字节的操作码中的第一个字节替换为INT3中断指令，INT3的操作码是0xCC，因此设置了断点后，刚刚的语句中的8B就被替换为CC即

`0x44332211: CCC3 MOV EAX, EBX`

当CPU执行到这个操作码时，CPU暂停，触发一个INT3(3号中断)事件，调试器就处理这个事件。

当调试器被告知在目标地址设置一个断点，它首先读取目标地址的第一个字节的操作码， 然后保存起来，同时把地址存储在内部的中断列表中。然后调试器把一个字节操作码CC写
入刚才的地址。当CPU执行到CC操作码的时候就会触发一个 INT3 中断事件，此时调试器就能捕捉到这个事件。调试器继续判断这个发生中断事件的地址(通过EIP指针)是不是自己先前设置断点的地址。 如果在调试器内部的断点列表中找到了这个地址，就将设置断点前存储起来的操作码写回到目标地址，这样进程被调试器恢复后就能正常的执行。

![soft_breakpoint](./images/soft_breakpoint.png)

软中断会改变程序的内存值，如果如果程序对内存值进行了CRC校验，如果发现有错误就会结束程序。

#### 硬件断点

设置在CPU级别，并使用调试寄存器。一个CPU一般有8个调试寄存器(DR0-DR7)，它们用于管理硬件断点。
调试寄存器DR0到DR3存储硬件断点地址。因此同一时间内最多只能有4个硬件断点。DR4和DR5保留。DR6是状态寄存器，说明了被断点触发的调试事件的类型。DR7本质上是一个硬件断点的开关寄存器，同时也存储了断点的不同类型。   
通过在DR7寄存器里设置不同标志，能够创建以下几种断点：

* 当特定的地址上有指令执行的时候中断
* 当特定的地址上有数据可以写入的时候
* 当特定的地址上有数据读或者写但不执行的时候 

![DR7](./images/DR7.png) 

0-7位是硬件断点的激活与关闭开关。在这七位中L和G字段是局部和全局作用域的标志。我把两个位都设置了，以我的经验用户模式的调试中只设置一个就能工作。8-25 位 在我们一般的调试中用不到，在x86的手册上你可以找到关于这些字节的详细解释。16-31位决定了设置在4个断点寄存器中硬件断点的类型与长度。

![DR7_Set](./images/DR7_Set.png)

硬件断点不是用INT3中断，而是用INT1(1号中断)
INT1负责硬件中断和步进事件。步进Single-step意味着一步一步的执行指令，从而精确
的观察关键代码以便监视数据的变化。在CPU每次执行代码之前，都会先确认当前将执行的代码的地址是否是硬件断点的地址，同时也要确认是否有代码要访问被设置了硬件断点的内存区域。如果任何储存在DR0-DR3中的地址所指向的区域被访问了，就会触发INT1中断，同时暂停CPU。如果没有，CPU执行代码，到下一行代码时，CPU继续重复上面的检查。

硬件断点只能检测4个内存数据的改变，如果要调试一大块内存数据就不行了。

#### 内存断点

内存断点改变了内存中某个块或页的权限。一个内存页是OS处理的最小内存单位。一个页被申请成功后，就拥有了一个权限集，它决定了内存该如何被访问。

* 可执行页 允许执行但不允许读或写，否则抛出访问异常
* 可读页 只允许从页面中读取数据，其余的则抛出访问异常
* 可写页 允许将数据写入页面

有权限保护的页，常被用于分离堆和栈或者确保一部分内存数据不会增长出边界。
当一个特定的内存块被进程命中（访问）了，就暂停进程。 
例子：如果我们在逆向一个网络服务程序，在其接收到网络数据包以后，我们在存储数据包的内存上设置保护页，接着运行程序，一旦有任何对保护页的访问，都会使CPU暂停，抛出一个保护页调试异常，这时候我们就能确定程序是在什么时候用什么方式访问接收到的数据了。之后再进一步跟踪观察访问内存的指令，继而确定程序对数据做了什么操作。这种断点同时也解决了软件断点数据更新的问题，因为我们没有修改任何运行着的代码。

### 调试器

#### 调试器直接运行程序

调试器是父进程，对被调试程序的控制权大

```c++
BOOL WINAPI CreateProcessA(
    LPCSTR lpApplicationName, //程序的路径
    LPTSTR lpCommandLine, //传递给程序的参数
    LPSECURITY_ATTRIBUTES lpProcessAttributes,
    LPSECURITY_ATTRIBUTES lpThreadAttributes,
    BOOL bInheritHandles,
    DWORD dwCreationFlags, // 
    LPVOID lpEnvironment,
    LPCTSTR lpCurrentDirectory,
    LPSTARTUPINFO lpStartupInfo,//创 建 子 进 程 时 设 置 各 种 属 性 
    LPPROCESS_INFORMATION lpProcessInformation //进程创建后接收相关信息 该结构由系统填写
);
```



#### 调试器动态附加到运行的程序

在kernel32.dll 库中   

```c++
// 1. 获取目标程序句柄
HANDLE WINAPI OpenProcess(
    DWORD dwDesiredAccess, //权限 PROCESS_ALL_ACCESS 
    BOOL bInheritHandle // False
    DWORD dwProcessId // pid
);
// 2. attach到目标进程
BOOL WINAPI DebugActiveProcess(
	DWORD dwProcessId
);
// 3. 循环等待调试事件
BOOL WINAPI WaitForDebugEvent(
	LPDEBUG_EVENT lpDebugEvent,
	DWORD dwMilliseconds //INFINITE
);
// 4. 继续程序执行
BOOL WINAPI ContinueDebugEvent(
    DWORD dwProcessId,
    DWORD dwThreadId,
    DWORD dwContinueStatus
);

// 5. 与目标进程分离
DebugActiveProcessStop(pid)
```

#### 获取寄存器状态

* 枚举所有线程

`CreateToolhelp32Snapshot`可以枚举一个进程内部所有线程列表、加载的模块dll列表、使用的堆列表

```c++
HANDLE WINAPI CreateToolhelp32Snapshot(
	DWORD dwFlags,  // 要收集的数据类型（线程、模块、dll、堆）
	DWORD th32ProcessID // 进程id
);
```

获取一个进程的所以线程列表后，使用`Thread32First()` 枚举它们

```c++
BOOL WINAPI Thread32First(
	HANDLE hSnapshot,  // 镜像句柄
	LPTHREADENTRY32 lpte // THREADENTRY32结构，获取第一个线程的信息
);
```

`THREADENTRY32`的定义

```c++
typedef struct THREADENTRY32{
    DWORD dwSize;   // sizeof(THREADENTRY32)
    DWORD cntUsage;
    DWORD th32ThreadID; // tid
    DWORD th32OwnerProcessID; // pid
    LONG tpBasePri;
    LONG tpDeltaPri;
    DWORD dwFlags;
};
```

使用`Thread32Next()`获取快照中的下一个线程信息，它的参数和`Thread32First`的一样。

#### 获取线程句柄

```c++
HANDLE WINAPI OpenThread(
    DWORD dwDesiredAccess, //THREAD_ALL_ACCESS
    BOOL bInheritHandle, // None
    DWORD dwThreadId // TID
);
```

#### 获取和修改线程上下文

```c++
BOOL WINAPI GetThreadContext(
	HANDLE hThread, // OpenThread得到的线程句柄
	LPCONTEXT lpContext // 线程的上下文，包含所有寄存器状态
);
BOOL WINAPI SetThreadContext(
	HANDLE hThread,
	LPCONTEXT lpContext
);
```

#### 调试事件处理

`WaitForDebugEvent`捕获到一个调试事件后，会返回一个填充好的`DEBUG_EVENT`.

```c++
typedef struct DEBUG_EVENT {
    DWORD dwDebugEventCode;  // 事件类型代码，决定union中的值
    DWORD dwProcessId;
    DWORD dwThreadId;
    union {
        EXCEPTION_DEBUG_INFO Exception;  // 0x1
        CREATE_THREAD_DEBUG_INFO CreateThread; // 0x2
        CREATE_PROCESS_DEBUG_INFO CreateProcessInfo; // 0x3
        EXIT_THREAD_DEBUG_INFO ExitThread; // 0x4
        EXIT_PROCESS_DEBUG_INFO ExitProcess; // 0x5
        LOAD_DLL_DEBUG_INFO LoadDll; // 0x6
        UNLOAD_DLL_DEBUG_INFO UnloadDll; // 0x7
        OUTPUT_DEBUG_STRING_INFO DebugString; // 0x8
        RIP_INFO RipInfo;  // 0x9
    }u;
};
```

#### 断点实现

##### 软件断点

软件断点需要修改目标进程的内存，使用

```c++
BOOL WINAPI ReadProcessMemory(
    HANDLE hProcess,
    LPCVOID lpBaseAddress,  // 起始地址
    LPVOID lpBuffer,    // 接收读出的数据
    SIZE_T nSize,     // 读多少
    SIZE_T* lpNumberOfBytesRead //实际读了多少
);
BOOL WINAPI WriteProcessMemory(
    HANDLE hProcess,
    LPCVOID lpBaseAddress,  
    LPCVOID lpBuffer,
    SIZE_T nSize,
    SIZE_T* lpNumberOfBytesWritten
);
```

获取一个函数的地址使用`GetProcAddress() `需要一个模块句柄作为参数，使用`GetModuleHandle`获取模块的句柄

```c++
FARPROC WINAPI GetProcAddress(
    HMODULE hModule,
    LPCSTR lpProcName
);
HMODULE WINAPI GetModuleHandle(
	LPCSTR lpModuleName
);
```

##### 硬件断点

枚举所有线程，然后获取它们的CPU寄存器状态，定义`DR0-DR3`,让其包含目标断点地址，最后在DR7设置断点属性和长度。

##### 内存断点

* 查询一个内存块，并找到它的基地址（页的起始地址）

```c++
SIZE_T WINAPI VirtualQuery(
    HANDLE hProcess,
    LPCVOID lpAddress,
    PMEMORY_BASIC_INFORMATION lpBuffer, // 获取页信息
SIZE_T dwLength
);
typedef struct MEMORY_BASIC_INFORMATION{
    PVOID BaseAddress;   // 地址所在页的基地址
    PVOID AllocationBase;
    DWORD AllocationProtect;
    SIZE_T RegionSize;
    DWORD State;
    DWORD Protect;
    DWORD Type;
}
```

* 设置这个页的权限使其成为guard页

```
BOOL WINAPI VirtualProtectEx(
    HANDLE hProcess,
    LPVOID lpAddress,
    SIZE_T dwSize,
    DWORD flNewProtect,
    PDWORD lpflOldProtect
);
```

当CPU访问这个内存时，会抛出一个`GUARD_PAGE_EXCEPTION`异常，调试器捕获这个事件后，把页权限恢复，再让程序继续执行

获取系统页的默认大小使用`GetSystemInfo`它返回的`SYSTEM_INFO`结构包括`wPageSize`成员。









