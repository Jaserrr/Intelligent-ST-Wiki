#include "linklist.cpp"  // 从linklist.cpp调用函数

int main(){
	const char *filename = "3.txt";
    struct node *headPtr = ReadList(filename);
    printf("链表各节点数据为:"); 
    printAllNode(headPtr);
    unsigned int t;
    int val;
    printf("请输入想要插入的节点位置t:"); // 样例 0 1 10
    scanf("%u",&t);
    printf("请输入想要添加的节点值val:"); // 样例 100
    scanf("%d",&val);
    InsertBefore(headPtr,t,val,filename);
	return 0;
}
