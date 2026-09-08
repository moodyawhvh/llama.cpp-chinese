> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# 安装 llama.cpp 预编译版本

| 安装渠道 | Windows | Mac  | Linux |
|-------------|---------|------|-------|
| conda-forge | ✅      | ✅   | ✅   |
| Winget      | ✅      |      |      |
| Homebrew    |         | ✅   | ✅   |
| MacPorts    |         | ✅   |      |
| Nix         |         | ✅   | ✅   |

## conda-forge(Windows、Mac 和 Linux)

conda-forge 提供以下构建:
 - CUDA(Windows 和 Linux)
 - Vulkan(Windows 和 Linux)
 - Apple Metal(macOS)

```sh
conda install -c conda-forge llama.cpp
```

```sh
mamba install -c conda-forge llama.cpp
```

```sh
# 项目本地安装
pixi add llama.cpp

# 全局安装
pixi global install llama.cpp
```

该发行版由 [`conda-forge/llama.cpp-feedstock`](https://github.com/conda-forge/llama.cpp-feedstock/) 维护。

如遇任何问题,请到[它的 issue 跟踪器](https://github.com/conda-forge/llama.cpp-feedstock/issues)提 issue。

## Winget(Windows)

```sh
winget install llama.cpp
```

该包会随 `llama.cpp` 新版本发布自动更新。更多信息:https://github.com/ggml-org/llama.cpp/issues/8188

## Homebrew(Mac 和 Linux)

```sh
brew install llama.cpp
```

该 formula 会随 `llama.cpp` 新版本发布自动更新。更多信息:https://github.com/ggml-org/llama.cpp/discussions/7668

## MacPorts(Mac)

```sh
sudo port install llama.cpp
```

另见:https://ports.macports.org/port/llama.cpp/details/

## Nix(Mac 和 Linux)

```sh
nix profile install nixpkgs#llama-cpp
```

适用于启用 flake 的安装。

或者

```sh
nix-env --file '<nixpkgs>' --install --attr llama-cpp
```

适用于未启用 flake 的安装。

该表达式会在 [nixpkgs 仓库](https://github.com/NixOS/nixpkgs/blob/nixos-24.05/pkgs/by-name/ll/llama-cpp/package.nix#L164)内自动更新。
