## Libevent

Libevent是一个C语言实现的跨平台的网络异步IO库 官网http://libevent.org/

官网建议的学习资料（基于2.0版本）

https://github.com/nmathewson/libevent-book

### 基本介绍

##### 阻塞IO

当你执行一个IO的调用时，执行过程是同步的，即只有当IO操作执行完了之后才会返回调用的地方。例如TCP连接时调用`coonect()`，操作系统发送一个SYN包给目的主机，只有收到目的主机应答的ACK或者超时后，才会返回调用`connect()`的地方，继续顺序执行程序。

网络通信的接口`connect()`、`accept()`、`send()`、`recv()`都是阻塞调用

##### 现实问题

当我们调用这些阻塞接口时，如果不需要做其他事情，等待也没有问题，但是在等待的时候我们还要处理其他事情，例如处理多个请求的连接的数据，如果使用阻塞方式，我们必须等待一个连接的数据收完之后，再去获取下一个连接的数据。

```c
char buf[1024];
int i, n;
while (i_still_want_to_read()) {
    for (i=0; i<n_sockets; ++i) {
        n = recv(fd[i], buf, sizeof(buf), 0);
        if (n==0)
            handle_close(fd[i]);
        else if (n<0)
            handle_error(fd[i], errno);
        else
            handle_input(fd[i], buf, n);
    }
}
```

如果是`fd[2]`的数据先发来，此时由于0、1的socket数据还没处理，所以`fd[2]`对应的数据一直没有机会取到。

##### 多线程或进程处理方式

一种简单的处理方法是对每一个连接创建一个线程或进程去处理这个连接的数据传输。这样不同的连接不会阻塞其他链接的执行。

但是创建线程或进程，以及线程数量大的情况下CPU切换线程的效率很低。

###### 类成员函数作为线程处理函数

* 注意下面的例子中，使用了类的成员函数作为线程的处理函数。

由于创建线程函数把的处理函数Proc后的参数作为处理函数Proc的参数传递，而类的成员函数的签名中，第一个参数固定为类的this指针，导致函数的类型不一致，无法直接使用。因此

1. 可以在类中添加一个静态成员函数作为线程处理函数，在把类的this指针作为线程函数的参数传入，静态的线程函数中再去调用类的成员函数。
2. 增加一个全局函数作为类的友元，这个全局函数作为线程处理函数，而友元函数中使用类成员
3. 把类的成员函数和一个线程函数声明定义为一个Union，在创建线程时使用union中的线程函数表示方式，本质上都是指向了同一个函数地址

```c++
void MemoryServer::AcceptOneConnectionWithThread(SOCKET listenSocket)
{
	SOCKET connectSocket;
	while (true)
	{
		// 接受一个客户端的连接
		SOCKADDR_IN clientAddr;
		int clientAddrLen = sizeof(clientAddr);
		connectSocket = accept(listenSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
		if (connectSocket == INVALID_SOCKET)
		{
			printf("Accept error:%d\n", WSAGetLastError());
		}
		else
		{
			printf("one connection come...\n");
			// 一个线程处理一个连接
			ThreadParam threadParam;
			threadParam.dwHandle = (DWORD)this;
			threadParam.param = (void*)connectSocket;
			DWORD dwThread = 0;
			HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)ThreadProc, (LPVOID)&threadParam, 0, &dwThread);
			if (hThread == NULL)
			{
				printf("CreateThread error:%d\n", WSAGetLastError());
				break;
			}
			CloseHandle(hThread);
		}
	}	
}

LPTHREAD_START_ROUTINE MemoryServer::ThreadProc(LPVOID lpParam)
{
	ThreadParam* threadParam = (ThreadParam*)lpParam;
	((MemoryServer*)(threadParam->dwHandle))->ProcessConnection(threadParam->param);
	return 0;
}

void MemoryServer::ProcessConnection(void* param)
{
	SOCKET connectSocket = (SOCKET)param;
	char szBuffer[BUFSIZE] = { 0 };
	while (true)
	{
		// 收客户端数据
		int nLen = recv(connectSocket, szBuffer, BUFSIZE, 0);
		if (nLen == 0)
		{
			printf("Recv Finished\n");
		}
		else if (nLen == SOCKET_ERROR)
		{
			printf("Recv error:%d\n", WSAGetLastError());
		}
		else
		{
			// 给客户端发数据
			for (int i = 0; i < nLen; i++)
			{
				if (szBuffer[i] == 'q')
				{
					break;
				}
				char out = ROT13(szBuffer[i]);
				int ret = send(connectSocket, &out, 1, 0);
				if (ret == SOCKET_ERROR)
				{
					printf("Send error:%d\n", WSAGetLastError());
				}
			}
		}
	}
	closesocket(connectSocket);
}
```

###### 一个使用进程的例子

