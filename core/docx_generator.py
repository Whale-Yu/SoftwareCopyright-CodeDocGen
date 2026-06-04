# -*- coding: utf-8 -*-
'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:06:01
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 11:35:04
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/core/docx_generator.py
Description: 

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

"""Docx生成模块：页眉 + 页脚页码 + 正文分页"""
import datetime
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from .comment_stripper import strip_comments


# 页码格式渲染函数
_CN_NUMBERS = [
    "\u96f6", "\u4e00", "\u4e8c", "\u4e09", "\u56db",
    "\u4e94", "\u516d", "\u4e03", "\u516b", "\u4e5d", "\u5341",
]


def _cn_number(n: int) -> str:
    """将数字转为中文数字（简单版，支持1-99）"""
    if n <= 10:
        return _CN_NUMBERS[n]
    if n < 20:
        return "\u5341" + _CN_NUMBERS[n - 10]
    tens = n // 10
    ones = n % 10
    result = _CN_NUMBERS[tens] + "\u5341"
    if ones:
        result += _CN_NUMBERS[ones]
    return result


def _roman_number(n: int) -> str:
    """将数字转为大写罗马数字"""
    values = [
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = ""
    for val, sym in values:
        while n >= val:
            result += sym
            n -= val
    return result


def render_page_number(fmt_key: str, current: int, total: int, custom_template: str = "") -> str:
    """根据格式key渲染页码"""
    renderers = {
        "arabic": lambda: str(current),
        "dash": lambda: f"- {current} -",
        "emdash": lambda: f"\u2014\u2014 {current} \u2014\u2014",
        "roman": lambda: _roman_number(current),
        "page_cn": lambda: f"\u7b2c {current} \u9875",
        "page_total": lambda: f"\u7b2c {current} \u9875 \u5171 {total} \u9875",
        "slash": lambda: f"{current} / {total}",
        "cn_num": lambda: f"\u7b2c{_cn_number(current)}\u9875",
        "cn_total": lambda: f"\u7b2c{_cn_number(current)}\u9875 \u5171 {total} \u9875",
        "cn_comma": lambda: "\uff0c".join(str(i) for i in range(1, total + 1)) if current == 1 else "",
        "custom": lambda: custom_template.replace("{page}", str(current)).replace("{total}", str(total)),
    }
    fn = renderers.get(fmt_key)
    if fn:
        return fn()
    return str(current)


def _set_font(run, font_name: str = "\u5b8b\u4f53", size_pt: float = 8):
    """设置 run 的字体"""
    run.font.size = Pt(size_pt)
    run.font.name = font_name
    # 设置中文字体
    r = run._element
    rPr = r.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        r.insert(0, rPr)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:eastAsia'), font_name)


def _set_paragraph_line_spacing(paragraph, pt_val: float = 12):
    """设置段落行距为固定值"""
    pPr = paragraph._element.get_or_add_pPr()
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    spacing.set(qn('w:line'), str(int(pt_val * 20)))
    spacing.set(qn('w:lineRule'), 'exact')


def generate_docx(
    header_text: str,
    page_format: str,
    custom_page_format: str,
    files: list[Path],
    ignore_dir_names: set[str],
    strip_comments_flag: bool,
    strip_empty_lines_flag: bool,
    lines_per_page: int,
    output_mode: str,
    output_dir: str,
) -> Path:
    """
    生成软著代码文档 docx。
    返回生成的 docx 文件路径。
    """
    doc = Document()

    # --- 页面设置 ---
    section = doc.sections[0]
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    # --- 设置默认字体 ---
    style = doc.styles['Normal']
    style.font.size = Pt(8)
    style.font.name = "\u5b8b\u4f53"
    style.element.rPr.rFonts.set(qn('w:eastAsia'), "\u5b8b\u4f53")

    # --- 页眉 ---
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hr = hp.add_run(header_text)
    _set_font(hr, "\u5b8b\u4f53", 8)

    # --- 页脚（页码）---
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 收集所有有效代码行
    all_lines: list[str] = []
    for f in files:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").split("\n")
        except Exception:
            continue
        if strip_comments_flag:
            lines = strip_comments(lines, f.suffix)
        # 可选去空行
        if strip_empty_lines_flag:
            lines = [l for l in lines if l.strip()]
        all_lines.extend(lines)

    total_lines = len(all_lines)

    # 输出模式处理
    if output_mode == "auto":
        if total_lines > 3000:
            output_mode = "split"
        else:
            output_mode = "all"

    if output_mode == "split":
        half = lines_per_page * 30  # 前后各30页 ≈ 1500行
        if total_lines > half * 2:
            all_lines = all_lines[:half] + all_lines[-half:]

    # --- 写入正文 ---
    total_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page
    page_num = 0

    for i, line in enumerate(all_lines):
        if i % lines_per_page == 0:
            if i > 0:
                doc.add_page_break()
            page_num += 1
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        _set_paragraph_line_spacing(p, 12)
        run = p.add_run(line.rstrip())
        _set_font(run, "\u5b8b\u4f53", 8)

    # 补足最后一页到 lines_per_page 行
    remaining = len(all_lines) % lines_per_page
    if remaining > 0:
        for _ in range(lines_per_page - remaining):
            doc.add_paragraph()

    # 刷新 total_pages
    total_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page

    # 写入页码到页脚（使用 XML 域代码实现每页不同页码）
    _add_page_number_field(footer, page_format, total_pages, custom_page_format)

    # --- 生成文件名 ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"\u8f6f\u8457\u4ee3\u7801\u6587\u6863_{timestamp}.docx"
    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))

    return output_path


