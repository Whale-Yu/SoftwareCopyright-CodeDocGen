# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:04:01
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:36:26
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/models/presets.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""预设数据"""
from core.language_config import get_all_suffixes, get_default_selected_suffixes

# 预设页码格式
PAGE_FORMATS: dict[str, str] = {
    "arabic": "1, 2, 3...",
    "dash": "- 1 -, - 2 -, - 3 -...",
    "emdash": "—— 1 ——, —— 2 ——, —— 3 ——",
    "roman": "Ⅰ, Ⅱ, Ⅲ...",
    "page_cn": "第 1 页",
    "page_total": "第 1 页 共 X 页",
    "slash": "1 / X",
    "cn_num": "第一页",
    "cn_total": "第一页 共 X 页",
    "cn_comma": "1，2，3，...",
    "custom": "自定义",
}

# 预设代码后缀
PRESET_SUFFIXES: list[str] = get_all_suffixes()

# 默认选中的后缀
DEFAULT_SELECTED_SUFFIXES: list[str] = []

# 预设屏蔽目录
PRESET_IGNORE_DIRS: list[str] = [
    "node_modules", "dist", ".git", "__pycache__", "build",
    "target", ".venv", "venv", ".idea", ".vscode",
]

# 代码处理选项默认值
STRIP_EMPTY_LINES_DEFAULT: bool = True # 是否去除空行
STRIP_COMMENTS_DEFAULT: bool = False # 是否去除注释