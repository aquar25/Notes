#pragma once

#define FD_SETSIZE      4096
#include <winsock2.h>

struct ThreadParam
{
	DWORD dwHandle;
	void* param;
};

class MemoryServer
{
public:
	MemoryServer();
	~MemoryServer();

	void Init();
	void InitLibevent();

	void AcceptOneConnection(SOCKET listenSocket);

	void AcceptOneConnectionWithThread(SOCKET listenSocket);

private:
	char ROT13(char in);

	static LPTHREAD_START_ROUTINE ThreadProc(LPVOID lpParam);
	void ProcessConnection(void* param);
	
};

