# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:56:35
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 19:37:56
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/widgets/options_panel.py
Description: 代码后缀和屏蔽文件夹组件

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

import flet as ft
from models.presets import PRESET_SUFFIXES, PRESET_IGNORE_DIRS, DEFAULT_SELECTED_SUFFIXES, STRIP_EMPTY_LINES_DEFAULT, STRIP_COMMENTS_DEFAULT
from ui.widgets.chip_input import ChipInput


class OptionsPanel(ft.Column):
    """代码后缀、屏蔽目录、统计源码行数三个独立卡片面板"""

    def __init__(self, on_suffix_changed=None, on_ignore_changed=None, on_count_click=None):
        self.on_suffix_changed = on_suffix_changed
        self.on_ignore_changed = on_ignore_changed
        self.on_count_click = on_count_click



        # ------ 代码后缀 ------
        self._suffix_checkboxes: dict[str, ft.Checkbox] = {}
        for suffix in PRESET_SUFFIXES:
            # https://flet.dev/docs/controls/checkbox/
            self._suffix_checkboxes[suffix] = ft.Checkbox(
                label=suffix,
                label_style=ft.TextStyle(size=18),
                value=suffix in DEFAULT_SELECTED_SUFFIXES,
                on_change=self._on_suffix_toggle,
                visual_density=ft.VisualDensity.COMPACT,
                scale=0.75
            )

        suffix_items = [ft.Container(self._suffix_checkboxes[suf], width=55) for suf in PRESET_SUFFIXES]
        self._suffix_custom_chips = ft.Row(wrap=True, spacing=4, run_spacing=4)
        suffix_items.append(self._suffix_custom_chips)
        
        self._suffix_add_btn = ft.ElevatedButton(
            "+自定义后缀",
            on_click=self._show_suffix_input,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.Padding(12, 2, 12, 2),
                bgcolor=ft.Colors.BLUE_50,
                color=ft.Colors.BLUE_700,
            ),
            height=32,
        )
        suffix_items.append(self._suffix_add_btn)
        
        suffix_wrap = ft.Row(
            suffix_items,
            spacing=4,
            wrap=True,
            run_spacing=4,
        )

        self._suffix_chip_input = ChipInput(
            label="自定义后缀（如 .dart）",
            on_changed=self._on_custom_suffix_changed,
            show_chips=False,
        )
        self._suffix_chip_input.visible = False
        self._suffix_chip_input._input.on_submit = self._on_suffix_input_submit
        self._suffix_chip_input._input.on_blur = self._on_suffix_input_blur

        # 代码后缀卡片
        suffix_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CODE, color=ft.Colors.GREY_600),
                            ft.Text("代码后缀", size=14, weight=ft.FontWeight.W_500),
                            ft.Text("选择需要处理的代码文件后缀名", size=11, color=ft.Colors.GREY_500),
                        ],
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    suffix_wrap,
                    self._suffix_chip_input,
                ],
                spacing=8,
            ),
            padding=ft.Padding(16, 16, 16, 16),
            border=ft.Border(
                left=ft.BorderSide(1, ft.Colors.GREY_300),
                top=ft.BorderSide(1, ft.Colors.GREY_300),
                right=ft.BorderSide(1, ft.Colors.GREY_300),
                bottom=ft.BorderSide(1, ft.Colors.GREY_300),
            ),
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
        )

        # ------ 屏蔽文件夹 ------
        self._ignore_checkboxes: dict[str, ft.Checkbox] = {}
        for dname in PRESET_IGNORE_DIRS:
            self._ignore_checkboxes[dname] = ft.Checkbox(
                label=dname,
                label_style=ft.TextStyle(size=18),
                value=True,
                on_change=self._on_ignore_toggle,
                visual_density=ft.VisualDensity.COMPACT,
                scale=0.75
            )

        ignore_items = [ft.Container(self._ignore_checkboxes[d], width=110) for d in PRESET_IGNORE_DIRS]
        self._ignore_custom_chips = ft.Row(wrap=True, spacing=4, run_spacing=4)
        ignore_items.append(self._ignore_custom_chips)
        
        self._ignore_add_btn = ft.ElevatedButton(
            "+自定义屏蔽目录",
            on_click=self._show_ignore_input,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=ft.Padding(12, 2, 12, 2),
                bgcolor=ft.Colors.BLUE_50,
                color=ft.Colors.BLUE_700,
            ),
            height=32,
        )
        ignore_items.append(self._ignore_add_btn)
        
        ignore_wrap = ft.Row(
            ignore_items,
            spacing=4,
            wrap=True,
            run_spacing=4,
        )

        self._ignore_chip_input = ChipInput(
            label="自定义屏蔽目录",
            on_changed=self._on_custom_ignore_changed,
            show_chips=False,
        )
        self._ignore_chip_input.visible = False
        self._ignore_chip_input._input.on_submit = self._on_ignore_input_submit
        self._ignore_chip_input._input.on_blur = self._on_ignore_input_blur

        # 屏蔽文件夹卡片
        ignore_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.FOLDER_OPEN, color=ft.Colors.GREY_600),
                            ft.Text("屏蔽目录", size=14, weight=ft.FontWeight.W_500),
                            ft.Text("选择要排除扫描的目录", size=11, color=ft.Colors.GREY_500),
                        ],
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ignore_wrap,
                    self._ignore_chip_input,
                ],
                spacing=8,
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

        # ------ 代码处理选项 ------
        self._strip_empty_lines = ft.Checkbox(
            label="去除空行（推荐：优化代码排版以规范程序鉴别材料）",
            label_style=ft.TextStyle(size=14),
            value=STRIP_EMPTY_LINES_DEFAULT,
            visual_density=ft.VisualDensity.COMPACT,
            scale=0.85,
        )
        self._strip_comments = ft.Checkbox(
            label="去除注释（不建议：保留注释可提高与文档鉴别材料的匹配度）",
            label_style=ft.TextStyle(size=14),
            value=STRIP_COMMENTS_DEFAULT,
            visual_density=ft.VisualDensity.COMPACT,
            scale=0.85,
        )
        process_options_wrap = ft.Row(
            [
                ft.Container(self._strip_empty_lines, width=330),
                ft.Container(self._strip_comments, width=330),
            ],
            spacing=8,
            wrap=True,
            run_spacing=4,
        )

        # 代码处理卡片
        process_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SETTINGS, color=ft.Colors.GREY_600),
                            ft.Text("代码处理", size=14, weight=ft.FontWeight.W_500),
                            ft.Text("统计前的预处理选项（不对源码内容产生影响，仅用于读取和统计）", size=11, color=ft.Colors.GREY_500),
                        ],
                        spacing=4,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    process_options_wrap,
                ],
                spacing=8,
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

        # ------ 统计源码行数按钮 ------
        self._count_btn = ft.ElevatedButton(
            "统计源码行数",
            on_click=self.on_count_click,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
            width=200,
            height=40,
        )

        # 统计按钮
        count_card = ft.Container(
            content=ft.Row([self._count_btn], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.Padding(0, 2, 0, 2),
        )

        super().__init__(
            [
                suffix_card,
                ignore_card,
                process_card,
                count_card,
            ],
            spacing=12,
        )

        self._refresh_suffix_custom_chips()
        self._refresh_ignore_custom_chips()

    # --- 事件 ---
    def _on_suffix_toggle(self, e):
        if self.on_suffix_changed:
            self.on_suffix_changed(self.get_selected_suffixes())

    def _show_suffix_input(self, e):
        self._suffix_chip_input.visible = True
        self._suffix_add_btn.visible = False
        self._suffix_chip_input._input.focus()
        self.update()

    def _on_suffix_input_submit(self, e):
        text = e.control.value.strip()
        if text and text not in self._suffix_chip_input.chips:
            self._suffix_chip_input.chips.append(text)
            self._suffix_chip_input._refresh_chips()
            self._refresh_suffix_custom_chips()
            if self.on_suffix_changed:
                self.on_suffix_changed(self.get_selected_suffixes())
        self._suffix_chip_input._input.value = ""
        self._suffix_chip_input.visible = False
        self._suffix_add_btn.visible = True
        self.update()

    def _on_suffix_input_blur(self, e):
        text = e.control.value.strip()
        if not text:
            self._suffix_chip_input._input.value = ""
            self._suffix_chip_input.visible = False
            self._suffix_add_btn.visible = True
            self.update()

    def _on_custom_suffix_changed(self, chips):
        self._refresh_suffix_custom_chips()
        if self.on_suffix_changed:
            self.on_suffix_changed(self.get_selected_suffixes())

    def _on_ignore_toggle(self, e):
        if self.on_ignore_changed:
            self.on_ignore_changed(self.get_ignore_dirs())

    def _show_ignore_input(self, e):
        self._ignore_chip_input.visible = True
        self._ignore_add_btn.visible = False
        self._ignore_chip_input._input.focus()
        self.update()

    def _on_ignore_input_submit(self, e):
        text = e.control.value.strip()
        if text and text not in self._ignore_chip_input.chips:
            self._ignore_chip_input.chips.append(text)
            self._ignore_chip_input._refresh_chips()
            self._refresh_ignore_custom_chips()
            if self.on_ignore_changed:
                self.on_ignore_changed(self.get_ignore_dirs())
        self._ignore_chip_input._input.value = ""
        self._ignore_chip_input.visible = False
        self._ignore_add_btn.visible = True
        self.update()

    def _on_ignore_input_blur(self, e):
        text = e.control.value.strip()
        if not text:
            self._ignore_chip_input._input.value = ""
            self._ignore_chip_input.visible = False
            self._ignore_add_btn.visible = True
            self.update()

    def _on_custom_ignore_changed(self, chips):
        self._refresh_ignore_custom_chips()
        if self.on_ignore_changed:
            self.on_ignore_changed(self.get_ignore_dirs())

    def _refresh_suffix_custom_chips(self):
        self._suffix_custom_chips.controls = self._suffix_chip_input.get_chip_controls()
        try:
            if self._suffix_custom_chips.page:
                self._suffix_custom_chips.update()
                # 确保按钮始终在最后
                if hasattr(self, '_suffix_add_btn'):
                    self._suffix_add_btn.update()
        except RuntimeError:
            pass

    def _refresh_ignore_custom_chips(self):
        self._ignore_custom_chips.controls = self._ignore_chip_input.get_chip_controls()
        try:
            if self._ignore_custom_chips.page:
                self._ignore_custom_chips.update()
                # 确保按钮始终在最后
                if hasattr(self, '_ignore_add_btn'):
                    self._ignore_add_btn.update()
        except RuntimeError:
            pass

    # --- 数据获取 ---
    def get_selected_suffixes(self) -> list[str]:
        suffixes = []
        for suf, cb in self._suffix_checkboxes.items():
            if cb.value:
                suffixes.append(suf)
        suffixes.extend(self._suffix_chip_input.get_chips())
        return suffixes

    def get_ignore_dirs(self) -> list[str]:
        dirs = []
        for d, cb in self._ignore_checkboxes.items():
            if cb.value: 
                dirs.append(d)
        dirs.extend(self._ignore_chip_input.get_chips())
        return dirs

    def get_process_options(self) -> dict:
        """获取代码处理选项配置"""
        return {
            "strip_empty_lines": self._strip_empty_lines.value,
            "strip_comments": self._strip_comments.value,
        }

    def apply_config(self, config: dict):
        """从配置 dict 恢复 UI 状态"""
        for suf, state in config.get("preset_suffix_states", {}).items():
            if suf in self._suffix_checkboxes:
                self._suffix_checkboxes[suf].value = state

        for d, state in config.get("preset_ignore_states", {}).items():
            if d in self._ignore_checkboxes:
                self._ignore_checkboxes[d].value = state

        self._suffix_chip_input.set_chips(config.get("suffixes", []))
        self._ignore_chip_input.set_chips(config.get("ignore_dirs", []))
        
        # 恢复代码处理选项
        if "strip_empty_lines" in config:
            self._strip_empty_lines.value = config["strip_empty_lines"]
        if "strip_comments" in config:
            self._strip_comments.value = config["strip_comments"]

        self._refresh_suffix_custom_chips()
        self._refresh_ignore_custom_chips()
        self.update()

    def get_config(self) -> dict:
        return {
            "suffixes": self.get_selected_suffixes(),
            "preset_suffix_states": {k: v.value for k, v in self._suffix_checkboxes.items()},
            "ignore_dirs": [d for d in self._ignore_chip_input.get_chips()],
            "preset_ignore_states": {k: v.value for k, v in self._ignore_checkboxes.items()},
            "strip_empty_lines": self._strip_empty_lines.value,
            "strip_comments": self._strip_comments.value,
        }
