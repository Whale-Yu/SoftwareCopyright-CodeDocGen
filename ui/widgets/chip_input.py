# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:06:41
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 10:23:25
FilePath: /SC-CodeDocGen/ui/widgets/chip_input.py
Description: 标签输入组件：用于自定义后缀 / 屏蔽目录的输入

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

import flet as ft


class ChipInput(ft.Column):
    """标签输入组件：输入文本按回车添加标签，标签可删除"""

    def __init__(self, label: str = "", on_changed=None, show_chips: bool = True):
        self.on_changed = on_changed
        self.show_chips = show_chips
        self.chips: list[str] = []

        self._input = ft.TextField(
            label=label,
            hint_text="输入后按回车即可添加喔~",
            border_radius=8,
            dense=True,
            text_size=13,
            on_submit=self._add_chip,
        )

        self._chips_row = ft.Row(wrap=True, spacing=5, run_spacing=2)

        controls = [self._input]
        if self.show_chips:
            controls.append(self._chips_row)

        super().__init__(
            controls,
            spacing=6,
        )

    def _add_chip(self, e):
        text = self._input.value.strip()
        if text and text not in self.chips:
            self.chips.append(text)
            self._refresh_chips()
            self._input.value = ""
            self._input.update()
            if self.on_changed:
                self.on_changed(self.chips)

    def _remove_chip(self, text: str):
        if text in self.chips:
            self.chips.remove(text)
            self._refresh_chips()
            if self.on_changed:
                self.on_changed(self.chips)

    def _build_chip_control(self, chip: str):
        '''
        https://flet.dev/docs/controls/chip
        '''
        return ft.Chip(
            label=ft.Text(chip, size=12),
            on_delete=lambda e, c=chip: self._remove_chip(c),
            bgcolor=ft.Colors.BLUE_100,
            delete_icon=ft.Icons.CLOSE,
            padding=ft.Padding(8, 2, 8, 2),
            shape=ft.RoundedRectangleBorder(radius=20),
        )

    def _refresh_chips(self):
        if self.show_chips:
            self._chips_row.controls.clear()
            for chip in self.chips:
                self._chips_row.controls.append(self._build_chip_control(chip))
            self._chips_row.update()

    def get_chip_controls(self) -> list[ft.Chip]:
        return [self._build_chip_control(chip) for chip in self.chips]

    def set_chips(self, chips: list[str]):
        self.chips = list(chips)
        self._refresh_chips()

    def get_chips(self) -> list[str]:
        return list(self.chips)