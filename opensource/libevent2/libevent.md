## Libevent

2019-01-05 周末学习 外面雾霾很大

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

##### epoll

`select()`调用中，内核只是通知我们关心的fd的状态就绪了，但不会把是哪一个告诉我们，但是我们还是需要从0开始循环遍历到系统分配给我们的最大的fd值，例如新建一个socket后，系统给的fd数字编号为5000，就要从0开始遍历到5000，然后发现5000这个fd的状态是可读，然后使用这个fd进行读数据。

看到一个以收快递的例子：

阻塞模式：你阻塞在家里等待快递员给你送快递，此时你什么都做不了，只能阻塞在门口看有没有快递员来，以免错过快递

异步轮询模式：你不停的给每一个快递公司打电话问快递到了没，此时你一直很忙，也做不了其他事

select的模式：你在家里面看电影或者做家务，9点的时候，你收到短信通知有快递到了，但是没有告诉你是那个包裹到了，你就要把门口的每一个快递员问一遍有没有你的快递。

epoll模式：在短信里面告诉你是申通和铁通的快递快递到了，你就不用去把门口的所有快递员逐个问一遍了。

```c
// create fd for epoll self, tell the kernel care about 1000 fds 
int epfd = epoll_create(1000);
// add a care fd to epoll
epoll_ctl(epfd, EPOLL_CTL_ADD, fd_conn, &care_event);

while(1) {
    // blocked wait for event trigger
    int count = epoll_wait(epfd, events, 1000, -1);
    
    for (i = 0; i<count; i++)
    {
        if (events[i].data.fd == listen_fd)
        {
            // accept and add the new connnection fd to epoll
        }
        else if (events[i].events & EPOLLIN)
        {
             // read data from events[i].data.fd
        }
        else if (events[i].events & EPOLLOUT)
        {
             // write data to events[i].data.fd
        }
    }
}
   
```

##### epoll触发模式

* 水平触发 只要一个fd没有被用户处理，下次内核还会通知，直到用户处理了
* 边缘触发 一个fd的状态就绪后，只会通知一次，这个状态就被清除了

#### 反应堆Reactor模式

每一个事件句柄/描述符(handle)都和对应的事件处理接口(EventHandler)一起注册到反应堆中

反应堆里面集成了一个多路事件分离器(demultiplexer)，用来检测是否有注册的事件发生。例如select或epoll函数，当然也可以使用自己维护的消息队列

当一个事件被检测到触发后，反应堆把事件派发(dispatch)给处理这个事件的处理接口

![reactor.png](./images/reactor.png)



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

#### 库文件

* `libevent_core`包括核心的event和buffer功能
* `libevent_extra`具体协议的实现，例如HTTP、DNS和RPC
* `libevent`历史原因而存在，包含以上两个库，如果是新程序，**不要用**这个库文件
* `libevent_pthreads` 和`libevent_openssl`只有编译时配置了才会生成，如果需要线程和锁，或者需要openssl支持，编译时可以选择配置上，一起编译。

### 基本应用

1. **头文件**在本地工程目录下新建include目录，并把Libevent的event2文件夹复制到include目录中。根据书中说明libevent2.0之后的API有调整，只需要include目录下的event2文件夹，对于Windows，还需要把WIN32-Code目录下的event2目录中的`event-config.h`拷贝到工程目录。在工程属性设置中，`C/C++--常规--附加包含目录`添加`$(ProjectDir)\include`
2. **库文件**在本地工程目录下新建lib目录，并把`libevent_extras.lib`,`libevent_core.lib`这两个编译出来的文件拷贝到lib目录里面。根据说明`libevent.lib`这个文件在2.0之后不再使用，后续会移除。在工程属性设置中，`链接器--输入--附加依赖项`添加`libevent_extras.lib`,`libevent_core.lib`这两个文件；`链接器--常规--附加库目录`添加`$(ProjectDir)\lib`
3. 之后可以在对应的实现文件中使用`#include <event2/event.h>`来引用Libevent的接口。

