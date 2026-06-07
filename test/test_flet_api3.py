
"""测试具体的API用法"""
import flet as ft

print("=== Checking Icons ===")
icon_names = ['FOLDER', 'FOLDER_OPEN', 'FOLDER_OUTLINED', 'FOLDER_ROUNDED', 
              'ANALYTICS', 'ANALYTICS_OUTLINED', 'ANALYTICS_ROUNDED',
              'CLOSE', 'CLOSE_OUTLINED', 'CLOSE_ROUNDED']

for name in icon_names:
    if hasattr(ft.Icons, name):
        print(f"✓ ft.Icons.{name} exists")
    else:
        print(f"✗ ft.Icons.{name} NOT found")

print("\n=== Testing Border ===")
try:
    b = ft.BorderSide(2, ft.Colors.BLUE_300)
    print("✓ ft.BorderSide works")
    border = ft.Border(left=b, top=b, right=b, bottom=b)
    print("✓ ft.Border works")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing Padding ===")
try:
    p = ft.Padding(16, 16, 16, 16)
    print("✓ ft.Padding works")
    p2 = ft.Padding(0, 0, 0, 8)
    print("✓ ft.Padding works with all args")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing ButtonStyle ===")
try:
    bs = ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=8),
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
    )
    print("✓ ft.ButtonStyle works")
except Exception as e:
    print(f"Error: {e}")
