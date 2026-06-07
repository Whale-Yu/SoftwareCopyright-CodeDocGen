# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:04:52
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:34:33
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/core/counter.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""代码行统计模块：去空行 + 去注释，返回有效行数"""
from pathlib import Path
from .comment_stripper import strip_comments


class CodeStats:
    """代码统计结果"""
    def __init__(self, total_lines: int = 0, page_lines: int = 50):
        self.total_lines = total_lines
        self.pages = (total_lines + page_lines - 1) // page_lines if total_lines > 0 else 0

    @property
    def summary(self) -> str:
        return f"有效代码共 {self.total_lines} 行 \u2248 {self.pages} \u9875\uff0850\u884c/\u9875\uff09"


def count_code_lines(
    files: list[Path],
    strip_comments_flag: bool = True,
    strip_empty_lines_flag: bool = True,
    lines_per_page: int = 50,
) -> CodeStats:
    """
    统计所有文件的有效代码行数。
    - 可选去除空行
    - 可选去除注释
    """
    total = 0
    for f in files:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").split("\n")
        except Exception:
            continue

        if strip_comments_flag:
            lines = strip_comments(lines, f.suffix)

        # 统计行数（可选去除空行）
        for line in lines:
            if strip_empty_lines_flag:
                if line.strip():
                    total += 1
            else:
                total += 1

    return CodeStats(total_lines=total, page_lines=lines_per_page)


def count_single_file_lines(
    file_path: Path,
    strip_comments_flag: bool = True,
    strip_empty_lines_flag: bool = True,
) -> int:
    """
    统计单个文件的有效代码行数。
    - 可选去除空行
    - 可选去除注释
    """
    try:
        lines = file_path.read_text(encoding="utf-8", errors="replace").split("\n")
    except Exception:
        return 0

    if strip_comments_flag:
        lines = strip_comments(lines, file_path.suffix)

    # 统计行数（可选去除空行）
    count = 0
    for line in lines:
        if strip_empty_lines_flag:
            if line.strip():
                count += 1
        else:
            count += 1

    return count