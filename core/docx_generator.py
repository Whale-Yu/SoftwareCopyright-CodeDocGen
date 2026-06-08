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
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from .comment_stripper import strip_comments


# 页码格式渲染函数
_CN_NUMBERS = [
    "零", "一", "二", "三", "四",
    "五", "六", "七", "八", "九", "十",
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
        "emdash": lambda: f"—— {current} ——",
        "roman": lambda: _roman_number(current),
        "page_cn": lambda: f"第 {current} 页",
        "page_total": lambda: f"第 {current} 页 共 {total} 页",
        "slash": lambda: f"{current} / {total}",
        "cn_num": lambda: f"第{_cn_number(current)}页",
        "cn_total": lambda: f"第{_cn_number(current)}页 共 {total} 页",
        "cn_comma": lambda: "，".join(str(i) for i in range(1, total + 1)) if current == 1 else "",
        "custom": lambda: custom_template.replace("{page}", str(current)).replace("{total}", str(total)),
    }
    fn = renderers.get(fmt_key)
    if fn:
        return fn()
    return str(current)


def _set_font(run, font_name: str = "宋体", size_pt: float = 10.5):
    """设置 run 的字体：中文宋体，英文Times New Roman"""
    run.font.size = Pt(size_pt)
    # 设置中文字体和英文字体
    r = run._element
    rPr = r.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        r.insert(0, rPr)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    # 设置中文字体
    rFonts.set(qn('w:eastAsia'), font_name)
    # 设置英文字体为Times New Roman
    rFonts.set(qn('w:ascii'), "Times New Roman")
    rFonts.set(qn('w:hAnsi'), "Times New Roman")


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
    page_position: str,
    line_numbering: str,
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
    # 设置A4纸张大小
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    # 标准文档边距设置
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    section.top_margin = Cm(2.3)
    section.bottom_margin = Cm(2.3)
    section.header_distance = Cm(1.5)
    section.footer_distance = Cm(1.75)
    # 根据配置设置行号
    if line_numbering == "continuous":
        line_numbering_elem = OxmlElement('w:lnNumType')
        line_numbering_elem.set(qn('w:start'), '0')
        line_numbering_elem.set(qn('w:countBy'), '1')
        line_numbering_elem.set(qn('w:restart'), 'continuous')
        section._sectPr.append(line_numbering_elem)
    elif line_numbering == "per_page":
        line_numbering_elem = OxmlElement('w:lnNumType')
        line_numbering_elem.set(qn('w:start'), '0')
        line_numbering_elem.set(qn('w:countBy'), '1')
        line_numbering_elem.set(qn('w:restart'), 'newPage')
        section._sectPr.append(line_numbering_elem)

    # --- 设置默认字体 ---
    style = doc.styles['Normal']
    style.font.size = Pt(10.5)
    style.font.name = "宋体"
    # 设置中文字体和英文字体
    style.element.rPr.rFonts.set(qn('w:eastAsia'), "宋体")
    style.element.rPr.rFonts.set(qn('w:ascii'), "Times New Roman")
    style.element.rPr.rFonts.set(qn('w:hAnsi'), "Times New Roman")

    # --- 页眉 ---
    header = section.header
    header.is_linked_to_previous = False
    # 先清空页眉，后面根据 page_position 决定是否添加页眉内容
    hp = header.paragraphs[0]
    hp.clear()

    # --- 页脚（页码）---
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.clear()

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
            output_mode = "before_after_30"
        else:
            output_mode = "all"

    if output_mode == "before_after_30":
        half = lines_per_page * 30  # 前后各30页 ≈ 1500行
        if total_lines > half * 2:
            all_lines = all_lines[:half] + all_lines[-half:]

    # --- 写入正文 ---
    # total_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page
    # page_num = 0

    # for i, line in enumerate(all_lines):
    #     if i % lines_per_page == 0:
    #         if i > 0:
    #             doc.add_page_break()
    #         page_num += 1
    #     p = doc.add_paragraph()
    #     p.paragraph_format.space_before = Pt(0)
    #     p.paragraph_format.space_after = Pt(0)
    #     _set_paragraph_line_spacing(p, 14)
    #     run = p.add_run(line.rstrip())
    #     _set_font(run, "宋体", 10.5)

    # # 补足最后一页到 lines_per_page 行
    # remaining = len(all_lines) % lines_per_page
    # if remaining > 0:
    #     for _ in range(lines_per_page - remaining):
    #         doc.add_paragraph()
    # --- 写入正文 ---
    # 严格计算：A4可用高度 25.1cm = 711.43 磅。 711.43 / 50 = 14.22 磅
    # 这里取 14.2 磅，留出约 0.4 磅的微弱安全余量，确保绝对不会因为四舍五入溢出到第 51 行
    target_line_spacing = 711.4 / lines_per_page 

    for i, line in enumerate(all_lines):
        p = doc.add_paragraph()
        pPr = p._element.get_or_add_pPr()
        
        # 1. 严格清除段前段后距
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        
        # 2. 核心：关闭孤行控制、禁止段中分页，强制单行独立排版
        p.paragraph_format.widow_control = False
        p.paragraph_format.keep_with_next = False
        
        # 3. 核心：关闭“对齐文档网格”，让固定行距完全由代码控制
        snapToGrid = OxmlElement('w:snapToGrid')
        snapToGrid.set(qn('w:val'), '0')  # 0 代表关闭
        pPr.append(snapToGrid)
        
        # 4. 设置精准固定行距
        _set_paragraph_line_spacing(p, target_line_spacing)
        
        # 5. 写入文本并设置字体
        run = p.add_run(line.rstrip())
        _set_font(run, "宋体", 10.5)

    # 此时无需加任何手动分页符，Word 自带的软分页在展现和打印时，每页必定是雷打不动的 50 行

    # 刷新 total_pages
    total_pages = (len(all_lines) + lines_per_page - 1) // lines_per_page

    # 根据 page_position 决定在哪里添加页码
    _add_page_number_by_position(section, header_text, page_position, page_format, total_pages, custom_page_format)

    # --- 生成文件名 ---
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"软著代码文档_{timestamp}.docx"
    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))

    return output_path


