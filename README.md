# SC-CodeDocGen 软著代码文档生成器

> 基于 [Flet](https://flet.dev/) 的软件著作权源代码文档生成工具，一秒将你的源码转化为标准的软著源代码文档。

---

## 功能特性

-  **多语言支持**：支持 Python、Java、JavaScript、TypeScript、C/C++、Go、PHP、Vue、React、SQL、Shell 等 20+ 主流编程语言
-  **灵活的文件筛选**：按文件后缀勾选，并支持预设屏蔽目录（node_modules、dist、.git、__pycache__ 等）+ 自定义屏蔽目录
-  **代码去冗余**：可选去除注释行、去除空行，让文档更规范
-  **页眉页脚自定义**：自定义页眉文字（软件名称+版本号），10+ 种页码格式可选（阿拉伯数字、罗马数字、中文数字、`自定义模板` 等），页码位置可选（页眉/页脚 × 左/中/右）
-  **精确排版控制**：A4 纸张（21×29.7 cm），每页行数自定义（默认 50 行/页），中文宋体 + 英文 Times New Roman，固定行距严格对齐
-  **智能输出模式**：支持「全部输出」和「前后各 30 页（共 60 页）」两种模式，满足不同字数要求；自动推荐
-  **实时统计**：扫描前自动统计文件数量与总大小，统计后显示有效代码行数与预估页数
-  **可视化文件列表**：带语言图标的文件列表，一目了然
-  **一键生成 Word**：生成 `.docx` 格式文档，文件命名自动附加时间戳，支持一键打开

## 技术栈

| 组件 | 技术 |
|------|------|
| GUI 框架 | [Flet](https://flet.dev/)（基于 Flutter 的 Python 桌面开发框架） |
| Word 文档生成 | [python-docx](https://python-docx.readthedocs.io/) |
| 语言 | Python 3.8+ |
| 平台 | Windows / macOS / Linux（Flet 跨平台） |

## 项目结构

```
SC-CodeDocGen/
├── main.py                     # 程序入口，初始化 Flet 窗口
├── requirements.txt            # 依赖列表
├── core/                       # 核心业务逻辑
│   ├── scanner.py              # 目录扫描与文件筛选
│   ├── counter.py              # 代码行数统计
│   ├── docx_generator.py       # Word 文档生成（页眉/页脚/正文分页）
│   ├── comment_stripper.py     # 注释去除器
│   └── language_config.py      # 语言后缀、图标、注释规则配置
├── models/                     # 数据模型
│   ├── config.py               # 应用配置数据类 AppConfig
│   └── presets.py              # 预设数据（页码格式、屏蔽目录、默认选项）
├── ui/                         # UI 组件
│   ├── main_view.py            # 主界面整体布局
│   ├── panels/                 # 功能面板
│   │   ├── config_panel.py     # 文档配置面板（页眉/页码/输出）
│   │   ├── options_panel.py    # 选项面板（后缀/屏蔽目录/处理选项）
│   │   ├── code_stats2_panel.py # 统计结果展示
│   │   └── code_file_list_panel.py # 文件列表
│   └── widgets/                # 自定义组件
│       ├── folder_drop_zone.py # 文件夹拖拽/选择区
│       ├── chip_input.py       # Chip 标签输入
│       └── snackbar_util.py    # 提示条工具
├── assets/                     # 静态资源
│   └── language_icons/icons/   # 各语言 SVG 图标（基于 seti-ui）
└── test/                       # 调试与测试脚本（开发时使用）
```

## 快速开始

### 1. 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：

- `flet >= 0.24` — 跨平台 GUI 框架
- `python-docx >= 1.1` — Word 文档生成库

### 3. 运行程序

```bash
python main.py
```

程序启动后将打开一个桌面窗口，默认窗口大小 1280×800（最小 900×600），浅色主题。

## 使用流程

1.  **选择源码目录**：点击「选择文件夹」或直接拖拽目录到左上角区域
2.  **配置筛选条件**（左侧中部）：
    - 勾选需要的代码文件后缀（默认已勾选主流语言）
    - 勾选或自定义需要屏蔽的目录
    - 可选「去除空行」「去除注释」
    - 点击「统计代码」查看有效行数与预估页数
3.  **配置文档输出**（右侧面板）：
    - 填写页眉文字（如：`XXX软件 V1.0 源代码`）
    - 选择页码格式、页码位置、是否显示行号、每页行数
    - 选择输出模式（全部输出 / 前后各 30 页）和输出目录
4.  **点击「生成文档」**：几秒后即可得到标准的 `.docx` 软著代码文档

## 页码格式说明

| 格式 key | 示例 | 说明 |
|----------|------|------|
| `arabic` | `1, 2, 3` | 阿拉伯数字 |
| `dash` | `- 1 -, - 2 -` | 连字符包裹 |
| `emdash` | `—— 1 ——, —— 2 ——` | 全角破折号包裹 |
| `roman` | `Ⅰ, Ⅱ, Ⅲ` | 罗马数字 |
| `page_cn` | `第 1 页, 第 2 页` | 中文带页码 |
| `page_total` | `第 1 页 共 10 页` | 带总页数 |
| `slash` | `1 / 10` | 斜杠分隔 |
| `cn_num` | `第一页, 第二页` | 中文数字 |
| `cn_total` | `第一页 共 10 页` | 中文数字带总页数 |
| `custom` | `自定义模板` | 使用 `{page}` 和 `{total}` 占位符 |

## 文档排版规格

| 项目 | 规格 |
|------|------|
| 纸张 | A4（21 cm × 29.7 cm） |
| 页边距 | 上 2.3 cm / 下 2.3 cm / 左右 3.17 cm |
| 页眉距离 | 1.5 cm |
| 页脚距离 | 1.75 cm |
| 正文字体 | 中文 宋体 五号（10.5 pt），英文 Times New Roman |
| 每页行数 | 默认 50 行，可自定义 |
| 行距 | 根据每页行数自动计算（50 行 ≈ 14.2 pt 固定行距） |
| 文件名 | `软著代码文档_YYYYMMDD_HHMMSS.docx` |

## 支持的语言与后缀

| 分类 | 后缀（语言） |
|------|------|
| 后端主流 | `.py` Python、`.java` Java、`.go` Go、`.php` PHP、`.cs` C#、`.rb` Ruby |
| Web 前端 | `.html` HTML、`.css` CSS、`.scss` SCSS、`.js` JavaScript、`.ts` TypeScript、`.vue` Vue、`.jsx/.tsx` React |
| C/C++ 系统级 | `.c` C、`.cpp` C++、`.h` C Header、`.hpp` C++ Header |
| 移动开发 | `.swift` Swift、`.kt` Kotlin、`.m` Objective-C/MATLAB、`.dart` Dart |
| 其他 | `.rs` Rust、`.sql` SQL、`.sh` Shell |

## 开发说明

### 核心模块说明

-  **`core/scanner.py`** — 递归扫描目录，按后缀过滤，按目录名屏蔽
-  **`core/counter.py`** — 读取文件内容，可选去空行/去注释，返回有效行数与预估页数
-  **`core/docx_generator.py`** — 通过 `python-docx` 严格控制页面布局，插入 Word 域代码实现动态页码 `PAGE` / `NUMPAGES`
-  **`core/comment_stripper.py`** — 基于语言后缀的单行/多行注释去除实现
-  **`core/language_config.py`** — 后缀 → 语言名称 → 图标 → 注释规则的统一映射表

### 添加新语言支持

在 `core/language_config.py` 中同时修改三处即可：

1.  `PRESET_SUFFIXES` — 添加后缀与语言名称
2.  `LANGUAGE_ICONS` — 指定对应图标 SVG（放置于 `assets/language_icons/icons/`）
3.  `get_comment_rules()` — 添加注释规则

## 参考

- [Flet 官方文档](https://flet.dev/docs/)
- [python-docx 文档](https://python-docx.readthedocs.io/)
- 图标来源：[seti-ui](https://github.com/jesseweed/seti-ui/tree/master)

## 许可证

Copyright (c) 2026 — 基于 Python / Flet 开源技术栈开发。
