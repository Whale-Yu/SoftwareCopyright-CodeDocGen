# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 08:10:03
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 20:29:45
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/widgets/code_stats2_panel.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""代码统计2组件"""
import flet as ft


class CodeStats2Panel(ft.Container):
    """代码统计展示组件"""

    def __init__(self):
        # 有效代码行数
        self._effective_lines = ft.Text(
            "0 行",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700,
        )

        # 预计页数
        self._estimated_pages = ft.Text(
            "0 页",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )

        # 推荐输出模式
        self._recommend_mode = ft.Text(
            "全部输出",
            size=16,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.BLUE_600,
        )

        super().__init__(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.ANALYTICS, color=ft.Colors.GREY_600),
                            ft.Text("代码统计", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREY_700),
                        ],
                        spacing=8,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("有效代码行数", size=12, color=ft.Colors.GREY_600),
                                        self._effective_lines,
                                    ],
                                    spacing=4,
                                ),
                                padding=ft.Padding(16, 12, 16, 12),
                                border_radius=8,
                                bgcolor=ft.Colors.GREY_100,
                                expand=1,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("预计页数（50 行/页）", size=12, color=ft.Colors.GREY_600),
                                        self._estimated_pages,
                                    ],
                                    spacing=4,
                                ),
                                padding=ft.Padding(16, 12, 16, 12),
                                border_radius=8,
                                bgcolor=ft.Colors.GREY_100,
                                expand=1,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("推荐输出模式", size=12, color=ft.Colors.GREY_600),
                                        ft.Row(
                                            [
                                                ft.Icon(ft.Icons.STAR_OUTLINE, color=ft.Colors.GREEN_600, size=18),
                                                self._recommend_mode,
                                            ],
                                            spacing=4,
                                        ),
                                    ],
                                    spacing=4,
                                ),
                                padding=ft.Padding(16, 12, 16, 12),
                                border_radius=8,
                                bgcolor=ft.Colors.GREY_100,
                                expand=1,
                            ),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=12,
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
        )

    def update_stats(self, effective_lines: int, estimated_pages: int, recommend_mode: str = "全部输出"):
        """更新统计数据"""
        self._effective_lines.value = f"{effective_lines:,} 行"
        self._estimated_pages.value = f"{estimated_pages:,} 页"
        self._recommend_mode.value = recommend_mode
        self.update()
