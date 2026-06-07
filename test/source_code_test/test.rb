# Ruby 测试文件
def greet(name)
  "Hello, #{name}!"
end

puts greet("World")

class Test
  def initialize(name)
    @name = name
  end
end