# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 08:10:54
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:32:30
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/widgets/code_file_list_panel.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""代码文件列表组件"""
import flet as ft
import os
from pathlib import Path
from datetime import datetime
from typing import List
from core.language_config import (
    get_language_name,
    get_language_icon,
    ICON_WIDTH,
    ICON_HEIGHT
)
from core.counter import count_single_file_lines


class CodeFileInfo:
    """代码文件信息"""
    def __init__(self, file_path: str, root_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        
        # 计算相对于根目录的相对路径
        try:
            self.relative_path = os.path.relpath(file_path, root_path)
        except ValueError:
            self.relative_path = file_path
        
        # 检测语言
        self.language = self._detect_language()
        
        # 获取文件大小
        self.size = os.path.getsize(file_path)
        
        # 获取修改时间
        self.modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # 统计代码行数
        self.code_lines = count_single_file_lines(Path(file_path))

    def _detect_language(self) -> str:
        """根据文件扩展名检测语言"""
        ext = os.path.splitext(self.file_name)[1].lower()
        return get_language_name(ext)

    def get_formatted_size(self) -> str:
        """获取格式化的文件大小"""
        if self.size < 1024:
            return f"{self.size} B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.2f} KB"
        else:
            return f"{self.size / (1024 * 1024):.2f} MB"

    def get_formatted_date(self) -> str:
        """获取格式化的日期"""
        return self.modified_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_file_icon(self) -> str:
        """根据文件扩展名获取图标"""
        ext = os.path.splitext(self.file_name)[1].lower()
        return get_language_icon(ext)


class CodeFileListPanel(ft.Container):
    """代码文件列表组件（带分页）"""

    ITEMS_PER_PAGE = 10

    def __init__(self):
        self._all_files: List[CodeFileInfo] = []
        self._current_page = 1
        self._total_pages = 0
        self._root_path = ""

        self._file_list = ft.Column(
            spacing=4,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        self._total_count = ft.Text(
            "共 0 个文件",
            size=12,
            color=ft.Colors.GREY_600,
        )

        # 分页控件
        self._page_info = ft.Text("第 1 页", size=11, color=ft.Colors.GREY_600)
        self._prev_btn = ft.IconButton(
            ft.Icons.ARROW_BACK,
            icon_size=20,
            on_click=self._on_prev_page,
            disabled=True,
        )
        self._next_btn = ft.IconButton(
            ft.Icons.ARROW_FORWARD,
            icon_size=20,
            on_click=self._on_next_page,
            disabled=True,
        )

        pagination = ft.Row(
            [
                self._prev_btn,
                self._page_info,
                self._next_btn,
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.FILE_COPY_OUTLINED, color=ft.Colors.GREY_600),
                            ft.Text("代码文件列表", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_700),
                            ft.Container(expand=True),
                            self._total_count,
                        ],
                        spacing=8,
                    ),
                    ft.Row(
                        [
                            ft.Text("文件名", weight=ft.FontWeight.W_500, size=12, expand=1),
                            ft.Text("文件路径", weight=ft.FontWeight.W_500, size=12, expand=3),
                            ft.Text("语言", weight=ft.FontWeight.W_500, size=12, expand=1),
                            ft.Text("大小", weight=ft.FontWeight.W_500, size=12, expand=1),
                            ft.Text("行数", weight=ft.FontWeight.W_500, size=12, expand=1),
                            ft.Text("修改时间", weight=ft.FontWeight.W_500, size=12, expand=2),
                        ],
                        spacing=4,
                    ),
                    self._file_list,
                    pagination,
                ],
                spacing=8,
                expand=True,
            ),
            padding=ft.Padding(16, 16, 16, 16),
            border=ft.Border(
                left=ft.BorderSide(1, ft.Colors.GREY_300),
                top=ft.BorderSide(1, ft.Colors.GREY_300),
                right=ft.BorderSide(1, ft.Colors.GREY_300),
                bottom=ft.BorderSide(1, ft.Colors.GREY_300),
            ),
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
            expand=True,
        )

    def update_files(self, files: List[str], root_path: str = ""):
        """更新文件列表"""
        self._root_path = root_path
        self._all_files = [CodeFileInfo(file_path, root_path) for file_path in files]
        self._total_pages = (len(self._all_files) + self.ITEMS_PER_PAGE - 1) // self.ITEMS_PER_PAGE
        if self._total_pages == 0:
            self._total_pages = 1
        
        self._current_page = 1
        self._refresh_page()

    def _refresh_page(self):
        """刷新当前页的数据"""
        self._file_list.controls.clear()

        # 计算当前页的起始和结束索引
        start_idx = (self._current_page - 1) * self.ITEMS_PER_PAGE
        end_idx = min(start_idx + self.ITEMS_PER_PAGE, len(self._all_files))

        # 显示当前页的文件
        for file_info in self._all_files[start_idx:end_idx]:
            # 获取图标（预设图标、自定义默认图标）
            icon_path = file_info.get_file_icon()
            if icon_path:
                file_icon = ft.Image(
                    src=icon_path,
                    width=ICON_WIDTH,
                    height=ICON_HEIGHT,
                )
            else: # 如果没有图标，使用默认图标
                file_icon = ft.Icon(
                    ft.Icons.CODE,
                    size=16,
                    color=ft.Colors.BLUE_600,
                )
            
            file_row = ft.Row(
                [
                    ft.Row(
                        [
                            ft.Text(
                                file_info.file_name,
                                size=12,
                                tooltip=file_info.file_path,
                                no_wrap=True,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                expand=2,
                            ),
                        ],
                        spacing=4,
                        expand=1,
                    ),
                    ft.Text(
                        file_info.relative_path,
                        size=12,
                        expand=3,
                        tooltip=file_info.file_path,
                        color=ft.Colors.GREY_600,
                        no_wrap=True,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Row(
                        [
                            file_icon,
                            ft.Text(file_info.language, size=12, color=ft.Colors.BLUE_700),
                        ],
                        spacing=4,
                        expand=1,
                    ),
                    ft.Text(file_info.get_formatted_size(), size=12, expand=1),
                    ft.Text(str(file_info.code_lines), size=12, expand=1),
                    ft.Text(file_info.get_formatted_date(), size=12, expand=2),
                ],
                spacing=4,
            )
            self._file_list.controls.append(file_row)

        # 更新计数和分页信息
        self._total_count.value = f"已筛选出共 {len(self._all_files)} 个文件"
        self._page_info.value = f"第 {self._current_page} / {self._total_pages} 页"

        # 更新按钮状态
        self._prev_btn.disabled = self._current_page <= 1
        self._next_btn.disabled = self._current_page >= self._total_pages

        try:
            if self.page:
                self._file_list.update()
                self._total_count.update()
                self._page_info.update()
                self._prev_btn.update()
                self._next_btn.update()
        except RuntimeError:
            pass

    def _on_prev_page(self, e):
        """上一页"""
        if self._current_page > 1:
            self._current_page -= 1
            self._refresh_page()

    def _on_next_page(self, e):
        """下一页"""
        if self._current_page < self._total_pages:
            self._current_page += 1
            self._refresh_page()
