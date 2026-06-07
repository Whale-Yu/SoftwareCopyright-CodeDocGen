"""测试 FilePicker 的用法"""
import flet as ft
import inspect

print("=== FilePicker 签名 ===")
print(inspect.signature(ft.FilePicker))

print("\n=== FilePicker 文档 ===")
print(ft.FilePicker.__doc__)
