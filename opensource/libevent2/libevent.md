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

通常一个网络数据传输的过程如下：

1. 把需要给一个连接发送的数据先缓存到一个buffer中
2. 等待链接变为可写状态
3. 写入尽可能多的数据
4. 记下已经写了多少还有多少需要写，等待连接再次可以写入

bufferevent实现了底层的传输，有一个读buffer和一个写buffer，当读或写的buffer中的数据足够后，回调用户提供的接口。

##### 回调和水位

每一个bufferevent有两个数据相关的回调函数，一个读数据回调，一个写数据回调。通过设置bufferevent的水位(watermarks)，可以控制读和写回调函数什么时候被执行。

有四种类型的水位

* 读-底限水位：默认值为0，当bufferevent的输入buffer的大小大于这个值时，触发读回调函数。因此默认只要有输入数据，就会触发读回调函数。
* 读-高限水位：当bufferevent的输入buffer的大小高于这个水位后，bufferevent会停止向input buffer中写入数据，直到用户从输入buffer中提取了数据后，使当前的水位低于这个值。默认为无限，因此永远不会停止从socket读数据。
* 写-低限水位：当输出buffer的水位低于这个值后，调用写回调函数，默认值为0，因此只有输出buffer为空的时候，才会回调写函数。
* 写-高限水位：bufferevent没有直接使用，只有一个bufferevent作为另一个bufferevent的底层传输通道时才有用。参见`filtering bufferevents`

##### 其他回调类型

bufferevent也一些非数据类型的错误和事件的回调通知，例如连接关闭或者发生任何错误。

`BEV_EVENT_READING`和`BEV_EVENT_WRITING`表示当前bufferevent正在执行读或写操作

`BEV_EVENT_ERROR` `BEV_EVENT_TIMEOUT` `BEV_EVENT_EOF`  `BEV_EVENT_CONNECTED`

##### 延迟回调(deferred callbacks)

通常一个回调函数会在对应的条件满足后立即执行，但是当多个回调直接有依赖关系时，容易产生问题。例如一个回调向buffer中写输入数据，而另一个回调从buffer中读数据，这两个之间需要有序执行，否则可能会产生栈溢出。

此时可以告诉bufferevent的回调函数需要被延迟执行，而不立即执行，这样这个回调会被放到`event_loop()`的队列中，在常规的事件回调之后被执行。

##### bufferevent的设置标志

* `BEV_OPT_CLOSE_ON_FREE`当bufferevent被释放后，其底层的socket也被关闭释放
* `BEV_OPT_THREADSAFE`增加锁操作，从而支持多线程使用
* `BEV_OPT_DEFER_CALLBACKS`注册的回调函数被放到队列延迟执行
* `BEV_OPT_UNLOCK_CALLBACKS`当设置了线程安全标记后，bufferevent的锁在调用用户的回调时，还是会保持锁的状态，设置了这个标记后，bufferevent调用用户的回调函数时，会释放自己的锁。

##### socket-based bufferevents

使用event事件的接口，并用socket传输数据

##### asynchronous-IO bufferevents

使用Windows的IOCP接口发送和接收数据

##### filtering bufferevents

可以对传输的数据可以预处理，然后再传输

##### paired bufferevents

两个bufferevent互相传输数据

```c
// 创建一个基于socket的bufferevent
struct bufferevent *bufferevent_socket_new(
    struct event_base *base,
    evutil_socket_t fd, // 注意确保这个socket是非阻塞的
    enum bufferevent_options options);
// 把一个socket设置为非阻塞的
evutil_make_socket_nonblocking(evutil_socket_t fd);
// 如果一个socket还没有连接，可以建立新连接，这样不用调用基于系统的connect接口
// 如果调用这个接口时，还没有给bufferevent设置socket，则它会自动创建一个。如果已经有socket，调用这个接口后，Libevent会知道这个socket没有连接，在这个connect成功之前都不会读或写这个socket
// 在socket连接建立之前给out buffer添加数据是允许的
int bufferevent_socket_connect(struct bufferevent *bev,
    struct sockaddr *address, int addrlen);
// 使用主机名的方式，如果域名解析失败，触发对应错误事件
int bufferevent_socket_connect_hostname(struct bufferevent *bev,
    struct evdns_base *dns_base, int family, const char *hostname,
    int port);    
// 获取使用主机名连接时的错误
int bufferevent_socket_get_dns_error(struct bufferevent *bev);
```

