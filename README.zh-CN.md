# llama.cpp 中文文档

![llama](https://raw.githubusercontent.com/ggml-org/llama.brand/refs/heads/master/cover/llama-cpp/cover-llama-cpp-dark.svg)

<div align="center">

<b>LLM inference in C/C++ — 中文翻译文档</b>

[![原项目](https://img.shields.io/badge/原项目-ggml-org--llama.cpp-blue?style=flat-square&logo=github)](https://github.com/ggml-org/llama.cpp)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat-square&label=原项目Stars)](https://github.com/ggml-org/llama.cpp/stargazers)
[![微信联系](https://img.shields.io/badge/微信-uaycar-brightgreen?style=flat-square&logo=wechat)](#)

</div>

> 本文档是 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 官方 README 的中文翻译版本，仅供参考，一切以原项目英文文档为准。
>
> **代部署 / 定制服务 / 技术咨询 请添加微信：uaycar**

---

## 项目简介

llama.cpp 的核心目标是：用最少的配置，在从本地到云端的各种硬件上，实现大语言模型（LLM）与视觉语言模型（VLM）的 SOTA 级推理性能。

- 纯 C/C++ 实现，无任何第三方依赖
- Apple Silicon 一等公民支持——通过 ARM NEON、Accelerate 和 Metal 框架深度优化
- x86 架构支持 AVX、AVX2、AVX512 与 AMX
- RISC-V 架构支持 RVV、ZVFH、ZFH、ZICBOP 与 ZIHINTPAUSE
- 提供 1.5-bit、2-bit、3-bit、4-bit、5-bit、6-bit 和 8-bit 整数量化，加快推理并降低内存占用
- 面向 NVIDIA GPU 的定制 CUDA 内核（通过 HIP 支持 AMD GPU，通过 MUSA 支持摩尔线程 GPU）
- Vulkan 与 SYCL 后端支持
- CPU+GPU 混合推理：当模型超出总显存容量时，可部分加速

llama.cpp 构建在 [ggml](https://github.com/ggml-org/ggml) 张量库之上。

## 快速开始

在你的机器上安装 llama.cpp 有以下几种方式：

- 访问 https://llama.app 并按照指引操作
- 使用 Docker 运行——参见原项目 [Docker 文档](https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md)
- 从 [Releases 页面](https://github.com/ggml-org/llama.cpp/releases) 下载预编译二进制
- 克隆本仓库从源码构建——参见[构建指南](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)

安装完成后：

```sh
# 直接从 Hugging Face 下载并运行模型
llama cli -hf ggml-org/Qwen3.5-0.8B-GGUF

# 启动 OpenAI 兼容 API 服务器
llama serve -hf ggml-org/Qwen3.5-0.8B-GGUF
```

`llama cli` 提供交互式终端会话（支持 VLM 多模态），`llama serve` 则附带内置 Web UI，开箱即用。

从源码构建（通用流程）：

```sh
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release -j
```

> 💡 **代部署 / 定制服务 / 技术咨询 请添加微信：uaycar**

## 支持的后端

| 后端 | 目标设备 |
| --- | --- |
| [BLAS](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#blas-build) | 全部 |
| [BLIS](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/BLIS.md) | 全部 |
| [CANN](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#cann) | 华为昇腾 NPU |
| [CUDA](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#cuda) | NVIDIA GPU |
| [HIP](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#hip) | AMD GPU |
| [Hexagon](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/snapdragon/README.md) | 高通骁龙 |
| [IBM zDNN](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/zDNN.md) | IBM Z 与 LinuxONE |
| [MUSA](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#musa) | 摩尔线程 GPU |
| [Metal](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#metal-build) | Apple Silicon |
| [OpenCL](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/OPENCL.md) | Adreno GPU |
| [OpenVINO（开发中）](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/OPENVINO.md) | Intel CPU、GPU 与 NPU |
| [RPC](https://github.com/ggml-org/llama.cpp/tree/master/tools/rpc) | 全部 |
| [SYCL](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/SYCL.md) | Intel GPU |
| [VirtGPU](https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/VirtGPU.md) | VirtGPU APIR |
| [Vulkan](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#vulkan) | GPU |
| [WebGPU](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#webgpu) | 全部 |
| [ZenDNN](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md#zendnn) | AMD CPU |

## 文档与工具

**工具：**

- [cli](https://github.com/ggml-org/llama.cpp/tree/master/tools/cli) — 命令行交互客户端
- [completion](https://github.com/ggml-org/llama.cpp/tree/master/tools/completion) — 补全工具
- [server](https://github.com/ggml-org/llama.cpp/tree/master/tools/server) — OpenAI 兼容 API 服务器
- [GBNF 语法](https://github.com/ggml-org/llama.cpp/tree/master/grammars) — 结构化输出约束

**开发文档：**

- [如何构建](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)
- [Docker 运行](https://github.com/ggml-org/llama.cpp/blob/master/docs/docker.md)
- [Android 构建](https://github.com/ggml-org/llama.cpp/blob/master/docs/android.md)
- [多 GPU 使用](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md)
- [性能排障](https://github.com/ggml-org/llama.cpp/blob/master/docs/development/token_generation_performance_tips.md)
- [模型文档](https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md)

## 参与贡献

- 贡献者可以提交 PR
- 根据贡献情况邀请成为协作者
- Maintainer 可向 `llama.cpp` 仓库分支推送代码，并将 PR 合并进 `master` 分支
- 协助管理 Issue、PR 和项目的工作也非常欢迎！
- 详情请阅读原项目 [CONTRIBUTING.md](https://github.com/ggml-org/llama.cpp/blob/master/CONTRIBUTING.md)

## 致谢

- [yhirose/cpp-httplib](https://github.com/yhirose/cpp-httplib) — 单头文件 HTTP 服务器，`llama-server` 使用 — MIT 许可证
- [nothings/stb](https://github.com/nothings/stb) — 单头文件图像格式解码器，多模态子系统使用 — 公有领域
- [nlohmann/json](https://github.com/nlohmann/json) — 单头文件 JSON 库，多个工具/示例使用 — MIT 许可证
- [mackron/miniaudio](https://github.com/mackron/miniaudio) — 单头文件音频格式解码器，多模态子系统使用 — 公有领域
- [sheredom/subprocess.h](https://github.com/sheredom/subprocess.h) — C/C++ 单头文件进程启动方案 — 公有领域

---

> **代部署 / 定制服务 / 技术咨询 请添加微信：uaycar**

本项目为 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 的中文翻译文档，所有代码版权归原项目作者所有，遵循其原始 MIT 许可证。

**如果觉得有用，请给原项目点个 Star！** ⭐
