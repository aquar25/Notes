// LibeventWork.cpp : �������̨Ӧ�ó������ڵ㡣
//

#include "stdafx.h"
#ifdef _SERVER_
#include "MemoryServer.h"
#else
#include "MemoryClient.h"
#endif


int _tmain(int argc, _TCHAR* argv[])
{

#ifdef _SERVER_
	MemoryServer server;
	//server.Init();
	server.InitLibevent();

#else
	MemoryClient client;
	client.Init();
#endif

	getchar();
	return 0;
}

