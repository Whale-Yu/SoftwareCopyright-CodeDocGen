// Objective-C 测试文件
#import <Foundation/Foundation.h>

NSString* greet(NSString *name) {
    return [NSString stringWithFormat:@"Hello, %@!", name];
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"%@", greet(@"World"));
    }
    return 0;
}