```c
    if (listen(listener, 16)<0) {
        perror("listen");
        return;
    }

    while (1) {
        struct sockaddr_storage ss;
        socklen_t slen = sizeof(ss);
        int fd = accept(listener, (struct sockaddr*)&ss, &slen);
        if (fd < 0) {
            perror("accept");
        } else {
            if (fork() == 0) {
                child(fd);
                exit(0);
            }
        }
    }
// 新的进程函数
void
child(int fd)
{
    char outbuf[MAX_LINE+1];
    size_t outbuf_used = 0;
    ssize_t result;

    while (1) {
        char ch;
        result = recv(fd, &ch, 1, 0);
        if (result == 0) {
            break;
        } else if (result == -1) {
            perror("read");
            break;
        }

        /* We do this test to keep the user from overflowing the buffer. */
        if (outbuf_used < sizeof(outbuf)) {
            outbuf[outbuf_used++] = rot13_char(ch);
        }

        if (ch == '\n') {
            send(fd, outbuf, outbuf_used, 0);
            outbuf_used = 0;
            continue;
        }
    }
}
```

#### 非阻塞IO

在Linux平台可以使用`fcntl(fd, F_SETFL, O_NONBLOCK)`来把一个socket设置为非阻塞的。

第一个参数`fd`是socket的文件描述符。**文件描述**符是内核分配给一个socket的数字，在执行系统调用时，你可以使用这个数字来指向调用操作的socket。由于所以的对象都是文件，所以就是file descriptor.

当把一个socket设置为非阻塞后，原来的阻塞的网络接口会立即执行或者返回一个特殊的错误码告诉我们现在无法工作，try again。因此我们只能循环不停的调用recv来判断是否有新数据来。有两个问题：

1. 即使没有数据，while还会一直执行占用CPU
2. 当有多个socket连接后，每一个都会执行一次**系统调用**，即使这个连接现在根本没有数据

```c
/* This will work, but the performance will be unforgivably bad. */
int i, n;
char buf[1024];
for (i=0; i < n_sockets; ++i)
    fcntl(fd[i], F_SETFL, O_NONBLOCK);

while (i_still_want_to_read()) {
    for (i=0; i < n_sockets; ++i) {
        n = recv(fd[i], buf, sizeof(buf), 0);
        if (n == 0) {
            handle_close(fd[i]);
        } else if (n < 0) {
            if (errno == EAGAIN)
                 ; /* The kernel didn't have any data for us to read. */
            else
                 handle_error(fd[i], errno);
         } else {
            handle_input(fd[i], buf, n);
         }
    }
}
```

为了解决上述两个问题，需要让系统告诉我们当前哪个连接有数据，我们需要去取数据了，这样不用我们不停的自己轮询在每一个socket上执行系统调用。Linux提供了`select()`系统调用解决这个问题。

##### select调用

`int select (int maxfd + 1, fd_set *readset, fd_set *writeset, fd_set *exceptset, const struct timeval * timeout);` 

select使用三组文件描述符状态，一组表示可以读数据，一组表示可以写数据，一组表示异常，其中`fd_set`使用bit数组的每一个位表示一个文件表述符，最后一个参数时间单位是微秒，当设置为NULL时，select以阻塞方式执行，直到某一组的文件描述符发生变化，如果设置为0，则直接执行。

select相对于多线程的方式适合连接请求量比较大的情况，如果请求的连接数量不多，那就不如使用多线程的方式。在用户空间，我们可以按自己实际处理的socket的数量来初始化和检测fd的状态，但是在内核空间，内核是要判断最大的文件描述符的数值的大小，而不是实际的fd的个数。例如只有一个fd，而这个fd的值刚好被分配为65000，内核就要把0-65001个文件描述符都检测一遍的。而应用层因为知道当前的文件描述符的值，所以直接检测这个fd的状态。

