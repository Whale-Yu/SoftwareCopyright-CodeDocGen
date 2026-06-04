
"""测试具体的API用法 - 无Unicode"""
import flet as ft

print("=== Checking Icons ===")
icon_names = ['FOLDER', 'FOLDER_OPEN', 'FOLDER_OUTLINED', 'FOLDER_ROUNDED', 
              'ANALYTICS', 'ANALYTICS_OUTLINED', 'ANALYTICS_ROUNDED',
              'CLOSE', 'CLOSE_OUTLINED', 'CLOSE_ROUNDED']

for name in icon_names:
    if hasattr(ft.Icons, name):
        print(f"OK ft.Icons.{name} exists")
    else:
        print(f"NO ft.Icons.{name} NOT found")

print("\n=== Looking for some folder icons ===")
for name in dir(ft.Icons):
    if 'FOLDER' in name:
        print(f"  {name}")

print("\n=== Looking for some close icons ===")
for name in dir(ft.Icons):
    if 'CLOSE' in name and len(name) < 20:
        print(f"  {name}")

print("\n=== Looking for analytics/statistics icons ===")
for name in dir(ft.Icons):
    if any(keyword in name for keyword in ['ANALYTICS', 'STATS', 'DATA', 'BAR_CHART']):
        print(f"  {name}")
