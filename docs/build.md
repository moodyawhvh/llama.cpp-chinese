> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。
>
> 📝 注:原文超过 10000 字符,本译文覆盖核心构建章节,个别小众平台的冗长细节有精简,完整内容以英文原版为准。

# 本地构建 llama.cpp

本项目的主要产物是 `llama` 库。其 C 风格接口见 [include/llama.h](../include/llama.h)。

项目还包含许多使用 `llama` 库的示例程序和工具,从简单的最小代码片段,到复杂的子项目(如 OpenAI 兼容的 HTTP server)。

**获取代码:**

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
```

以下各节介绍如何使用不同后端和选项进行构建。

* [CPU 构建](#cpu-构建)
* [BLAS 构建](#blas-构建)
* [Metal 构建](#metal-构建)
* [SYCL](#sycl)
* [CUDA](#cuda)
* [MUSA](#musa)
* [HIP](#hip)
* [Vulkan](#vulkan)
* [CANN](#cann)
* [ZenDNN](#zendnn)
* [Arm® KleidiAI™](#arm-kleidiai)
* [OpenCL](#opencl)
* [Android](#android)
* [OpenVINO](#openvino)
* [Hexagon](#hexagon)
* [关于 GPU 加速后端的说明](#关于-gpu-加速后端的说明)

## CPU 构建

使用 `CMake` 构建 llama.cpp:

```bash
cmake -B build
cmake --build build --config Release
```

**注意**:

- 想编译更快,加 `-j` 参数并行执行多个任务,或使用 Ninja 这类自动并行的生成器。例如 `cmake --build build --config Release -j 8` 会并行跑 8 个任务。
- 想让重复编译更快,安装 [ccache](https://ccache.dev/)。
- Debug 构建分两种情况:

    1. 单配置生成器(如默认的 `Unix Makefiles`;注意它们会直接忽略 `--config` 参数):

       ```bash
       cmake -B build -DCMAKE_BUILD_TYPE=Debug
       cmake --build build
       ```

    2. 多配置生成器(`-G` 参数设为 Visual Studio、XCode 等):

       ```bash
       cmake -B build -G "Xcode"
       cmake --build build --config Debug
       ```

    更多细节和支持的生成器列表,见 [CMake 文档](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html)。
- 静态构建,加 `-DBUILD_SHARED_LIBS=OFF`:
  ```
  cmake -B build -DBUILD_SHARED_LIBS=OFF
  cmake --build build --config Release
  ```

- 在 Windows(x86、x64、arm64)上用 MSVC 或 clang 作为编译器构建:
    - 安装 Visual Studio 2022,例如[社区版](https://visualstudio.microsoft.com/vs/community/)。安装器中至少勾选以下选项(会自动装上 CMake 等所需工具):
    - "工作负荷"页:使用 C++ 的桌面开发
    - "单个组件"页(可用搜索快速定位):适用于 Windows 的 C++_CMake_ 工具、适用于 Windows 的 _Git_、适用于 Windows 的 C++_Clang_ 编译器、LLVM 工具集的 MS-Build 支持(clang)
    - 记住:git、构建、测试请始终在适用于 VS2022 的开发人员命令提示符 / PowerShell 中进行
    - Windows on ARM(arm64、WoA)构建:
      ```bash
      cmake --preset arm64-windows-llvm-release -D GGML_OPENMP_FETCH=ON
      cmake --build build-arm64-windows-llvm-release
      ```
      - 在 ARM64 机器上构建请使用 `ARM64 Native Tools Command Prompt for VS 2022`。
      - `GGML_OPENMP_FETCH` 会下载官方 LLVM OpenMP 运行时,配置阶段需要 Clang、7-Zip 和网络。CMake 会按目标架构选择运行时,因此从 x64 交叉编译 WoA 时同样可用。解压出的头文件、导入库、DLL 和 OpenMP 许可证放在 `build/_deps` 下,构建会把 `libomp.dll` 和 `LICENSE-LLVM-OpenMP` 复制到运行时输出目录并一并安装。不传该选项则走 CMake 常规 OpenMP 探测,或传 `-D GGML_OPENMP=OFF` 直接禁用 OpenMP。
    - 使用 ninja 生成器 + clang 编译器为默认组合构建:
      - 设置路径:
        ```
        set LIB=C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\um\x64;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.41.34120\lib\x64\uwp;C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\ucrt\x64
        ```
      - 执行:
        ```bash
        cmake --preset x64-windows-llvm-release
        cmake --build build-x64-windows-llvm-release
        ```
- 如果需要 HTTPS/TLS 功能,可安装 OpenSSL 开发库。未安装时项目也能正常构建运行,只是不带 SSL 支持。
  - **Debian / Ubuntu:** `sudo apt-get install libssl-dev`
  - **Fedora / RHEL / Rocky / Alma:** `sudo dnf install openssl-devel`
  - **Arch / Manjaro:** `sudo pacman -S openssl`

## BLAS 构建

带 BLAS 支持构建,可在批量大于 32 的 prompt 处理(默认 512)上获得一定性能提升。BLAS 不影响生成性能。目前有多种 BLAS 实现可选:

### Accelerate Framework

仅 Mac 可用,默认启用,按常规方式构建即可。

### OpenBLAS

仅用 CPU 提供 BLAS 加速。确保机器上已安装 OpenBLAS。

- Linux 上使用 `CMake`:

    ```bash
    cmake -B build -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS
    cmake --build build --config Release
    ```

### BLIS

更多信息见 [BLIS.md](./backend/BLIS.md)。

### Intel oneMKL

通过 oneAPI 编译器构建,可以为不支持 avx512 / avx512_vnni 的 Intel 处理器启用 avx_vnni 指令集。注意此构建配置**不支持 Intel GPU**。Intel GPU 支持请参考 [llama.cpp for SYCL](./backend/SYCL.md)。

- 手动安装 oneAPI:
  默认 `GGML_BLAS_VENDOR` 为 `Generic`,如果已 source intel 环境脚本并在 cmake 中加 `-DGGML_BLAS=ON`,会自动选中 MKL 版 BLAS。否则请安装 oneAPI 并按以下步骤:
    ```bash
    source /opt/intel/oneapi/setvars.sh # oneapi-basekit docker 镜像内可跳过,仅手动安装时需要
    cmake -B build -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=Intel10_64lp -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx -DGGML_NATIVE=ON
    cmake --build build --config Release
    ```

- 使用 oneAPI docker 镜像:
  不想手动配环境的话,可以直接用 intel 官方容器构建:[oneAPI-basekit](https://hub.docker.com/r/intel/oneapi-basekit),然后使用上面的命令。

更多信息见 [Optimizing and Running LLaMA2 on Intel® CPU](https://builders.intel.com/solutionslibrary/optimizing-and-running-llama2-on-intel-cpu)。

### 其他 BLAS 库

设置 `GGML_BLAS_VENDOR` 选项即可使用其他 BLAS 库。支持的厂商列表见 [CMake 文档](https://cmake.org/cmake/help/latest/module/FindBLAS.html#blas-lapack-vendors)。

## Metal 构建

MacOS 上 Metal 默认启用,使用 Metal 会让计算跑在 GPU 上。
编译期禁用 Metal 使用 `-DGGML_METAL=OFF` cmake 选项。

带 Metal 支持构建后,运行时可用 `--n-gpu-layers 0` 命令行参数显式禁用 GPU 推理。

## SYCL

SYCL 是一种更高层的编程模型,用于提升各类硬件加速器上的开发效率。

基于 SYCL 的 llama.cpp 用于**支持 Intel GPU**(Data Center Max 系列、Flex 系列、Arc 系列、内置 GPU 与 iGPU)。

详细信息见 [llama.cpp for SYCL](./backend/SYCL.md)。

## CUDA

使用 NVIDIA GPU 提供 GPU 加速。确保已安装 [CUDA toolkit](https://developer.nvidia.com/cuda-toolkit)。

#### 直接从 NVIDIA 下载
官方下载页:[NVIDIA developer site](https://developer.nvidia.com/cuda-downloads)。


#### 在 Fedora Toolbox 容器中编译运行
我们也提供了在 Fedora [toolbox 容器](https://containertoolbx.org/)中配置 CUDA toolkit 的[指南](./backend/CUDA-FEDORA.md)。

**适用于:**
- [Fedora Atomic Desktops](https://fedoraproject.org/atomic-desktops/)(如 [Silverblue](https://fedoraproject.org/atomic-desktops/silverblue/)、[Kinoite](https://fedoraproject.org/atomic-desktops/kinoite/))用户***必选***
  - (这些系统没有受支持的 CUDA 软件包)
- 宿主机不属于 [受支持的 Nvidia CUDA 发布平台](https://developer.nvidia.com/cuda-downloads)的用户***必选***
  - (例如宿主操作系统是 [Fedora 42 Beta](https://fedoramagazine.org/announcing-fedora-linux-42-beta/))
- 运行 [Fedora Workstation](https://fedoraproject.org/workstation/) 或 [Fedora KDE Plasma Desktop](https://fedoraproject.org/spins/kde)、想保持宿主系统干净的用户会觉得***方便***
- [Arch Linux](https://archlinux.org/)、[Red Hat Enterprise Linux >= 8.5](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)、[Ubuntu](https://ubuntu.com/download) 也有 toolbox 软件包*可选*


### 编译

通用说明(如加速编译)请先阅读 CPU 构建一节的注意事项。

```bash
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release
```

### 非 Native 构建

默认情况下,llama.cpp 会针对构建当时连接的硬件编译。
要构建覆盖所有 CUDA GPU 的版本,禁用 `GGML_NATIVE`:

```bash
cmake -B build -DGGML_CUDA=ON -DGGML_NATIVE=OFF
```

产物应能在所有 CUDA GPU 上以最优性能运行,部分场景可能需要少量即时编译。

### 覆盖算力(Compute Capability)规格

如果 `nvcc` 检测不到你的 GPU,可能看到类似警告:
 ```text
