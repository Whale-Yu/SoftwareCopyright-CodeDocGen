"""测试 Dropdown 的用法"""
import flet as ft
import inspect

print("Dropdown signature:", inspect.signature(ft.Dropdown))
print("\nDropdown attributes:", [attr for attr in dir(ft.Dropdown) if not attr.startswith('_')])

fp = ft.Dropdown(options=[ft.dropdown.Option("test")])
print("\nDropdown instance attributes:", [attr for attr in dir(fp) if not attr.startswith('_') and not callable(getattr(fp, attr))])