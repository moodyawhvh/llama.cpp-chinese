> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# 贡献者

本项目将贡献者分为 3 个层级:

- 贡献者(Contributors):曾经提交过贡献的人(没有任何特殊权限)
- 协作者(Collaborators / Triage):有重要贡献的人,可能负责部分代码,并需要维护和评审自己负责部分的贡献
- 维护者(Maintainers):在代码所有者批准后,负责评审和合并 PR

# AI 使用政策

> [!IMPORTANT]
>
> 允许使用 AI 生成代码。但无论代码是怎么产生的,你要对每一行代码承担 100% 的责任。
>
> 隐瞒 AI 使用情况可能导致你的账号被永久禁止参与本项目贡献。
>
> 关于 AI 允许与限制用途的详细信息,请参阅 [AGENTS.md](AGENTS.md) 文件。

如果使用 AI 生成了任何部分代码,贡献者必须遵守以下要求:

1. 明确披露 AI 的使用方式。
2. 先检查是否已有针对同一改动的 PR;如果存在,在该 PR 下留言与作者协作,不要另开重复 PR。
3. 提交 PR 前进行全面的 manual 人工审查。
4. 当维护者询问时,能够解释你提交的每一行代码。
5. 严禁使用 AI 替你撰写帖子(bug 报告、功能请求、PR 描述、GitHub 讨论、回复他人等)。

更多信息请参阅 [AGENTS.md](AGENTS.md) 文件。

# Pull Request(面向贡献者与协作者)

### 动手之前

