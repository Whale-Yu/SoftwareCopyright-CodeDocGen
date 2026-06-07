// Kotlin 测试文件
fun greet(name: String): String {
    return "Hello, $name!"
}

fun main() {
    println(greet("World"))
}

class Test(private val name: String) {
    fun sayHello() = "Hello, $name!"
}