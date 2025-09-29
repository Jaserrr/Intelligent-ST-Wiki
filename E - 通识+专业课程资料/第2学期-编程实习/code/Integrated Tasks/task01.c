#include <stdio.h>
#include <string.h>

// 计算LPS数组（部分匹配表/前缀表）
// 确认前、后缀相同部分的长度，以确定子串指针j在匹配失败时回溯到的位置，降低时间复杂度
void LPSArray(char* pattern, int M, int* lps) {
    int len = 0; // 记录最长相同前后缀的长度
    int i = 1;
    lps[0] = 0; // LPS数组的第一个值总是0
    while (i < M) {
        // 如果当前字符匹配
        if (pattern[i] == pattern[len]) {
            len++; // 增加最长相同前后缀的长度
            lps[i] = len; // 在LPS数组中记录
            i++; // 移动到下一个字符
        } else {
            if (len != 0) {
                len = lps[len - 1]; // 更新len为之前匹配的最长相同前后缀的长度
            } else {
                lps[i] = 0; // 如果没有匹配的前后缀，LPS数组当前位置值为0
                i++; // 移动到下一个字符
            }
        }
    }
}

// 使用KMP算法进行子串匹配
int KMPSearch(char* text, char* pattern) {
    int M = strlen(pattern); // 模式串的长度
    int N = strlen(text); // 主串的长度
    int lps[M]; // 用于存储模式串的LPS数组
    LPSArray(pattern, M, lps); // 构建LPS数组
    int i = 0; // text的索引
    int j = 0; // pattern的索引
    // 循环遍历整个主串
    while (i < N) {
        if (pattern[j] == text[i]) { // 当前字符匹配
            i++; // 主串索引前移
            j++; // 模式串索引前移
        }
        if (j == M) { // 完全匹配
            return i - j; // 匹配成功，返回起始索引
        } else if (i < N && pattern[j] != text[i]) { // 当前字符不匹配
            if (j != 0) {
                j = lps[j - 1]; // 使用LPS数组跳转模式串索引
            } else {
                i++; // 主串索引前移
            }
        }
    }
    return -1; // 匹配失败
}


int main() {
    char a[1000], b[1000];       // 定义字符数组a,b，最多包含1000个字符
    printf("请输入长字符串a: ");
    fgets(a,1000,stdin);         // 从stdin读取最多1000个字符（含终止符'\0'），存储在字符数组a中
                                 // stdin表示标准输入流（standard input stream），通常是键盘输入。
    a[strcspn(a,"\n")]='\0';     // 去除字符串末尾换行符，更改为'\0'终止符
    printf("请输入待匹配子串b: ");
    fgets(b,1000,stdin);
    b[strcspn(b,"\n")]='\0';     // 去除字符串末尾换行符，更改为'\0'终止符
    int result = KMPSearch(a,b); // 调用KMPSearch函数，计算结果
    printf("%d\n", result);
    return 0;
}
