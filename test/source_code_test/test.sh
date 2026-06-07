#!/bin/bash
# Shell 测试文件

greet() {
    echo "Hello, $1!"
}

greet "World"

echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"