如果使用`bufferevent_socket_connect()`，被通知的事件为`BEV_EVENT_CONNECTED`，如果是自己使用系统的connect进行socket连接，被通知的事件为写事件。

如果想自己调用connect，并获取`BEV_EVENT_CONNECTED`事件，需要在`connect()`返回-1后的错误码为`EAGAIN` 或` EINPROGRESS`后调用`bufferevent_socket_connect(bev, NULL, 0)`

##### bufferevent的通用操作

```c
// 释放，只有当所有的回调函数都被执行了之后才会释放
void bufferevent_free(struct bufferevent *bev);
// 数据的回调
typedef void (*bufferevent_data_cb)(struct bufferevent *bev, void *ctx);
// 事件的回调类型
typedef void (*bufferevent_event_cb)(struct bufferevent *bev,
    short events, void *ctx);
// 设置读、写和事件的回调函数，最后一个参数作为回调函数的ctx参数，所有的回调函数共用
void bufferevent_setcb(struct bufferevent *bufev,
    bufferevent_data_cb readcb, bufferevent_data_cb writecb,
    bufferevent_event_cb eventcb, void *cbarg);
// 对应的读接口
void bufferevent_getcb(struct bufferevent *bufev,
    bufferevent_data_cb *readcb_ptr,
    bufferevent_data_cb *writecb_ptr,
    bufferevent_event_cb *eventcb_ptr,
    void **cbarg_ptr);
// 设置一个bufferevent使用和禁用的事件，可以禁用EV_READ, EV_WRITE事件，bufferevent就不会读写数据了。默认新建的bufferevent可以写，不能读，因为没数据啊。
void bufferevent_enable(struct bufferevent *bufev, short events);
void bufferevent_disable(struct bufferevent *bufev, short events);
// 获取一个bufferevent可用的事件
short bufferevent_get_enabled(struct bufferevent *bufev);
// 设置水位events是EV_READ设置读的，EV_WRITE设置写的。如果上限设置为0，则为无限
void bufferevent_setwatermark(struct bufferevent *bufev, short events,
    size_t lowmark, size_t highmark);
// 获取读写buffer
struct evbuffer *bufferevent_get_input(struct bufferevent *bufev);
struct evbuffer *bufferevent_get_output(struct bufferevent *bufev);
// 向写buffer中写入数据
int bufferevent_write(struct bufferevent *bufev, const void *data,size_t size);
int bufferevent_write_buffer(struct bufferevent *bufev, struct evbuffer *buf);
// 从读buffer中读数据，返回值size_t为实际读的
size_t bufferevent_read(struct bufferevent *bufev, void *data, size_t size);
int bufferevent_read_buffer(struct bufferevent *bufev,
    struct evbuffer *buf);
// 设置一个超时时间，在这个时间后如果没有任何数据读或写，就会触发timeout事件，当设置的时间为NULL时，表示移除这个超时事件注册。只有bufferevent准备读或写时，这个超时设置才生效，如果当前的输入buffer是满的或者写被禁用或没有触发写事件，则不会计时。当读或写超时发生后，对应的读写操作被禁用，此时事件回调函数被调用，并通知时间为EV_EVENT_TIMEOUT|BEV_EVENT_READING或BEV_EVENT_TIMEOUT|BEV_EVENT_WRITING.
void bufferevent_set_timeouts(struct bufferevent *bufev,
    const struct timeval *timeout_read, const struct timeval *timeout_write);

```

##### Type-specific bufferevent functions

```c
// 通知bufferevent尽可能从底层socket上读或写数据到buffer中, BEV_FINISHED告诉对端没有数据了，socket-based的bufferevent不支持
int bufferevent_flush(struct bufferevent *bufev,
    short iotype, // EV_READ|EV_WRITE
    enum bufferevent_flush_mode state); //BEV_NORMAL,BEV_FLUSH, or BEV_FINISHED
// 设置bufferevent的优先级，本质同event_priority_set()
int bufferevent_priority_set(struct bufferevent *bufev, int pri);
int bufferevent_get_priority(struct bufferevent *bufev);
// 设置基于socket的bufferevent的fd
int bufferevent_setfd(struct bufferevent *bufev, evutil_socket_t fd);
evutil_socket_t bufferevent_getfd(struct bufferevent *bufev);
// 获取event_base
struct event_base *bufferevent_get_base(struct bufferevent *bev);
// 获取这个bufev底层传输使用的bufferevent (filtering bufferevents)
struct bufferevent *bufferevent_get_underlying(struct bufferevent *bufev);
// 手动对bufferevent加锁，其中的evbuffer也会被锁，这样保证对bufferevent的操作是原子的，需要设置了BEV_OPT_THREADSAFE标记才行。加锁操作是迭代的，如果对一个bufferevent锁了两次，那么就要解锁两次
void bufferevent_lock(struct bufferevent *bufev);
void bufferevent_unlock(struct bufferevent *bufev);
```

