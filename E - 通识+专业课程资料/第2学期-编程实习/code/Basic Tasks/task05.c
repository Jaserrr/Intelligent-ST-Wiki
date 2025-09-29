#include "linklist.cpp"  // 从linklist.cpp调用函数

int main(){
    const char *filename = "5.txt";
    struct node *headPtr = ReadList(filename);
    if (headPtr!=NULL){
        printf("原始链表为：\n");
        printAllNode(headPtr);
        reverseList(&headPtr);
        printf("逆置链表为：\n");
        printAllNode(headPtr);
        WriteFile(headPtr,filename);
    }
    deleteAllNodes(&headPtr);
	return 0;
}
