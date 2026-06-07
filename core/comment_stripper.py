# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:04:44
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:33:59
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/core/comment_stripper.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""多语言注释去除引擎

支持的注释规则：

| 语言 | 单行注释 | 多行注释 |
|------|---------|---------|
| .py  | #       | \"\"\"...\"\"\", '''...''' |
| .js, .ts, .java, .cpp, .c, .cs, .go, .rs, .swift, .kt, .m, .dart | // | /*...*/ |
| .html, .vue | — | <!--...--> |
| .rb, .sh  | # | — |
| .sql | -- | /*...*/ |
| .css, .scss | — | /*...*/ |
| .php | //, # | /*...*/ |
"""
import re
from .language_config import get_comment_rules


_LANG_RULES = get_comment_rules()


def strip_comments(lines: list[str], suffix: str) -> list[str]:
    """去除指定后缀代码行的注释，返回去除后的行列表"""
    rules = _LANG_RULES.get(suffix)
    if not rules:
        return lines

    # 先合并为单个字符串处理多行注释
    text = "\n".join(lines)

    # 移除多行注释块
    for start, end in rules["multi"]:
        pattern = re.escape(start) + r".*?" + re.escape(end)
        text = re.sub(pattern, "", text, flags=re.DOTALL)

    result = []
    for line in text.split("\n"):
        stripped = line
        # 查找行内是否包含单行注释标记（不在字符串内的）
        for marker in rules["single"]:
            # 简单策略：找标记首次出现且前面不是引号内的
            idx = _find_comment_start(stripped, marker)
            if idx != -1:
                stripped = stripped[:idx].rstrip()
                break
        result.append(stripped)

    return result


def _find_comment_start(line: str, marker: str) -> int:
    """在行内查找注释标记的位置，忽略字符串内的"""
    in_str = False
    str_char = ""
    i = 0
    while i < len(line):
        ch = line[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == str_char:
                in_str = False
            i += 1
            continue
        if ch in ('"', "'"):
            in_str = True
            str_char = ch
            i += 1
            continue
        if line[i:i + len(marker)] == marker:
            return i
        i += 1
    return -1
