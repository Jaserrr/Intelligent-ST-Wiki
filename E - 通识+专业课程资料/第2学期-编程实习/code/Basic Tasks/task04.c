#include "linklist.cpp"  // 从linklist.cpp调用函数

int main(){
	const char *filename = "4.txt";
    struct node *head = ReadList(filename);
    printAllNode(head);
    if (head!=NULL){
        printf("读取到的链表节点数据：");
        printAllNode(head);
        int max, min; double mean, variance;
        // 调用函数计算最大值、最小值、均值、方差
        Calculate(head, &max, &min, &mean, &variance);
        // 将以上各值输出到文件filename中
        AppendToFile(filename, max, min, mean, variance);
    }
    deleteAllNodes(&head);
	return 0;
}
