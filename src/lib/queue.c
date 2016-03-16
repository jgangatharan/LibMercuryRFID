#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include "queue.h"

Queue* createQueue()
{
	Queue *q;
	q = (Queue*)malloc(sizeof(Queue));
	q->firstElement = NULL;
	q->lastElement = NULL;

	if(pthread_mutex_init(&q->EnqueueLock, NULL) != 0)
	{
		return NULL;
	}
	
	if(pthread_mutex_init(&q->DequeueLock, NULL) != 0)
	{
		return NULL;
	}

	return q;
}

void Enqueue(struct QueueStructure *q, int data)
{
	pthread_mutex_lock(&q->EnqueueLock);

	if(q->firstElement == NULL)
	{
		struct QueueElement* newElement = malloc(sizeof(struct QueueElement));

		newElement->nextElement = NULL;
		newElement->data = data;

		q->firstElement = newElement;
		q->lastElement = newElement;
	}
	else
	{
		struct QueueElement* newElement = malloc(sizeof(struct QueueElement));

		newElement->nextElement = NULL;
		newElement->data = data;

		q->lastElement->nextElement = newElement;
		q->lastElement = newElement;
	}

	pthread_mutex_unlock(&q->EnqueueLock);
}

int Dequeue(struct QueueStructure *q)
{
	pthread_mutex_lock(&q->DequeueLock);

	if(q->firstElement == NULL)
	{
		return -1;
	}

	int data = q->firstElement->data;

	struct QueueElement* oldNext = q->firstElement;
	struct QueueElement* newNext = q->firstElement->nextElement;

	free(oldNext);

	q->firstElement = newNext;

	pthread_mutex_unlock(&q->DequeueLock);

	return data;
}

void deleteQueue(struct QueueStructure *q)
{
	pthread_mutex_destroy(&q->EnqueueLock);
	pthread_mutex_destroy(&q->DequeueLock);
}