### 核心组件

#### evutil

抽象了不同平台的网络编程的实现差异

#### event_base

核心部分，提供了基于event的非阻塞IO后端。通知应用socket是否可以读或写，还包括了基本的超时功能以及检测系统信号。可以看做是Reactor模式的反应堆，其中注册了一堆event集合，检测哪个事件激活后，回调事件注册的处理函数。

一个进程中可以创建多个`event_base`，每一个管理一组事件。`event_base`如果设置了使用锁，则可以在多个线程间访问，但是它的loop只能在一个线程中运行。

##### 使用

```c
struct event_base *base;
// 这个接口创建的为默认的event_base，检测系统环境变量选择一个最快的多路复用接口
base = event_base_new();

// 其他事件初始化和注册 
// 事件循环loop
event_base_dispatch(base);
```

##### 配置

可以使用`event_config`并调用`event_base_new_with_config()`创建自定义的`event_base`

```c
struct event_config *event_config_new(void);
struct event_base *event_base_new_with_config(const struct event_config *cfg);
void event_config_free(struct event_config *cfg);
// 指定不用哪些多路复用接口(后端接口)
int event_config_avoid_method(struct event_config *cfg, const char *method);
// 无法满足指定features的后端接口，例如支持边缘触发、或者支持任意类型的fd，如果不支持则不会被使用
int event_config_require_features(struct event_config *cfg,
                                  enum event_method_feature feature);
// 设置属性例如不用锁来提高性能，或在Windows平台使用IOCP机制
int event_config_set_flag(struct event_config *cfg,
    enum event_base_config_flag flag);
// (windows) 指示使用多少个cpu
int event_config_set_num_cpus_hint(struct event_config *cfg, int cpus);
// 获取可以使用的后端
const char **event_get_supported_methods(void);
// 获取实际使用的后端
const char *event_base_get_method(const struct event_base *base);
// 释放一个不再使用的event_base，不会释放它管理的event和fd
void event_base_free(struct event_base *base);
// 设置一个event_base支持的最大优先级个数，优先级范围为[0, n_priorities-1],0的优先级最高
// 默认情况下，所以添加的event的优先级为n_priorities / 2
int event_base_priority_init(struct event_base *base, int n_priorities);
// 当创建一个子进程后，如果需要在子进程中继续使用event_base，需重新初始化
int event_reinit(struct event_base *base);
```

举例：

```c
struct event_config *cfg;
struct event_base *base;
cfg = event_config_new();
event_config_avoid_method(cfg, "select");
event_config_require_features(cfg, EV_FEATURE_ET);

base = event_base_new_with_config(cfg);

event_config_free(cfg);

if (fork()) {
    /* In parent */
    continue_running_parent(base); /*...*/
} else {
    /* In child */
    event_reinit(base);
    continue_running_child(base); /*...*/
}
```



#### event

Libevent的基本操作单元是一个事件。事件代表了一组条件发生了包括以下几种：

* 一个fd现在可以读或写
* 一个fd变得可以读或写
* 超时的时间到了
* 一个信号发生
* 用户触发的事件

##### 事件状态切换

![event_state.png](./images/event_state.png)

* 默认情况下，如果一个事件从pending变为active后，它就为non-pending状态了，如果要使其可以pending，可能需要在回调函数中手动调用一次add接口，此时可以设置为一个事件为`EV_PERSIST`，那么它在触发后，回调函数执行完会变为pending

##### 事件相关接口

