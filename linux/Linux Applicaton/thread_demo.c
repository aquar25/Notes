#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <assert.h>
#include <math.h>
#include <unistd.h>

// init a mutex for pthread_once function
pthread_once_t my_init_mutex = PTHREAD_ONCE_INIT;

void initialize_once_app(void)
{
	printf("work only once\n");
}

void* EntryFunction(void* arg)
{
    printf("Thread %d ran~\n", (int)arg);

    pthread_t id = pthread_self();
    printf("my id is %x\n", (int)id);
    int detachid = 2;
    if (detachid == (int)arg)
    {
    	printf("I am thread %d and I must detached bye...", detachid);
    	pthread_detach(id);
    }

    pthread_once(&my_init_mutex, initialize_once_app);

    /* Terminate the thread */
    pthread_exit(arg);
}

int thread_create_demo()
{
	printf("start up...\n");

    int ret;
    pthread_t mythread1;
    pthread_t mythread2;
    int arg1 = 1;
    int arg2 = 2;
    
    ret = pthread_create(&mythread1, NULL, EntryFunction, (void*)arg1);
    printf("pthread_t is %x\n", (int)mythread1);

    ret = pthread_create(&mythread2, NULL, EntryFunction, (void*)arg2);    

    if (ret!=0)
    {
		printf("Can't create pthread (%s)\n", strerror(errno));
		exit(-1);
    }
    int status = 0;
    // wait for mythread run finished
    printf("wait for mythread 1 working \n");
    ret = pthread_join(mythread1, (void**)&status);
    if (ret!=0)
    {
    	printf("Error joining thread (%s)\n", strerror(errno));
    }
    else
    {
    	printf("Thread status = %d \n", status);
    }
    printf("mythread1 finished\n");
    
    return 0;
}

pthread_mutex_t cntr_mutex = PTHREAD_MUTEX_INITIALIZER;
long countVariable = 0;

void *product(void* arg)
{
	int i, ret=0;
	for (int i = 0; i < 100; ++i)
	{
		ret = pthread_mutex_lock(&cntr_mutex);
		assert(ret == 0);
		countVariable++;
		printf("value is %ld\n", countVariable);
		ret = pthread_mutex_unlock(&cntr_mutex);
		assert(ret == 0);
	}
	pthread_exit(NULL);
}

#define MAX_THREADS (10)

int thread_mutex_demo()
{
	int i, ret;
	pthread_t threadIds[MAX_THREADS];
	for (int i = 0; i < MAX_THREADS; ++i)
	{
		ret = pthread_create(&threadIds[i], NULL, product, NULL);
	}
	for (int i = 0; i < MAX_THREADS; ++i)
	{
		ret = pthread_join(threadIds[i], NULL);
	}
	printf("The protected value is %ld\n", countVariable);

	ret = pthread_mutex_destroy(&cntr_mutex);

	return 0;
}

#define MAX_CONSUMERS (10)

pthread_mutex_t cond_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t condition = PTHREAD_COND_INITIALIZER;

void *producerFunc(void* arg)
{
	int ret = 0;
	double result = 0.0;
	printf("producer started\n");
	for (int i = 0; i < 30; ++i)
	{
		ret = pthread_mutex_lock(&cond_mutex);
		if (ret == 0)
		{
			printf("producer create work (%d)\n", countVariable);
			countVariable++;
			pthread_cond_broadcast(&condition);
			pthread_mutex_unlock(&cond_mutex);
		}

		for (int i = 0; i < 600000; ++i)
		{
			result = result + (double)random();			
		}
		sleep(2);
	}

	printf("producer finished\n");
	pthread_exit(NULL);
}

void *consumerFunc(void* arg)
{
	int ret;
	//you won’t ever join with the creating thread
	pthread_detach(pthread_self());

	printf("Consumer %x: Started\n", pthread_self() );

	while(1) {
		assert(pthread_mutex_lock( &cond_mutex ) == 0);
		assert( pthread_cond_wait( &condition, &cond_mutex ) == 0);
		printf("Consumer %x: recv condition\n", pthread_self());
		if (countVariable)
		{
			countVariable--;
			printf("Consumer %x: Performed work (%d)\n", pthread_self(), countVariable);
			sleep(4);
		}
		assert(pthread_mutex_unlock(&cond_mutex)==0);

	}

	// never executed, because the thread is cancel by the creator
	printf("Consumer %x: Finished\n", pthread_self() );

	pthread_exit( NULL );
}

int thread_conditon_demo()
{
	pthread_t consumers[MAX_CONSUMERS];
	pthread_t producer;

	// spawn the consumer thread
	for (int i = 0; i < MAX_CONSUMERS; ++i)
	{
		pthread_create(&consumers[i], NULL, consumerFunc, NULL);
	}

	// spawn the producer thread
	pthread_create(&producer, NULL, producerFunc, NULL);

	// wait for the producer thread
	pthread_join(producer, NULL);

	while((countVariable>0));

	// cancel and join the consumer threads
	for (int i = 0; i < MAX_CONSUMERS; ++i)
	{
		pthread_cancel(consumers[i]);
	}

	pthread_mutex_destroy(&cond_mutex);
	pthread_cond_destroy(&condition);

	return 0;
}

int main()
{
	//thread_create_demo();

	//thread_mutex_demo();

	thread_conditon_demo();

	getchar();

    return 0;
}
