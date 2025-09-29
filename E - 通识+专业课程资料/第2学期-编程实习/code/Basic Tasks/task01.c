#include "linklist.cpp"  // 从linklist.cpp调用函数

int main(){
    const char *filename = "1.txt";
    struct node *headPtr = ReadList(filename);
    printf("链表各节点数据为:"); 
    printAllNode(headPtr);
    
    // 删除所有节点，释放内存
    deleteAllNodes(&headPtr);
	return 0;
}
