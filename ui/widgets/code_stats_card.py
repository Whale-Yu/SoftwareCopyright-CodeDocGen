# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:06:55
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:32:53
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/widgets/code_stats_card.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""代码统计结果卡片组件"""
import flet as ft


class CodeStatsCard(ft.Container):
    """代码统计结果展示卡片"""

    def __init__(self):
        self._total_lines = 0
        self._pages = 0
        self._lines_per_page = 50

        self._summary_text = ft.Text(
            "",
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.BLUE_800,
        )

        self._output_mode_group = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="all", label="全部输出"),
                    ft.Radio(value="split", label="前后各30页"),
                ],
                spacing=20,
            ),
            value="all",
        )

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.GREEN_600, size=20),
                            self._summary_text,
                        ],
                        spacing=8,
                    ),
                    ft.Divider(height=1),
                    ft.Text("输出模式:", size=12, color=ft.Colors.GREY_600),
                    self._output_mode_group,
                ],
                spacing=8,
            ),
            padding=ft.Padding(16, 16, 16, 16),
            border_radius=10,
            bgcolor=ft.Colors.GREEN_50,
            border=ft.Border(
                left=ft.BorderSide(1, ft.Colors.GREEN_200),
                top=ft.BorderSide(1, ft.Colors.GREEN_200),
                right=ft.BorderSide(1, ft.Colors.GREEN_200),
                bottom=ft.BorderSide(1, ft.Colors.GREEN_200),
            ),
            visible=False,
        )

    def update_stats(self, total_lines: int, lines_per_page: int = 50):
        self._total_lines = total_lines
        self._lines_per_page = lines_per_page
        self._pages = (total_lines + lines_per_page - 1) // lines_per_page if total_lines > 0 else 0
        self._summary_text.value = (
            f"有效代码共 {total_lines} 行 "
            f"≈ {self._pages} 页（{lines_per_page}行/页）"
        )
        if total_lines > 3000:
            self._output_mode_group.value = "split"
        else:
            self._output_mode_group.value = "all"
        self.visible = True
        self.update()

    @property
    def output_mode(self) -> str:
        return self._output_mode_group.value or "all"

    @property
    def total_lines(self) -> int:
        return self._total_lines

    def set_visible(self, visible: bool):
        self.visible = visible
        self.update()