nvcc warning : Cannot find valid GPU for '-arch=native', default arch is used
```

一个办法是按上文做非 native 构建,但产物大、编译慢。
也可以显式指定 CUDA 架构。非 native 构建同样可以这么干,具体可参考 `ggml/src/ggml-cuda/CMakeLists.txt` 中的逻辑作为起点。

覆盖默认 CUDA 架构:

#### 1. 记下你 NVIDIA 设备的 `Compute Capability`:["CUDA: Your GPU Compute > Capability"](https://developer.nvidia.com/cuda-gpus)。

```text
GeForce RTX 4090      8.9
GeForce RTX 3080 Ti   8.6
GeForce RTX 3070      8.6
```

#### 2. 在 `CMAKE_CUDA_ARCHITECTURES` 列表中手动列出每个不同的 `Compute Capability`。

```bash
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES="86;89"
```

### 覆盖 CUDA 版本

系统里装了多个 CUDA、想指定用某个版本编译时(例如装在 `/opt/cuda-11.7` 的 CUDA 11.7):

```bash
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_COMPILER=/opt/cuda-11.7/bin/nvcc -DCMAKE_INSTALL_RPATH="/opt/cuda-11.7/lib64;\$ORIGIN" -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
```

#### 修复旧 CUDA 与新 glibc 的兼容问题

旧版 CUDA(如 v11.7)搭配新版 glibc 可能报这样的错:

```
/usr/include/bits/mathcalls.h(83): error: exception specification is
  incompatible with that of previous function "cospi"


  /opt/cuda-11.7/bin/../targets/x86_64-linux/include/crt/math_functions.h(5545):
  here
