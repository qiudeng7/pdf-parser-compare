# Docker 运行说明

## 构建镜像

```bash
cd docker

# 构建 marker 镜像
docker compose build marker

# 构建 unstructured 镜像
docker compose build unstructured
```

## 运行容器

### Marker 默认模式

```bash
docker compose run --rm marker

# 在容器内执行转换
marker_single /data/test-pdfs/level-1-markdown.pdf --output_dir /data/results/marker/level-1-markdown
```

### Marker LLM 模式（使用 Kimi）

```bash
# 设置环境变量
export OPENAI_API_KEY="sk-jIT61AX2DKPPUxT892vmlRBSwNjVipYKG5pA9jj1JfkWv2wL"
export OPENAI_BASE_URL="https://api.moonshot.cn/v1"
export OPENAI_MODEL="kimi-k2.6"

docker compose run --rm marker-llm

# 在容器内执行转换
marker_single /data/test-pdfs/level-1-markdown.pdf --use_llm \
  --llm_service marker.services.openai.OpenAIService \
  --output_dir /data/results/marker-llm/level-1-markdown
```

### Unstructured

```bash
docker compose run --rm unstructured

# 在容器内执行转换（不同策略）
# fast 策略
python3 -c "
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf('/data/test-pdfs/level-1-markdown.pdf', strategy='fast')
print('\\n\\n'.join([str(el) for el in elements]))
" > /data/results/unstructured-fast/level-1-markdown.txt

# hi_res 策略
python3 -c "
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf('/data/test-pdfs/level-1-markdown.pdf', strategy='hi_res')
print('\\n\\n'.join([str(el) for el in elements]))
" > /data/results/unstructured-hi-res/level-1-markdown.txt

# ocr_only 策略
python3 -c "
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf('/data/test-pdfs/level-1-markdown.pdf', strategy='ocr_only')
print('\\n\\n'.join([str(el) for el in elements]))
" > /data/results/unstructured-ocr-only/level-1-markdown.txt
```

## 批量处理脚本

见 `scripts/run_all.sh`