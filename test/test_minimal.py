"""最小化测试"""
import flet as ft


def main(page: ft.Page):
    page.title = "测试"
    page.window.width = 400
    page.window.height = 400
    
    # 测试1: 简单的 Container
    page.add(ft.Container(width=100, height=100, bgcolor=ft.Colors.RED))
    page.update()
    
    print("添加 Container 成功")
    
    # 测试2: Text
    try:
        text1 = ft.Text("测试文本")
        page.add(text1)
        page.update()
        print("添加 Text 成功")
    except Exception as e:
        print(f"添加 Text 失败: {e}")
        
    # 测试3: Column
    try:
        col = ft.Column([ft.Text("第一行"), ft.Text("第二行")])
        page.add(col)
        page.update()
        print("添加 Column 成功")
    except Exception as e:
        print(f"添加 Column 失败: {e}")


if __name__ == "__main__":
    ft.run(main)