```c
// 回调函数声明
typedef void (*event_callback_fn)(evutil_socket_t, short, void *);
// 创建一个non-pending的event，what为事件类型，如果fd为非负，则为我们关心的fd
struct event *event_new(struct event_base *base, evutil_socket_t fd,
    short what, event_callback_fn cb,
    void *arg); // 回调函数参数
// 释放一个event
void event_free(struct event *event);
//  ev = event_new(base, -1, EV_PERSIST, cb_func, event_self_cbarg());
void *event_self_cbarg(); // 返回当前创建的event对象的指针，使得event可以作为它的回调函数的参数 Libevent 2.1.1
// 支持POSIX-style的signal，以evsignal_开头
#define evsignal_new(base, signum, cb, arg) \
    event_new(base, signum, EV_SIGNAL|EV_PERSIST, cb, arg)
// 注册一个event，tv表示时间到了事件会触发，执行后事件变为pending状态
int event_add(struct event *ev, const struct timeval *tv);
// 把事件转换non-pending，如果一个事件处于active，且callback还没执行，此时执行了del会导致callback不会被执行了
int event_del(struct event *ev);
// 移除一个event的超时时间
int event_remove_timer(struct event *ev);
// event在初始化后，可以设置它的优先级
int event_priority_set(struct event *event, int priority);
// 以下接口获取event的状态
int event_pending(const struct event *ev, short what, struct timeval *tv_out);
#define event_get_signal(ev) /* ... */
evutil_socket_t event_get_fd(const struct event *ev);
struct event_base *event_get_base(const struct event *ev);
short event_get_events(const struct event *ev);
event_callback_fn event_get_callback(const struct event *ev);
void *event_get_callback_arg(const struct event *ev);
int event_get_priority(const struct event *ev);
void event_get_assignment(const struct event *event,
        struct event_base **base_out,
        evutil_socket_t *fd_out,
        short *events_out,
        event_callback_fn *callback_out,
        void **arg_out);
// 获取当前运行的事件的指针
struct event *event_base_get_running_event(struct event_base *base);
// 创建一个只会触发一次的事件，callback调用之后Libevent会删除和释放这个event
int event_base_once(struct event_base *, evutil_socket_t, short,
  void (*)(evutil_socket_t, short, void *), void *, const struct timeval *);
// 手动激活一个事件，在一个event的callback中手动激活这个event会导致死循环，可以先判断一个event时pending之后，先del在添加进base，并设置超时时间为0
void event_active(struct event *ev, int what, short ncalls);
```

* 当关注同一个fd的两个事件都发生时，这两个事件对象的回调函数执行顺序是不确定的。
* `evtimer_*`开头的宏方便创建timeout事件对`event_*`进行了重声明
* 一个进程中如果有两个`event_base`监听信号，那么只有一个`event_base`可以监听到信号，即使是不同的signal，这个由系统提供的backend函数决定
* 从2.1.2版本开始，如果释放了`event_base`，里面的event结构也会被释放，之前的版本不支持

##### 举例

```c
void cb_func(evutil_socket_t fd, short what, void *arg)
{
        const char *data = arg;
        printf("Got an event on socket %d:%s%s%s%s [%s]",
            (int) fd,
            (what&EV_TIMEOUT) ? " timeout" : "",
            (what&EV_READ)    ? " read" : "",
            (what&EV_WRITE)   ? " write" : "",
            (what&EV_SIGNAL)  ? " signal" : "",
            data);
}

struct event *ev1, *unimportant;
struct timeval five_seconds = {5,0};
struct event_base *base = event_base_new();
event_base_priority_init(base, 2);
important = event_new(base, fd1, EV_TIMEOUT|EV_READ|EV_PERSIST, cb_func,
           (char*)"Reading event");
event_priority_set(important, 0);
unimportant = event_new(base, fd2, EV_WRITE|EV_PERSIST, cb_func,
           (char*)"Writing event");
event_priority_set(unimportant, 1);
event_add(important, &five_seconds);
event_add(unimportant, NULL);
event_base_dispatch(base);
```

##### 使用非堆创建的event

有些时候处于性能考虑，不想使用heap上创建的event，而想把event作为一个大结构的一部分。这样可以节省：

* 堆上分配的小内存块负载
* 解引用指向event内存指针的消耗
* The time overhead from a possible additional cache miss if the  event is not already in the cache.