###### 举例

```c
void eventcb(struct bufferevent *bev, short events, void *ptr)
{
    if (events & BEV_EVENT_CONNECTED) {
         /* We're connected to 127.0.0.1:8080.   Ordinarily we'd do
            something here, like start reading or writing. */
    } else if (events & BEV_EVENT_ERROR) {
         /* An error occured while connecting. */
    }
}

int main_loop(void)
{
    struct event_base *base;
    struct bufferevent *bev;
    struct sockaddr_in sin;

    base = event_base_new();

    memset(&sin, 0, sizeof(sin));
    sin.sin_family = AF_INET;   
    sin.sin_addr.s_addr = htonl(0x7f000001); /* 127.0.0.1 */
    sin.sin_port = htons(8080); /* Port 8080 */

    bev = bufferevent_socket_new(base, -1, BEV_OPT_CLOSE_ON_FREE);

    bufferevent_setcb(bev, NULL, NULL, eventcb, NULL);

    if (bufferevent_socket_connect(bev,
        (struct sockaddr *)&sin, sizeof(sin)) < 0) {
        /* Error starting connection */
        bufferevent_free(bev);
        return -1;
    }

    event_base_dispatch(base);
    return 0;
}
// -----------------------设置水位举例---------------------------------
struct info {
    const char *name;
    size_t total_drained;
};

void read_callback(struct bufferevent *bev, void *ctx)
{
    struct info *inf = ctx;
    struct evbuffer *input = bufferevent_get_input(bev);
    size_t len = evbuffer_get_length(input);
    if (len) {
        inf->total_drained += len;
        evbuffer_drain(input, len);
        printf("Drained %lu bytes from %s\n",
             (unsigned long) len, inf->name);
    }
}

void event_callback(struct bufferevent *bev, short events, void *ctx)
{
    struct info *inf = ctx;
    struct evbuffer *input = bufferevent_get_input(bev);
    int finished = 0;

    if (events & BEV_EVENT_EOF) {
        size_t len = evbuffer_get_length(input);
        printf("Got a close from %s.  We drained %lu bytes from it, "
            "and have %lu left.\n", inf->name,
            (unsigned long)inf->total_drained, (unsigned long)len);
        finished = 1;
    }
    if (events & BEV_EVENT_ERROR) {
        printf("Got an error from %s: %s\n",
            inf->name, evutil_socket_error_to_string(EVUTIL_SOCKET_ERROR()));
        finished = 1;
    }
    if (finished) {
        free(ctx);
        bufferevent_free(bev);
    }
}

struct bufferevent *setup_bufferevent(void)
{
    struct bufferevent *b1 = NULL;
    struct info *info1;

    info1 = malloc(sizeof(struct info));
    info1->name = "buffer 1";
    info1->total_drained = 0;

    /* ... Here we should set up the bufferevent and make sure it gets
       connected... */

    /* Trigger the read callback only whenever there is at least 128 bytes
       of data in the buffer. */
    bufferevent_setwatermark(b1, EV_READ, 128, 0);

    bufferevent_setcb(b1, read_callback, NULL, event_callback, info1);

    bufferevent_enable(b1, EV_READ); /* Start reading. */
    return b1;
}

///--------------------------读写数据-----------------------------------////
void
read_callback_uppercase(struct bufferevent *bev, void *ctx)
{
        /* This callback removes the data from bev's input buffer 128
           bytes at a time, uppercases it, and starts sending it
           back.
           (Watch out!  In practice, you shouldn't use toupper to implement
           a network protocol, unless you know for a fact that the current
           locale is the one you want to be using.)
         */
        char tmp[128];
        size_t n;
        int i;
        while (1) {
                n = bufferevent_read(bev, tmp, sizeof(tmp));
                if (n <= 0)
                    break; /* No more data. */
                for (i=0; i<n; ++i)
                    tmp[i] = toupper(tmp[i]);
                bufferevent_write(bev, tmp, n);
        }
}

struct proxy_info {
        struct bufferevent *other_bev;
};
void
read_callback_proxy(struct bufferevent *bev, void *ctx)
{
        /* You might use a function like this if you're implementing
           a simple proxy: it will take data from one connection (on
           bev), and write it to another, copying as little as
           possible. */
        struct proxy_info *inf = ctx;
        bufferevent_read_buffer(bev,
            bufferevent_get_output(inf->other_bev));
}

struct count {
        unsigned long last_fib[2];
};

void
write_callback_fibonacci(struct bufferevent *bev, void *ctx)
{
        /* Here's a callback that adds some Fibonacci numbers to the
           output buffer of bev.  It stops once we have added 1k of
           data; once this data is drained, we'll add more. */
        struct count *c = ctx;
        struct evbuffer *tmp = evbuffer_new();
        while (evbuffer_get_length(tmp) < 1024) {
                 unsigned long next = c->last_fib[0] + c->last_fib[1];
                 c->last_fib[0] = c->last_fib[1];
                 c->last_fib[1] = next;

                 evbuffer_add_printf(tmp, "%lu", next);
        }

        /* Now we add the whole contents of tmp to bev. */
        bufferevent_write_buffer(bev, tmp);

        /* We don't need tmp any longer. */
        evbuffer_free(tmp);
}
```



