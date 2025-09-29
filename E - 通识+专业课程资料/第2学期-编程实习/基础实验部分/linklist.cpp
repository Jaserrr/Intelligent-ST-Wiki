#include <stdio.h> 
#include <stdlib.h>

struct node
{
	int data;
	struct node *next;
};
struct node* createNode(int val)
{
	struct node *pnode = (struct node*)malloc(sizeof(struct node));
	if(pnode!=NULL)
	{
		pnode->data=val;
		pnode->next=NULL;
	}
	return pnode;
}

int addNode(struct node **pheadptr,int val)
{
	struct node *p = createNode(val);
	if(p==NULL)
		return 0;
	if(*pheadptr==NULL)
		*pheadptr=p;
	else
	{
		struct node *ptmp=*pheadptr;
		while(ptmp->next)
			ptmp=ptmp->next;
		ptmp->next=p;
	}
	return 1;
}

unsigned countOfNodes(struct node *headptr)
{
	unsigned c=0;
	while(headptr)
	{
		++c;
		headptr=headptr->next;
	}
	return c;
}

void printAllNode(struct node *headptr)
{
	while(headptr)
	{
		printf("%d ",headptr->data);
		headptr=headptr->next;
	}
	printf("\n");
}

int deleteNode(struct node **pheadptr, unsigned loc)
{
	unsigned c = countOfNodes(*pheadptr);
	if(c<loc)
		return 0;
	struct node *p = *pheadptr;
	if(loc==1)
	{
		*pheadptr = (*pheadptr)->next;
		free(p);
	}
	else
	{
		for(int i=2;i<loc;++i)
			p=p->next;
		struct node *pdel = p->next;
		p->next = pdel->next;
		free(pdel);
	}
	return 1;
}

void deleteAllNodes(struct node **pheadptr)
{
	while(countOfNodes(*pheadptr))
		deleteNode(pheadptr,1);
}

int main()
{
	struct node *headPtr=NULL;
	for(int i=1;i<5;++i)
		addNode(&headPtr, i * 10);
	printf("The number of linked list nodes is:%u\n",countOfNodes(headPtr));
	printAllNode(headPtr);
	printf("Delete the node at location 2.\n");
	deleteNode(&headPtr, 2);
	printf("The number of linked list nodes is:%u\n",countOfNodes(headPtr));
	printAllNode(headPtr);
	deleteAllNodes(&headPtr);
	return 0;
}