def _add_page_number_by_position(section, header_text: str, page_position: str, page_format: str, total_pages: int, custom_template: str = ""):
    """根据 page_position 参数决定在页眉还是页脚添加页码，以及对齐方式"""
    header = section.header
    footer = section.footer
    hp = header.paragraphs[0]
    fp = footer.paragraphs[0]

    # 解析 page_position，格式为 "header_left" / "footer_right" 等
    if page_position.startswith("header_"):
        # 页码在页眉，同一行：页眉内容始终居中，页码在左或右
        
        if page_position.endswith("_left"):
            # 页眉左侧：[页码][tab][页眉内容]
            hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            paragraph_format = hp.paragraph_format
            tab_stops = paragraph_format.tab_stops
            tab_stops.add_tab_stop(Cm(7.5), WD_TAB_ALIGNMENT.CENTER)
            
            _add_page_number_field_content(hp, page_format, total_pages, custom_template)
            hp.add_run("\t")
            hr = hp.add_run(header_text)
            _set_font(hr, "宋体", 10)
            
        elif page_position.endswith("_right"):
            # 页眉右侧：[页眉内容][tab][页码]
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            paragraph_format = hp.paragraph_format
            tab_stops = paragraph_format.tab_stops
            tab_stops.add_tab_stop(Cm(7.5), WD_TAB_ALIGNMENT.CENTER)
            
            hr = hp.add_run(header_text)
            _set_font(hr, "宋体", 10)
            hp.add_run("\t")
            _add_page_number_field_content(hp, page_format, total_pages, custom_template)
            
        else:
            # 默认页眉右侧
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            
            paragraph_format = hp.paragraph_format
            tab_stops = paragraph_format.tab_stops
            tab_stops.add_tab_stop(Cm(7.5), WD_TAB_ALIGNMENT.CENTER)
            
            hr = hp.add_run(header_text)
            _set_font(hr, "宋体", 10)
            hp.add_run("\t")
            _add_page_number_field_content(hp, page_format, total_pages, custom_template)
    else:
        # 页码在页脚，页眉正常显示
        hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        hr = hp.add_run(header_text)
        _set_font(hr, "宋体", 10)

        # 确定页脚对齐方式
        if page_position.endswith("_left"):
            fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        elif page_position.endswith("_center"):
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif page_position.endswith("_right"):
            fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        else:
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 添加页码到页脚
        _add_page_number_field_content(fp, page_format, total_pages, custom_template)