#### evbuffer

bufferevent的内部的buffer实现。

evbuffer实现了一个字节类型的队列，对从队尾添加数据和队首删除数据做了优化。

##### 基本接口

```c
// 创建或释放buffer
struct evbuffer *evbuffer_new(void);
void evbuffer_free(struct evbuffer *buf);
// 线程安全加锁，默认不支持锁
int evbuffer_enable_locking(struct evbuffer *buf, void *lock);
void evbuffer_lock(struct evbuffer *buf);
void evbuffer_unlock(struct evbuffer *buf);
// 获取大小，单位字节
size_t evbuffer_get_length(const struct evbuffer *buf);
// evbuffer中的内存可能被分割为多个块存储，这个函数返回第一块的大小
size_t evbuffer_get_contiguous_space(const struct evbuffer *buf);
// 添加数据到队尾
int evbuffer_add(struct evbuffer *buf, const void *data, size_t datlen);
// 添加类似printf输出的格式化子串到队尾，返回添加的字节数
int evbuffer_add_printf(struct evbuffer *buf, const char *fmt, ...)
int evbuffer_add_vprintf(struct evbuffer *buf, const char *fmt, va_list ap);
// 扩充buffer的大小到datlen
int evbuffer_expand(struct evbuffer *buf, size_t datlen);
// evbuffer之间的数据移动，把src的全部移到dst中
int evbuffer_add_buffer(struct evbuffer *dst, struct evbuffer *src);
// 把src的前datlen字节数量的数据移到dst中
int evbuffer_remove_buffer(struct evbuffer *src, struct evbuffer *dst,
    size_t datlen);
// 在buffer前插入数据，bufferevent的evbuffer不能使用这两个接口
int evbuffer_prepend(struct evbuffer *buf, const void *data, size_t size);
int evbuffer_prepend_buffer(struct evbuffer *dst, struct evbuffer* src);
// 删除数据
int evbuffer_drain(struct evbuffer *buf, size_t len);
// 删除并拷贝到data中，返回实际删除字节数量
int evbuffer_remove(struct evbuffer *buf, void *data, size_t datlen);
// 从头开始拷贝datlen个字节出来
ev_ssize_t evbuffer_copyout(struct evbuffer *buf, void *data, size_t datlen);
// 从pos开始拷贝datlen个字节出来
ev_ssize_t evbuffer_copyout_from(struct evbuffer *buf,
     const struct evbuffer_ptr *pos,
     void *data_out, size_t datlen);
// 如果上面两个拷贝太慢用这个
evbuffer_peek();
// 一次读取一行数据出来，返回的char*是新allocated NUL-terminated string（很多网络协议都以行为单位）
char *evbuffer_readln(struct evbuffer *buffer, size_t *n_read_out,
    enum evbuffer_eol_style eol_style);
// 设置buffer为add- or remove-only bufferevent内部使用这两个接口来阻止意外的修改evbuffer
int evbuffer_freeze(struct evbuffer *buf, int at_front);
int evbuffer_unfreeze(struct evbuffer *buf, int at_front);
```

只有当你对evbuffer进行了多个操作的时候才需要加锁，如果只是一个操作，不用加锁，本身就是原子的，不会插入其他操作。

##### 内存块(chunk)

由于数据可能被分成了多个块存储，如果我们想对最开头的一部分数据按字节顺序解析，此时如果刚好被分割为不同的块，就不连续了。此时需要使用

