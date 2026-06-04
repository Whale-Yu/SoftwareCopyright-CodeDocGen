# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:46:50
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:37:18
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/main_debug.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""带调试的 main"""
import sys
import traceback
import flet as ft
from ui.main_view import MainView


def main(page: ft.Page):
    try:
        page.title = "SC-CodeDocGen - 软著代码文档生成器"
        page.window.width = 1100
        page.window.height = 720
        page.window.min_width = 900
        page.window.min_height = 600
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.spacing = 0
        
        print("创建 MainView...")
        main_view = MainView()
        
        print("添加到 page...")
        page.add(main_view)
        
        print("更新 page...")
        page.update()
        print("启动成功")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        traceback.print_exc()
        
        # 显示错误页面
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("错误发生", size=24, color=ft.Colors.RED),
                    ft.Text(str(e), size=14),
                    ft.Text(traceback.format_exc(), size=10, selectable=True),
                ]),
                padding=20,
            )
        )
        page.update()


if __name__ == "__main__":
    ft.run(main)