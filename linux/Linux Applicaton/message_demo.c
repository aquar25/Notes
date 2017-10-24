#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <assert.h>
#include <math.h>
#include <unistd.h>
#include <sys/msg.h>
#include <time.h>
#include <sys/types.h>

#define MAX_LINE	(80)
#define MY_MQ_ID    (111)

typedef struct 
{
	long type;               // msg type
	float fval;		         // user message
	unsigned int uival;      //user message
	char strval[MAX_LINE+1]; // user message
} MY_TYPE_T;

#define MSG_KEY "/home/edison/msgqueue" 

// create a message queue
void create_msg_queue()
{
	key_t msgKey;
	int msgid = 0;
	msgKey = ftok(MSG_KEY, 0);
	msgid = msgget(msgKey, 0666|IPC_CREAT);

	if (msgid>=0)
	{
		printf("create a message queue %d\n", msgid);
	}
}

void config_msg_queue()
{
	key_t msgKey;
	int msgid = 0;
	int ret = 0;
	struct msqid_ds buf;
	msgKey = ftok(MSG_KEY, 0);
	// get the message id
	msgid = msgget(msgKey, 0);
	if (msgid>=0)
	{		
		ret = msgctl(msgid, IPC_STAT, &buf);
		buf.msg_perm.uid = geteuid();
		buf.msg_perm.gid = getegid();
		buf.msg_perm.mode = 0644;
		buf.msg_qbytes = 4096;

		printf( "Number of messages queued: %ld\n", buf.msg_qnum);
		printf( "Number of bytes on queue : %ld\n", buf.msg_cbytes);
		printf("Last change time : %s", ctime(&buf.msg_ctime) );
		if (buf.msg_stime) {
			printf("Last msgsnd time : %s",ctime(&buf.msg_stime) );
		}
		if (buf.msg_rtime) {
			printf("Last msgrcv time : %s",ctime(&buf.msg_rtime) );
		}

		ret = msgctl(msgid, IPC_SET, &buf);
		if (ret == 0)
		{
			printf("config_msg_queue successfully\n");
		}
		else
		{
			printf("Error %d\n", errno);
		}
	}
}

void remove_msg_queue()
{
	key_t msgKey;
	int msgid = 0;
	int ret = 0;
	struct msqid_ds buf;
	msgKey = ftok(MSG_KEY, 0);
	// get the message id
	msgid = msgget(msgKey, 0);
	if (msgid>=0)
	{
		ret = msgctl(msgid, IPC_RMID, NULL);
		if (ret == 0)
		{
			printf("Remove msg queue successfully\n");
		}
		else
		{
			printf("Remove msg queue failed... %d\n", errno);
		}
	}
}

int main()
{
	create_msg_queue();

	config_msg_queue();

	remove_msg_queue();

	getchar();

    return 0;
}
