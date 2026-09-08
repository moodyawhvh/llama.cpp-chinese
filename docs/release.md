> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# 发布流程

llama.cpp 采用[语义化版本](https://semver.org)(`主版本.次版本.补丁版本`)。

## 版本号递增指南

| 改动类型 | 递增的版本位 |
|---|---|
| 公开 C API(`include/llama.h`)的不兼容改动         | `主版本(MAJOR)` |
| 向后兼容的新功能、模型支持或 API 新增    | `次版本(MINOR)` |
| 不涉及 API 变更的 bug 修复                                      | `补丁版本(PATCH)` |

版本号在根目录 `CMakeLists.txt` 顶部的三个变量中设置:

```cmake
set(LLAMA_VERSION_MAJOR 0)
set(LLAMA_VERSION_MINOR 1)
set(LLAMA_VERSION_PATCH 0)
```

_版本号递增应包含在引入该改动的 PR 中,或在发版前合并的一个专门的 bump 提交里。_

_TODO: 增加 PR 标签(`semver: patch`、`semver: minor`、`semver: major`),帮助识别哪些 PR 在发版前需要递增版本号。_

## 制作发布

发布通过手动触发的 [make-release](.github/workflows/make-release.yml) 工作流完成。

该工作流运行在 "Run workflow" 对话框中选择的分支上(默认 `master`),可选传入一个 `commit` SHA。指定了 commit 时,工作流会校验该 commit 属于该分支、且距分支 HEAD 不超过 3 天,然后发布该 commit 而不是分支 HEAD。

工作流会创建一个附注 git 标签(如 `v0.1.0`)并推送到远程。不会创建 GitHub Release 对象,标签本身就是发布产物。

## 构建发布版

默认 `LLAMA_BUILD_IS_DEV=ON`,会给 `LLAMA_VERSION` 追加 `-dev` 后缀,标记为 nightly/开发构建。从发布标签构建的分发方必须传 `-DLLAMA_BUILD_IS_DEV=OFF`,以生成干净的版本号字符串(如 `0.1.0` 而非 `0.1.0-dev`)。

## 发布如何到达用户
目前发布版不发布到 GitHub Releases,那里只有 nightly/开发构建。用户获取发布版的渠道如下:

- **llama-install.sh**  — 下载基于发布标签构建的预编译二进制。
- **包管理器**  — 直接消费 git 标签。
- **从源码构建** — 用户克隆仓库并 checkout 对应标签。