```c
struct fd_state *state[FD_SETSIZE];
for (i = 0; i < FD_SETSIZE; ++i)
     state[i] = NULL;
fd_set readset, writeset, exset;
int i, n;
char buf[1024];
if (listen(listener, 16)<0) {
        perror("listen");
        return;
}

while (1) {
    maxfd = listener;
    // 每次都需要重新初始化一次
    FD_ZERO(&readset);
    FD_ZERO(&writeset);
    FD_ZERO(&exset);
    // 获取监听连接状态
    FD_SET(listener, &readset);
    for (i=0; i < FD_SETSIZE; ++i) {
        if (state[i]) {
            // 获取最大的文件描述符的数字编号，给select的第一个参数用
            if (i > maxfd)
                maxfd = i;
            // 把已经建立的连接加入读数据中，如果是写的，也加入写的组
            FD_SET(i, &readset);
            if (state[i]->writing) {
                FD_SET(i, &writeset);
            }
        }
    }
    // 阻塞等待直到有文件描述符可以读写
    if (select(maxfd+1, &readset, &writeset, &exset, NULL) < 0) {
        perror("select");
        return;
    }
    // 判断是否有新的连接来了
    if (FD_ISSET(listener, &readset)) {
        struct sockaddr_storage ss;
        socklen_t slen = sizeof(ss);
        // 建立一个连接后，把这个连接的fd加入select的检测状态表中
        int fd = accept(listener, (struct sockaddr*)&ss, &slen);
        if (fd < 0) {
            perror("accept");
        } else if (fd > FD_SETSIZE) { // 超过了select能处理的最大个数
            close(fd);
        } else {
            make_nonblocking(fd);
            state[fd] = alloc_fd_state();
            assert(state[fd]);/*XXX*/
        }
    }
    for (i=0; i < maxfd+1; ++i) {
        int r = 0;
        // 服务端监听的socket已经处理过读写了
        if (i == listener)
            continue;
        // 检测是哪一个可以读数据
        if (FD_ISSET(i, &readset)) {
            r = do_read(i, state[i]);
        }
        // 如果不是读，判断是不是写准备好了
        if (r == 0 && FD_ISSET(i, &writeset)) {
            r = do_write(i, state[i]);
        }
        // 处理过的要释放
        if (r) {
            free_fd_state(state[i]);
            state[i] = NULL;
            close(i);
        }
    }
}

int
do_read(int fd, struct fd_state *state)
{
    char buf[1024];
    int i;
    ssize_t result;
    while (1) {
        result = recv(fd, buf, sizeof(buf), 0);
        if (result <= 0)
            break;

        for (i=0; i < result; ++i)  {
            if (state->buffer_used < sizeof(state->buffer))
                state->buffer[state->buffer_used++] = rot13_char(buf[i]);
            if (buf[i] == '\n') {
                state->writing = 1;
                state->write_upto = state->buffer_used;
            }
        }
    }

    if (result == 0) {
        return 1;
    } else if (result < 0) {
        if (errno == EAGAIN)
            return 0;
        return -1;
    }

    return 0;
}

int
do_write(int fd, struct fd_state *state)
{
    while (state->n_written < state->write_upto) {
        ssize_t result = send(fd, state->buffer + state->n_written,
                              state->write_upto - state->n_written, 0);
        if (result < 0) {
            if (errno == EAGAIN)
                return 0;
            return -1;
        }
        assert(result != 0);

        state->n_written += result;
    }

    if (state->n_written == state->buffer_used)
        state->n_written = state->write_upto = state->buffer_used = 0;

    state->writing = 0;

    return 0;
}
```

##### select的替代

Linux有`epoll()`， BSDs (including Darwin) 的`kqueue()`, Solaris  `evports` 和`/dev/poll`。但是所有的这些接口在不同的平台上都不一样。**Libevent**对以上接口进行了统一的封装，根据当前的平台使用当前平台适合的select类似的底层接口，方便开发跨平台的程序。



### Libevent编译

#### Windows+VS2013

版本`libevent-2.1.8-stable`

1. 打开`VS2013 开发人员命令提示`，转到Libevent的目录

2. 到官方的github主页的test目录下载`print-winsock-errors.c`,并把这个文件拷贝到本地的test目录。官方的2.1.8包里面这个文件应该是遗漏了

3. 执行`nmake /f Makefile.nmake`

4. 如果编译过程中出现`regress_http.c`文件错误，可以直接修改对应的错误行代码，只保留结构体初始化的值，不用`struct http_server hs = { .port = 0, .ssl = ssl, };`的语法方式，直接为`struct http_server hs = {  0, ssl, }`。在VS2012有这个问题，VS2013没有遇到

5. 默认提供的`Makefile.nmake`文件编译出来的是release版本的，如果要编译Debug版本，需要修改文件中的

   ```bat
   # For optimization and warnings
   CFLAGS=$(CFLAGS) /Ox /W3 /wd4996 /nologo
   # 改为，其中的/MDd根据应用的类型调整
   CFLAGS=$(CFLAGS) /Od /MDd /Zi /W3 /wd4996 /nologo
   ```

   清空工程`nmake /f Makefile_Debug.nmake clean`，在用修改后的Debug版本编译

6. 编译完成后得到3个库文件`libevent.lib`,`libevent_extras.lib`,`libevent_core.lib`

### 基本应用

1. **头文件**在本地工程目录下新建include目录，并把Libevent的event2文件夹复制到include目录中。根据书中说明libevent2.0之后的API有调整，只需要include目录下的event2文件夹，对于Windows，还需要把WIN32-Code目录下的event2目录中的`event-config.h`拷贝到工程目录。在工程属性设置中，`C/C++--常规--附加包含目录`添加`$(ProjectDir)\include`
2. **库文件**在本地工程目录下新建lib目录，并把`libevent_extras.lib`,`libevent_core.lib`这两个编译出来的文件拷贝到lib目录里面。根据说明`libevent.lib`这个文件在2.0之后不再使用，后续会移除。在工程属性设置中，`链接器--输入--附加依赖项`添加`libevent_extras.lib`,`libevent_core.lib`这两个文件；`链接器--常规--附加库目录`添加`$(ProjectDir)\lib`
3. 之后可以在对应的实现文件中使用`#include <event2/event.h>`来引用Libevent的接口。