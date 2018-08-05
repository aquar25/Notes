##Accelerated Linux Core Dump Analysis

[source code](http://www.patterndiagnostics.com/Training/ALCDA/ALCDA-Dumps.tar.gz)
    ```
    Kernel Space
    User Space
    NULL Pointers
    ```

Linux memory range is divided into kernel space part, user space part and an inaccessible part to catch null pointers.

The mode is execution privilege attribute, for example, code running in kernel space has higher execution privilege than code running in user space.

modules in Windows are organized sequentially in virtual memory space. A process then is setup for running, and a process ID is assigned to it. If you run another such app, it will have the different virtual memory space.

When we save a process core memory dump a user space portion of the process space is saved without any kernel space stuff.However, we never see such large core dumps unless we have memory leaks. This is because process space has gaps unfilled with code and data. These unallocated parts are not saved in a core dump. However, if some parts were paged out and reside in a page file, they are usually brought back before saving a core dump.

threads transition to kernel space via libc dynamic library similar to ntdll on Windows and libsystem_kernel in Mac OS X.

###Dump Collection
Dump file is switch off by default.
* Temporary for current user: `ulimit -c unlimited`
* Permanent for every user except root: Edit the file `/etc/security/limits.conf` Add or uncomment the line `soft core unlimited`, To limit root to 1GB add or uncomment this line `root hart core 1000000`

####Generation Method
* kill (requires ulimit): `kill -s SIGQUIT PID` or `kill -s SIGABRT PID`
* gcore: `gcore PID`

####Practice
* Load a core file `gdb -c ./core_file -se ./app_file`
* List all threads: `info threads`
* Get all thread stack traces: `thread apply all bt`
* Switch to a thread and get its stack trace: `thread thread_id`
* Check the key function in the thread: `disassemble fun_name`
* Compare with intel disassembly flavor: `set disassembly-flavor intel` and then run `disassemble fun_name` or `set disassembly-flavor att`
* Get app's data section from the pmap file `pmap.3308`
    ```
    3308:   ./App1
    0000000000400000    732K r-x--  /home/training/ALCDA/App1/App1
    00000000006b6000      8K rw---  /home/training/ALCDA/App1/App1
    00000000006b8000     28K rw---    [ anon ]
    000000000227c000    140K rw---    [ anon ]
    00007f2257e66000      4K -----    [ anon ]
    00007f2257e67000   8192K rw---    [ anon ]
    00007f2258667000      4K -----    [ anon ]
    00007f2258668000   8192K rw---    [ anon ]
    00007f2258e68000      4K -----    [ anon ]
    00007f2258e69000   8192K rw---    [ anon ]
    00007f2259669000      4K -----    [ anon ]
    00007f225966a000   8192K rw---    [ anon ]
    00007f2259e6a000      4K -----    [ anon ]
    00007f2259e6b000   8192K rw---    [ anon ]
    00007ffc7d24d000    132K rw---    [ stack ]
    00007ffc7d299000      4K r-x--    [ anon ]
    ffffffffff600000      4K r-x--    [ anon ]
     total            42028K
    ```
* compare with the section information in the core dump `(gdb)maintenance info sections`
* Dump data with possible symbolic information: `x/512a 0x006b6000` this will output info like `address <name>: value1 value2`, each value is 8 bytes, and next address is +16 bytes
* Explore the contents of memory pointed to an address 
    ```
    x/u 0x6b6af0
    x/u &__nptl_nthreads
    x/2a 0x6b69e0
    x/2a &__nptl_nthreads // show 2 values with address
    x/10c 0x6b69e0 //show 10 value with char
    x/5s 0x6b69e0  // show 5 value with string
    ```
* Explore the contents of memory pointed to by environ variable address: `x/a &environ`
```
(gdb) x/a &environ
0x6bd4c8 <environ>: 0x7ffc7d26c808

(gdb) x/10a 0x7ffc7d26c808
0x7ffc7d26c808: 0x7ffc7d26d9ae 0x7ffc7d26d9be
0x7ffc7d26c818: 0x7ffc7d26d9c9 0x7ffc7d26d9d9
0x7ffc7d26c828: 0x7ffc7d26d9e7 0x7ffc7d26df08
0x7ffc7d26c838: 0x7ffc7d26df20 0x7ffc7d26df5e
0x7ffc7d26c848: 0x7ffc7d26df7c 0x7ffc7d26df8d

(gdb) x/4s 0x7ffc7d26d9ae
0x7ffc7d26d9ae: "SHELL=/bin/bash"
0x7ffc7d26d9be: "TERM=linux"
0x7ffc7d26d9c9: "HUSHLOGIN=FALSE"
0x7ffc7d26d9d9: "USER=training"
```

* Get the list of loaded modules: `info sharedlibrary`

* Disassemble bar_two function and follow the indirect sleep function call:
```
(gdb) disassemble bar_two
Dump of assembler code for function bar_two:
0x00000000004005f9 <+0>: push %rbp
0x00000000004005fa <+1>: mov %rsp,%rbp
0x00000000004005fd <+4>: mov $0xffffffff,%edi
0x0000000000400602 <+9>: callq 0x4004a0 <sleep@plt>
0x0000000000400607 <+14>: pop %rbp
0x0000000000400608 <+15>: retq
End of assembler dump.
(gdb) disassemble 0x4004a0
Dump of assembler code for function sleep@plt:
0x00000000004004a0 <+0>: jmpq *0x20090a(%rip) # 0x600db0 <sleep@got.plt>
0x00000000004004a6 <+6>: pushq $0x2
0x00000000004004ab <+11>: jmpq 0x400470
```

* Disassemble the problem instruction and check CPU register(s) details (NULL data pointer):
```
(gdb) x/i 0x400500
=> 0x400500 <procA+16>: movl $0x1,(%rax)
(gdb) info r $rax
rax 0x0 0
(gdb) x $rax
0x0: Cannot access memory at address 0x0
```

* List all thread stack traces and identify other anomalies such as non-waiting active threads:`(gdb) thread apply all bt`
* Check the CPU instruction and the stack pointer of the thread #6 for any signs of stack overflow(unaccessible stack addresses below the current stack pointer):
    ```
    (gdb) thread 6
    [Switching to thread 6 (Thread 0x7f560d467700 (LWP 3483))]
    #0 0x00000000004324a9 in clone ()
    (gdb) bt
    #0 0x00000000004324a9 in clone ()
    #1 0x0000000000401560 in ?? () at pthread_create.c:217
    #2 0x00007f560d467700 in ?? ()
    #3 0x0000000000000000 in ?? ()
    (gdb) x/i 0x4324a9
    => 0x4324a9 <clone+57>: test %rax,%rax
    (gdb) x/xg $rsp
    0x7f560d466e90: 0x0000000000401560
    (gdb) x/xg $rsp-8
    0x7f560d466e88: 0x0000000000000000
    (gdb) x/xg $rsp-x10
    0x7f560d466e80: 0x0000000000000000
    ```
