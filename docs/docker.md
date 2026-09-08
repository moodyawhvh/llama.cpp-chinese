> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# Docker

## 前置条件
* 系统中必须已安装并运行 Docker。
* 创建一个用于存放大型模型与中间文件的目录(例如 /llama/models)。

## 镜像
本项目提供三个 Docker 镜像:

1. `ghcr.io/ggml-org/llama.cpp:full`:包含 `llama-cli`、`llama-completion` 可执行文件,以及把 LLaMA 模型转换为 ggml 并做 4-bit 量化的工具。(平台:`linux/amd64`、`linux/arm64`、`linux/s390x`)
2. `ghcr.io/ggml-org/llama.cpp:light`:仅包含 `llama-cli` 和 `llama-completion` 可执行文件。(平台:`linux/amd64`、`linux/arm64`、`linux/s390x`)
3. `ghcr.io/ggml-org/llama.cpp:server`:仅包含 `llama-server` 可执行文件。(平台:`linux/amd64`、`linux/arm64`、`linux/s390x`)

此外还有以下镜像,与上面类似:

- `ghcr.io/ggml-org/llama.cpp:full-cuda`:同 `full`,但编译了 CUDA 12 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:full-cuda13`:同 `full`,但编译了 CUDA 13 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:light-cuda`:同 `light`,但编译了 CUDA 12 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:light-cuda13`:同 `light`,但编译了 CUDA 13 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:server-cuda`:同 `server`,但编译了 CUDA 12 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:server-cuda13`:同 `server`,但编译了 CUDA 13 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:full-rocm`:同 `full`,但编译了 ROCm 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:light-rocm`:同 `light`,但编译了 ROCm 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:server-rocm`:同 `server`,但编译了 ROCm 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:full-musa`:同 `full`,但编译了 MUSA 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:light-musa`:同 `light`,但编译了 MUSA 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:server-musa`:同 `server`,但编译了 MUSA 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:full-intel`:同 `full`,但编译了 SYCL 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:light-intel`:同 `light`,但编译了 SYCL 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:server-intel`:同 `server`,但编译了 SYCL 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:full-vulkan`:同 `full`,但编译了 Vulkan 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:light-vulkan`:同 `light`,但编译了 Vulkan 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:server-vulkan`:同 `server`,但编译了 Vulkan 支持。(平台:`linux/amd64`、`linux/arm64`)
- `ghcr.io/ggml-org/llama.cpp:full-openvino`:同 `full`,但编译了 OpenVino 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:light-openvino`:同 `light`,但编译了 OpenVino 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:server-openvino`:同 `server`,但编译了 OpenVino 支持。(平台:`linux/amd64`)
- `ghcr.io/ggml-org/llama.cpp:full-s390x`:与 `full` 完全相同,是 `s390x` 平台的别名。(平台:`linux/s390x`)
- `ghcr.io/ggml-org/llama.cpp:light-s390x`:与 `light` 完全相同,是 `s390x` 平台的别名。(平台:`linux/s390x`)
- `ghcr.io/ggml-org/llama.cpp:server-s390x`:与 `server` 完全相同,是 `s390x` 平台的别名。(平台:`linux/s390x`)

GPU 版镜像目前 CI 只验证能构建,不做进一步测试。它们与 [.devops/](../.devops/) 中定义的 Dockerfile 以及 [.github/workflows/docker.yml](../.github/workflows/docker.yml) 中定义的 GitHub Action 构建产物完全一致,没有任何差异。如果你需要不同的配置(例如不同版本的 CUDA、ROCm 或 MUSA 库),目前需要自己在本地构建镜像。

## 用法

下载模型、转换为 ggml 并做优化的最简单方式,是使用 `--all-in-one` 一体化命令,它包含在 full 镜像中。

把下面的 `/path/to/models` 替换为你下载模型的实际路径。

```bash
docker run -v /path/to/models:/models ghcr.io/ggml-org/llama.cpp:full --all-in-one "/models/" 7B
```

跑完之后就可以直接玩了!

```bash
docker run -v /path/to/models:/models ghcr.io/ggml-org/llama.cpp:full --run -m /models/7B/ggml-model-q4_0.gguf
docker run -v /path/to/models:/models ghcr.io/ggml-org/llama.cpp:full --run-legacy -m /models/32B/ggml-model-q8_0.gguf -no-cnv -p "Building a mobile app can be done in 15 steps:" -n 512
```

或者用 light 镜像:

```bash
docker run -v /path/to/models:/models --entrypoint /app/llama-cli ghcr.io/ggml-org/llama.cpp:light -m /models/7B/ggml-model-q4_0.gguf
docker run -v /path/to/models:/models --entrypoint /app/llama-completion ghcr.io/ggml-org/llama.cpp:light -m /models/32B/ggml-model-q8_0.gguf -no-cnv -p "Building a mobile app can be done in 15 steps:" -n 512
```

或者用 server 镜像:

```bash
docker run -v /path/to/models:/models -p 8080:8080 ghcr.io/ggml-org/llama.cpp:server -m /models/7B/ggml-model-q4_0.gguf --port 8080 --host 0.0.0.0 -n 512
```

上面的示例中,为了说明清楚而显式写了 `--entrypoint /app/llama-cli`,实际上可以安全地省略,因为它是容器的默认入口。

## CUDA 版 Docker

假设你已在 Linux 上正确安装 [nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-container-toolkit),或使用带 GPU 的云主机,容器内即可访问 `cuBLAS`。

## 本地构建 Docker 镜像

```bash
docker build -t local/llama.cpp:full-cuda --target full -f .devops/cuda.Dockerfile .
docker build -t local/llama.cpp:light-cuda --target light -f .devops/cuda.Dockerfile .
docker build -t local/llama.cpp:server-cuda --target server -f .devops/cuda.Dockerfile .
```

根据容器宿主机支持的 CUDA 环境以及 GPU 架构,你可能需要传入不同的 `ARGS`。

默认值为:

- `CUDA_VERSION` 设为 `12.8.1`
- `CUDA_DOCKER_ARCH` 设为 cmake 构建默认值,涵盖所有受支持的架构

构建出的镜像与非 CUDA 版本基本一致:

1. `local/llama.cpp:full-cuda`:包含 `llama-cli`、`llama-completion` 可执行文件,以及把 LLaMA 模型转换为 ggml 并做 4-bit 量化的工具。
2. `local/llama.cpp:light-cuda`:仅包含 `llama-cli` 和 `llama-completion` 可执行文件。
3. `local/llama.cpp:server-cuda`:仅包含 `llama-server` 可执行文件。

## 用法

本地构建完成后,用法与非 CUDA 示例类似,但需要加 `--gpus` 参数,同时建议使用 `--n-gpu-layers` 参数。

```bash
docker run --gpus all -v /path/to/models:/models local/llama.cpp:full-cuda --run -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512 --n-gpu-layers 1
docker run --gpus all -v /path/to/models:/models local/llama.cpp:light-cuda -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512 --n-gpu-layers 1
docker run --gpus all -v /path/to/models:/models local/llama.cpp:server-cuda -m /models/7B/ggml-model-q4_0.gguf --port 8080 --host 0.0.0.0 -n 512 --n-gpu-layers 1
```

## MUSA 版 Docker

假设你已在 Linux 上正确安装 [mt-container-toolkit](https://developer.mthreads.com/musa/native),容器内即可访问 `muBLAS`。

## 本地构建 Docker 镜像

```bash
docker build -t local/llama.cpp:full-musa --target full -f .devops/musa.Dockerfile .
docker build -t local/llama.cpp:light-musa --target light -f .devops/musa.Dockerfile .
docker build -t local/llama.cpp:server-musa --target server -f .devops/musa.Dockerfile .
```

根据容器宿主机支持的 MUSA 环境以及 GPU 架构,你可能需要传入不同的 `ARGS`。

默认值为:

- `MUSA_VERSION` 设为 `rc4.3.0`

构建出的镜像与非 MUSA 版本基本一致:

1. `local/llama.cpp:full-musa`:包含 `llama-cli`、`llama-completion` 可执行文件,以及把 LLaMA 模型转换为 ggml 并做 4-bit 量化的工具。
2. `local/llama.cpp:light-musa`:仅包含 `llama-cli` 和 `llama-completion` 可执行文件。
3. `local/llama.cpp:server-musa`:仅包含 `llama-server` 可执行文件。

## 用法

本地构建完成后,用法与非 MUSA 示例类似,但需要把 `mthreads` 设为默认 Docker runtime。可以在宿主机上执行 `(cd /usr/bin/musa && sudo ./docker setup $PWD)` 完成设置,再用 `docker info | grep mthreads` 验证改动是否生效。同时建议使用 `--n-gpu-layers` 参数。

```bash
docker run -v /path/to/models:/models local/llama.cpp:full-musa --run -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512 --n-gpu-layers 1
docker run -v /path/to/models:/models local/llama.cpp:light-musa -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512 --n-gpu-layers 1
docker run -v /path/to/models:/models local/llama.cpp:server-musa -m /models/7B/ggml-model-q4_0.gguf --port 8080 --host 0.0.0.0 -n 512 --n-gpu-layers 1
```

## SYCL 版 Docker

## 本地构建 Docker 镜像

```bash
docker build -t local/llama.cpp:full-intel --target full -f .devops/intel.Dockerfile .
docker build -t local/llama.cpp:light-intel --target light -f .devops/intel.Dockerfile .
docker build -t local/llama.cpp:server-intel --target server -f .devops/intel.Dockerfile .
```

根据容器宿主机支持的 SYCL 环境以及 GPU 架构,你可能需要传入不同的 `ARGS`。
可用的 `ARGS` 及其默认值见 [.devops/intel.Dockerfile](../.devops/intel.Dockerfile)。

构建出的镜像与非 SYCL 版本基本一致:

1. `local/llama.cpp:full-intel`:包含 `llama-cli`、`llama-completion` 可执行文件,以及把 LLaMA 模型转换为 ggml 并做 4-bit 量化的工具。
2. `local/llama.cpp:light-intel`:仅包含 `llama-cli` 和 `llama-completion` 可执行文件。
3. `local/llama.cpp:server-intel`:仅包含 `llama-server` 可执行文件。

## 用法

本地构建完成后,用法与非 SYCL 示例类似,但需要加 `--device` 参数。

```bash
# 先找到所有 DRI 显卡设备
ls -la /dev/dri
# 然后选择你要用的卡(这里以 /dev/dri/card0 为例)。
docker run --device /dev/dri/renderD128:/dev/dri/renderD128 --device /dev/dri/card0:/dev/dri/card0 -v /path/to/models:/models local/llama.cpp:full-intel -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512 --n-gpu-layers 99
docker run --device /dev/dri/renderD128:/dev/dri/renderD128 --device /dev/dri/card0:/dev/dri/card0 -v /path/to/models:/models local/llama.cpp:light-intel -m /models/7B/ggml-model-q4_0.gguf -p "Building a website can be done in 10 simple steps:" -n 512 --n-gpu-layers 99
docker run --device /dev/dri/renderD128:/dev/dri/renderD128 --device /dev/dri/card0:/dev/dri/card0 -v /path/to/models:/models local/llama.cpp:server-intel -m /models/7B/ggml-model-q4_0.gguf --port 8080 --host 0.0.0.0 -n 512 --n-gpu-layers 99
```

*注意:*
- Docker 已在原生 Linux 上测试通过。WSL 支持尚未验证。
- 可能需要在**宿主机**上安装 Intel GPU 驱动 *(详情请参考 [Linux 配置](./backend/SYCL.md#linux))*。
