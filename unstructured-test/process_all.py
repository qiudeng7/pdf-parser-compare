#!/usr/bin/env python3
"""
Unstructured PDF 处理脚本
按顺序处理所有级别的 PDF 文件
"""

import os
import re

# 设置 tesseract 语言数据路径
os.environ["TESSDATA_PREFIX"] = "/home/qiudeng/tessdata"

from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_md


def get_title_level(text):
    """从标题文本推断层级"""
    text = text.strip()
    # 匹配数字编号格式：1.  1.1  1.1.1  2.1  等
    import re
    # 匹配开头的数字编号部分
    # "1. " 格式（最后有点号）或 "1.1 " 格式（最后没有点号）
    match = re.match(r'^(\d+(?:\.\d+)*)(?:\.\s|\s)', text)
    if match:
        numbering = match.group(1)  # 如 "1" 或 "1.1" 或 "1.1.1"
        parts = numbering.split('.')
        # 层级：1 -> ##（二级），1.1 -> ###（三级），1.1.1 -> ####（四级）
        return len(parts) + 1
    # 无编号的主标题 -> #（一级）
    return 1


def element_to_md_formatted(e):
    """将单个元素转换为格式化的 markdown"""
    category = e.category
    text = e.text.strip() if e.text else ""

    if category == "Title":
        # 标题：根据编号推断层级
        level = get_title_level(text)
        prefix = "#" * level
        return f"\n{prefix} {text}\n"
    elif category == "SectionHeader":
        return f"\n## {text}\n"
    elif category == "ListItem":
        return f"- {text}"
    elif category == "NarrativeText" or category == "Text" or category == "UncategorizedText":
        return text
    elif category == "Formula":
        # 公式：输出图片引用
        if hasattr(e.metadata, 'image_path') and e.metadata.image_path:
            img_name = os.path.basename(e.metadata.image_path)
            return f"\n![Formula: {img_name}](images/{img_name})\n"
        # 如果没有图片，输出 LaTeX 格式（如果有）
        return f"\n$$ {text} $$\n"
    elif category == "Image":
        # 图片元素：输出图片引用
        if hasattr(e.metadata, 'image_path') and e.metadata.image_path:
            img_name = os.path.basename(e.metadata.image_path)
            return f"\n![{img_name}](images/{img_name})\n"
        return text
    elif category == "Table":
        # 表格：优先用 HTML，否则用图片
        if hasattr(e.metadata, 'text_as_html') and e.metadata.text_as_html:
            return f"\n{e.metadata.text_as_html}\n"
        elif hasattr(e.metadata, 'image_path') and e.metadata.image_path:
            img_name = os.path.basename(e.metadata.image_path)
            return f"\n![Table: {img_name}](images/{img_name})\n"
        return text
    elif category == "FigureCaption":
        return f"\n*{text}*\n"
    elif category == "PageBreak":
        return "\n---\n"
    else:
        return text


def elements_to_md_with_images(elements, images_dir):
    """生成带图片引用的 markdown，保留结构格式"""
    md_parts = []
    for e in elements:
        md_parts.append(element_to_md_formatted(e))
    return "\n".join(md_parts)

BASE_DIR = "/home/qiudeng/pdf-parser-compare"
TEST_PDFS = {
    "level-1-markdown": {
        "path": f"{BASE_DIR}/test-pdfs/level-1-markdown.pdf",
        "languages": ["chi_sim"],  # 中文简体
    },
    "level-2-paper": {
        "path": f"{BASE_DIR}/test-pdfs/level-2-paper-3p.pdf",
        "languages": ["eng"],  # 英文
    },
    "level-3-markdown-picture": {
        "path": f"{BASE_DIR}/test-pdfs/level-3-markdown-picture.pdf",
        "languages": ["chi_sim"],  # 中文简体
    },
    "level-4-paper-picture": {
        "path": f"{BASE_DIR}/test-pdfs/level-4-paper-picture-3p.pdf",
        "languages": ["eng"],  # 英文
    },
}

STRATEGIES = ["fast", "hi_res"]  # ocr_only 需要 poppler-utils，跳过

def process_pdf(name, pdf_info, strategy):
    """处理单个 PDF 文件"""
    pdf_path = pdf_info["path"]
    languages = pdf_info["languages"]

    output_dir = f"{BASE_DIR}/results/unstructured-{strategy}/{name}"
    images_dir = f"{output_dir}/images"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    output_file = f"{output_dir}/{name}.md"

    print(f"Processing {name} with strategy={strategy}, languages={languages}...")

    # hi_res 策略提取图片（包含公式）
    if strategy == "hi_res":
        elements = partition_pdf(
            pdf_path,
            strategy=strategy,
            languages=languages,
            extract_image_block_types=["Image", "Table", "Formula"],
            extract_image_block_output_dir=images_dir,
        )
        md = elements_to_md_with_images(elements, images_dir)
    else:
        elements = partition_pdf(pdf_path, strategy=strategy, languages=languages)
        md = elements_to_md(elements)

    with open(output_file, 'w') as f:
        f.write(md)

    print(f"  Done: {output_file}")

def main():
    for strategy in STRATEGIES:
        print(f"\n=== Strategy: {strategy} ===")
        for name, pdf_info in TEST_PDFS.items():
            process_pdf(name, pdf_info, strategy)

if __name__ == "__main__":
    main()