`unsigned char *evbuffer_pullup(struct evbuffer *buf, ev_ssize_t size);`

把前size字节的数据放到连续的块中，如果size为负数，表示全部都要排到一个块中，函数返回内存块的首地址。由于可能存在大量内存的移动操作，可能导致很慢。

```c
#include <event2/buffer.h>
#include <event2/util.h>
#include <string.h>
int parse_socks4(struct evbuffer *buf, ev_uint16_t *port, ev_uint32_t *addr)
{
    /* Let's parse the start of a SOCKS4 request!  The format is easy:
     * 1 byte of version, 1 byte of command, 2 bytes destport, 4 bytes of
     * destip. */
    unsigned char *mem;
    mem = evbuffer_pullup(buf, 8);
    if (mem == NULL) {
        /* Not enough data in the buffer */
        return 0;
    } else if (mem[0] != 4 || mem[1] != 1) {
        /* Unrecognized protocol or command */
        return -1;
    } else {
        memcpy(port, mem+2, 2);
        memcpy(addr, mem+4, 4);
        *port = ntohs(*port);
        *addr = ntohl(*addr);
        /* Actually remove the data from the buffer now that we know we
           like it. */
        evbuffer_drain(buf, 8);
        return 1;
    }
}

int get_record(struct evbuffer *buf, size_t *size_out, char **record_out)
{
    /* Let's assume that we're speaking some protocol where records
       contain a 4-byte size field in network order, followed by that
       number of bytes.  We will return 1 and set the 'out' fields if we
       have a whole record, return 0 if the record isn't here yet, and
       -1 on error.  */
    size_t buffer_len = evbuffer_get_length(buf);
    ev_uint32_t record_len;
    char *record;

    if (buffer_len < 4)
       return 0; /* The size field hasn't arrived. */

   /* We use evbuffer_copyout here so that the size field will stay on
       the buffer for now. */
    evbuffer_copyout(buf, &record_len, 4);
    /* Convert len_buf into host order. */
    record_len = ntohl(record_len);
    if (buffer_len < record_len + 4)
        return 0; /* The record hasn't arrived */

    /* Okay, _now_ we can remove the record. */
    record = malloc(record_len);
    if (record == NULL)
        return -1;

    evbuffer_drain(buf, 4);
    evbuffer_remove(buf, record, record_len);

    *record_out = record;
    *size_out = record_len;
    return 1;
}
```

##### 在一个evbuffer中遍历和查找

`evbuffer_ptr`结构指向`evbuffer`中的一个位置。

任何修改`evbuffer`的内容或者移动内部的内存布局，都会导致`evbuffer_ptr`的值不可靠

```c
struct evbuffer_ptr {
        ev_ssize_t pos; //惟一用户可以使用的公共字段，表示偏移位置
        struct {
                /* internal fields */
        } _internal; // 用户不要用
};
// 在buffer中从start位置开始找len长度的what子串，返回找到的位置，如果start为空，则从头开始找
struct evbuffer_ptr evbuffer_search(struct evbuffer *buffer,
    const char *what, size_t len, const struct evbuffer_ptr *start);
struct evbuffer_ptr evbuffer_search_range(struct evbuffer *buffer,
    const char *what, size_t len, const struct evbuffer_ptr *start,
    const struct evbuffer_ptr *end);
struct evbuffer_ptr evbuffer_search_eol(struct evbuffer *buffer,
    struct evbuffer_ptr *start, size_t *eol_len_out,
    enum evbuffer_eol_style eol_style);
// 移动一个指针的位置
enum evbuffer_ptr_how {
        EVBUFFER_PTR_SET, // 设置绝对位置
        EVBUFFER_PTR_ADD   //向前进一定的位置
};
int evbuffer_ptr_set(struct evbuffer *buffer, 
                     struct evbuffer_ptr *pos, // 被移动的指针    
                     size_t position,          // 移动多少 
                     enum evbuffer_ptr_how how);//移动的方式
```

##### 使用evbuffer中间的数据而不拷贝出来

我只想看看里面的数据，不想拷贝，不然太慢了呢

`evbuffer_peek()`需要一个`evbuffer_iovec`结构的数组参数，数组长度为`n_vec`,他把每一个内部的块的指针放到`iov_base`，块长度放到`iov_len`。如果`n_vec`为负数，则会填满你给的结构体数组。返回的数据不能修改，否则导致不确定错误。如果buffer中的数据已经被修改了，则修改之前返回的`evbuffer_iovec`是无效的。注意多线程加锁

