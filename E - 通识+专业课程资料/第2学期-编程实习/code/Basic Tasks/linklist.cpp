#include <stdio.h> 
#include <stdlib.h>

struct node{int data; struct node *next;};

struct node* createNode(int val){
	struct node *pnode=(struct node*)malloc(sizeof(struct node));
	if(pnode!=NULL){
		pnode->data=val;
		pnode->next=NULL;
	}
	return pnode;
}

int addNode(struct node **pheadptr,int val){
	struct node *p=createNode(val);
	if(p==NULL)
		return 0;
	if(*pheadptr==NULL)
		*pheadptr=p;
	else{
		struct node *ptmp=*pheadptr;
		while(ptmp->next)
			ptmp=ptmp->next;
		ptmp->next=p;
	}
	return 1;
}

unsigned countOfNodes(struct node *headptr){
	unsigned c=0;
	while(headptr){
		++c; headptr=headptr->next;
	}
	return c;
}

void printAllNode(struct node *headptr){
	while(headptr){
		printf("%d ",headptr->data);
		headptr=headptr->next;
	}
	printf("\n");
}

int deleteNode(struct node **pheadptr, unsigned loc){
	unsigned c=countOfNodes(*pheadptr);
	if(c<loc)
		return 0;
	struct node *p=*pheadptr;
	if(loc==1){
		*pheadptr=(*pheadptr)->next;
		free(p);
	}
	else{
		for(int i=2;i<loc;++i)
			p=p->next;
		struct node *pdel=p->next;
		p->next=pdel->next;
		free(pdel);
	}
	return 1;
}

void deleteAllNodes(struct node **pheadptr){
	while(countOfNodes(*pheadptr))
		deleteNode(pheadptr,1);
}

void findNode(struct node *headptr, unsigned p){
    unsigned c=countOfNodes(headptr);
    if(p>=c||p<0)
        printf("not found\n");
    else{
        if(p>0)
            for(unsigned i=0;i<=p-1;++i)
                headptr=headptr->next;
        printf("%d\n",headptr->data);
    }
}

void WriteFile(struct node *headptr, const char *filename){
    FILE *file=fopen(filename,"a");
    if (file==NULL){
        printf("[提示]无法打开文件%s！\n",filename);
        return;
    }
    fprintf(file,"\n生成的新链表为:\n");
    while(headptr){
        fprintf(file,"%d ",headptr->data);
        headptr=headptr->next;
    }
    fclose(file);
    printf("[提示]链表数据已成功写入%s！\n",filename);
}

int InsertBefore(struct node *headptr,unsigned t,int val,const char *filename){
    unsigned c=countOfNodes(headptr);
    if(t>c||t<0){
        printf("由于指针不在范围内，添加节点失败！\n");
        return 0;
    }
    struct node *newNode=createNode(val);
    if(newNode==NULL){
        printf("由于未输入插入值val，添加节点失败！\n");
        return 0;
    }
    if(t==0){
        newNode->next=headptr;
        headptr=newNode;
    }else{
        struct node *p=headptr;
        for(unsigned i=0;i<t-1;++i)
            p=p->next;
        newNode->next=p->next;
        p->next=newNode;
    }
    printf("插入成功！新的链表数据为：\n");
    printAllNode(headptr);
    WriteFile(headptr,filename);
    return 1;
}

struct node* ReadList(const char *filename){
    FILE *file=fopen(filename, "r");
    if (file==NULL){
        printf("[提示]无法打开文件%s！\n", filename);
        return NULL;
    }
    struct node *headptr=NULL;
    int val; char ch;
    while (fscanf(file,"%d%c",&val,&ch)==2)
        addNode(&headptr,val);
    fclose(file);
    return headptr;
}

void Calculate(struct node *headptr, int *max, int *min, double *mean, double *variance){
    if (headptr==NULL) return;
    int sum=0, sum2=0, count=0;
    *max=headptr->data;
    *min=headptr->data;
    struct node *current=headptr;
    while(current){
        if(current->data>*max) *max=current->data;
        if(current->data<*min) *min=current->data;
        sum+=current->data;
        sum2+=current->data*current->data;
        count++;
        current=current->next;
    }
    *mean=(double)sum / count;
    *variance=((double)sum2/count)-((*mean)*(*mean));
}

void AppendToFile(const char *filename, int max, int min, double mean, double variance){
    FILE *file=fopen(filename, "a");
    if (file==NULL){
        printf("[提示]无法打开文件%s！\n",filename);
        return;
    }
    fprintf(file, "\n数据:\n");
    fprintf(file, "最大值: %d\n最小值: %d\n均值: %.6f\n方差: %.6f\n",max,min,mean,variance);
    fclose(file);
    printf("[提示]各需求数据已成功写入%s！\n", filename);
}

void reverseList(struct node **headptr){
    struct node *prev=NULL;
    struct node *current=*headptr;
    struct node *next=NULL;
    while (current != NULL){
        next=current->next;
        current->next=prev;
        prev=current;
        current=next;
    }
    *headptr=prev;
}
