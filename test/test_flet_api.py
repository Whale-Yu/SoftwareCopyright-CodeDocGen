
"""测试Flet API可用性"""
import flet as ft

print("Testing Flet API...")

# 测试Icons
print("\n=== Icons ===")
try:
    print(f"ft.icons.FOLDER_OPEN: {hasattr(ft.icons, 'FOLDER_OPEN')}")
    print(f"ft.icons.FOLDER: {hasattr(ft.icons, 'FOLDER')}")
    print(f"ft.icons.ANALYTICS: {hasattr(ft.icons, 'ANALYTICS')}")
    print(f"ft.icons.CLOSE: {hasattr(ft.icons, 'CLOSE')}")
except Exception as e:
    print(f"Error testing icons: {e}")

# 测试Colors
print("\n=== Colors ===")
try:
    print(f"ft.colors.BLUE_400: {hasattr(ft.colors, 'BLUE_400')}")
    print(f"ft.colors.GREY_600: {hasattr(ft.colors, 'GREY_600')}")
    print(f"ft.colors.GREEN_400: {hasattr(ft.colors, 'GREEN_400')}")
    print(f"ft.colors.BLUE_50: {hasattr(ft.colors, 'BLUE_50')}")
except Exception as e:
    print(f"Error testing colors: {e}")

# 测试控件和属性
print("\n=== Controls ===")
try:
    print(f"ft.Container: {hasattr(ft, 'Container')}")
    print(f"ft.Column: {hasattr(ft, 'Column')}")
    print(f"ft.Row: {hasattr(ft, 'Row')}")
    print(f"ft.ElevatedButton: {hasattr(ft, 'ElevatedButton')}")
    print(f"ft.Dropdown: {hasattr(ft, 'Dropdown')}")
    print(f"ft.dropdown.Option: {hasattr(ft.dropdown, 'Option')}")
    print(f"ft.Chip: {hasattr(ft, 'Chip')}")
    print(f"ft.Radio: {hasattr(ft, 'Radio')}")
    print(f"ft.RadioGroup: {hasattr(ft, 'RadioGroup')}")
    print(f"ft.FilePicker: {hasattr(ft, 'FilePicker')}")
    print(f"ft.SnackBar: {hasattr(ft, 'SnackBar')}")
    print(f"ft.SnackBarAction: {hasattr(ft, 'SnackBarAction')}")
    print(f"ft.ProgressBar: {hasattr(ft, 'ProgressBar')}")
    print(f"ft.Divider: {hasattr(ft, 'Divider')}")
    print(f"ft.VerticalDivider: {hasattr(ft, 'VerticalDivider')}")
except Exception as e:
    print(f"Error testing controls: {e}")

# 测试样式
print("\n=== Styles ===")
try:
    print(f"ft.ButtonStyle: {hasattr(ft, 'ButtonStyle')}")
    print(f"ft.RoundedRectangleBorder: {hasattr(ft, 'RoundedRectangleBorder')}")
except Exception as e:
    print(f"Error testing styles: {e}")

# 测试枚举
print("\n=== Enums ===")
try:
    print(f"ft.TextAlign: {hasattr(ft, 'TextAlign')}")
    print(f"ft.MainAxisAlignment: {hasattr(ft, 'MainAxisAlignment')}")
    print(f"ft.CrossAxisAlignment: {hasattr(ft, 'CrossAxisAlignment')}")
    print(f"ft.ScrollMode: {hasattr(ft, 'ScrollMode')}")
    print(f"ft.ThemeMode: {hasattr(ft, 'ThemeMode')}")
    print(f"ft.FontWeight: {hasattr(ft, 'FontWeight')}")
    print(f"ft.KeyboardType: {hasattr(ft, 'KeyboardType')}")
    print(f"ft.TextOverflow: {hasattr(ft, 'TextOverflow')}")
except Exception as e:
    print(f"Error testing enums: {e}")

# 测试padding
print("\n=== Padding ===")
try:
    print(f"ft.padding: {hasattr(ft, 'padding')}")
    print(f"ft.padding.all: {hasattr(ft.padding, 'all') if hasattr(ft, 'padding') else False}")
except Exception as e:
    print(f"Error testing padding: {e}")

# 测试border
print("\n=== Border ===")
try:
    print(f"ft.border: {hasattr(ft, 'border')}")
    print(f"ft.border.all: {hasattr(ft.border, 'all') if hasattr(ft, 'border') else False}")
except Exception as e:
    print(f"Error testing border: {e}")
