// Swift 测试文件
import Foundation

func greet(_ name: String) -> String {
    return "Hello, \(name)!"
}

print(greet("World"))

class Test {
    var name: String
    init(name: String) {
        self.name = name
    }
}