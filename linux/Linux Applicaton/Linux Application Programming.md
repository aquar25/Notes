[TOC]
##Linux Application Programming Second Edition

### Application Development Topics

#### Introduction to Sockets Programming

##### Layered Model of Networking

![layer_model_of_network](./images/layer_model_of_network.png)

* Port

  The port is the endpoint for a given process for a protocol. Ports are commonly called "bound" when they are attached to a given socket. Port numbers below 1024 are reserved for well-known service.

##### Client and Server application

![client_server_app](./images/client_server_app.png)

1. Create a socket. Socket is the communication endpoint that is created by the *socket* call.
2. The server *bind* an address and port.
3. The server *listen* on the port and wait for client to *connect* it.
4. When a client *connects* to a server, the server *accepts* the connection. Then a new socket connection exist between the client and server.
5. Both the client and server can *send* and *recv* data asynchronously.
6. Finally, each side can *close* the connection asynchronously and the other side automatically receives an indication of the closure.

#### Select调用

#### POSIX Threads

The 2.6 kernel utilizes the new Native POSIX Thread Library, or NPTL (introduced in 2002), which is a higher performance implementation with numerous advantages over the older component.

check the pthread version of current system with : `$getconf GNU_LIBPTHREAD_VERSION`, this will output `NPTL 2.23` on  my ubuntu 16.04.

When a process is forked,  a new process is created with its own globals and stack. When a thread is created, the only new element created is a stack that is unique for the thread. The code and global data section are common between the threads.

![create_a_new_process](/images/create_a_new_process.png)

![create_a_new_thread](/images/create_a_new_thread.png)

A process can create and manage numerous threads. Each thread is identified by a thread identifier that is unique for every thread in a system. Because the data space is shared by threads,  they share more than just user data. Such as file descriptors for open files or sockets are shared too. So we have to handle the resources been access by multiple threads.

The author strongly suggest that using shared data while developing threaded applications.

All pthread API will return 0 for success but a positive value to indicate an error. 

##### Create a thread

```c++
int pthread_create( pthread_t *thread, pthread_attr_t *attr,
	void *(*start_routine)(void *), void *arg );
int pthread_exit( void *retval );
```

`pthread_create`create a thread with `pthread_t` and a base function. The function `start_routine` represents the top level code that is executed within the thread. The `pthread_t` object mythread represents the new thread. We can use the fourth argument to send a value or a structure containing a variety of elements to the thread. The exit value presented to `pthread_exit` must not be of local scope; otherwise it won't exist after the thread is destroyed.

```c++
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

void* EntryFunction(void* arg)
{
    printf("Thread ran~\n");

    /* Terminate the thread */
    pthread_exit(NULL);
}

int main()
{
	printf("start up...\n");

    int ret;
    pthread_t mythread;
    
    ret = pthread_create(&mythread, NULL, EntryFunction, NULL);

    if (ret!=0)
    {
		printf("Can't create pthread (%s)\n", strerror(errno));
		exit(-1);
    }
    
    getchar();

    return 0;
}
```

build the demo with a make file

```makefile
threadapp: thread_demo.o
	gcc -pthread -lpthread -o threadapp thread_demo.o

thread_demo.o: thread_demo.c
	gcc -pthread -c -o thread_demo.o thread_demo.c 
```







###Debugging and Test

####Advanced Debugging

#####Memory Debugging
* Invalid use of a freed buffer
* Buffer overruns
* Memory leaks

