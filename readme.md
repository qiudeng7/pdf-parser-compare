# PDF Parser Comparison

对比各 PDF 转 Markdown 工具的效果。

## 用于测试的 pdf (测试集)

本测试集包含四个难度层级的 PDF 文件，位于`test-pdfs` 目录下，用于评估解析工具在不同场景下的表现。

| 级别 | 文件名 | 难度 | 描述 |
|------|--------|------|------|
| Level 1 | `level-1-markdown.pdf` | 简单 | 由 Markdown 文档转换生成的 PDF |
| Level 2 | `level-2-paper.pdf` | 中等 | 从 arXiv 下载的学术论文 PDF |
| Level 3 | `level-3-markdown-picture.pdf` | 困难 | 与 Level 1 内容相同，但每页为截图形式 |
| Level 4 | `level-4-paper-picture.pdf` | 最困难 | 与 Level 2 内容相同，但每页为截图形式 |

### 难度说明

**Level 1 - Markdown 生成的 PDF**

- 来源：Markdown 文档导出
- 特点：文本层清晰、格式规范、无复杂排版
- 测试重点：基础文本提取、格式还原

**Level 2 - arXiv 论文**

- 来源：arXiv 学术论文
- 特点：包含数学公式、图表、引用、多栏布局
- 测试重点：复杂排版处理、公式识别、表格提取

**Level 3 - Markdown 截图版**

- 内容：与 Level 1 相同
- 形式：每页转换为图片后拼接
- 特点：无文本层，需依赖 OCR
- 测试重点：OCR 准确性、格式还原（有参照对比）

**Level 4 - 论文截图版**

- 内容：与 Level 2 相同
- 形式：每页转换为图片后拼接
- 特点：无文本层、内容复杂、需 OCR
- 测试重点：复杂内容的 OCR 能力、公式图表识别


## 测试结果

各工具的转换结果存放在 `results/` 目录下, 测试环境为 3070ti laptop, 8G 显存 + 32G 运行内存, 系统环境为 wsl.

### 目录结构

```
results/
└── {工具名称}/
    └── {测试级别}/
        ├── {pdf文件名}.md    # 转换后的 Markdown 文件
        └── images/           # 提取的图片资源
```

### 已测试工具

| 工具 | 说明 |
|------|------|
| doc2x | 付费 api, 闭源模型, 10 块钱可以处理 500 页 pdf |
| marker | 开源本地转换工具，支持 LLM 增强 |
| unstructured-fast | Unstructured 快速模式，直接提取文本 |
| unstructured-hi_res | Unstructured 高精度模式，布局分析+图片提取 |

未成功的对比项:
- **unstructured-ocr_only**：部署时遇到环境问题（poppler-utils依赖），暂时未成功运行测试
- **marker-llm**：理论上可提高质量，但部署遇到网络问题（未测试成功）


## 测试总结

所有的对比项的结果都在仓库中可以查看, 下面是我的主观评价, 具体效果可以自己查看 markdown.

### 运行速度

1. marker 最慢, 五分钟到十分钟
2. unstructured 的 hires 模式 (high resolution) 和 doc2x 速度差不多, 三十秒到一分钟
3. unstructured 的 fast 模式最快，十秒以内, 但是效果几乎不可用.

### 处理结果

#### Level 1 - Markdown PDF

所有工具都能正确处理文字, 但是格式不一定.

| 工具 | 对比 |
|------|------|
| **marker** | 能处理粗体字和多级列表 |
| **doc2x** | 不能识别粗体和多级列表 |
| **unstructured** | 与 doc2x 相近，不能识别粗体和嵌套列表 |


#### Level 2 - 学术论文

| 工具 | 评价 |
|------|------|
| **marker** | 排版处理最符合直觉，优于 doc2x；可以正确公式转换latex |
| **doc2x** | 少量段落排版错位; 可以正确公式 转换 latex |
| **unstructured** | 会将连续段落合并; 无公式 LaTeX 转换能力（仅提取图片）, 但可以外接其他工具搭配使用. |

**主观排版能力排序**：marker > unstructured > doc2x

#### Level 3 - Markdown 截图（中文 OCR）

| 工具 | 评价 |
|------|------|
| **doc2x** | 相比 level 1 几乎无质量下降，OCR 中文能力强 |
| **marker** | 相比 Level 1 有质量下降，纯图片中文处理不如 doc2x |
| **unstructured** | 相比 Level 1 有质量下降，同上 |

结果说明对于中文纯图片 pdf, 只有 doc2x 的效果比较理想.

#### Level 4 - 论文截图（英文 OCR）

| 工具 | 评价 |
|------|------|
| **marker** | 相比 Level 2 几乎无质量下降，纯图片英文处理能力强 |
| **doc2x** | 与 Level 2 结果一致 |
| **unstructured** | 相比 Level 2 几乎无质量下降 |

结果说明开源的 marker 和 unstructured 其实也有不错的 ocr 能力, 只是对中文效果一般.

### 总结

| 特性 | doc2x | marker | unstructured |
|------|-------|--------|--------------|
| 公式处理 | LaTeX 文字 | LaTeX 文字 | 图片提取 |
| 输出定制 | 无 | 无 | 需自定义 |
| 中文 OCR | 优秀 | 较弱 | 较弱 |
| 英文 OCR | 优秀 | 良好 | 良好 |
| 排版还原 | 一般 | 优秀 | 较好 |
| 速度 | 中等 | 慢 | 快 |

**总体最优**：unstructured 在速度、质量、成本方面综合最优。

实际应用推荐混合方案: 大部分 pdf 可以用 unstructured 开源版的 hi_res 模式; 中文扫描件使用 doc2x; 复杂排版用 marker; 如果需要极快处理且对质量要求不高, 用 unstructured 的 fast 模式; 理论上 marker 使用 llm 增强可以处理的更好.
