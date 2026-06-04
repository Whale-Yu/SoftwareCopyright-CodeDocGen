// Rust 测试文件
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

fn main() {
    println!("{}", greet("World"));
}

struct Test {
    name: String,
}