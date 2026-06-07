"""测试 FilePicker 的详细用法"""
import flet as ft

print("=== FilePicker 类内容 ===")
for name in dir(ft.FilePicker):
    if not name.startswith('_'):
        print(f"  {name}")

print("\n=== 创建 FilePicker 实例 ===")
fp = ft.FilePicker()
print("  FilePicker 实例属性:")
for name in dir(fp):
    if not name.startswith('_'):
        value = getattr(fp, name)
        if not callable(value):
            print(f"    {name}: {value}")
