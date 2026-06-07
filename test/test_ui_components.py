"""测试 UI 组件"""
import flet as ft


def test1(page):
    """测试 Container、Column、Row"""
    page.add(ft.Text("测试1: Container、Column、Row"))
    c1 = ft.Container(
        width=200,
        height=50,
        bgcolor=ft.Colors.BLUE_200,
        border=ft.Border(
            left=ft.BorderSide(2, ft.Colors.BLUE),
            top=ft.BorderSide(2, ft.Colors.BLUE),
            right=ft.BorderSide(2, ft.Colors.BLUE),
            bottom=ft.BorderSide(2, ft.Colors.BLUE),
        ),
        border_radius=8,
        content=ft.Column([
            ft.Text("测试文本 1"),
            ft.Text("测试文本 2"),
        ]),
    )
    page.add(c1)
    page.add(ft.Divider(height=1))
    page.update()


def test2(page):
    """测试 TextField"""
    page.add(ft.Text("测试2: TextField"))
    tf1 = ft.TextField(label="测试标签", hint_text="测试提示")
    page.add(tf1)
    page.add(ft.Divider(height=1))
    page.update()


def test3(page):
    """测试 Dropdown"""
    page.add(ft.Text("测试3: Dropdown"))
    dd1 = ft.Dropdown(
        label="测试下拉框",
        options=[
            ft.dropdown.Option(key="a", text="选项 A"),
            ft.dropdown.Option(key="b", text="选项 B"),
        ],
        value="a",
    )
    page.add(dd1)
    page.add(ft.Divider(height=1))
    page.update()


def test4(page):
    """测试 Button"""
    page.add(ft.Text("测试4: Button"))
    btn1 = ft.ElevatedButton("测试按钮")
    page.add(btn1)
    page.add(ft.Divider(height=1))
    page.update()


def test5(page):
    """测试 Checkbox"""
    page.add(ft.Text("测试5: Checkbox"))
    cb1 = ft.Checkbox(label="测试复选框", value=True)
    page.add(cb1)
    page.add(ft.Divider(height=1))
    page.update()


def test6(page):
    """测试 Icons"""
    page.add(ft.Text("测试6: Icons"))
    ic1 = ft.Icon(ft.Icons.FOLDER, size=48, color=ft.Colors.RED)
    page.add(ic1)
    page.add(ft.Divider(height=1))
    page.update()


def main(page: ft.Page):
    page.title = "UI 组件测试"
    page.window.width = 600
    page.window.height = 800
    page.scroll = ft.ScrollMode.AUTO
    
    try:
        test1(page)
    except Exception as e:
        page.add(ft.Text(f"测试1 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        test2(page)
    except Exception as e:
        page.add(ft.Text(f"测试2 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        test3(page)
    except Exception as e:
        page.add(ft.Text(f"测试3 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        test4(page)
    except Exception as e:
        page.add(ft.Text(f"测试4 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        test5(page)
    except Exception as e:
        page.add(ft.Text(f"测试5 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        test6(page)
    except Exception as e:
        page.add(ft.Text(f"测试6 失败: {e}", color=ft.Colors.RED))
        page.update()


if __name__ == "__main__":
    ft.run(main)