def _add_page_number_field(footer, page_format: str, total_pages: int, custom_template: str = ""):
    """在页脚中添加 PAGE / NUMPAGES 域代码，实现动态页码"""
    # 需要根据 page_format 来构建域代码
    # Flet/python-docx 插入 PAGE 域代码的方式
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.clear()

    # 根据格式构建域代码
    if page_format == "arabic":
        _add_field(fp, "PAGE")
    elif page_format == "dash":
        fp.add_run("- ").font.size = Pt(8)
        _add_field(fp, "PAGE")
        fp.add_run(" -").font.size = Pt(8)
    elif page_format == "emdash":
        fp.add_run("\u2014\u2014 ").font.size = Pt(8)
        _add_field(fp, "PAGE")
        fp.add_run(" \u2014\u2014").font.size = Pt(8)
    elif page_format == "roman":
        _add_field(fp, "PAGE", "ROMAN")
    elif page_format == "page_cn":
        fp.add_run("\u7b2c ").font.size = Pt(8)
        _add_field(fp, "PAGE")
        fp.add_run(" \u9875").font.size = Pt(8)
    elif page_format == "page_total":
        fp.add_run("\u7b2c ").font.size = Pt(8)
        _add_field(fp, "PAGE")
        fp.add_run(" \u9875 \u5171 ").font.size = Pt(8)
        _add_field(fp, "NUMPAGES")
        fp.add_run(" \u9875").font.size = Pt(8)
    elif page_format == "slash":
        _add_field(fp, "PAGE")
        fp.add_run(" / ").font.size = Pt(8)
        _add_field(fp, "NUMPAGES")
    elif page_format == "cn_num":
        fp.add_run("\u7b2c").font.size = Pt(8)
        _add_field(fp, "PAGE")
        fp.add_run("\u9875").font.size = Pt(8)
    elif page_format == "cn_total":
        fp.add_run("\u7b2c").font.size = Pt(8)
        _add_field(fp, "PAGE")
        fp.add_run("\u9875 \u5171 ").font.size = Pt(8)
        _add_field(fp, "NUMPAGES")
        fp.add_run("\u9875").font.size = Pt(8)
    elif page_format == "custom":
        # 解析自定义模板
        parts = custom_template.replace("{page}", "\x00PAGE\x00").replace("{total}", "\x00NUMPAGES\x00")
        for part in parts.split("\x00"):
            if part == "PAGE":
                _add_field(fp, "PAGE")
            elif part == "NUMPAGES":
                _add_field(fp, "NUMPAGES")
            elif part:
                fp.add_run(part).font.size = Pt(8)
    else:
        _add_field(fp, "PAGE")

    for run in fp.runs:
        run.font.size = Pt(8)


def _add_field(paragraph, field_type: str, fmt: str = None):
    """在段落中插入 Word 域代码 (PAGE / NUMPAGES)"""
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._element.append(fldChar1)

    run2 = paragraph.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    text = field_type
    if fmt:
        text += f" \\* {fmt}"
    instrText.text = text
    run2._element.append(instrText)

    run3 = paragraph.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run3._element.append(fldChar2)