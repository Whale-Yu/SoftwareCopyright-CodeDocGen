/**
 * C Header 测试文件
 */
#ifndef TEST_H
#define TEST_H

#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

void greet(const char *name);
int add(int a, int b);

#ifdef __cplusplus
}
#endif

#endif /* TEST_H */