```c
struct evbuffer_iovec {
	void *iov_base;
	size_t iov_len;
};

int evbuffer_peek(struct evbuffer *buffer, ev_ssize_t len,
    struct evbuffer_ptr *start_at,
    struct evbuffer_iovec *vec_out, int n_vec);
```

* 举例

```c
{
    /* Let's look at the first two chunks of buf, and write them to stderr. */
    int n, i;
    struct evbuffer_iovec v[2];
    n = evbuffer_peek(buf, -1, NULL, v, 2);
    for (i=0; i<n; ++i) { /* There might be less than two chunks available. */
        fwrite(v[i].iov_base, 1, v[i].iov_len, stderr);
    }
}

{
    /* Let's send the first 4906 bytes to stdout via write. */
    int n, i, r;
    struct evbuffer_iovec *v;
    size_t written = 0;

    /* determine how many chunks we need. */
    n = evbuffer_peek(buf, 4096, NULL, NULL, 0);
    /* Allocate space for the chunks.  This would be a good time to use
       alloca() if you have it. */
    v = malloc(sizeof(struct evbuffer_iovec)*n);
    /* Actually fill up v. */
    n = evbuffer_peek(buf, 4096, NULL, v, n);
    for (i=0; i<n; ++i) {
        size_t len = v[i].iov_len;
        if (written + len > 4096)
            len = 4096 - written;
        r = write(1 /* stdout */, v[i].iov_base, len);
        if (r<=0)
            break;
        /* We keep track of the bytes written separately; if we don't,
           we may write more than 4096 bytes if the last chunk puts
           us over the limit. */
        written += len;
    }
    free(v);
}

{
    /* Let's get the first 16K of data after the first occurrence of the
       string "start\n", and pass it to a consume() function. */
    struct evbuffer_ptr ptr;
    struct evbuffer_iovec v[1];
    const char s[] = "start\n";
    int n_written;

    ptr = evbuffer_search(buf, s, strlen(s), NULL);
    if (ptr.pos == -1)
        return; /* no start string found. */

    /* Advance the pointer past the start string. */
    if (evbuffer_ptr_set(buf, &ptr, strlen(s), EVBUFFER_PTR_ADD) < 0)
        return; /* off the end of the string. */

    while (n_written < 16*1024) {
        /* Peek at a single chunk. */
        if (evbuffer_peek(buf, -1, &ptr, v, 1) < 1)
            break;
        /* Pass the data to some user-defined consume function */
        consume(v[0].iov_base, v[0].iov_len);
        n_written += v[0].iov_len;

        /* Advance the pointer so we see the next chunk next time. */
        if (evbuffer_ptr_set(buf, &ptr, v[0].iov_len, EVBUFFER_PTR_ADD)<0)
            break;
    }
}
```

##### 直接给evbuffer添加数据

有时不想先把一个数据拷贝到一个字节数组后，再拷贝到evbuffer中，就想直接把数据放到buffer中。

```c
// 先扩展size空间，并把扩展空间的结构指针给你, n_vecs至少为1，不然怎么给你分地方
// 出于性能考虑，最好至少2个vector传进去。函数返回他实际需要的vector的个数
int evbuffer_reserve_space(struct evbuffer *buf, ev_ssize_t size,
    struct evbuffer_iovec *vec, int n_vecs);
// 把数据给vec后，提交给evbuffer，你也可以不把申请的都用了
int evbuffer_commit_space(struct evbuffer *buf,
    struct evbuffer_iovec *vec, int n_vecs);

/* Suppose we want to fill a buffer with 2048 bytes of output from a
   generate_data() function, without copying. */
struct evbuffer_iovec v[2];
int n, i;
size_t n_to_add = 2048;

/* Reserve 2048 bytes.*/
n = evbuffer_reserve_space(buf, n_to_add, v, 2);
if (n<=0)
   return; /* Unable to reserve the space for some reason. */

for (i=0; i<n && n_to_add > 0; ++i) {
   size_t len = v[i].iov_len;
   if (len > n_to_add) /* Don't write more than n_to_add bytes. */
      len = n_to_add;
   if (generate_data(v[i].iov_base, len) < 0) {
      /* If there was a problem during data generation, we can just stop
         here; no data will be committed to the buffer. */
      return;
   }
   /* Set iov_len to the number of bytes we actually wrote, so we
      don't commit too much. */
   v[i].iov_len = len;
}

/* We commit the space here.  Note that we give it 'i' (the number of
   vectors we actually used) rather than 'n' (the number of vectors we
   had available. */
if (evbuffer_commit_space(buf, v, i) < 0)
   return; /* Error committing */

//-------------------错误用法--------------------------
/* Here are some mistakes you can make with evbuffer_reserve().
   DO NOT IMITATE THIS CODE. */
struct evbuffer_iovec v[2];

{
  /* Do not use the pointers from evbuffer_reserve_space() after
     calling any functions that modify the buffer. */
  evbuffer_reserve_space(buf, 1024, v, 2);
  evbuffer_add(buf, "X", 1);
  /* WRONG: This next line won't work if evbuffer_add needed to rearrange
     the buffer's contents.  It might even crash your program. Instead,
     you add the data before calling evbuffer_reserve_space. */
  memset(v[0].iov_base, 'Y', v[0].iov_len-1);
  evbuffer_commit_space(buf, v, 1);
}

{
  /* Do not modify the iov_base pointers. */
  const char *data = "Here is some data";
  evbuffer_reserve_space(buf, strlen(data), v, 1);
  /* WRONG: The next line will not do what you want.  Instead, you
     should _copy_ the contents of data into v[0].iov_base. */
  v[0].iov_base = (char*) data;
  v[0].iov_len = strlen(data);
  /* In this case, evbuffer_commit_space might give an error if you're
     lucky */
  evbuffer_commit_space(buf, v, 1);
}
```

