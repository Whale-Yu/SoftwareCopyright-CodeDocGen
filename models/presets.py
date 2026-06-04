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
    "emdash": "\u2014\u2014 1 \u2014\u2014, \u2014\u2014 2 \u2014\u2014, \u2014\u2014 3 \u2014\u2014",
    "roman": "\u2160, \u2161, \u2162...",
    "page_cn": "\u7b2c 1 \u9875",
    "page_total": "\u7b2c 1 \u9875 \u5171 X \u9875",
    "slash": "1 / X",
    "cn_num": "\u7b2c\u4e00\u9875",
    "cn_total": "\u7b2c\u4e00\u9875 \u5171 X \u9875",
    "cn_comma": "1\uff0c2\uff0c3\uff0c...",
    "custom": "\u81ea\u5b9a\u4e49",
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
