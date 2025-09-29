#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 定义常量
#define MAX_NAME 50       // 学生姓名的最大长度
#define FILENAME "students.txt"  // 存储学生信息的文件名
#define NUM_MARKS 5       // 学生成绩数量
#define MAX_MARK_LEN 5    // 每个成绩的最大长度

// 定义学生结构体
typedef struct {
    char name[MAX_NAME];                // 学生姓名
    char marks[NUM_MARKS][MAX_MARK_LEN]; // 学生成绩
} Student;

Student *List = NULL;  // 动态分配的学生列表数组
int count = 0;         // 当前学生数量
int capacity = 0;      // 当前分配的数组容量

// 从文件加载学生信息
void loadFromFile() {
    FILE *file = fopen(FILENAME, "r");
    if (file != NULL) {
        while (1) {
            Student temp;
            char line[256];
            if (fgets(line, sizeof(line), file) == NULL) {
                break;
            }
            // 解析读取的行
            char *token = strtok(line, ",");
            strcpy(temp.name, token);
            for (int i = 0; i < NUM_MARKS; i++) {
                token = strtok(NULL, ",");
                if (token != NULL) {
                    strncpy(temp.marks[i], token, MAX_MARK_LEN);
                } else {
                    strcpy(temp.marks[i], " ");
                }
            }
            // 动态扩展数组
            if (count >= capacity) {
                capacity += 10;
                List = realloc(List, capacity * sizeof(Student));
            }
            List[count++] = temp;
        }
        fclose(file);
    }
}

// 保存学生信息到文件
void saveToFile() {
    FILE *file = fopen(FILENAME, "w");
    // 将学生信息保存到文件中
    for (int i = 0; i < count; i++) {
        fprintf(file, "%s", List[i].name);
        for (int j = 0; j < NUM_MARKS; j++) {
            fprintf(file, ",%s", List[i].marks[j]);
        }
        fprintf(file, "\n");
    }
    fclose(file);
}

// 添加学生
void addStudent() {
    // 动态扩展数组
    if (count >= capacity) {
        capacity += 10;
        List = realloc(List, capacity * sizeof(Student));
    }
    printf("输入学生姓名：");
    scanf("%s", List[count].name);
    getchar();  // 清除缓冲区的换行符
    
    // 初始化五个成绩为空格
    for (int i = 0; i < NUM_MARKS; i++) {
        strcpy(List[count].marks[i], " ");
    }
    count++;
    saveToFile();
}


// 删除学生
void deleteStudent() {
    char name[MAX_NAME];
    printf("输入要删除的学生姓名：");
    scanf("%s", name);
    for (int i = 0; i < count; i++) {
        if (strcmp(List[i].name, name) == 0) {
            // 删除学生并调整数组
            for (int j = i; j < count - 1; j++) {
                List[j] = List[j + 1];
            }
            count--;
            saveToFile();
            printf("学生 %s 已被删除。\n", name);
            return;
        }
    }
    printf("学生 %s 未找到。\n", name);
}

// 查找学生信息
void findStu() {
    char name[MAX_NAME];
    printf("输入要查找的学生姓名：");
    scanf("%s", name);
    for (int i = 0; i < count; i++) {
        if (strcmp(List[i].name, name) == 0) {
            printf("学生：%s\n成绩：", List[i].name);
            for (int j = 0; j < NUM_MARKS - 1; j++)
                printf("%s,", List[i].marks[j]);
            printf("%s\n", List[i].marks[NUM_MARKS - 1]);
            return;
        }
    }
    printf("学生 %s 未找到。\n", name);
}

// 显示所有学生信息
void showList() {
    printf("班级全体信息如下：\n");
    for (int i = 0; i < count; i++) {
        printf("姓名：%s, 成绩：", List[i].name);
        for (int j = 0; j < NUM_MARKS - 1; j++)
            printf("%s,", List[i].marks[j]);
        printf("%s\n", List[i].marks[NUM_MARKS - 1]);
    }
    printf("\n");
}

// 编辑学生成绩
void editStudent() {
    char name[MAX_NAME];
    printf("输入要录入成绩的学生姓名：");
    scanf("%s", name);
    // 清除缓冲区，准备读取成绩
    while (getchar() != '\n');
    for (int i = 0; i < count; i++) {
        if (strcmp(List[i].name, name) == 0) {
            char buffer[10];
            // 修改学生的成绩
            for (int j = 0; j < NUM_MARKS; j++) {
                while (1) {
                    printf("输入 %s 的第 %d 个更新成绩（输入回车以保留当前成绩 %s）：", name, j + 1, List[i].marks[j]);
                    fgets(buffer, sizeof(buffer), stdin);
                    // 如果只打了回车，跳过修改
                    if (buffer[0] == '\n')
                        break;
                    // 去除换行符
                    buffer[strcspn(buffer, "\n")] = '\0';
                    int mark;
                    // 验证输入是否为0~100的有效数字
                    if (sscanf(buffer, "%d", &mark) == 1 && mark >= 0 && mark <= 100) {
                        strncpy(List[i].marks[j], buffer, MAX_MARK_LEN);
                        break;
                    } else {
                        printf("成绩无效，请输入0~100之间的数字。\n");
                    }
                }
            }
            saveToFile();
            printf("学生 %s 的成绩已更新！\n", name);
            return;
        }
    }
    printf("学生 %s 未找到。\n", name);
}

int main() {
    int num;
    loadFromFile(); // 从文件加载学生信息
    while (1) {
        printf("输入 (1) 将学生信息加入班级列表\n");
        printf("     (2) 从班级列表删除学生信息\n");
        printf("     (3) 查找学生信息\n");
        printf("     (4) 编辑学生成绩\n");
        printf("     (5) 展示班级列表\n");
        printf("     (6) 退出此系统\n");
        scanf("%d", &num);
        while (getchar() != '\n'); // 清除缓冲区
        switch(num){
            case 1:
                addStudent();
                showList();
                break;
            case 2:
                deleteStudent();
                showList();
                break;
            case 3:
                findStu();
                break;
            case 4:
                editStudent();
                break;
            case 5:
                showList();
                break;
            case 6:
                printf("等待程序关闭……\n");
                free(List); // 释放动态分配的内存
                return 0;
            default:
                printf("输入不正确，请重新输入：\n");
        }
    }
    return 0;
}
