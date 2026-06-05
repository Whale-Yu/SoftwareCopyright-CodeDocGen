# -*- coding: utf-8 -*-

'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:07:52
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:38:06
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/config_panel.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""右侧配置面板"""
import os
import flet as ft
from models.presets import PAGE_FORMATS


class ConfigPanel(ft.Column):
    """右侧配置面板"""

    def __init__(
        self,
        on_generate_click=None,
        on_config_changed=None,
    ):
        self.on_generate_click = on_generate_click
        self.on_config_changed = on_config_changed

        # ------ 区域1：文档信息 ------
        self._header_label = ft.Text("页眉（软件名称+版本号）", size=14)
        self._header_input = ft.TextField(
            label="例如：SC-CodeDocGenV1.0",
            border_radius=8,
            dense=True,
            text_size=13,
            expand=True,
            on_change=self._notify_config,
        )

        self._page_format_label = ft.Text("页码样式", size=14)
        self._page_format_dd = ft.Dropdown(
            options=[
                ft.dropdown.Option(key=k, text=f"{k} ({v})") for k, v in PAGE_FORMATS.items()
            ],
            value="arabic",
            border_radius=8,
            dense=True,
            text_size=13,
            expand=True,
            on_select=self._on_page_format_change,
        )

        self._custom_page_format = ft.TextField(
            hint_text="{page}/{total}",
            border_radius=8,
            dense=True,
            text_size=13,
            visible=False,
            expand=True,
            on_change=self._notify_config,
        )

        # 页码位置
        self._page_position_label = ft.Text("页码位置", size=14)
        self._page_position_dd = ft.Dropdown(
            options=[
                ft.dropdown.Option(key="header_left", text="页眉左侧（顶端居左）", style=ft.TextStyle(color=ft.Colors.BLUE_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="header_center", text="页眉中间（顶端居中）", style=ft.TextStyle(color=ft.Colors.BLUE_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="header_right", text="页眉右侧（顶端居右）", style=ft.TextStyle(color=ft.Colors.BLUE_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="header_inner", text="页眉内侧（顶端内侧）", style=ft.TextStyle(color=ft.Colors.BLUE_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="header_outer", text="页眉外侧（顶端外侧）", style=ft.TextStyle(color=ft.Colors.BLUE_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="footer_left", text="页脚左侧（底端居左）", style=ft.TextStyle(color=ft.Colors.GREEN_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="footer_center", text="页脚中间（底端居中）", style=ft.TextStyle(color=ft.Colors.GREEN_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="footer_right", text="页脚右侧（底端居右）", style=ft.TextStyle(color=ft.Colors.GREEN_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="footer_inner", text="页脚内侧（底端内侧）", style=ft.TextStyle(color=ft.Colors.GREEN_600, size=12, weight=ft.FontWeight.W_500)),
                ft.dropdown.Option(key="footer_outer", text="页脚外侧（底端外侧）", style=ft.TextStyle(color=ft.Colors.GREEN_600, size=12, weight=ft.FontWeight.W_500)),
            ],
            value="header_right",
            border_radius=8,
            dense=True,
            text_size=12,
            expand=True,
            on_select=self._notify_config,
        )

         # 文档信息卡片
        doc_info_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.GREY_600),
                            ft.Text("文档信息", size=14, weight=ft.FontWeight.W_500),
                            ft.Text("设置页眉和页码", size=11, color=ft.Colors.GREY_500),
                        ],
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Container(height=8),
                    self._header_label,
                    ft.Container(height=2),
                    self._header_input,
                    ft.Container(height=12),
                    self._page_format_label,
                    ft.Container(height=2),
                    ft.Row(
                        [self._page_format_dd, self._custom_page_format],
                        spacing=10,
                    ),
                    ft.Container(height=12),
                    self._page_position_label,
                    ft.Container(height=2),
                    self._page_position_dd,
                ],
                spacing=0,
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

        # ------ 区域2：输出设置 ------
        # 每页代码行数（固定50不可修改）
        self._lines_per_page_label = ft.Text("每页代码行数", size=14)
        self._lines_per_page = ft.TextField(
            value="50",
            border_radius=8,
            dense=True,
            text_size=13,
            read_only=True,
            disabled=True,
            width=100,
        )
        self._lines_per_page_unit = ft.Text("行/页", size=13)

        # 输出模式
        self._output_mode_label = ft.Text("输出模式", size=14)
        self._output_mode_group = ft.RadioGroup(
            content=None,
            value="auto",
            on_change=self._notify_config,
        )
        output_mode_radios = ft.Column(
            [
                ft.Row(
                    [
                        ft.Radio(value="auto", label="自动推荐"),
                        ft.Text("系统推荐：全部输出", size=12, color=ft.Colors.GREEN_600),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Radio(value="all", label="全部输出"),
                ft.Radio(value="before_after_30", label="前后各30页（共60页）"),
            ],
            spacing=4,
        )
        self._output_mode_group.content = output_mode_radios

        # 输出路径
        self._output_path_label = ft.Text("输出路径", size=14)
        self._output_path_input = ft.TextField(
            hint_text="默认保存到桌面",
            border_radius=8,
            dense=True,
            text_size=13,
            expand=True,
            on_change=self._notify_config,
        )
        self._output_path_btn = ft.ElevatedButton(
            "浏览",
            on_click=self._on_select_output_path,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )

        # 按钮
        self._generate_btn = ft.ElevatedButton(
            "开始生成文档",
            on_click=self.on_generate_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
            ),
        )

    
        # 输出设置卡片
        output_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.PRINT, color=ft.Colors.GREY_600),
                            ft.Text("输出设置", size=14, weight=ft.FontWeight.W_500),
                            ft.Text("配置输出模式和路径", size=11, color=ft.Colors.GREY_500),
                        ],
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            self._lines_per_page_label,
                            ft.Container(width=20),
                            self._lines_per_page,
                            self._lines_per_page_unit,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=12),
                    self._output_mode_label,
                    ft.Container(height=2),
                    self._output_mode_group,
                    ft.Container(height=12),
                    self._output_path_label,
                    ft.Container(height=2),
                    ft.Row(
                        [self._output_path_input, self._output_path_btn],
                        spacing=10,
                    ),
                ],
                spacing=0,
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

        # ------ 区域3：生成按钮 ------
        generate_card = ft.Container(
            content=ft.Row([self._generate_btn], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.Padding(0, 2, 0, 2),
        )

        super().__init__(
            [
                doc_info_card,
                output_card,
                generate_card,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    # --- 事件 ---
    def _notify_config(self, e=None):
        if self.on_config_changed:
            self.on_config_changed(self.get_config())

    def _on_page_format_change(self, e):
        self._custom_page_format.visible = (self._page_format_dd.value == "custom")
        self._custom_page_format.update()
        self._notify_config()

    def _on_select_output_path(self, e):
        """选择输出路径"""
        def on_path_result(e):
            if e.path:
                self._output_path_input.value = e.path
                self._output_path_input.update()
                self._notify_config()

        self.page.get_directory_path_dialog = ft.FilePicker(on_result=on_path_result)
        self.page.overlay.append(self.page.get_directory_path_dialog)
        self.page.update()
        initial_path = self._output_path_input.value or os.path.expanduser("~/Desktop")
        self.page.get_directory_path_dialog.get_directory_path(initial_directory=initial_path)

    # --- 数据获取 ---
    def get_header(self) -> str:
        return self._header_input.value.strip()

    def get_page_format(self) -> str:
        return self._page_format_dd.value or "arabic"

    def get_custom_page_format(self) -> str:
        return self._custom_page_format.value.strip()

    def get_page_position(self) -> str:
        return self._page_position_dd.value or "header_right"

    def get_lines_per_page(self) -> int:
        return 50

    def get_output_mode(self) -> str:
        return self._output_mode_group.value or "auto"

    def get_output_path(self) -> str:
        return self._output_path_input.value.strip() or os.path.expanduser("~/Desktop")

    def get_config(self) -> dict:
        return {
            "header": self.get_header(),
            "page_format": self.get_page_format(),
            "custom_page_format": self.get_custom_page_format(),
            "page_position": self.get_page_position(),
            "lines_per_page": self.get_lines_per_page(),
            "output_mode": self.get_output_mode(),
            "output_path": self.get_output_path(),
        }

    def apply_config(self, config: dict):
        """从配置 dict 恢复 UI 状态"""
        if not config:
            return
        self._header_input.value = config.get("header", "")
        self._page_format_dd.value = config.get("page_format", "arabic")
        self._custom_page_format.value = config.get("custom_page_format", "")
        self._custom_page_format.visible = (self._page_format_dd.value == "custom")
        self._page_position_dd.value = config.get("page_position", "header_right")
        self._output_mode_group.value = config.get("output_mode", "auto")
        self._output_path_input.value = config.get("output_path", "")
        self.update()

    # --- 按钮状态 ---
    def set_button_enabled(self, enabled: bool):
        self._generate_btn.disabled = not enabled
        self._generate_btn.update()
