// Dart 测试文件
void main() {
  print(greet('World'));
}

String greet(String name) {
  return 'Hello, $name!';
}

class Test {
  final String name;
  Test(this.name);
}