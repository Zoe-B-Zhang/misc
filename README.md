MISC items
1. # 1_ImageTool - Image Batch Tool 

A lightweight desktop application for batch processing images — perfect for preparing images for web publishing, portfolios, or content protection.

## 🌟 Features

- ✅ **Batch Resize**: Resize images to fit within a max width/height (e.g. 1024×1024 px)
- ✅ **Watermark Support**:
  - 🔤 Add customizable text watermark
  - 🖼️ Add PNG logo watermark (auto-scaled based on image size)
- ✅ **Flexible Options**:
  - Choose to apply resize only, watermark only, or both
  - Select text or logo watermark type
  - Choose output folder freely
- ✅ **Supports common formats**: JPG, JPEG, PNG

## 🖥️ How to Use

1. **Launch** the app (`image_batch_gui.exe`, you can download from build folder directly)
  pyinstaller --onefile --noconsole --icon=bird.ico --add-data "assets;assets" image_batch_gui.py
2. **Select**:
   - Input image folder
   - Output folder
   - Resize and/or watermark options
3. **Click Start** — and the processed images will be saved to the output folder.

## 📦 Packaging Info

- Built with `Python 3.10`
- GUI built using `Tkinter`
- Packaged into `.exe` using [PyInstaller](https://pyinstaller.org)
- Requires no installation (standalone EXE)

## 📁 Assets

- Icon: `bird.ico` (used in `.exe`)
- GUI Title Icon: `bird.gif` (used in window title)
- Optional font: bundled if not using system default

---

2. # 🎨 绘画色彩分析器简介
这是一个功能强大的网页版色彩分析工具，支持单张或批量处理画作，并提供深度定制的分析报告。无论您是专业设计师、艺术家还是色彩爱好者，都能通过它轻松解读画作的色彩语言。

---

## 📁 使用指南

### 1. 操作流程
- **上传图片**：点击“上传图片”按钮，选择一张或多张图片，支持批量分析。
- **调整设置**：
  - 设定单图取色精度：通过滑动条调整每张图片提取的主色数量。
  - 选择取色算法：
    - **K-Means（默认）**：提取画面色彩的“平均值”，结果具有代表性。
    - **中位切分法**：提取画面中“实际存在”的颜色，结果更鲜艳。
  - 忽略背景色：自动忽略占比最高且饱和度最低的颜色，聚焦核心色彩。
- **开始分析**：点击“开始分析”按钮，等待处理完成。
- **导出报告**：点击“导出分析报告”按钮，下载完整 JSON 数据报告。

---

### 2. 报告内容说明

#### 📊 批处理总结报告
- **共通色板**：展示所有图片中的核心颜色，采用六色分区（红、橙、黄、绿、蓝、紫）归类。

#### 🖼 单张图片分析
- **色彩堆栈图**：展示主色调的占比分布。
- **详细信息**：每个主色显示 HEX 值、占比、HSL 值。
- **响应式色轮**：
  - 六色分区分类
  - 点的位置代表色相与饱和度，大小代表占比
  - 可视化颜色分布关系

#### 📈 统计分析报告
- **色彩比例**：总结各色系占比
- **色温分析**：评估画作冷暖倾向
- **饱和度分析**：判断色彩鲜艳度
- **对比度分析**：分析明度与色相对比强度
- **色彩和谐分析**：检测类似色、互补色、三色组等经典配色关系

---

### 3. 背后原理

- **取色原理**：使用 CIELAB 色彩空间进行聚类，更符合人眼感知。
- **颜色分区**：采用六色分区逻辑，符合美术色彩理论。
- **和谐分析**：
  - 类似色：色相相邻
  - 互补色：色相相差约 180°
  - 三色组：色相构成等边三角形

---

© 2025 Bei Zhang — All Rights Reserved.

