/**
 * C++ 测试文件
 */
#include <iostream>
#include <string>

using namespace std;

string greet(const string& name) {
    return "Hello, " + name + "!";
}

int main() {
    cout << greet("World") << endl;
    return 0;
}