/**
 * C 测试文件
 */
#include <stdio.h>
#include <string.h>

void greet(const char *name) {
    printf("Hello, %s!\n", name);
}

int main() {
    greet("World");
    return 0;
}