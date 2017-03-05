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