##### 读socket数据接口

Unix类型的系统可以读写所有支持读写操作的fd，Windows上只支持socket

```c
int evbuffer_write(struct evbuffer *buffer, evutil_socket_t fd);
int evbuffer_write_atmost(struct evbuffer *buffer, evutil_socket_t fd,
        ev_ssize_t howmuch);
int evbuffer_read(struct evbuffer *buffer, evutil_socket_t fd, int howmuch);
```

##### 回调函数

当有数据添加到buffer或从buffer中删除，会触发注册的回调函数

```c
struct evbuffer_cb_info {
        size_t orig_size;
        size_t n_added;
        size_t n_deleted;
};

typedef void (*evbuffer_cb_func)(struct evbuffer *buffer,
    const struct evbuffer_cb_info *info, void *arg);

struct evbuffer_cb_entry; // 一个空结构体用来引用回调函数的实例，删除的时候要用
// 一个buffer上可注册多个回调函数，添加新的不会删除旧的
struct evbuffer_cb_entry *evbuffer_add_cb(struct evbuffer *buffer,
    evbuffer_cb_func cb, void *cbarg);
int evbuffer_remove_cb_entry(struct evbuffer *buffer,
    struct evbuffer_cb_entry *ent);
int evbuffer_remove_cb(struct evbuffer *buffer, evbuffer_cb_func cb,
    void *cbarg);
// 临时禁用一个回调
#define EVBUFFER_CB_ENABLED 1
int evbuffer_cb_set_flags(struct evbuffer *buffer,
                          struct evbuffer_cb_entry *cb,
                          ev_uint32_t flags);
int evbuffer_cb_clear_flags(struct evbuffer *buffer,
                          struct evbuffer_cb_entry *cb,
                          ev_uint32_t flags);
// 延迟调用一个buffer的回调
int evbuffer_defer_callbacks(struct evbuffer *buffer, struct event_base *base);


/* Here's a callback that remembers how many bytes we have drained in
   total from the buffer, and prints a dot every time we hit a
   megabyte. */
struct total_processed {
    size_t n;
};
void count_megabytes_cb(struct evbuffer *buffer,
    const struct evbuffer_cb_info *info, void *arg)
{
    struct total_processed *tp = arg;
    size_t old_n = tp->n;
    int megabytes, i;
    tp->n += info->n_deleted;
    megabytes = ((tp->n) >> 20) - (old_n >> 20);
    for (i=0; i<megabytes; ++i)
        putc('.', stdout);
}

void operation_with_counted_bytes(void)
{
    struct total_processed *tp = malloc(sizeof(*tp));
    struct evbuffer *buf = evbuffer_new();
    tp->n = 0;
    evbuffer_add_cb(buf, count_megabytes_cb, tp);

    /* Use the evbuffer for a while.  When we're done: */
    evbuffer_free(buf);
    free(tp);
}
```

##### 避免数据拷贝

网络数据传输中希望快速传输数据，因此不想到处拷贝数据

