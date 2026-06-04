"""检查 flet.Colors 中的颜色"""
import flet as ft

# 检查 flet.Colors 中有什么
print("flet.Colors 中的颜色:")
colors = [attr for attr in dir(ft.Colors) if not attr.startswith('_')]
for color in sorted(colors):
    print(f"  - {color}")

# 检查 BLACK87 是否存在
print("\n检查 BLACK87:")
try:
    print(f"  BLACK87: {ft.Colors.BLACK87}")
except AttributeError:
    print("  ft.Colors 中没有 BLACK87")

# 检查常用颜色
print("\n常用颜色:")
common_colors = ['BLACK', 'WHITE', 'GREY', 'GREY_50', 'GREY_100', 'GREY_500', 'GREY_600', 'GREY_700', 'GREY_800']
for c in common_colors:
    try:
        print(f"  {c}: {getattr(ft.Colors, c)}")
    except AttributeError:
        print(f"  {c}: 不存在")