```

目前看来最不坏的办法是给 CUDA 安装打补丁,声明正确的签名。把 `/path/to/your/cuda/installation/targets/x86_64-linux/include/crt/math_functions.h` 中的以下行:

```C++
// original lines
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ double                 cospi(double x);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ float                  cospif(float x);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ double                 sinpi(double x);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ float                  sinpif(float x);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ double                 rsqrt(double x);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ float                  rsqrtf(float x);

// edited lines
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ double                 cospi(double x) noexcept (true);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ float                  cospif(float x) noexcept (true);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ double                 sinpi(double x) noexcept (true);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ float                  sinpif(float x) noexcept (true);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ double                 rsqrt(double x) noexcept (true);
extern __DEVICE_FUNCTIONS_DECL__ __device_builtin__ float                  rsqrtf(float x) noexcept (true);
```

### 运行时 CUDA 环境变量

可以在运行时设置 [CUDA 环境变量](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars)。

```bash
# Use `CUDA_VISIBLE_DEVICES` to hide the first compute device.
CUDA_VISIBLE_DEVICES="-0" ./build/bin/llama-server --model /srv/models/llama.gguf
```

#### CUDA_SCALE_LAUNCH_QUEUES

环境变量 [`CUDA_SCALE_LAUNCH_QUEUES`](https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/environment-variables.html#cuda-scale-launch-queues) 控制 CUDA 命令缓冲区大小,决定 CPU 等待 GPU 追上前能排队多少 GPU 操作。更大的缓冲区能减少 CPU 侧停顿,允许在 GPU 上排更多任务。

建议尝试 `CUDA_SCALE_LAUNCH_QUEUES=4x`,把 CUDA 命令缓冲区扩大到默认的 4 倍。该优化对**带流水线并行的多 GPU 设置**尤其有效,能显著提升 prompt 处理吞吐。

#### GGML_CUDA_CUBLAS_COMPUTE_TYPE

覆盖 cuBLAS 矩阵乘法默认的速度优先计算类型。
合法值:`auto`、`f16`、`fp16`、`bf16`、`f32`、`fp32`。

### 统一内存(Unified Memory)

在 Linux 上可用环境变量 `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` 启用统一内存:GPU 显存耗尽时换页到系统内存而不是崩溃。Windows 上对应 NVIDIA 控制面板中的 `System Memory Fallback`。

### 点对点访问(Peer Access)

环境变量 `GGML_CUDA_P2P` 可启用多 GPU 之间的点对点访问,让 GPU 直接互传数据而不经过系统内存。
需要驱动支持(通常仅工作站/数据中心 GPU)。
某些主板和 BIOS 设置(如 IOMMU)下可能导致崩溃或输出损坏。

### 性能调优

以下编译选项可用于调优性能:

| 选项                          | 合法值                 | 默认值  | 说明                                                                                                                                                                                                                                                                                                                                                                               |
|-------------------------------|------------------------|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GGML_CUDA_FORCE_MMQ           | 布尔                   | false   | 强制对量化模型使用自定义矩阵乘内核,而不是 FP16 cuBLAS,即使没有 int8 tensor core 实现可用(影响 V100、CDNA、RDNA3+)。支持 int8 tensor core 的 GPU 默认启用 MMQ 内核。强制开启 MMQ 后,大批量速度变差,但显存占用更低。 |
| GGML_CUDA_FORCE_CUBLAS        | 布尔                   | false   | 强制对量化模型使用 FP16 cuBLAS 而非自定义矩阵乘内核。可能有数值溢出问题(V100、CDNA、RDNA4 除外,它们默认用 FP32 计算类型),内存占用更高。在较新的数据中心 GPU 上 prompt 处理可能变快(自定义内核主要针对 RTX 3000/4000 调优)。   |
| GGML_CUDA_FA_ALL_QUANTS       | 布尔                   | false   | 为 FlashAttention CUDA 内核编译全部 KV cache 量化类型(组合)的支持。KV cache 大小控制更细,但编译时间大幅增加。                                                                                                                                                                                                                                                           |

## MUSA

使用摩尔线程(Moore Threads)GPU 提供 GPU 加速。确保已安装 [MUSA SDK](https://developer.mthreads.com/musa/musa-sdk)。

#### 直接从摩尔线程下载

官方下载页:[Moore Threads developer site](https://developer.mthreads.com/sdk/download/musa)。

### 编译

```bash
cmake -B build -DGGML_MUSA=ON
cmake --build build --config Release
```

#### 覆盖算力规格

默认启用所有受支持的算力。要自定义,可在 CMake 命令中指定 `MUSA_ARCHITECTURES`:

```bash
cmake -B build -DGGML_MUSA=ON -DMUSA_ARCHITECTURES="21"
cmake --build build --config Release
```

此配置只编译算力 `2.1`(MTT S80),可缩短编译时间。

#### 编译选项

CUDA 可用的大部分编译选项对 MUSA 同样适用,只是尚未经过充分测试。

- 静态构建,加 `-DBUILD_SHARED_LIBS=OFF` 和 `-DCMAKE_POSITION_INDEPENDENT_CODE=ON`:
  ```
  cmake -B build -DGGML_MUSA=ON \
    -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON
  cmake --build build --config Release
  ```

### 运行时 MUSA 环境变量

可在运行时设置 [MUSA 环境变量](https://docs.mthreads.com/musa-sdk/musa-sdk-doc-online/programming_guide/Z%E9%99%84%E5%BD%95/)。

```bash
# Use `MUSA_VISIBLE_DEVICES` to hide the first compute device.
MUSA_VISIBLE_DEVICES="-0" ./build/bin/llama-server --model /srv/models/llama.gguf
```

### 统一内存

Linux 上可用环境变量 `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` 启用统一内存:GPU 显存耗尽时换页到系统内存而不是崩溃。

## HIP

在支持 HIP 的 AMD GPU 上提供 GPU 加速。
确保已安装 ROCm,可从发行版包管理器安装,或从这里下载:[ROCm Quick Start (Linux)](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/tutorial/quick-start.html#rocm-install-quick)。

- Linux 上使用 `CMake`(假设是 gfx1030 兼容的 AMD GPU):
  ```bash
  HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -R)" \
      cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1030 -DCMAKE_BUILD_TYPE=Release \
      && cmake --build build --config Release -- -j 16
  ```

  注意:`GPU_TARGETS` 可选,省略时会为当前系统所有 GPU 编译。

  如果报如下错误:
  ```
  clang: error: cannot find ROCm device library; provide its path via '--rocm-path' or '--rocm-device-lib-path', or pass '-nogpulib' to build without ROCm device library
  ```
  尝试在 `HIP_PATH` 下搜索包含 `oclc_abi_version_400.bc` 文件的目录,然后在命令开头加上 `HIP_DEVICE_LIB_PATH=<刚找到的目录>`,类似:
  ```bash
  HIPCXX="$(hipconfig -l)/clang" HIP_PATH="$(hipconfig -p)" \
  HIP_DEVICE_LIB_PATH=<directory-you-just-found> \
      cmake -S . -B build -DGGML_HIP=ON -DGPU_TARGETS=gfx1030 -DCMAKE_BUILD_TYPE=Release \
      && cmake --build build -- -j 16
  ```

- Windows 上使用 `CMake`(用 x64 Native Tools Command Prompt for VS,假设是 gfx1100 兼容的 AMD GPU):
  ```bash
  set PATH=%HIP_PATH%\bin;%PATH%
  cmake -S . -B build -G Ninja -DGPU_TARGETS=gfx1100 -DGGML_HIP=ON -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release
  cmake --build build
  ```
  如有必要,把 `GPU_TARGETS` 改成你要编译的 GPU 架构。上面的示例用 `gfx1100`,对应 Radeon RX 7900XTX/XT/GRE。目标列表见[这里](https://llvm.org/docs/AMDGPUUsage.html#processors)。
  用 `rocminfo | grep gfx | head -1 | awk '{print $2}'` 的输出匹配处理器列表中最主要的版本信息,找到你的 GPU 版本串,例如 `gfx1035` 映射到 `gfx1030`。


环境变量 [`HIP_VISIBLE_DEVICES`](https://rocm.docs.amd.com/en/latest/understand/gpu_isolation.html#hip-visible-devices) 可指定使用哪些 GPU。
如果官方不支持你的 GPU,可以把环境变量 [`HSA_OVERRIDE_GFX_VERSION`] 设成相近 GPU 的版本,例如 RDNA2 用 10.3.0(如 gfx1030、gfx1031、gfx1035),RDNA3 用 11.0.0。注意 [`HSA_OVERRIDE_GFX_VERSION`] [在 Windows 上不受支持](https://github.com/ROCm/ROCm/issues/2654)。

### 统一内存

Linux 上可通过环境变量 `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` 使用统一内存架构(UMA)在 CPU 与核显之间共享主内存。不过这会拖累非核显 GPU 的性能(但能让核显可用)。

## Vulkan

### Windows 用户:

**w64devkit**

下载并解压 [`w64devkit`](https://github.com/skeeto/w64devkit/releases)。

按默认设置下载安装 [`Vulkan SDK`](https://vulkan.lunarg.com/sdk/home#windows)。

启动 `w64devkit.exe`,执行以下命令复制 Vulkan 依赖:
```sh
SDK_VERSION=1.3.283.0
cp /VulkanSDK/$SDK_VERSION/Bin/glslc.exe $W64DEVKIT_HOME/bin/
cp /VulkanSDK/$SDK_VERSION/Lib/vulkan-1.lib $W64DEVKIT_HOME/x86_64-w64-mingw32/lib/
cp -r /VulkanSDK/$SDK_VERSION/Include/* $W64DEVKIT_HOME/x86_64-w64-mingw32/include/
cat > $W64DEVKIT_HOME/x86_64-w64-mingw32/lib/pkgconfig/vulkan.pc <<EOF
Name: Vulkan-Loader
Description: Vulkan Loader
Version: $SDK_VERSION
Libs: -lvulkan-1
EOF

```

切换到 `llama.cpp` 目录,用 CMake 构建。
```sh
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release
```

**Git Bash MINGW64**

按默认设置下载安装 [`Git-SCM`](https://git-scm.com/downloads/win)。

下载安装 [`Visual Studio Community Edition`](https://visualstudio.microsoft.com/),记得勾选 `C++`。

按默认设置下载安装 [`CMake`](https://cmake.org/download/)。

按默认设置下载安装 [`Vulkan SDK`](https://vulkan.lunarg.com/sdk/home#windows)。

进入 `llama.cpp` 目录,右键选 `Open Git Bash Here`,然后执行:

```
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release
```

现在就可以用 `Vulkan` 以会话模式加载模型了:

```sh
build/bin/Release/llama-cli -m "[PATH TO MODEL]" -ngl 100 -c 16384 -t 10 -n -2 -cnv
```

**MSYS2**

安装 [MSYS2](https://www.msys2.org/),在 UCRT 终端中执行以下命令安装依赖。
```sh
pacman -S git \
    mingw-w64-ucrt-x86_64-gcc \
    mingw-w64-ucrt-x86_64-cmake \
    mingw-w64-ucrt-x86_64-vulkan-devel \
    mingw-w64-ucrt-x86_64-shaderc \
    mingw-w64-ucrt-x86_64-spirv-headers
```

切换到 `llama.cpp` 目录,用 CMake 构建。
```sh
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release
```

### Docker 用户:

无需安装 Vulkan SDK,容器内会自动装好。

```sh
# Build the image
docker build -t llama-cpp-vulkan --target light -f .devops/vulkan.Dockerfile .

# Then, use it:
docker run -it --rm -v "$(pwd):/app:Z" --device /dev/dri/renderD128:/dev/dri/renderD128 --device /dev/dri/card1:/dev/dri/card1 llama-cpp-vulkan -m "/app/models/YOUR_MODEL_FILE" -p "Building a website can be done in 10 simple steps:" -n 400 -e -ngl 33
```

### Linux 用户:

#### 使用 LunarG Vulkan SDK

先按照官方 LunarG 指南 [Getting Started with the Linux Tarball Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/linux/getting_started.html) 安装配置 Vulkan SDK。

> [!IMPORTANT]
> 第一步完成后,务必在当前终端会话中对 Vulkan SDK 内的 `setup_env.sh` 执行 `source`。否则构建无法进行。另外,关掉终端后若要再次构建,必须重新执行该步骤。当然也有持久化的办法,详见第一步链接的 Vulkan SDK 指南。

#### 使用系统软件包

Debian / Ubuntu 上可以这样安装所需依赖:
```sh
sudo apt-get install libvulkan-dev glslc spirv-headers
```

Vulkan 后端需要 SPIRV-Headers(`spirv/unified1/spirv.hpp`),**并不是**所有发行版的 Vulkan loader 开发包都会带上它。其他发行版的包名一般是 `spirv-headers`(Ubuntu / Debian / Arch)或 `spirv-headers-devel`(Fedora / openSUSE)。Windows 上 LunarG Vulkan SDK 的 `Include` 目录已包含这些头文件。

#### 通用步骤

确认已按 SDK 安装/配置步骤全部做完后,先用这个命令检查:
```bash
vulkaninfo
```

然后,假设你已 `cd` 进 llama.cpp 目录且 `vulkaninfo` 没有报错,就可以用下面的 CMake 命令构建 llama.cpp:
```bash
cmake -B build -DGGML_VULKAN=1
cmake --build build --config Release
```

构建完成后,应该可以这样做:
```bash
# Test the output binary
# "-ngl 99" should offload all of the layers to GPU for most (if not all) models.
./build/bin/llama-cli -m "PATH_TO_MODEL" -p "Hi you how are you" -ngl 99

# You should see in the output, ggml_vulkan detected your GPU. For example:
# ggml_vulkan: Using Intel(R) Graphics (ADL GT2) | uma: 1 | fp16: 1 | warp size: 32
```

### Mac 用户:

一般按 LunarG 的 [Getting Started with the MacOS Vulkan SDK](https://vulkan.lunarg.com/doc/sdk/latest/mac/getting_started.html) 指南安装配置即可。macOS 上有两种 Vulkan 驱动,都通过转换层把 Vulkan 映射到 Metal。可以通过把 `VK_ICD_FILENAMES` 环境变量指向对应 ICD JSON 文件来热切换。

安装 LunarG Vulkan SDK 时勾选 "KosmicKrisp"。

安装后为 LunarG Vulkan SDK 设置环境变量(可选写入 shell profile 以持久化):
```bash
source /path/to/vulkan-sdk/setup-env.sh
```

#### 使用 MoltenVK

MoltenVK 是 macOS 上 LunarG Vulkan SDK 默认安装的 Vulkan 驱动,上面的环境变量设置原样可用。

#### 使用 KosmicKrisp

为 KosmicKrisp 覆盖环境变量:
```bash
export VK_ICD_FILENAMES=$VULKAN_SDK/share/vulkan/icd.d/libkosmickrisp_icd.json
export VK_DRIVER_FILES=$VULKAN_SDK/share/vulkan/icd.d/libkosmickrisp_icd.json
```

#### 构建

这是唯一与[上文](#通用步骤)不同的步骤。
```bash
cmake -B build -DGGML_VULKAN=1 -DGGML_METAL=OFF
cmake --build build --config Release
```

## CANN
使用昇腾(Ascend)NPU 的 AI 核心提供 NPU 加速。[CANN](https://www.hiascend.com/en/software/cann) 是一套分层 API,帮助基于昇腾 NPU 快速构建 AI 应用与服务。

更多昇腾 NPU 信息见 [Ascend Community](https://www.hiascend.com/en/)。

确保已安装 CANN toolkit,下载地址:[CANN Toolkit](https://www.hiascend.com/developer/download/community/result?module=cann)。

进入 `llama.cpp` 目录,用 CMake 构建。
```bash
cmake -B build -DGGML_CANN=on -DCMAKE_BUILD_TYPE=release
cmake --build build --config release
```

可以用下面的命令测试:

```bash
./build/bin/llama-cli -m PATH_TO_MODEL -p "Building a website can be done in 10 steps:" -ngl 32
```

如果屏幕输出以下信息,说明你正在使用带 CANN 后端的 `llama.cpp`:
```bash
llm_load_tensors:       CANN model buffer size = 13313.00 MiB
llama_new_context_with_model:       CANN compute buffer size =  1260.81 MiB
```

详细信息(模型/设备支持、CANN 安装等)见 [llama.cpp for CANN](./backend/CANN.md)。

## ZenDNN

ZenDNN 为 AMD EPYC™ CPU 提供优化的深度学习原语,可加速推理负载中的矩阵乘法运算。

### 编译

- Linux 上使用 `CMake`(自动构建):

    ```bash
    cmake -B build -DGGML_ZENDNN=ON
    cmake --build build --config Release
    ```

    首次构建会自动下载并编译 ZenDNN,可能需要 5-10 分钟,后续构建会快很多。

- 使用自定义 ZenDNN 安装路径:

    ```bash
    cmake -B build -DGGML_ZENDNN=ON -DZENDNN_ROOT=/path/to/zendnn/install
    cmake --build build --config Release
    ```

### 测试

可以用下面的命令测试:

```bash
./build/bin/llama-cli -m PATH_TO_MODEL -p "Building a website can be done in 10 steps:" -n 50
```

硬件支持、配置说明、性能优化等详细信息见 [llama.cpp for ZenDNN](./backend/ZenDNN.md)。

## Arm® KleidiAI™
KleidiAI 提供优化的 Arm CPU 微内核(microkernel),供 ggml CPU 后端使用。构建时启用只是让这些内核可用,并不强制每个算子都走 KleidiAI。运行时,llama.cpp 会根据检测到的 CPU 特性、张量类型、算子形状和当前后端优先级,选择最合适的兼容 CPU 内核。

支持的目标:

| 平台 | 支持的 ABI / 架构 | 说明 |
| --- | --- | --- |
| Linux | AArch64 / arm64 | 运行时自动检测 CPU 特性。 |
| Android | `arm64-v8a` | 便携构建请使用下方的 Android NDK 命令。 |
| Apple | arm64 | 运行时自动检测 CPU 特性。非流式 SVE 向量长度视为不可用。 |
| Windows | arm64 | 运行时自动检测 CPU 特性。在验证检测路径前,SMCU 数量视为未知。 |

`GGML_CPU_KLEIDIAI=ON` 仅对 AArch64/arm64 构建有效。不要在 x86、32 位 Arm 或 `arm64-v8a` 之外的 Android ABI 上启用。

### 原生 AArch64/arm64 构建

在 llama.cpp 源码目录:

```bash
cmake -S . -B build -DGGML_CPU_KLEIDIAI=ON
cmake --build build --config Release
```

### Android arm64-v8a NDK 构建

把 `ANDROID_NDK` 指向 Android NDK 根目录,在 llama.cpp 源码目录执行以下命令。该命令配置便携的 Android `arm64-v8a` 构建并启用 KleidiAI,同时避免依赖不属于 NDK 稳定原生 API 集合的 Android 组件。

```bash
cmake -S . -B build-android \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE="$ANDROID_NDK/build/cmake/android.toolchain.cmake" \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-28 \
  -DGGML_CPU_KLEIDIAI=ON \
  -DGGML_NATIVE=OFF \
  -DGGML_OPENMP=OFF \
  -DGGML_LLAMAFILE=OFF \
  -DLLAMA_OPENSSL=OFF
cmake --build build-android --config Release --parallel
cmake --install build-android --prefix {install-dir} --config Release
```

重要 Android 选项:

- `GGML_CPU_KLEIDIAI=ON`:为 Android `arm64-v8a` 启用 KleidiAI。
- `GGML_NATIVE=OFF`:交叉编译必需,因为构建宿主 CPU 不是 Android 目标 CPU。
- `GGML_OPENMP=OFF`:避免在 NDK 命令行构建中引入 OpenMP 运行时依赖。
- `GGML_LLAMAFILE=OFF`:避开 Android 不支持的 llamafile 后端。
- `LLAMA_OPENSSL=OFF`:避免依赖不属于 Android NDK 稳定原生 API 集合的 OpenSSL。

`examples/llama.android` 下的 Android Studio 工程会为 `arm64-v8a` 自动启用 KleidiAI。`arm64-v8a` 上的 Android 命令行 CMake 构建需显式传 `-DGGML_CPU_KLEIDIAI=ON`。

便携的 Android `arm64-v8a` 构建不需要 `-march=armv8.7a` 之类的全局 -march 标志——全局 -march 会抬高通用代码的基线指令集。无需手动选择架构相关源码,llama.cpp 会在运行时选择兼容的 KleidiAI 内核,各内核的 -march 由 KleidiAI 库内部 CMake 处理。

### 验证构建

运行安装后或源码树内的二进制:

```bash
./build/bin/llama-cli -m PATH_TO_MODEL -p "What is a car?"
```

如果启用了 KleidiAI,输出中会有类似这样的一行:

```
load_tensors: CPU_KLEIDIAI model buffer size =  3474.00 MiB
```

这说明模型张量是通过 KleidiAI CPU 缓冲区分配的,但不代表每个算子(或任何特定 SME 系算子)都用了 KleidiAI 微内核——运行时 CPU 特性、张量类型、算子形状和后端优先级仍然决定分发。按构建目标不同,另一个后端可能优先级更高。要强制走 CPU,可在构建期禁用更高优先级后端(如 `-DGGML_METAL=OFF`),或在支持的运行时用 `--device none` 之类的设备选项。

### 运行时分发

KleidiAI 微内核用到 dotprod、i8mm、SVE、SME/SME2 等 Arm CPU 特性。构建期配置让内核可用,运行时分发为检测到的 CPU 和算子选择兼容内核,较老或特性较少的 CPU 会自动回退。

KleidiAI 加速 F32 和常见量化格式的部分 `GGML_OP_MUL_MAT` 路径。实际覆盖取决于内置 KleidiAI 版本和 llama.cpp 运行时选择器,因此即使 CPU 支持所需 Arm 特性,不支持的张量类型、算子形状或更高优先级后端也可能绕过 KleidiAI——这也是 SME 硬件上模型可能没走 SME 内核的原因。当前 llama.cpp 的 KleidiAI SVE 选择器只在运行时 SVE 向量长度恰为 QK8_0 字节(32 字节)时启用 SVE 内核:Linux/Android 运行时查询,Apple 和 Windows arm64 因无法可靠获得该值而视为未知(SVE 可用性同样如此),Windows arm64 的 SMCU 数量在验证检测机制前也视为未知。可用 SME 系内核集合取决于内置 KleidiAI 版本和检测到的 CPU 能力;生产配置不需要任何 KleidiAI 运行时环境变量。

### 诊断与调试覆盖

KleidiAI 运行时环境变量是诊断/调试用的覆盖项,不是生产配置,日常使用请保持未设置。

`GGML_KLEIDIAI_SME` 控制 SME 系内核选择,并覆盖分配给所选量化 SME 系内核的最大线程数:

- 未设置:自动运行时检测。
- `0`:禁用 SME 系内核。
- `<n> > 0`:启用兼容的 SME 系内核,量化 SME 系内核最多允许 `<n>` 个线程。

Windows arm64 上,在自动 SMCU 数量检测验证之前,可用 `GGML_KLEIDIAI_SME=<n>` 作为 SME 线程上限标定的临时诊断/调试覆盖。

如果 CPU 不支持某个内置内核所需的 SME 系能力,无论环境变量如何,该内核都会被禁用。

## OpenCL

通过 OpenCL 在较新的 Adreno GPU 上提供 GPU 加速。
OpenCL 后端更多信息见 [OPENCL.md](./backend/OPENCL.md)。

### Android

假设 NDK 位于 `$ANDROID_NDK`。先安装 OpenCL 头文件和 ICD loader 库(如果没有),

```sh
mkdir -p ~/dev/llm
cd ~/dev/llm

git clone https://github.com/KhronosGroup/OpenCL-Headers && \
cd OpenCL-Headers && \
cp -r CL $ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include

cd ~/dev/llm

git clone https://github.com/KhronosGroup/OpenCL-ICD-Loader && \
cd OpenCL-ICD-Loader && \
mkdir build_ndk && cd build_ndk && \
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
  -DOPENCL_ICD_LOADER_HEADERS_DIR=$ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/include \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=24 \
  -DANDROID_STL=c++_shared && \
ninja && \
cp libOpenCL.so $ANDROID_NDK/toolchains/llvm/prebuilt/linux-x86_64/sysroot/usr/lib/aarch64-linux-android
```

然后启用 OpenCL 构建 llama.cpp,

```sh
cd ~/dev/llm

git clone https://github.com/ggml-org/llama.cpp && \
cd llama.cpp && \
mkdir build-android && cd build-android

cmake .. -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-28 \
  -DBUILD_SHARED_LIBS=OFF \
  -DGGML_OPENCL=ON

ninja
```

### Windows Arm64

先安装 OpenCL 头文件和 ICD loader 库(如果没有),

```powershell
mkdir -p ~/dev/llm

cd ~/dev/llm
git clone https://github.com/KhronosGroup/OpenCL-Headers && cd OpenCL-Headers
mkdir build && cd build
cmake .. -G Ninja `
  -DBUILD_TESTING=OFF `
  -DOPENCL_HEADERS_BUILD_TESTING=OFF `
  -DOPENCL_HEADERS_BUILD_CXX_TESTS=OFF `
  -DCMAKE_INSTALL_PREFIX="$HOME/dev/llm/opencl"
cmake --build . --target install

cd ~/dev/llm
git clone https://github.com/KhronosGroup/OpenCL-ICD-Loader && cd OpenCL-ICD-Loader
mkdir build && cd build
cmake .. -G Ninja `
  -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_PREFIX_PATH="$HOME/dev/llm/opencl" `
  -DCMAKE_INSTALL_PREFIX="$HOME/dev/llm/opencl"
cmake --build . --target install
```

然后启用 OpenCL 构建 llama.cpp,

```powershell
cmake .. -G Ninja `
  -DCMAKE_TOOLCHAIN_FILE="$HOME/dev/llm/llama.cpp/cmake/arm64-windows-llvm.cmake" `
  -DCMAKE_BUILD_TYPE=Release `
  -DCMAKE_PREFIX_PATH="$HOME/dev/llm/opencl" `
  -DBUILD_SHARED_LIBS=OFF `
  -DGGML_OPENCL=ON
ninja
```

## Android

Android 构建文档见[这里](./android.md)。

## WebGPU

WebGPU 后端依赖 [Dawn](https://dawn.googlesource.com/dawn)。按[这里](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/quickstart-cmake.md)的说明在本地安装 Dawn,让 CMake 能找到它。当前实现与 Dawn 提交 `18eb229` 同步。

在 llama.cpp 目录用 CMake 构建:

```
cmake -B build -DGGML_WEBGPU=ON
cmake --build build --config Release
```

### 浏览器支持

WebGPU 允许受支持的浏览器跨平台访问 GPU。我们使用 [Emscripten](https://emscripten.org/) 把 ggml 的 WebGPU 后端编译为 WebAssembly。Emscripten 官方尚未支持 WebGPU 绑定,但 Dawn 自己维护了一套叫 emdawnwebgpu 的 WebGPU 绑定。

按[这里](https://dawn.googlesource.com/dawn/+/refs/heads/main/src/emdawnwebgpu/)的说明下载或构建 emdawnwebgpu 包(注意,本地构建 emdawnwebgpu 包可能更稳妥,以便与你安装的 Dawn 版本保持同步)。用 CMake 构建时,需要用 `EMDAWNWEBGPU_DIR` 标志指定 emdawnwebgpu port 文件路径。

## IBM Z & LinuxONE

IBM Z & LinuxONE 构建文档见[这里](./build-s390x.md)。

## OpenVINO

[OpenVINO](https://docs.openvino.ai/) 是用于优化和部署高性能 AI 推理的开源工具包,专为 Intel 硬件(CPU、GPU、NPU)设计。

构建说明与用法示例见 [OPENVINO.md](backend/OPENVINO.md)。

### Hexagon

特定目标的构建与运行信息见 [README.md](./backend/snapdragon/README.md)。

---
## 关于 GPU 加速后端的说明

即使使用 `-ngl 0` 选项,GPU 仍可能被用于加速部分计算。可以用 `--device none` 完全禁用 GPU 加速。

大多数情况下,可以同时构建并使用多个后端。例如用 `-DGGML_CUDA=ON -DGGML_VULKAN=ON` 的 CMake 选项同时构建支持 CUDA 和 Vulkan 的 llama.cpp。运行时用 `--device` 选项指定使用哪些后端设备,`--list-devices` 选项可查看可用设备列表。

后端可以构建为动态库,在运行时动态加载。这样同一个 llama.cpp 二进制就能在不同 GPU 的机器上使用。启用该功能请在构建时使用 `GGML_BACKEND_DL` 选项。