######Valgrind:  
* memwatch of [Valgrind](http://valgrind.org/) suite. 

Valgrind works as CPU emulator, so the test application will slow by 20 or 30 times.

* intall `sudo apt-get install valgrind`
* compile our application with `-g`. like `g++ -g -o test test.cpp`
* using valgrind to run the application `valgrind --tool=memcheck ./test`
* profile an application's cache usage. `valgrind --tool=cachegrind ./test`

This utility details both instruction and data cache usage for the Level1 and Level2 caches. This is extremely useful for profiling cache usage to improve it for greater performance.

######Electric Fence(not recommend)
Electric Fence helps you detect two common programming bugs:

* software that overruns the boundaries of a malloc()memory allocation,
* software that touches a memory allocation that has been released by free().
* Unlike other malloc() debuggers, Electric Fence will detect read accesses as well as writes, and it will pinpoint the exact instruction that causes an error.

Electric Fence uses the virtual memory hardware of your computer to place an inaccessible memory page immediately after (or before, at the user's option) each memory allocation. So it will make our program to run slower with more memory. 

* install `sudo apt-get install electric-fence`
* using: link the library into your application `gcc -o test test.c -lefence`

######yamd
[yamd](https://www.cs.hmc.edu/~nate/yamd/) is a malloc debugging utility.  
Using `~$yamd-gcc test.c` to build our program and generate an executable called `a.out`. Execute the file `./a.out` will show the information.

######mtrace
mtrace just parse a trace file that is collected during the execution of an instrumented program. To instrument your program, add mtrace() function to log malloc and free calls. The mtrace is used in GNU libc, so if you are using GNU libc, it's ready to using.
```
#include <mcheck.h>

int
main (int argc, char *argv[])
{
#ifdef DEBUGGING
  mtrace ();
#endif
  …
}
```

######Custom but dangerous
think about using allocators.
* override the new/delete operator / malloc()/free() function.
* manage the allocated memory with a link-list
```
struct ALLOC_MEM_INFO
{
    DWORD pre;     // address of the pre memory
    DWORD next;    // address of the next memory
    DWORD stack[8];  // call stack to malloc 
};

```
The memory will malloc like 
FLAG + using_size + ALLOC_MEM_INFO + FLAG

######Others
[Memory debugger](https://en.wikipedia.org/wiki/Memory_debugger) on Wikipedia.

#### 时间处理

1. 将系统第一次开机以来的tick数保存在EEPROM中
2. 每次修改时间时，将最新的绝对时间和tick数保存EEPROM中
3. 系统时间通过RTC来保证正常运行，每次开机时从RTC中读取最新的时间

* 举例

保存系统绝对时间和第一次开机以来的绝对tick的变量分别为absTime和absTick

系统应用使用的时间为sysTime，同时有一个变量sysTick维护本次开机以来的tick数

sysTime每次开机时从RTC中读出来，而sysTick从开机后就一直每秒增加1.

当用户修改时间时，将sysTime设置为用户设置的时间，同时将它的值保存到RTC中。与此同时，需要将最新的绝对时间也更新保存到EEPROM中，最新的绝对tick数absTick = baseOffsetTick+sysTick.其中baseOffsetTick的值在第一次开机时为0。每次开机初始化时baseOffsetTick = 上次保存的absTick+（当前系统时间减去上次保存时间经过的秒数），因为设置时间时会同时设置RTC中和EEPROM中的时间，因此正常情况下EEPROM中的时间值肯定时小于RTC的，通过将RTC中的系统时间减去EEPROM中的绝对时间，就可以得到上次保存时间到这次开机经过的秒数，从而计算出第一次开机到现在本次开机经过的秒数。当系统中需要唯一的全局绝对Tick数时，就可以通过absTick = baseOffsetTick+sysTick得到。

1. 第一次开机时间为15:00 此时absTime为0,absTick也为0，用户需要设置系统时间为15:00,因此将设置sysTime为15:00并将其更新到RTC中，同时将absTime保存为15:00,absTick为本次开机经过的tick数，即0+sysTick，假设此时tick为200
2. 在经过1个小时后，即16:00时，用户将时间又修改为14:00，此时sysTime和absTime都为16:00,absTick=0+200+3600=3800s
3. 用户关机了一个小时，重新开机时，读取EEPROM中的上次保存的absTick和absTime，由于此时保存在RTC中的sysTime经过一个小时变成了15:00,因此计算本次开机时的baseOffsetTick=上次保存的绝对tick数+关机过程中经过的tick数=absTick+（sysTime-absTime）=3800s+3600s = 7400s，因此从第一次开机到此次开机时刻的绝对tick数就为7400s
4. 当系统需要使用全局绝地tick时，就通过本次开机时的绝对tick+本次开机到现在的系统tick数，absTick = baseOffsetTick+sysTick得到。