这些都是非常小的损耗，对于大部分程序都不需要考虑。如果一定要用可以使用`event_assign()`来初始化栈上的event对象。但是使用这个方法存在不同版本的Libevent之间event对象的大小不同的风险。高级玩法，还是不要随便尝试了。

```c
int event_assign(struct event *event, struct event_base *base,
    evutil_socket_t fd, short what,
    void (*callback)(evutil_socket_t, short, void *), void *arg);
// 获取当前版本的event结构的大小来处理兼容性
size_t event_get_struct_event_size(void);

struct event_pair {
         evutil_socket_t fd;
         struct event read_event;
         struct event write_event;
};
void readcb(evutil_socket_t, short, void *);
void writecb(evutil_socket_t, short, void *);
struct event_pair *event_pair_new(struct event_base *base, evutil_socket_t fd)
{
        struct event_pair *p = malloc(sizeof(struct event_pair));
        if (!p) return NULL;
        p->fd = fd;
        event_assign(&p->read_event, base, fd, EV_READ|EV_PERSIST, readcb, p);
        event_assign(&p->write_event, base, fd, EV_WRITE|EV_PERSIST, writecb, p);
        return p;
}
```

##### 公共超时优化

Libevent使用binary heap algorithm来跟踪每一个pending状态的时间的超时。这个算法对timeout大小有序的添加和删除一个超时事件可以达到O(lg n)的时间复杂度，这个方式是对timeout事件的时间是随机分布的一种优化，但是如果添加的1万个事件都是相同的5s后触发，这种情况下可以使用doubly-linked queue的方式，以O(1)的时间复杂度添加或删除一个event。但是使用队列的方式，对于添加随机timeout时间的事件需要O(n)，比二分法要差很多。

Libevent提供了一种公共超时接口，它把有相同时间的事件放到一个队列中，而其他的随机的时间的事件放到了binary heap中。如果有大量事件的时间都是相同的，可以使用这种优化。

```c
struct timeval ten_seconds = { 10, 0 };

void initialize_timeout(struct event_base *base)
{
    struct timeval tv_in = { 10, 0 };
    const struct timeval *tv_out;
    // 初始化一个公共超时结构
    tv_out = event_base_init_common_timeout(base, &tv_in);
    memcpy(&ten_seconds, tv_out, sizeof(struct timeval));
}

int my_event_add(struct event *ev, const struct timeval *tv)
{
    /* Note that ev must have the same event_base that we passed to
       initialize_timeout */
    if (tv && tv->tv_sec == 10 && tv->tv_usec == 0)
        // 使用这个的会放在一个单独的queue中
        return event_add(ev, &ten_seconds);
    else
        return event_add(ev, tv);
}
```

#### eventloop

```c
#define EVLOOP_ONCE		0x01 //阻塞执行loop直到有事件active，然后执行这个active事件，直到所有的事件执行完才会返回
#define EVLOOP_NONBLOCK		0x02 //非阻塞模式，检测是否有事件触发，然后执行这个事件的回调
#define EVLOOP_NO_EXIT_ON_EMPTY	0x04 // 即使事件为空，也不会结束执行而返回，除非event_base_loopbreak()或event_base_loopexit()被调用

int event_base_loop(struct event_base *base, int flags);
// 等价于没有设置任何flags，相当于设置了EVLOOP_NONBLOCK
int event_base_dispatch(struct event_base *base);
// 设置的tv时间之后停止loop，会把当前所有需要callback的执行完，再退出
int event_base_loopexit(struct event_base *base,
                        const struct timeval *tv);
// 执行完当前的那一个callback后，就立即退出
int event_base_loopbreak(struct event_base *base);
// 获取一个event loop是否是自己调用的退出
int event_base_got_exit(struct event_base *base);
int event_base_got_break(struct event_base *base);


```

默认情况下`event_base_loop`运行一个`event_base`直到这个base里面没有注册的事件即pending和active的事件。loop里面不断的检测注册的事件是否有被触发的，如果有，它把这个事件标记为active状态，并调用回调函数。

