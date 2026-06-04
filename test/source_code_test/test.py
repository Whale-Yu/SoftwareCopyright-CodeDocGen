# -*- coding: utf-8 -*-
"""Python 测试文件"""

def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("World"))