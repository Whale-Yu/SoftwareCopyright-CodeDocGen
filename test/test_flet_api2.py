
"""深入测试Flet 0.85.2 API"""
import flet as ft

print("=== Icons ===")
print(dir(ft)[:50])

print("\n=== Looking for Icons/Icons ===")
if hasattr(ft, 'Icons'):
    print("Found ft.Icons")
    print(dir(ft.Icons)[:30])
elif hasattr(ft, 'icons'):
    print("Found ft.icons")
    print(dir(ft.icons)[:30])

print("\n=== Looking for Colors ===")
if hasattr(ft, 'Colors'):
    print("Found ft.Colors")
    print(dir(ft.Colors)[:30])
elif hasattr(ft, 'colors'):
    print("Found ft.colors")
    print(dir(ft.colors)[:30])

print("\n=== Looking for Border ===")
print(dir(ft)[:100])
if hasattr(ft, 'border'):
    print("\nft.border has:")
    print(dir(ft.border))

print("\n=== Looking for Padding ===")
if hasattr(ft, 'padding'):
    print("ft.padding has:")
    print(dir(ft.padding))
