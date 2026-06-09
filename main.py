# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:09:31
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 09:49:44
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/main.py
Description: SC-CodeDocGen - 软著代码文档生成器
Turn your source code into standard copyright code documents in 1 second.

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

from pathlib import Path

import flet as ft
from ui.main_view import MainView


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
APP_ICON = str(Path(__file__).parent / "assets" / "icons" / "icon-1.ico")
"""
默认尺寸
width = 1600
height = 1000

适配：

1920×1080
2560×1440
最小尺寸
min_width = 1280
min_height = 800
"""


def main(page: ft.Page):
    page.title = "SC-CodeDocGen - \u8f6f\u8457\u4ee3\u7801\u6587\u6863\u751f\u6210\u5668"
    page.window.icon = APP_ICON
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.min_width = WINDOW_MIN_WIDTH
    page.window.min_height = WINDOW_MIN_HEIGHT
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0

    main_view = MainView()
    page.add(main_view)


if __name__ == "__main__":
    ft.run(main)