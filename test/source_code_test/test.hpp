/**
 * C++ Header 测试文件
 */
#ifndef TEST_HPP
#define TEST_HPP

#include <string>

class Test {
private:
    std::string name;
public:
    Test(const std::string& n);
    std::string greet() const;
};

#endif /* TEST_HPP */