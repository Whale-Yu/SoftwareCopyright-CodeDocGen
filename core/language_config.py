# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 11:17:16
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:33:30
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/core/language_config.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""语言配置：后缀映射、语言名称、注释规则等"""
import os
from pathlib import Path

# 图标基础路径
ICONS_DIR = Path(__file__).parent.parent / "assets" / "language_icons" / "icons"

# 语言后缀映射（按技术栈逻辑排序）
PRESET_SUFFIXES = [
    # 后端主流语言
    (".py", "Python", True),
    (".java", "Java", True),
    (".go", "Go", False),
    (".php", "PHP", True),
    (".cs", "C#", False),
    (".rb", "Ruby", False),

    # Web前端
    (".html", "HTML", True),
    (".css", "CSS", True),
    (".scss", "SCSS", True),
    (".js", "JavaScript", True),
    (".ts", "TypeScript", True),        
    (".vue", "Vue", False),
    (".jsx", "React", True),
    (".tsx", "React TS", True),

    
    # C/C++ 系统级
    (".c", "C", True),
    (".cpp", "C++", True),
    (".h", "C Header", True),
    (".hpp", "C++ Header", True),
    
    # 移动开发
    (".swift", "Swift", False),
    (".kt", "Kotlin", False),
    (".m", "M File", False),  # Objective-C / MATLAB
    (".dart", "Dart", False),
    
    # 其他
    (".rs", "Rust", False),
    (".sql", "SQL", True),
    (".sh", "Shell", True),
]

# 语言图标映射
LANGUAGE_ICONS = {       
    # 后端主流语言
    ".py": "python.svg",
    ".java": "java.svg",
    ".go": "go.svg",
    ".php": "php.svg",
    ".cs": "c-sharp.svg",
    ".rb": "ruby.svg",

    # Web前端
    ".html": "html.svg",
    ".css": "css.svg",
    ".scss": "sass.svg",
    ".js": "javascript.svg",
    ".ts": "typescript.svg",
    ".vue": "vue.svg",
    ".jsx": "react.svg",
    ".tsx": "react.svg",



    # C/C++ 系统级
    ".c": "c.svg",
    ".cpp": "cpp.svg",
    ".h": "c.svg",
    ".hpp": "cpp.svg",

    # 移动开发
    ".swift": "swift.svg",
    ".kt": "kotlin.svg",
    ".m": "c.svg",
    ".dart": "dart.svg",
    
    # 其他
    ".rs": "rust.svg",
    ".sql": "db.svg",
    ".sh": "shell.svg",
}

# 图标尺寸配置
ICON_WIDTH = 20
ICON_HEIGHT = 20

# 获取所有后缀名列表
def get_all_suffixes():
    return [suffix for suffix, _, _ in PRESET_SUFFIXES]

# 获取后缀到语言名称的映射
def get_language_map():
    return {suffix: name for suffix, name, _ in PRESET_SUFFIXES}

# 获取默认选中的后缀
def get_default_selected_suffixes():
    return [suffix for suffix, _, selected in PRESET_SUFFIXES if selected]

# 获取语言名称
def get_language_name(suffix):
    lang_map = get_language_map()
    return lang_map.get(suffix, suffix.lstrip(".").upper())

# 获取语言图标路径
def get_language_icon(suffix):
    icon_filename = LANGUAGE_ICONS.get(suffix)
    
    # 如果没有对应图标，使用默认图标
    if icon_filename is None:
        default_icon_path = ICONS_DIR / "default.svg"
        if default_icon_path.exists():
            return str(default_icon_path)
        return None
    
    icon_path = ICONS_DIR / icon_filename
    if icon_path.exists():
        return str(icon_path)
    
    # 如果指定的图标文件不存在，回退到默认图标
    default_icon_path = ICONS_DIR / "default.svg"
    if default_icon_path.exists():
        return str(default_icon_path)
    
    return None

# 注释规则映射
def get_comment_rules():
    return {
        ".py":  {"single": ["#"], "multi": [('"""', '"""'), ("'''", "'''")]},
        ".js":  {"single": ["//"], "multi": [("/*", "*/")]},
        ".ts":  {"single": ["//"], "multi": [("/*", "*/")]},
        ".jsx": {"single": ["//"], "multi": [("/*", "*/")]},
        ".tsx": {"single": ["//"], "multi": [("/*", "*/")]},
        ".java":{"single": ["//"], "multi": [("/*", "*/")]},
        ".cpp": {"single": ["//"], "multi": [("/*", "*/")]},
        ".c":   {"single": ["//"], "multi": [("/*", "*/")]},
        ".cs":  {"single": ["//"], "multi": [("/*", "*/")]},
        ".go":  {"single": ["//"], "multi": [("/*", "*/")]},
        ".rs":  {"single": ["//"], "multi": [("/*", "*/")]},
        ".swift":{"single": ["//"], "multi": [("/*", "*/")]},
        ".kt":  {"single": ["//"], "multi": [("/*", "*/")]},
        ".m":   {"single": ["//"], "multi": [("/*", "*/")]},
        ".dart":{"single": ["//"], "multi": [("/*", "*/")]},
        ".h":   {"single": ["//"], "multi": [("/*", "*/")]},
        ".hpp": {"single": ["//"], "multi": [("/*", "*/")]},
        ".html":{"single": [],      "multi": [("<!--", "-->")]},
        ".vue": {"single": [],      "multi": [("<!--", "-->")]},
        ".rb":  {"single": ["#"],   "multi": []},
        ".sh":  {"single": ["#"],   "multi": []},
        ".sql": {"single": ["--"],  "multi": [("/*", "*/")]},
        ".css": {"single": [],      "multi": [("/*", "*/")]},
        ".scss":{"single": [],      "multi": [("/*", "*/")]},
        ".php": {"single": ["//", "#"], "multi": [("/*", "*/")]},
    }
