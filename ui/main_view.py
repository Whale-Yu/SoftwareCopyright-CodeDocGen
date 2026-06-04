# -*- coding: utf-8 -*-

'''
Author: Whale-Yu 2933582448@qq.com
Date: 2026-06-04 07:09:18
LastEditors: Whale-Yu 2933582448@qq.com
LastEditTime: 2026-06-04 10:53:05
FilePath: /Tool_20260604_SoftwareCopyright-CodeDocGen/SC-CodeDocGen/ui/main_view.py
Description: 主界面整体布局

Copyright (c) 2026 by 余俊瑜, All Rights Reserved. 
'''

import json
import os
import threading
import time
from pathlib import Path

import flet as ft

from core.scanner import scan_files, get_ignore_dirs
from core.counter import count_code_lines
from core.docx_generator import generate_docx
from models.config import AppConfig
from ui.config_panel import ConfigPanel
from ui.widgets.folder_drop_zone import FolderDropZone
from ui.widgets.options_panel import OptionsPanel
from ui.widgets.code_stats2_panel import CodeStats2Panel
from ui.widgets.code_file_list_panel import CodeFileListPanel


CONFIG_PATH = Path(__file__).parent.parent / "config.json"


class MainView(ft.Column):
    """主界面"""

    def __init__(self):
        self._source_folder = ""
        self._config = AppConfig()
        self._load_config()
        self._files = []

        self._folder_zone = FolderDropZone(on_folder_selected=self._on_folder_selected)

        self._options_panel = OptionsPanel(
            on_suffix_changed=self._on_suffix_changed,
            on_ignore_changed=self._on_ignore_changed,
            on_count_click=self._on_count,
        )

        self._code_stats2_panel = CodeStats2Panel()

        self._code_file_list_panel = CodeFileListPanel()

        self._config_panel = ConfigPanel(
            on_generate_click=self._on_generate,
            on_config_changed=self._on_config_changed,
        )

        # 左侧区域 (占 65%)
        left_panel = ft.Container(
            content=ft.Column(
                [
                    self._folder_zone,
                    self._options_panel,
                    self._code_stats2_panel,
                    self._code_file_list_panel,
                ],
                spacing=16,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding(16, 16, 16, 16),
            expand=65,
        )

        # 右侧区域 (占 35%)
        right_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=self._config_panel,
                        padding=ft.Padding(16, 16, 16, 16),
                        border=ft.Border(
                            left=ft.BorderSide(1, ft.Colors.GREY_300),
                            top=ft.BorderSide(1, ft.Colors.GREY_300),
                            right=ft.BorderSide(1, ft.Colors.GREY_300),
                            bottom=ft.BorderSide(1, ft.Colors.GREY_300),
                        ),
                        border_radius=12,
                        bgcolor=ft.Colors.WHITE,
                        expand=True,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding(16, 16, 16, 16),
            expand=35,
        )

        # 状态栏
        self._status_text = ft.Text("", size=12, color=ft.Colors.GREY_600)
        self._progress_bar = ft.ProgressBar(width=200, visible=False)

        status_bar = ft.Container(
            content=ft.Row(
                [
                    self._status_text,
                    ft.Container(expand=True),
                    self._progress_bar,
                ],
                spacing=10,
            ),
            padding=ft.Padding(16, 0, 16, 8),
        )

        super().__init__(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            left_panel,
                            ft.VerticalDivider(width=1),
                            right_panel,
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
                status_bar,
            ],
            expand=True,
        )

    # --- 事件处理 ---
    def _on_folder_selected(self, path: str):
        self._source_folder = path
        self._status_text.value = f"已选择: {path}"
        self._status_text.update()
        self._config_panel.set_button_enabled(True)
        
        # 立即统计该目录下所有文件（筛选前）
        def scan_all_files():
            try:
                from pathlib import Path
                
                file_count = 0
                total_size = 0
                
                root_path = Path(path)
                for f in root_path.rglob("*"):
                    if f.is_file():
                        try:
                            file_count += 1
                            total_size += f.stat().st_size
                        except Exception:
                            pass
                
                self.page.loop.call_soon_threadsafe(
                    lambda: self._folder_zone.update_stats(file_count, total_size)
                )
            except Exception as ex:
                print(f"[统计] 扫描所有文件出错: {ex}")
        
        threading.Thread(target=scan_all_files, daemon=True).start()

    def _on_suffix_changed(self, suffixes):
        self._config.suffixes = suffixes

    def _on_ignore_changed(self, ignore_dirs):
        self._config.ignore_dirs = ignore_dirs

    def _on_config_changed(self, config_dict):
        pass

    def _on_count(self, e):
        """统计代码行数"""
        print(f"[统计] 统计按钮被点击，时间: {time.strftime('%H:%M:%S')}")
        
        if not self._source_folder:
            print(f"[统计] 错误：未选择源文件夹")
            self._show_snackbar("请先选择源文件夹", is_error=True)
            return

        suffixes = self._options_panel.get_selected_suffixes()
        print(f"[统计] 选择的后缀: {suffixes}")
        
        if not suffixes:
            print(f"[统计] 错误：未选择代码后缀")
            self._show_snackbar("请先选择代码后缀", is_error=True)
            return

        ignore_dirs = self._options_panel.get_ignore_dirs()
        options_config = self._options_panel.get_config()
        preset_ignore = options_config.get("preset_ignore_states", {})
        ignore_set = get_ignore_dirs(preset_ignore, ignore_dirs)
        print(f"[统计] 忽略目录: {ignore_set}")

        self._show_progress(True)
        self._status_text.value = "正在扫描文件..."
        self._status_text.update()
        print(f"[统计] 进度条已显示，开始后台扫描，时间: {time.strftime('%H:%M:%S')}")

        def _run():
            try:
                print(f"[后台] 后台线程启动，时间: {time.strftime('%H:%M:%S')}")
                print(f"[后台] 开始扫描文件夹: {self._source_folder}")
                
                self._files = scan_files(self._source_folder, suffixes, ignore_set)
                print(f"[后台] 扫描完成，找到 {len(self._files)} 个文件")
                
                lines_per_page = self._config_panel.get_lines_per_page()
                process_options = self._options_panel.get_process_options()
                strip_comments = process_options["strip_comments"]
                strip_empty_lines = process_options["strip_empty_lines"]
                print(f"[后台] 开始统计行数，每页 {lines_per_page} 行，去除注释: {strip_comments}，去除空行: {strip_empty_lines}")
                
                stats = count_code_lines(self._files, strip_comments, strip_empty_lines, lines_per_page)
                print(f"[后台] 统计完成: {stats.summary}")
                
                # 更新代码统计
                effective_lines = stats.total_lines
                estimated_pages = stats.pages
                recommend_mode = "全部输出"
                if estimated_pages > 200:
                    recommend_mode = "前 30 页"
                elif estimated_pages > 100:
                    recommend_mode = "前 50 页"
                
                print(f"[后台] 准备更新UI：有效行数 {effective_lines}，预计页数 {estimated_pages}")
                
                self.page.loop.call_soon_threadsafe(
                    lambda: self._code_stats2_panel.update_stats(effective_lines, estimated_pages, recommend_mode)
                )
                
                # 更新文件列表
                files_str = [str(f) for f in self._files]
                self.page.loop.call_soon_threadsafe(
                    lambda: self._code_file_list_panel.update_files(files_str, self._source_folder)
                )
                
                self.page.loop.call_soon_threadsafe(
                    lambda: setattr(self._status_text, "value", f"统计完成: {stats.summary}")
                )
                
                print(f"[后台] 后台任务成功完成，时间: {time.strftime('%H:%M:%S')}")
            except Exception as ex:
                print(f"[后台] 发生错误: {str(ex)}")
                error_msg = str(ex)
                self.page.loop.call_soon_threadsafe(
                    lambda: self._show_snackbar(f"统计失败: {error_msg}", is_error=True)
                )
            finally:
                print(f"[后台] 进入finally块，清理进度条")
                self.page.loop.call_soon_threadsafe(lambda: self._show_progress(False))
                self.page.loop.call_soon_threadsafe(lambda: self._status_text.update())

        print(f"[统计] 创建并启动后台线程")
        threading.Thread(target=_run, daemon=True).start()

    def _on_generate(self, e):
        """生成文档"""
        if not self._source_folder:
            self._show_snackbar("请先选择源文件夹", is_error=True)
            return

        suffixes = self._options_panel.get_selected_suffixes()
        if not suffixes:
            self._show_snackbar("请先选择代码后缀", is_error=True)
            return

        header = self._config_panel.get_header()
        if not header:
            self._show_snackbar("请先填写页眉（软件名称+版本号）", is_error=True)
            return

        self._save_config()

        ignore_dirs = self._options_panel.get_ignore_dirs()
        options_config = self._options_panel.get_config()
        preset_ignore = options_config.get("preset_ignore_states", {})
        ignore_set = get_ignore_dirs(preset_ignore, ignore_dirs)

        self._show_progress(True)
        self._status_text.value = "正在生成文档..."
        self._status_text.update()

        def _run():
            try:
                files = scan_files(self._source_folder, suffixes, ignore_set)
                output_dir = os.path.expanduser("~/Desktop")
                
                # 使用简单输出模式
                output_mode = "all"
                lines_per_page = self._config_panel.get_lines_per_page()
                process_options = self._options_panel.get_process_options()
                strip_comments = process_options["strip_comments"]
                strip_empty_lines = process_options["strip_empty_lines"]
                page_format = self._config_panel.get_page_format()
                custom_page_format = self._config_panel.get_custom_page_format()

                output_path = generate_docx(
                    header_text=header,
                    page_format=page_format,
                    custom_page_format=custom_page_format,
                    files=files,
                    ignore_dir_names=ignore_set,
                    strip_comments_flag=strip_comments,
                    strip_empty_lines_flag=strip_empty_lines,
                    lines_per_page=lines_per_page,
                    output_mode=output_mode,
                    output_dir=output_dir,
                )
                self.page.loop.call_soon_threadsafe(
                    lambda: self._on_generate_done(str(output_path))
                )
            except Exception as ex:
                self.page.loop.call_soon_threadsafe(
                    lambda: self._on_generate_error(str(ex))
                )

        threading.Thread(target=_run, daemon=True).start()

    def _on_generate_done(self, output_path: str):
        self._show_progress(False)
        self._status_text.value = "生成完成!"
        self._status_text.update()

        def open_file(e=None):
            os.startfile(output_path)

        def open_folder(e=None):
            os.startfile(os.path.dirname(output_path))

        self._show_snackbar(
            f"文档已生成: {os.path.basename(output_path)}",
            actions=[
                ft.SnackBarAction(label="打开文档", on_click=open_file),
                ft.SnackBarAction(label="打开文件夹", on_click=open_folder), # 无用
            ],
        )

    def _on_generate_error(self, error_msg: str):
        self._show_progress(False)
        self._status_text.value = f"生成失败: {error_msg}"
        self._status_text.update()
        self._show_snackbar(f"生成失败: {error_msg}", is_error=True)

    # --- 辅助方法 ---
    def _show_progress(self, visible: bool):
        """
        显示或隐藏进度条
        :param visible: True 显示，False 隐藏
        """
        self._progress_bar.visible = visible
        self._progress_bar.update()

    def _show_snackbar(self, message: str, is_error: bool = False, actions=None):
        """
        显示一个SnackBar消息
        :param message: 消息内容
        :param is_error: 是否为错误消息，决定颜色
        :param actions: 可选的操作按钮列表，格式为 [(label, on_click_function), ...]
        """
        bg = ft.Colors.RED_100 if is_error else ft.Colors.GREEN_100
        color = ft.Colors.RED_800 if is_error else ft.Colors.GREEN_800
        snack = ft.SnackBar(
            content=ft.Text(message, color=color),
            bgcolor=bg,
            show_close_icon=True,
            
        )
        if actions:
            snack.action = actions[0]
        self.page.show_dialog(snack)

    # --- 配置持久化 ---
    def _load_config(self):
        try:
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._config = AppConfig.from_dict(data)
        except Exception:
            self._config = AppConfig()

    def _save_config(self):
        config_dict = {
            **self._config_panel.get_config(),
            **self._options_panel.get_config(),
        }
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # --- 恢复配置 ---
    def did_mount(self):
        if self._config:
            config_dict = self._config.to_dict()
            self._config_panel.apply_config(config_dict)
            self._options_panel.apply_config(config_dict)
            if self._source_folder:
                self._config_panel.set_button_enabled(True)
