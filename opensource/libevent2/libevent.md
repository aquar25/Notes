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