def _add_page_number_field_content(paragraph, page_format: str, total_pages: int, custom_template: str = ""):
    """在段落中添加 PAGE / NUMPAGES 域代码，实现动态页码"""
    # 需要根据 page_format 来构建域代码
    # Flet/python-docx 插入 PAGE 域代码的方式
    fp = paragraph

    # 辅助函数：添加带字体设置的文本
    def add_text_run(text):
        run = fp.add_run(text)
        _set_font(run, "宋体", 9)
        return run

    # 根据格式构建域代码
    if page_format == "arabic":
        _add_field(fp, "PAGE")
    elif page_format == "dash":
        add_text_run("- ")
        _add_field(fp, "PAGE")
        add_text_run(" -")
    elif page_format == "emdash":
        add_text_run("—— ")
        _add_field(fp, "PAGE")
        add_text_run(" ——")
    elif page_format == "roman":
        _add_field(fp, "PAGE", "ROMAN")
    elif page_format == "page_cn":
        add_text_run("第 ")
        _add_field(fp, "PAGE")
        add_text_run(" 页")
    elif page_format == "page_total":
        add_text_run("第 ")
        _add_field(fp, "PAGE")
        add_text_run(" 页 共 ")
        _add_field(fp, "NUMPAGES")
        add_text_run(" 页")
    elif page_format == "slash":
        _add_field(fp, "PAGE")
        add_text_run(" / ")
        _add_field(fp, "NUMPAGES")
    elif page_format == "cn_num":
        add_text_run("第")
        _add_field(fp, "PAGE")
        add_text_run("页")
    elif page_format == "cn_total":
        add_text_run("第")
        _add_field(fp, "PAGE")
        add_text_run("页 共 ")
        _add_field(fp, "NUMPAGES")
        add_text_run("页")
    elif page_format == "custom":
        # 解析自定义模板
        parts = custom_template.replace("{page}", "\x00PAGE\x00").replace("{total}", "\x00NUMPAGES\x00")
        for part in parts.split("\x00"):
            if part == "PAGE":
                _add_field(fp, "PAGE")
            elif part == "NUMPAGES":
                _add_field(fp, "NUMPAGES")
            elif part:
                add_text_run(part)
    else:
        _add_field(fp, "PAGE")

    # 确保所有 run 都有正确的字体设置
    for run in fp.runs:
        if run.font.size is None or run.font.size.pt != 9:
            _set_font(run, "宋体", 9)


def _add_field(paragraph, field_type: str, fmt: str = None):
    """在段落中插入 Word 域代码 (PAGE / NUMPAGES)"""
    # 创建三个 run 并设置字体
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run._element.append(fldChar1)
    _set_font(run, "宋体", 9)

    run2 = paragraph.add_run()
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    text = field_type
    if fmt:
        text += f" \\* {fmt}"
    instrText.text = text
    run2._element.append(instrText)
    _set_font(run2, "宋体", 9)

    run3 = paragraph.add_run()
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run3._element.append(fldChar2)
    _set_font(run3, "宋体", 9)