/**
 * TypeScript 测试文件
 */
function greet(name: string): string {
    return `Hello, ${name}!`;
}

console.log(greet('World'));

interface Person {
    name: string;
    age: number;
}