```c
typedef void (*evbuffer_ref_cleanup_cb)(const void *data,
    size_t datalen, void *extra);
// 在buffer的末尾添加数据，但是不会拷贝，buffer里面只是存储了指向外部数据的指针，当buffer用完后，会调用clearup函数清理数据
int evbuffer_add_reference(struct evbuffer *outbuf,
    const void *data, size_t datlen,
    evbuffer_ref_cleanup_cb cleanupfn, void *extra);

/* In this example, we have a bunch of evbuffers that we want to use to
   spool a one-megabyte resource out to the network.  We do this
   without keeping any more copies of the resource in memory than
   necessary. */

#define HUGE_RESOURCE_SIZE (1024*1024)
struct huge_resource {
    /* We keep a count of the references that exist to this structure,
       so that we know when we can free it. */
    int reference_count;
    char data[HUGE_RESOURCE_SIZE];
};

struct huge_resource *new_resource(void) {
    struct huge_resource *hr = malloc(sizeof(struct huge_resource));
    hr->reference_count = 1;
    /* Here we should fill hr->data with something.  In real life,
       we'd probably load something or do a complex calculation.
       Here, we'll just fill it with EEs. */
    memset(hr->data, 0xEE, sizeof(hr->data));
    return hr;
}

void free_resource(struct huge_resource *hr) {
    --hr->reference_count;
    if (hr->reference_count == 0)
        free(hr);
}

static void cleanup(const void *data, size_t len, void *arg) {
    free_resource(arg);
}

/* This is the function that actually adds the resource to the
   buffer. */
void spool_resource_to_evbuffer(struct evbuffer *buf,
    struct huge_resource *hr)
{
    ++hr->reference_count;
    evbuffer_add_reference(buf, hr->data, HUGE_RESOURCE_SIZE,
        cleanup, hr);
}
```

###### 把文件直接添加到buffer

当操作系统支持`splice()` 或`sendfile()`时，Libevent在执行`evbuffer_write()时`会直接使用这两个 接口把数据通过fd发送到网络，而不会先把数据拷贝到内存，如果系统不支持这两个，但是支持`mmap()`，Libevent会mmap文件，而系统内核不会把数据拷贝到用户空间。如果都没有，才会把文件数据先拷贝到内存。当数据被flushed后，文件会被关闭。如果不想关闭文件，可以使用`file_segment`接口

由于`evbuffer_add_file() `有文件的所有权，当希望多次添加同一个文件时效率会很低。`evbuffer_file_segment`内部使用系统支持的`sendfile`,`splice`,`mmap`,`CreateFileMapping`,或者`malloc()` `read()`，默认使用最轻量级的机制对文件进行操作。可以设置标志了控制不使用哪种机制。

```c
int evbuffer_add_file(struct evbuffer *output, int fd, 
                      ev_off_t offset, // 文件起始位置
                      size_t length);   // 读入的数据长度

struct evbuffer_file_segment;
// 创建的结构体表示了一个文件中offset开始length长度的数据
struct evbuffer_file_segment *evbuffer_file_segment_new(
	int fd, ev_off_t offset, ev_off_t length, unsigned flags);
// 实际的空间只会在没有evbuffer再使用这个file segment才会被释放
void evbuffer_file_segment_free(struct evbuffer_file_segment *seg);
// 这里的offset是evbuffer_file_segment的，而不是原来文件的了
int evbuffer_add_file_segment(struct evbuffer *buf,
    struct evbuffer_file_segment *seg, ev_off_t offset, ev_off_t length);
// 可以注册一个callback来监听什么时候一个evbuffer_file_segment没有被引用，并将要被释放，由于这个evbuffer_file_segment即将被释放了，所以不能再回调函数里把它赋给一个evbuffer了
typedef void (*evbuffer_file_segment_cleanup_cb)(
    struct evbuffer_file_segment const *seg, int flags, void *arg);

void evbuffer_file_segment_add_cleanup_cb(struct evbuffer_file_segment *seg,
	evbuffer_file_segment_cleanup_cb cb, void *arg);
```

###### 以引用方式把一个evbuffer添加到另一个evbuffer

这种方式把一个evbuffer的内容的以引用方式添加给了另一个evbuffer，就好像是把outbuf的数据拷贝到了inbuf，但没有实际的拷贝操作。后续对inbuf的操作不会在outbuff上体现。

这种引用不支持嵌套操作，例如一个outbuf不能作为另一个的inbuf。

```c
int evbuffer_add_buffer_reference(struct evbuffer *outbuf,
    struct evbuffer *inbuf);
```