##### 内部执行的伪代码

默认情况下，event loop会先检测所有的事件状态，然后执行优先级最高的active的event的callback，然后再检测事件状态，再执行较低优先级的激活事件。如果需要在执行完一个callback后，立即检测一次事件状态，可以调用int event_base_loopcontinue(struct event_base *)。

```c
while (any events are registered with the loop,
        or EVLOOP_NO_EXIT_ON_EMPTY was set) {

    if (EVLOOP_NONBLOCK was set, or any events are already active)
        If any registered events have triggered, mark them active.
    else
        Wait until at least one event has triggered, and mark it active.
	// 这里是统一执行所有激活事件的callback，因此event_base_loopexit会把这里执行完
    for (p = 0; p < n_priorities; ++p) {
       if (any event with priority of p is active) {
          Run all active events with priority of p.
          // 只有这个优先级的事件被执行了，其他低优先级激活的event的都没有被执行
          break; /* Do not run any events of a less important priority */
       }
    }

    if (EVLOOP_ONCE was set or EVLOOP_NONBLOCK was set)
       break;
}
```

* 如果想在一个event的callback中获取当前的系统时间，而不想使用`gettimeofday()`这个系统调用导致性能问题，可以调用`int event_base_gettimeofday_cached(struct event_base *base, struct timeval *tv_out);`来获取Libevent的视角的当前这一轮callbacks开始执行的时间。如果当前没有在执行callbacks，这个接口调用`evutil_gettimeofday()`来获取当前的实际时间。如果你的callbacks的执行时间比较长，会导致这个接口获取的时间不是很精确，可以调用`int event_base_update_cache_time(struct event_base *base);`来立即更新时间

* 调试程序时，可能需要把`event_base`中当前所有的事件和他们的状态获取到，使用`void event_base_dump_events(struct event_base *base, FILE *f);`

* 对当前`event_base`中所有pending和active的event都执行一次一个函数。

  ```c
  typedef int (*event_base_foreach_event_cb)(const struct event_base *,
      const struct event *, void *);
  // event被迭代调用的顺序不确定，如果返回0，则会继续执行迭代，其他返回值会导致停止迭代
  // 这个函数中不能修改event和event_base的任何状态，同时执行这个函数时，如果event_base会加锁，以免其他线程修改了这个event_base，所以这个函数不要耗时操作
  int event_base_foreach_event(struct event_base *base,
                               event_base_foreach_event_cb fn,
                               void *arg);
  ```

  

##### 使用举例

```c
/* Here's a callback function that calls loopbreak */
void cb(int sock, short what, void *arg)
{
    struct event_base *base = arg;
    event_base_loopbreak(base);
}

void main_loop(struct event_base *base, evutil_socket_t watchdog_fd)
{
    struct event *watchdog_event;

    /* Construct a new event to trigger whenever there are any bytes to
       read from a watchdog socket.  When that happens, we'll call the
       cb function, which will make the loop exit immediately without
       running any other active events at all.
     */
    watchdog_event = event_new(base, watchdog_fd, EV_READ, cb, base);

    event_add(watchdog_event, NULL);

    event_base_dispatch(base);
}

void run_base_with_ticks(struct event_base *base)
{
  struct timeval ten_sec;

  ten_sec.tv_sec = 10;
  ten_sec.tv_usec = 0;

  /* Now we run the event_base for a series of 10-second intervals, printing
     "Tick" after each.  For a much better way to implement a 10-second
     timer, see the section below about persistent timer events. */
  while (1) {
     /* This schedules an exit ten seconds from now. */
     event_base_loopexit(base, &ten_sec);

     event_base_dispatch(base);
     puts("Tick");
  }
}
```





#### bufferevent

对Libevent的基于事件的核心功能进行了封装。应用可以获取到缓冲的可以读写的数据，而不用处理socket是否准备好读写。Windows上可以使用系统提供的IOCP机制。

#### evbuffer

bufferevent的内部的buffer实现