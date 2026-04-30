FROM nvidia/cuda:12.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# 系统依赖
RUN apt-get update && apt-get install -y \
    python3.11 python3-pip python3.11-venv \
    tesseract-ocr poppler-utils libmagic1 \
    git wget curl \
    && rm -rf /var/lib/apt/lists/*

# Tesseract 语言数据
RUN apt-get update && apt-get install -y tesseract-ocr-eng tesseract-ocr-chi-sim && rm -rf /var/lib/apt/lists/*

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

WORKDIR /app

# 安装 unstructured (包含 pdf 和 huggingface 支持)
RUN pip3 install "unstructured[pdf,huggingface]"

# 预下载模型
RUN python3 -c "from unstructured.partition.model_init import initialize; initialize()"

CMD ["/bin/bash"]