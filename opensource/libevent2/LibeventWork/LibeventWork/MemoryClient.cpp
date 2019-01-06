#include "stdafx.h"
#include "MemoryClient.h"

#include <winsock2.h>
#include <Ws2tcpip.h> // inet_pton()
#pragma comment(lib,"WS2_32")

#define BUFSIZE (4096)

MemoryClient::MemoryClient()
{
}


MemoryClient::~MemoryClient()
{
}

void MemoryClient::Init()
{
	printf("MemoryClient Start....\n");

	// 加载Winsock
	WSADATA wsd;
	if (WSAStartup(MAKEWORD(2, 2), &wsd) != 0) 
	{
		printf("WSAStartup failed.\n");
		return;
	}

	unsigned short port = 8025;
	struct sockaddr_in server;
	server.sin_family = AF_INET;
	server.sin_port = htons(port);
	inet_pton(AF_INET, "127.0.0.1", (void*)&server.sin_addr.S_un.S_addr);

	// 创建Socket
	SOCKET fdSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (fdSocket == INVALID_SOCKET)
	{
		printf("socket() failed: %d\n", WSAGetLastError());
		return ;
	}

	// 发起连接
	int ret = connect(fdSocket, (SOCKADDR*)&server, sizeof(server));
	if (ret == SOCKET_ERROR)
	{
		printf("connect error:%d\n", WSAGetLastError());
	}
	else
	{
		char szBuffer[BUFSIZE] = { 0 };
		while (true)
		{
			gets_s(szBuffer);
			// 给服务器发送数据
			int strLen = strlen(szBuffer);
			szBuffer[strlen(szBuffer)] = '\n';
			ret = send(fdSocket, szBuffer, strLen+1, 0);
			if (ret == SOCKET_ERROR) 
			{
				printf("Send error:%d\n", WSAGetLastError());
			}

			// 收服务器发来的数据
			ret = recv(fdSocket, szBuffer, BUFSIZE, 0);
			if (ret == SOCKET_ERROR)
			{
				printf("Recv error:%d\n", WSAGetLastError());
			}
			else
			{
				szBuffer[ret] = '\0';
				printf("Get data: %s\n", szBuffer);
			}
		}
	}	

	//关闭套接字
	closesocket(fdSocket);

	// 释放Winsock
	WSACleanup();
}
