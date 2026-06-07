"""测试 MainView"""
import flet as ft
from ui.widgets.folder_drop_zone import FolderDropZone
from ui.widgets.code_stats_card import CodeStatsCard
from ui.config_panel import ConfigPanel


def main(page: ft.Page):
    page.title = "MainView 测试"
    page.window.width = 1100
    page.window.height = 720
    
    print("开始添加控件")
    
    try:
        # 1. 先添加 folder_drop_zone
        print("1. 添加 FolderDropZone")
        folder_zone = FolderDropZone()
        page.add(folder_zone)
        page.update()
        print("FolderDropZone 成功")
    except Exception as e:
        page.add(ft.Text(f"1. 添加 FolderDropZone 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        # 2. 添加 CodeStatsCard
        print("2. 添加 CodeStatsCard")
        stats_card = CodeStatsCard()
        page.add(stats_card)
        page.update()
        print("CodeStatsCard 成功")
    except Exception as e:
        page.add(ft.Text(f"2. 添加 CodeStatsCard 失败: {e}", color=ft.Colors.RED))
        page.update()
        
    try:
        # 3. 添加 ConfigPanel
        print("3. 添加 ConfigPanel")
        config_panel = ConfigPanel()
        page.add(config_panel)
        page.update()
        print("ConfigPanel 成功")
    except Exception as e:
        page.add(ft.Text(f"3. 添加 ConfigPanel 失败: {e}", color=ft.Colors.RED))
        page.update()


if __name__ == "__main__":
    ft.run(main)