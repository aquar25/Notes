#include "stdafx.h"
#include "MemoryServer.h"


#include <Ws2tcpip.h> // inet_pton()
#pragma comment(lib,"WS2_32")

#define BUFSIZE (4096)

MemoryServer::MemoryServer()
{
}

MemoryServer::~MemoryServer()
{
}

void MemoryServer::Init()
{
	printf("MemoryServer Start....\n");
	// ����Winsock
	WSADATA wsd;
	if (WSAStartup(MAKEWORD(2, 2), &wsd) != 0)
	{
		printf("WSAStartup failed.\n");
		return;
	}
	unsigned short port = 8025;
	// ����˼�����Socket
	SOCKET listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	SOCKADDR_IN serverAddr;
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(port);
	serverAddr.sin_addr.S_un.S_addr = INADDR_ANY;

	// �󶨵�ַ��socket
	bind(listenSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));

	// ��ʼ�����ͻ�������listen
	listen(listenSocket, 5);

	//AcceptOneConnection(listenSocket);
	AcceptOneConnectionWithThread(listenSocket);

	// �ر�����	
	closesocket(listenSocket);

	WSACleanup();

}

char MemoryServer::ROT13(char c)
{
	/* We don't want to use isalpha here; setting the locale would change
	* which characters are considered alphabetical. */
	if ((c >= 'a' && c <= 'm') || (c >= 'A' && c <= 'M'))
		return c + 13;
	else if ((c >= 'n' && c <= 'z') || (c >= 'N' && c <= 'Z'))
		return c - 13;
	else
		return c;
}

void MemoryServer::AcceptOneConnection(SOCKET listenSocket)
{
	// ����һ���ͻ��˵�����
	SOCKADDR_IN clientAddr;
	int clientAddrLen = sizeof(clientAddr);
	SOCKET connectSocket = accept(listenSocket, (struct sockaddr*)&clientAddr, &clientAddrLen);
	if (connectSocket == INVALID_SOCKET)
	{
		printf("Accept error:%d\n", WSAGetLastError());
	}
	else
	{
		printf("one connection come...\n");
		char szBuffer[BUFSIZE] = { 0 };
		while (true)
		{
			// �տͻ�������
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
				// ���ͻ��˷�����
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
	}
	closesocket(connectSocket);
}

void MemoryServer::AcceptOneConnectionWithThread(SOCKET listenSocket)
{
	SOCKET connectSocket;
	while (true)
	{
		// ����һ���ͻ��˵�����
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
			// һ���̴߳���һ������
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
		// �տͻ�������
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
			// ���ͻ��˷�����
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
