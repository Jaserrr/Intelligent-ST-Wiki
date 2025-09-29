#include "linklist.cpp"  // 从linklist.cpp调用函数

int main(){
	const char *filename = "2.txt";
    struct node *headPtr = ReadList(filename);
    printf("链表各节点数据为:"); 
    printAllNode(headPtr);
    unsigned int i;
    printf("请输入想要定位的节点位置i:"); 
    scanf("%u",&i);
    findNode(headPtr,i);
    
    // 测试样例
    findNode(headPtr,0);
    findNode(headPtr,1);
    findNode(headPtr,10);
    deleteAllNodes(&headPtr);
	return 0;
}
