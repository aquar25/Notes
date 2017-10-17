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
