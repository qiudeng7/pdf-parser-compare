#!/bin/bash

# 批量处理所有 PDF 文件

set -e

PDFS=(
    "level-1-markdown"
    "level-2-paper"
    "level-3-markdown-picture"
    "level-4-paper-picture"
)

# =====================
# Marker 默认模式
# =====================
echo "Running Marker (default mode)..."

for pdf in "${PDFS[@]}"; do
    echo "Processing $pdf with marker..."
    mkdir -p /data/results/marker/$pdf
    marker_single /data/test-pdfs/${pdf}.pdf --output_dir /data/results/marker/$pdf
done

# =====================
# Marker LLM 模式
# =====================
echo "Running Marker (LLM mode with Kimi)..."

for pdf in "${PDFS[@]}"; do
    echo "Processing $pdf with marker-llm..."
    mkdir -p /data/results/marker-llm/$pdf
    marker_single /data/test-pdfs/${pdf}.pdf --use_llm \
        --llm_service marker.services.openai.OpenAIService \
        --openai_api_key "$OPENAI_API_KEY" \
        --openai_base_url "$OPENAI_BASE_URL" \
        --openai_model "$OPENAI_MODEL" \
        --output_dir /data/results/marker-llm/$pdf
done

# =====================
# Unstructured fast
# =====================
echo "Running Unstructured (fast)..."

for pdf in "${PDFS[@]}"; do
    echo "Processing $pdf with unstructured-fast..."
    mkdir -p /data/results/unstructured-fast/$pdf
    python3 << EOF
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import convert_to_markdown

elements = partition_pdf('/data/test-pdfs/${pdf}.pdf', strategy='fast')
md = convert_to_markdown(elements)
with open('/data/results/unstructured-fast/${pdf}/${pdf}.md', 'w') as f:
    f.write(md)
EOF
done

# =====================
# Unstructured hi_res
# =====================
echo "Running Unstructured (hi_res)..."

for pdf in "${PDFS[@]}"; do
    echo "Processing $pdf with unstructured-hi-res..."
    mkdir -p /data/results/unstructured-hi-res/$pdf
    python3 << EOF
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import convert_to_markdown

elements = partition_pdf('/data/test-pdfs/${pdf}.pdf', strategy='hi_res')
md = convert_to_markdown(elements)
with open('/data/results/unstructured-hi-res/${pdf}/${pdf}.md', 'w') as f:
    f.write(md)
EOF
done

# =====================
# Unstructured ocr_only
# =====================
echo "Running Unstructured (ocr_only)..."

for pdf in "${PDFS[@]}"; do
    echo "Processing $pdf with unstructured-ocr-only..."
    mkdir -p /data/results/unstructured-ocr-only/$pdf
    python3 << EOF
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import convert_to_markdown

elements = partition_pdf('/data/test-pdfs/${pdf}.pdf', strategy='ocr_only')
md = convert_to_markdown(elements)
with open('/data/results/unstructured-ocr-only/${pdf}/${pdf}.md', 'w') as f:
    f.write(md)
EOF
done

echo "All done!"