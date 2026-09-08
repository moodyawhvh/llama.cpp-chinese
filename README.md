<div align="center">

# llama.cpp 中文翻译版

**[中文版] llama.cpp — 高性能大语言模型本地推理框架，纯 C/C++ 实现无依赖，支持量化与多硬件后端加速**

[![原项目](https://img.shields.io/badge/原项目-ggml-org--llama.cpp-blue?style=flat-square&logo=github)](https://github.com/ggml-org/llama.cpp)
[![中文文档](https://img.shields.io/badge/中文文档-README.zh--CN.md-orange?style=flat-square)](README.zh-CN.md)
[![GitHub Stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat-square&label=原项目Stars)](https://github.com/ggml-org/llama.cpp/stargazers)
[![微信联系](https://img.shields.io/badge/微信-uaycar-brightgreen?style=flat-square&logo=wechat)](#)

</div>

---

> 这是 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 的中文翻译版本。
> 完整源代码请访问原项目：https://github.com/ggml-org/llama.cpp

**代部署 / 定制服务 / 技术咨询 请添加微信：uaycar**

---

## 📖 项目简介

llama.cpp 是由 ggml-org 维护的开源大语言模型（LLM/VLM）推理框架，目标是在最少配置的前提下，于本地和云端的各种硬件上实现最先进的推理性能。项目采用纯 C/C++ 编写、零依赖，基于自研的 ggml 张量库构建，从树莓派到 Apple Silicon、从 NVIDIA/AMD GPU 到昇腾、摩尔线程等国产算力都能跑。配合 1.5~8 bit 整数量化技术，普通消费级设备也能流畅运行数十亿参数的大模型。

## ✨ 主要特性

- **零依赖纯 C/C++ 实现**，编译简单，跨平台部署无负担
- **Apple Silicon 一等公民**：针对 ARM NEON、Accelerate 与 Metal 深度优化
- **x86 全面加速**：支持 AVX、AVX2、AVX512 与 AMX 指令集
- **RISC-V 支持**：RVV、ZVFH、ZFH 等向量扩展
- **1.5/2/3/4/5/6/8 bit 整数量化**：大幅降低显存占用、提升推理速度
- **NVIDIA GPU 专用 CUDA 内核**，并通过 HIP 支持 AMD GPU、通过 MUSA 支持摩尔线程 GPU
- **Vulkan 与 SYCL 后端**，覆盖 Intel GPU 等更多硬件
- **CPU+GPU 混合推理**：显存不够时可将部分层放到内存，跑超显存容量的大模型
- **丰富后端矩阵**：CUDA / Metal / Vulkan / SYCL / OpenVINO / CANN / OpenCL / WebGPU 等十余种
- **内置 llama-server**：一行命令启动 OpenAI 兼容 API 与 Web UI

## 📁 文件说明

| 文件 | 说明 |
|:-----|:-----|
| README.md | 本文件（中文简介） |
| README.zh-CN.md | 详细中文文档（完整汉化） |

## 🚀 快速开始

安装 llama.cpp 的几种方式（任选其一）：

1. 访问 https://llama.app 按页面指引安装
2. 使用 Docker 运行（详见原项目 `docs/docker.md`）
3. 从 [Releases 页面](https://github.com/ggml-org/llama.cpp/releases) 下载预编译二进制
4. 克隆仓库从源码构建（详见原项目 `docs/build.md`）

安装完成后，直接从 Hugging Face 拉取模型运行：

```sh
# 直接从 Hugging Face 下载并运行模型
llama cli -hf ggml-org/Qwen3.5-0.8B-GGUF

# 启动 OpenAI 兼容 API 服务器
llama serve -hf ggml-org/Qwen3.5-0.8B-GGUF
```

从源码构建的典型流程（Linux/macOS）：

```sh
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release -j
```

完整源代码与最新版本请访问原项目：https://github.com/ggml-org/llama.cpp

## 📞 联系方式

**代部署 / 定制服务 / 技术咨询 请添加微信：uaycar**

---

本项目为 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 的中文翻译版本，所有代码版权归原项目作者所有，遵循其原始许可证（MIT）。

**如果觉得有用，请给原项目点个 Star！** ⭐
