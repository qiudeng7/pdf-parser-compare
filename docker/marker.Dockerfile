FROM nvidia/cuda:12.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TORCH_DEVICE=cuda

# 系统依赖
RUN apt-get update && apt-get install -y \
    python3.10 python3-pip python3.10-venv \
    tesseract-ocr poppler-utils libmagic1 \
    git wget curl \
    && rm -rf /var/lib/apt/lists/*

# Tesseract 语言数据
RUN apt-get update && apt-get install -y tesseract-ocr-eng tesseract-ocr-chi-sim && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 marker
RUN pip3 install marker-pdf

# 预下载模型（首次运行时会自动下载，这里预先下载以节省时间）
RUN python3 -c "from marker.models import create_model_dict; create_model_dict()"

CMD ["/bin/bash"]