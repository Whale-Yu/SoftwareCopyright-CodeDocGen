# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:03:52
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:36:55
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/models/config.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""配置数据模型"""
from dataclasses import dataclass, field
from typing import Optional
from .presets import STRIP_EMPTY_LINES_DEFAULT, STRIP_COMMENTS_DEFAULT


@dataclass
class AppConfig:
    """应用配置数据类"""
    header: str = ""                              # 页眉
    page_format: str = "arabic"                   # 页码格式key
    custom_page_format: str = ""                  # 自定义页码模板
    line_numbering: str = "none"                  # 行号设置："none" | "continuous" | "per_page"
    lines_per_page: int = 50                      # 每页行数
    suffixes: list[str] = field(default_factory=list)          # 选中的代码后缀
    preset_suffix_states: dict[str, bool] = field(default_factory=dict)   # 预设后缀勾选状态
    ignore_dirs: list[str] = field(default_factory=list)        # 屏蔽目录（自定义）
    preset_ignore_states: dict[str, bool] = field(default_factory=dict)  # 预设屏蔽目录勾选状态
    output_mode: Optional[str] = None             # "all" | "before_after_30" | None
    output_path: str = ""                         # 输出路径
    strip_empty_lines: bool = STRIP_EMPTY_LINES_DEFAULT
    strip_comments: bool = STRIP_COMMENTS_DEFAULT

    def to_dict(self) -> dict:
        return {
            "header": self.header,
            "page_format": self.page_format,
            "custom_page_format": self.custom_page_format,
            "line_numbering": self.line_numbering,
            "lines_per_page": self.lines_per_page,
            "suffixes": self.suffixes,
            "preset_suffix_states": self.preset_suffix_states,
            "ignore_dirs": self.ignore_dirs,
            "preset_ignore_states": self.preset_ignore_states,
            "output_mode": self.output_mode,
            "output_path": self.output_path,
            "strip_empty_lines": self.strip_empty_lines,
            "strip_comments": self.strip_comments,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AppConfig":
        return cls(
            header=d.get("header", ""),
            page_format=d.get("page_format", "arabic"),
            custom_page_format=d.get("custom_page_format", ""),
            line_numbering=d.get("line_numbering", "none"),
            lines_per_page=d.get("lines_per_page", 50),
            suffixes=d.get("suffixes", []),
            preset_suffix_states=d.get("preset_suffix_states", {}),
            ignore_dirs=d.get("ignore_dirs", []),
            preset_ignore_states=d.get("preset_ignore_states", {}),
            output_mode=d.get("output_mode", None),
            output_path=d.get("output_path", ""),
            strip_empty_lines=d.get("strip_empty_lines", STRIP_EMPTY_LINES_DEFAULT),
            strip_comments=d.get("strip_comments", STRIP_COMMENTS_DEFAULT),
        )