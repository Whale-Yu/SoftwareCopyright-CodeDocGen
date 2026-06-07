# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:04:20
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:35:27
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/core/scanner.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""文件扫描模块：遍历目录，按后缀过滤 + 屏蔽目录过滤"""
import os
from pathlib import Path


def get_ignore_dirs(preset_states: dict[str, bool], custom_dirs: list[str]) -> set[str]:
    """根据预设勾选状态和自定义目录，返回需要屏蔽的目录名集合"""
    ignore = set()
    for name, checked in preset_states.items():
        if checked:
            ignore.add(name)
    for d in custom_dirs:
        d = d.strip()
        if d:
            ignore.add(d)
    return ignore


def scan_files(
    root_dir: str,
    suffixes: list[str],
    ignore_dir_names: set[str],
) -> list[Path]:
    """
    扫描源码目录，返回匹配后缀的文件列表。
    跳过 ignore_dir_names 中的目录。
    """
    root = Path(root_dir)
    result = []
    for entry in root.rglob("*"):
        if entry.is_file() and entry.suffix in suffixes:
            # 检查是否路径中包含屏蔽目录
            parts = set(entry.relative_to(root).parts[:-1])
            if parts & ignore_dir_names:
                continue
            result.append(entry)
    return sorted(result)