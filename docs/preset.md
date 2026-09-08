> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# llama.cpp INI 预设

## 简介

[PR#17859](https://github.com/ggml-org/llama.cpp/pull/17859) 引入的 INI 预设功能,允许用户为 llama.cpp 创建可复用、可分享的参数配置。

## 在 Server 中使用预设

在 server 上运行多个模型(router 模式)时,可以用 INI 预设文件配置模型专属参数。详情参考 [server 文档](../tools/server/README.md)。

### 使用 Hugging Face 预设

> [!IMPORTANT]
>
> 请只使用你信得过的预设!来源不明的预设可能不安全

你可以把自己的预设推到 Hugging Face Hub 与其他用户分享,方法:
1. 在 Hugging Face 上创建一个空的模型仓库
2. 在仓库根目录创建 `preset.ini` 文件

`preset.ini` 示例:

```ini
[*]
ctx-size             = 0
mmap                 = 1
kv-unified           = 1
parallel             = 4
spec-default         = 1

[Qwen3.5-4B]
hf                   = unsloth/Qwen3.5-4B-GGUF:Q4_K_M
ctx-size             = 262144
batch-size           = 2048
ubatch-size          = 2048
top-p                = 1.0
top-k                = 0
min-p                = 0.01
temp                 = 1.0

[gpt-oss-120b-hf]
hf                   = ggml-org/gpt-oss-120b-GGUF
ctx-size             = 262144
batch-size           = 2048
ubatch-size          = 2048
top-p                = 1.0
top-k                = 0
min-p                = 0.01
temp                 = 1.0
chat-template-kwargs = {"reasoning_effort": "high"}
```

预设的加载方式与 `--models-preset` 选项类似。因此你也可以用命令行参数覆盖其中的部分参数:

```sh
# Force temp = 0.1, overriding the preset value
llama-cli -hf username/my-preset --temp 0.1
```

### 命名预设

如果想为一个或多个 GGUF 模型定义多套预设配置,可以建一个只含单个 `preset.ini` 文件的空白 HF 仓库,在其中引用实际模型:

```ini
[*]
mmap = 1

[gpt-oss-20b-hf]
hf          = ggml-org/gpt-oss-20b-GGUF
batch-size  = 2048
ubatch-size = 2048
top-p       = 1.0
top-k       = 0
min-p       = 0.01
temp        = 1.0
chat-template-kwargs = {"reasoning_effort": "high"}

[gpt-oss-120b-hf]
hf          = ggml-org/gpt-oss-120b-GGUF
batch-size  = 2048
ubatch-size = 2048
top-p       = 1.0
top-k       = 0
min-p       = 0.01
temp        = 1.0
chat-template-kwargs = {"reasoning_effort": "high"}
```

然后通过 `llama-cli` 或 `llama-server` 使用,示例:

```sh
llama-server -hf user/repo:gpt-oss-120b-hf
```

请务必为每个子预设提供正确的 `hf-repo`。否则可能报错:`The specified tag is not a valid quantization scheme.`

## 系统级配置

[PR #26118](https://github.com/ggml-org/llama.cpp/pull/26118) 加入的系统级配置,可以让多个工具和示例共享同一套选项。与上文不同,它不限于 server。

启动时如果存在这些文件就会加载,后加载的文件覆盖先加载的:
1. 系统级:`/etc/llama.cpp/config.ini`(Windows 上为 `%PROGRAMDATA%\llama.cpp\config.ini`)
2. 用户级:`$XDG_CONFIG_HOME/llama.cpp/config.ini`,默认 `~/.config/llama.cpp/config.ini`(Windows 上为 `%APPDATA%\llama.cpp\config.ini`)

配置文件先生效,随后被环境变量、命令行参数和模型预设(router 模式)覆盖。

注意:
- 只使用 `[*]` 和 default 段;写在任何段头之前的选项属于 "default"。具名段会被忽略
- 可以写工具专属选项,但示例程序不支持时会忽略并给出警告<br/>例如:你写了 `port = 1234`,只有 `llama-server` 会用它,其他示例程序会忽略
- 不建议在系统级配置 `model` 或 `hf-repo`,因为可能引入冲突<br/>例如:配置文件里的 `hf-repo` 在你命令行传 `-m` 时仍然生效,可能导致加载的模型和你预期的不一致
