> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# 多模态(Multimodal)

llama.cpp 通过 `libmtmd` 支持多模态输入。目前有以下工具支持该功能:
- [llama-cli](../tools/cli/README.md)
- [llama-server](../tools/server/README.md),通过 OpenAI 兼容的 `/chat/completions` API
- [llama-mtmd-cli](../tools/mtmd/README.md),用于测试与开发

当前支持**图像**、**音频**和**视频**输入。

启用方式有以下 2 种:

- 对受支持的模型使用 `-hf` 选项(预量化模型列表见下文)
    - 使用 `-hf` 加载模型但禁用多模态:`--no-mmproj`
    - 使用 `-hf` 加载模型但指定自定义 mmproj 文件:`--mmproj local_file.gguf`
- 使用 `-m model.gguf` 搭配 `--mmproj file.gguf`,分别指定文本模型和多模态投影器

默认情况下,多模态投影器会被卸载(offload)到 GPU。若要禁用,加 `--no-mmproj-offload`。

例如:

```sh
# CLI 简单用法
llama-mtmd-cli -hf ggml-org/gemma-3-4b-it-GGUF

# server 简单用法
llama-server -hf ggml-org/gemma-3-4b-it-GGUF

# 使用本地文件
llama-server -m gemma-3-4b-it-Q4_K_M.gguf --mmproj mmproj-gemma-3-4b-it-Q4_K_M.gguf

# 不卸载到 GPU
llama-server -hf ggml-org/gemma-3-4b-it-GGUF --no-mmproj-offload
```

> [!IMPORTANT]
>
> OCR 模型使用特定的提示词和输入结构训练,更多信息请参考以下讨论:
> - PaddleOCR-VL: https://github.com/ggml-org/llama.cpp/pull/18825
> - GLM-OCR: https://github.com/ggml-org/llama.cpp/pull/19677
> - Deepseek-OCR: https://github.com/ggml-org/llama.cpp/pull/17400
> - Dots.OCR: https://github.com/ggml-org/llama.cpp/pull/17575
> - HunyuanOCR: https://github.com/ggml-org/llama.cpp/pull/21395

## 预量化模型

以下是开箱即用的模型,大部分默认带 `Q4_K_M` 量化。可在 ggml-org 的 Hugging Face 主页找到:https://huggingface.co/collections/ggml-org/multimodal-ggufs-68244e01ff1f39e5bebeeedc

把 `(tool_name)` 替换成你想用的二进制名称,例如 `llama-mtmd-cli` 或 `llama-server`。

注意:部分模型可能需要较大的上下文窗口,例如 `-c 8192`。

**视觉模型**:

```sh
# Gemma 3
(tool_name) -hf ggml-org/gemma-3-4b-it-GGUF
(tool_name) -hf ggml-org/gemma-3-12b-it-GGUF
(tool_name) -hf ggml-org/gemma-3-27b-it-GGUF

# SmolVLM
(tool_name) -hf ggml-org/SmolVLM-Instruct-GGUF
(tool_name) -hf ggml-org/SmolVLM-256M-Instruct-GGUF
(tool_name) -hf ggml-org/SmolVLM-500M-Instruct-GGUF
(tool_name) -hf ggml-org/SmolVLM2-2.2B-Instruct-GGUF
(tool_name) -hf ggml-org/SmolVLM2-256M-Video-Instruct-GGUF
(tool_name) -hf ggml-org/SmolVLM2-500M-Video-Instruct-GGUF

# Pixtral 12B
(tool_name) -hf ggml-org/pixtral-12b-GGUF

# Qwen 2 VL
(tool_name) -hf ggml-org/Qwen2-VL-2B-Instruct-GGUF
(tool_name) -hf ggml-org/Qwen2-VL-7B-Instruct-GGUF

# Qwen 2.5 VL
(tool_name) -hf ggml-org/Qwen2.5-VL-3B-Instruct-GGUF
(tool_name) -hf ggml-org/Qwen2.5-VL-7B-Instruct-GGUF
(tool_name) -hf ggml-org/Qwen2.5-VL-32B-Instruct-GGUF
(tool_name) -hf ggml-org/Qwen2.5-VL-72B-Instruct-GGUF

# Mistral Small 3.1 24B(IQ2_M 量化)
(tool_name) -hf ggml-org/Mistral-Small-3.1-24B-Instruct-2503-GGUF

# InternVL 2.5 与 3
(tool_name) -hf ggml-org/InternVL2_5-1B-GGUF
(tool_name) -hf ggml-org/InternVL2_5-4B-GGUF
(tool_name) -hf ggml-org/InternVL3-1B-Instruct-GGUF
(tool_name) -hf ggml-org/InternVL3-2B-Instruct-GGUF
(tool_name) -hf ggml-org/InternVL3-8B-Instruct-GGUF
(tool_name) -hf ggml-org/InternVL3-14B-Instruct-GGUF

# Llama 4 Scout
(tool_name) -hf ggml-org/Llama-4-Scout-17B-16E-Instruct-GGUF

# Moondream2 20250414 版本
(tool_name) -hf ggml-org/moondream2-20250414-GGUF

# Gemma 4
(tool_name) -hf ggml-org/gemma-4-E2B-it-GGUF
(tool_name) -hf ggml-org/gemma-4-E4B-it-GGUF
(tool_name) -hf ggml-org/gemma-4-26B-A4B-it-GGUF
(tool_name) -hf ggml-org/gemma-4-31B-it-GGUF
```

**音频模型**:

```sh
# Ultravox 0.5
(tool_name) -hf ggml-org/ultravox-v0_5-llama-3_2-1b-GGUF
(tool_name) -hf ggml-org/ultravox-v0_5-llama-3_1-8b-GGUF

# Qwen2-Audio 与 SeaLLM-Audio
# 注意:这两个模型没有预量化 GGUF,因为效果非常差
# 参考:https://github.com/ggml-org/llama.cpp/pull/13760

# Mistral 的 Voxtral
(tool_name) -hf ggml-org/Voxtral-Mini-3B-2507-GGUF

# Qwen3-ASR
(tool_name) -hf ggml-org/Qwen3-ASR-0.6B-GGUF
(tool_name) -hf ggml-org/Qwen3-ASR-1.7B-GGUF
```

**混合模态**:

```sh
# Qwen2.5 Omni
# 能力:音频输入、视觉输入
(tool_name) -hf ggml-org/Qwen2.5-Omni-3B-GGUF
(tool_name) -hf ggml-org/Qwen2.5-Omni-7B-GGUF

# Qwen3 Omni
# 能力:音频输入、视觉输入
(tool_name) -hf ggml-org/Qwen3-Omni-30B-A3B-Instruct-GGUF
(tool_name) -hf ggml-org/Qwen3-Omni-30B-A3B-Thinking-GGUF

# Gemma 4
# 能力:音频输入、视觉输入
(tool_name) -hf ggml-org/gemma-4-E2B-it-GGUF
(tool_name) -hf ggml-org/gemma-4-E4B-it-GGUF
```

## 寻找更多模型

Hugging Face 上具备视觉能力的 GGUF 模型可以在这里找:https://huggingface.co/models?pipeline_tag=image-text-to-text&sort=trending&search=gguf
