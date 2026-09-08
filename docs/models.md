> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# 获取与量化模型

[Hugging Face](https://huggingface.co) 平台托管了[数千个](https://huggingface.co/models?library=gguf&sort=trending)与 `llama.cpp` 兼容的模型:

- [热门趋势](https://huggingface.co/models?library=gguf&sort=trending)

用这个命令行参数即可使用 [Hugging Face](https://huggingface.co/) 上任何 `llama.cpp` 兼容的模型:`-hf <user>/<model>[:quant]`。例如:

```sh
llama cli -hf ggml-org/gemma-3-1b-it-GGUF
```

把 `MODEL_ENDPOINT` 环境变量指向一个与 Hugging Face API 兼容的端点,就能用同一条命令从其他站点下载。
`llama.cpp` 也能直接运行你已下载到本地文件系统的模型。

下载模型后,用 CLI 工具在本地运行它 —— 见下文。

`llama.cpp` 要求模型以 [GGUF](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) 文件格式存储。其他数据格式的模型可以用本仓库的 `convert_*.py` Python 脚本转换成 GGUF。
想深入了解模型量化,[阅读这份文档](../tools/quantize/README.md)。

Hugging Face 平台提供了多种在线工具,用于配合 `llama.cpp` 做模型转换、量化和托管:

- 用 [GGUF-my-repo 空间](https://huggingface.co/spaces/ggml-org/gguf-my-repo)转换 GGUF 格式并把模型权重量化到更小体积
- 用 [GGUF-my-LoRA 空间](https://huggingface.co/spaces/ggml-org/gguf-my-lora)把 LoRA 适配器转换为 GGUF 格式(更多信息:https://github.com/ggml-org/llama.cpp/discussions/10123 )
- 用 [GGUF-editor 空间](https://huggingface.co/spaces/CISCai/gguf-editor)在浏览器里编辑 GGUF 元数据(更多信息:https://github.com/ggml-org/llama.cpp/discussions/9268 )
- 用 [Inference Endpoints](https://ui.endpoints.huggingface.co/)直接在云端托管 `llama.cpp`(更多信息:https://github.com/ggml-org/llama.cpp/discussions/9669 )
