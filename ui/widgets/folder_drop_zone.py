# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:06:29
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 10:02:57
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/widgets/folder_drop_zone.py
Description: 文件夹选择组件：点击选择 + 拖拽

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

import flet as ft
import os
from datetime import datetime


class FolderDropZone(ft.Column):
    """文件夹选择区域"""

    def __init__(self, on_folder_selected=None):
        self.on_folder_selected = on_folder_selected
        self.selected_path = ""
        self.file_count = 0
        self.total_size = 0
        self.last_scan_time = ""
        
        self.container = ft.Container(
            width=None,
            height=120,
            expand=True,
            border=ft.Border(
                left=ft.BorderSide(2, ft.Colors.BLUE_300),
                top=ft.BorderSide(2, ft.Colors.BLUE_300),
                right=ft.BorderSide(2, ft.Colors.BLUE_300),
                bottom=ft.BorderSide(2, ft.Colors.BLUE_300),
            ),
            border_radius=8,
            bgcolor=ft.Colors.BLUE_50,
            content=self._get_unselected_content(),
        )
        
        super().__init__(
            controls=[self.container],
            expand=True,
        )

    def _get_unselected_content(self):
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Icon(ft.Icons.FOLDER_OPEN, size=40, color=ft.Colors.BLUE_400),
                        ft.Container(
                            content=ft.ElevatedButton(
                                "选择源码根目录",
                                icon=ft.Icons.FOLDER_OPEN,
                                on_click=self._on_click,
                            ),
                        ),
                        ft.Text(
                            "或拖拽到此处（该功能待实现）",
                            size=11,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.GREY_500,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                    expand=True,
                ),
            ],
            expand=True,
        )

    def _get_selected_content(self):
        # 顶部区域：图标 + 文件夹信息
        top_row = ft.Row(
            [
                ft.Icon(ft.Icons.FOLDER, size=32, color=ft.Colors.GREEN_400),
                ft.Column(
                    [
                        ft.Text(
                            "✅️ 已选择目录",
                            size=12,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.GREEN_700,
                        ),
                        ft.Text(
                            self.selected_path,
                            size=11,
                            color=ft.Colors.BLACK87,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            tooltip=self.selected_path,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

        # 底部区域：统计信息 + 更换按钮
        bottom_row = ft.Row(
            [
                ft.Icon(ft.Icons.DESCRIPTION, size=14, color=ft.Colors.GREY_500),
                ft.Text(
                    f"共发现 {self.file_count} 个代码文件",
                    size=11,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(width=8),
                ft.Text("|", size=11, color=ft.Colors.GREY_400),
                ft.Container(width=8),
                ft.Icon(ft.Icons.STORAGE, size=14, color=ft.Colors.GREY_500),
                ft.Text(
                    f"总大小 {self._format_size(self.total_size)}",
                    size=11,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(width=8),
                ft.Text("|", size=11, color=ft.Colors.GREY_400),
                ft.Container(width=8),
                ft.Icon(ft.Icons.SCHEDULE, size=14, color=ft.Colors.GREY_500),
                ft.Text(
                    f"最后扫描：{self.last_scan_time}",
                    size=11,
                    color=ft.Colors.GREY_600,
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "更换目录",
                    icon=ft.Icons.REFRESH,
                    on_click=self._on_click,
                    height=30,
                ),
            ],
            spacing=4,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        return ft.Column(
            [
                ft.Container(content=top_row, padding=ft.Padding(12, 10, 12, 6), expand=True),
                ft.Container(content=bottom_row, padding=ft.Padding(12, 0, 12, 10), expand=True),
            ],
            spacing=0,
            expand=True,
        )

    def _format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"

    async def _on_click(self, e):
        path = await ft.FilePicker().get_directory_path()
        if path:
            self.selected_path = path
            self._update_display()
            if self.on_folder_selected:
                self.on_folder_selected(path)

    def _on_drop(self, e):
        """处理拖拽事件（预留接口）"""
        # TODO: 后续实现拖拽选择功能
        pass

    def update_stats(self, file_count, total_size):
        self.file_count = file_count
        self.total_size = total_size
        self.last_scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.selected_path:
            self.container.content = self._get_selected_content()
            self.update()

    def _update_display(self):
        self.container.content = self._get_selected_content()
        self.container.bgcolor = ft.Colors.GREEN_50
        self.container.border = ft.Border(
            left=ft.BorderSide(2, ft.Colors.GREEN_300),
            top=ft.BorderSide(2, ft.Colors.GREEN_300),
            right=ft.BorderSide(2, ft.Colors.GREEN_300),
            bottom=ft.BorderSide(2, ft.Colors.GREEN_300),
        )
        self.update()
