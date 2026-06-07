"""测试 FilePicker 的事件类型"""
import flet as ft

print("=== 查看 flet 模块内容 ===")
# 查看 ft 模块下的内容
for name in dir(ft):
    if "FilePicker" in name or "File" in name and "Event" in name:
        print(f"  {name}")

print("\n=== 查看 FilePicker ===")
if hasattr(ft, "FilePicker"):
    print(f"  FilePicker 存在")
    # 查看 FilePicker 的内容
    fp = ft.FilePicker()
    print(f"  FilePicker 方法: {[m for m in dir(fp) if not m.startswith('_')]}")