- 先搜索已有的讨论和 PR —— 重复提交大概率会被直接关闭,不会有过多解释。
- 新功能必须先从 issue 开始,而不是 PR —— 先让关注度积累起来再写代码;小众功能可能只会以示例/工具的形式合入,或者只留在私有 fork 里。
- Bug 修复 PR 必须附上可复现的 issue,以及一个在改动前失败、改动后通过的回归测试。没有测试的修复可能未经评审就被关闭。
- 新增 CLI 或公开 API 的门槛**高于**内部改动 —— 需要说明为什么现有机制不够用。
- 即使满足上述所有条件也不保证一定能合并 —— 见 [Pull Request(面向维护者)](#pull-requests-面向维护者)。
- 如果你是新贡献者:
    - 同时保持的开放 PR 数量限制为 1 个
    - 不要提交琐碎的修复(如拼写错误、格式调整)

### 准备你的 PR

- llama.cpp 使用 ggml 张量库进行模型推理。如果你不熟悉 ggml,建议先看看 [ggml 仓库中的示例](https://github.com/ggml-org/ggml/tree/master/examples/)。[simple](https://github.com/ggml-org/ggml/tree/master/examples/simple) 展示了使用 ggml 的最简代码。[gpt-2](https://github.com/ggml-org/ggml/tree/master/examples/gpt-2) 包含基于 GPT-2 的最小语言模型推理实现。[mnist](https://github.com/ggml-org/ggml/tree/master/examples/mnist) 演示了如何训练和评估一个简单的图像分类器
- 测试你的改动:
  - 发布前先在本地执行[完整的 CI 流程](ci/README.md)
  - 用 `llama-perplexity` 和 `llama-bench` 确认困惑度和性能没有因你的改动而变差
  - 如果你修改了 `ggml` 源码,运行 `test-backend-ops` 工具,检查 `ggml` 算子的不同后端实现是否产生一致的结果(这需要能访问至少两个不同的 `ggml` 后端)
  - 如果你修改了某个 `ggml` 算子或新增了算子,请在 `test-backend-ops` 中补充对应的测试用例
- 每个功能或修复单独开 PR:
  - 避免在一个 PR 里混入不相关的改动
  - 新增模型或功能支持时,除非有充分理由,首个 PR 请**只聚焦 CPU 支持**。CUDA 等其他后端的支持放到后续 PR 中
  - 尤其要注意,新增数据类型(扩展 `ggml_type` 枚举)会带来不成比例的维护负担。因此,新增一种量化类型至少还需要满足以下*额外*条件:
    - 使用新类型把一个小模型转换为 GGUF 并上传到 HuggingFace
    - 提供与 FP16/BF16(以原生精度为准)以及相近大小类型之间的[困惑度](https://github.com/ggml-org/llama.cpp/tree/master/tools/perplexity)对比
    - 提供新类型与 FP16/BF16(以原生精度为准)版本以及相近大小类型之间计算的 KL 散度数据
    - 提供新类型与相近大小类型在纯 CPU 上的[性能数据](https://github.com/ggml-org/llama.cpp/tree/master/tools/llama-bench)对比
- 建议允许维护者对你的分支写入,这样可以加快评审速度,评审者可以直接推送提交

### 提交 PR 之后

- 请预期会收到修改要求,以确保代码符合 llama.cpp 的质量和长期可维护性标准
- 维护者在最终批准和合并 PR 时会依赖你的见解与确认
- 如果你的 PR 长期没有动静,把它 rebase 到最新的 `master` 上以引起维护者注意
- 可以考虑把自己加入 [CODEOWNERS](CODEOWNERS),表明你愿意修复相关 issue 并评审相关 PR

# Pull Request(面向维护者)

- 使用 squash-merge 合并 PR
- squash 后的提交标题格式:`<模块> : <提交标题> (#<issue 编号>)`。例如:`utils : fix typo in utils.py (#1234)`
- `<模块>` 可以从这里选取:https://github.com/ggml-org/llama.cpp/wiki/Modules
- 让其他维护者自行合并他们自己的 PR
- 合并 PR 前,务必充分理解改动内容
- 如果某个 PR 不值得触发新版本发布,在 squash 提交中加入 `[no release]`,节省 CI 资源
- 注意维护成本:一个功能的大部分工作量出现在 PR 合并之后。如果 PR 作者不打算长期投入,就需要由其他人(也就是你)来接手负责
- 给 PR 添加 ["merge ready"](https://github.com/ggml-org/llama.cpp/pulls?q=is%3Apr+is%3Aopen+draft%3Ano+sort%3Aupdated-desc+label%3A%22merge+ready%22+) 标签,表示该 PR 可以快速合并,无需等待 2 个独立评审。[(更多信息)](https://github.com/ggml-org/llama.cpp/pull/26178)
- 合并前等待 CI 结果

维护者保留出于任何原因拒绝评审或关闭 PR 的权利,无需解释,尤其在以下情况下:
- 提议的改动已经在 roadmap 或已有 issue 中提及,且已指派给某人。
- 该 PR 与已有 PR 重复。
- 贡献者未遵守本贡献指南或 AI 政策。
- 改动不符合现有架构,或者复杂度与其收益不成正比。

# 编码规范

- 避免引入第三方依赖、多余文件、多余头文件等
- 始终考虑与其他操作系统和架构的跨平台兼容性
- 避免花哨的现代 STL 写法,使用基础的 `for` 循环,避免模板,保持简单
- 垂直对齐能提高可读性,也便于批量编辑
- 清理行尾空白,使用 4 个空格缩进,大括号与语句同行,写作 `void * ptr`、`int & a`
- 公开 API 使用定长整数类型如 `int32_t`;分配大小或字节偏移等场景使用 `size_t` 也可以
- 使用 `struct foo {}` 声明结构体,而不是 `typedef struct foo {} foo`
    - 在 C++ 代码中,非必要时省略可选的 `struct` 和 `enum` 关键字
    ```cpp
    // 正确
    llama_context * ctx;
    const llama_rope_type rope_type;

    // 错误
    struct llama_context * ctx;
    const enum llama_rope_type rope_type;
    ```

    _(注:该规范尚未在 `llama.cpp` 代码库中全面执行。新代码应遵循此规范。)_

- 尽量遵循代码中的既有模式(缩进、空格等)。拿不准时,用 `clang-format`(clang-tools v15+ 版本)格式化新增代码
- 当前规范未覆盖的内容,参考 [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- 张量按行主序存储数据。维度 0 称为列,1 称为行,2 称为矩阵
- 矩阵乘法的约定非常规:[`C = ggml_mul_mat(ctx, A, B)`](https://github.com/ggml-org/llama.cpp/blob/880e352277fc017df4d5794f0c21c44e1eae2b84/ggml.h#L1058-L1064) 表示 $C^T = A B^T \Leftrightarrow C = B A^T.$

![matmul](media/matmul.png)

# 命名规范

- 函数、变量和类型名使用 `snake_case`
- 命名通常优先保证最长公共前缀(见 https://github.com/ggml-org/ggml/pull/302#discussion_r1243240963 )

    ```cpp
    // 错误
    int small_number;
    int big_number;

    // 正确
    int number_small;
    int number_big;
    ```

- 枚举值一律大写,并冠以枚举名作为前缀

    ```cpp
    enum llama_vocab_type {
        LLAMA_VOCAB_TYPE_NONE = 0,
        LLAMA_VOCAB_TYPE_SPM  = 1,
        LLAMA_VOCAB_TYPE_BPE  = 2,
        LLAMA_VOCAB_TYPE_WPM  = 3,
        LLAMA_VOCAB_TYPE_UGM  = 4,
        LLAMA_VOCAB_TYPE_RWKV = 5,
    };
    ```

- 总体命名模式为 `<class>_<method>`,其中 `<method>` 为 `<action>_<noun>`

    ```cpp
    llama_model_init();           // class: "llama_model",         method: "init"
    llama_sampler_chain_remove(); // class: "llama_sampler_chain", method: "remove"
    llama_sampler_get_seed();     // class: "llama_sampler",       method: "get_seed"
    llama_set_embeddings();       // class: "llama_context",       method: "set_embeddings"
    llama_n_threads();            // class: "llama_context",       method: "n_threads"
    llama_adapter_lora_free();    // class: "llama_adapter_lora",  method: "free"
    ```

    - `<action>` 为 `get` 时可以省略
    - `<noun>` 在不必要时可以省略
    - `<class>` 的 `_context` 后缀是可选的,需要区分同名符号时使用
    - 构造/析构 `<action>` 使用 `init`/`free`

- 当某个类型对用户应当是不透明(opaque)的时候,使用 `_t` 后缀 —— 用户不需要关心它本质上是结构体还是别的什么

    ```cpp
    typedef struct llama_context * llama_context_t;

    enum llama_pooling_type llama_pooling_type(const llama_context_t ctx);
    ```

    _(注:该规范尚未在 `llama.cpp` 代码库中全面执行。新代码应遵循此规范)_

- C/C++ 文件名全部小写并用连字符分隔。头文件使用 `.h` 扩展名,源文件使用 `.c` 或 `.cpp` 扩展名
- Python 文件名全部小写并用下划线分隔

- _(TODO:缩写词的使用规范)_

# 预处理指令

- _(TODO:补充带示例的规范并应用到代码库)_

    ```cpp
    #ifdef FOO
    #endif // FOO
    ```

# 代码维护

- 现有代码应在 [CODEOWNERS](CODEOWNERS) 文件中指定对应的协作者和/或维护者,负责:
  - 评审和合并相关 PR
  - 修复相关 bug
  - 提供开发者指导与支持

- 新增或修改大块代码时:
  - 如果你是协作者,务必把自己加入 [CODEOWNERS](CODEOWNERS),表明你愿意评审相关 PR
  - 如果你是贡献者,找到一位愿意长期评审并维护你代码的现有协作者
  - 提供测试改动所需的 CI 工作流(及硬件),参见 [ci/README.md](https://github.com/ggml-org/llama.cpp/tree/master/ci)

- 新代码应遵循本文档列出的各项规范(编码、命名等)。在与 `ggml` 接口不直接交互的、孤立的、特定后端代码部分允许例外。
  _(注:由于历史原因,现有代码不强制遵循此规范)_

- 涉及 server 的改动,请务必参考 [server 开发文档](./tools/server/README-dev.md)

# 文档

- 文档建设依靠社区力量
- 当你需要翻源码才能弄清某个 API 的用法时,考虑在头文件中补一段简短说明,方便后来人
- 发现文档错误或过时,请直接更新

# 资源

GitHub 的 issue、PR 和讨论中包含大量有助于熟悉代码库的信息。为方便查阅,部分重要内容在 GitHub 项目页面中做了索引:

https://github.com/ggml-org/llama.cpp/projects
