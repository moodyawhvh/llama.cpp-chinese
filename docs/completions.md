> 🌐 本文档由 [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) 翻译,英文原版见原项目。

# 命令行补全

部分环境支持命令行补全。

## Bash 补全

```bash
$ build/bin/llama-cli --completion-bash > ~/.llama-completion.bash
$ source ~/.llama-completion.bash
```

也可以把它加进 `.bashrc` 或 `.bash_profile` 实现自动加载。例如:

```console
$ echo "source ~/.llama-completion.bash" >> ~/.bashrc
```
