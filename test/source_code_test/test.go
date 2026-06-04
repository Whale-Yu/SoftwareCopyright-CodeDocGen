package main

import "fmt"

// Go 测试文件
func main() {
    fmt.Println("Hello, World!")
}

func greet(name string) string {
    return "Hello, " + name + "!"
}