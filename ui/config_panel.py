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

        # 页眉输入
        self._header_input = ft.TextField(
            label="页眉（软件名称+版本号）",
            hint_text="例如：SC-CodeDocGenV1.0",
            border_radius=8,
            dense=True,
            text_size=13,
            on_change=self._notify_config,
        )

        # 页码格式
        self._page_format_dd = ft.Dropdown(
            label="页码格式",
            options=[
                ft.dropdown.Option(key=k, text=f"{k} ({v})") for k, v in PAGE_FORMATS.items()
            ],
            value="arabic",
            border_radius=8,
            dense=True,
            text_size=13,
            on_select=self._on_page_format_change,
        )

        # 自定义页码模板
        self._custom_page_format = ft.TextField(
            label="自定义页码模板",
            hint_text="{page}/{total}",
            border_radius=8,
            dense=True,
            text_size=13,
            visible=False,
            on_change=self._notify_config,
        )

        # 每页行数
        self._lines_per_page = ft.TextField(
            label="每页行数",
            value="50",
            border_radius=8,
            dense=True,
            text_size=13,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=self._notify_config,
        )

        # 去除注释
        self._strip_comments = ft.Checkbox(
            label="去除注释",
            value=True,
            on_change=self._notify_config,
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

        super().__init__(
            [
                ft.Text("配置", size=16, weight=ft.FontWeight.BOLD),
                self._header_input,
                ft.Row(
                    [self._page_format_dd, self._custom_page_format],
                    spacing=10,
                ),
                ft.Row(
                    [self._lines_per_page, self._strip_comments],
                    spacing=10,
                ),
                self._generate_btn,
            ],
            spacing=8,
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

    # --- 数据获取 ---
    def get_header(self) -> str:
        return self._header_input.value.strip()

    def get_page_format(self) -> str:
        return self._page_format_dd.value or "arabic"

    def get_custom_page_format(self) -> str:
        return self._custom_page_format.value.strip()

    def get_lines_per_page(self) -> int:
        try:
            return int(self._lines_per_page.value)
        except ValueError:
            return 50

    def get_strip_comments(self) -> bool:
        return self._strip_comments.value

    def get_config(self) -> dict:
        return {
            "header": self.get_header(),
            "page_format": self.get_page_format(),
            "custom_page_format": self.get_custom_page_format(),
            "lines_per_page": self.get_lines_per_page(),
            "strip_comments": self.get_strip_comments(),
        }

    def apply_config(self, config: dict):
        """从配置 dict 恢复 UI 状态"""
        if not config:
            return
        self._header_input.value = config.get("header", "")
        self._page_format_dd.value = config.get("page_format", "arabic")
        self._custom_page_format.value = config.get("custom_page_format", "")
        self._custom_page_format.visible = (self._page_format_dd.value == "custom")
        self._lines_per_page.value = str(config.get("lines_per_page", 50))
        self._strip_comments.value = config.get("strip_comments", True)
        self.update()

    # --- 按钮状态 ---
    def set_button_enabled(self, enabled: bool):
        self._generate_btn.disabled = not enabled
        self._generate_btn.update()
