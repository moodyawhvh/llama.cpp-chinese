#!/usr/bin/env bash

# 中文注释版说明:
# 本脚本演示 ReAct(Reason + Act,推理-行动)模式的运行方式:
# 用 prompts/reason-act.txt 作为提示词,让模型交替输出 "Thought / Action / Observation",
# 通过 -r 参数把 "Question:" 和 "Observation:" 作为交互的重新触发点。
# 运行前请先构建 llama-cli,并确保 prompts/reason-act.txt 存在。
# (由 ggml-org/llama.cpp 中文翻译项目添加注释,代码逻辑与原版一致)

cd `dirname $0`
cd ..

# 若第一个参数为 -m,则取第二个参数作为模型路径,否则使用默认模型
if [ "$1" == "-m" ]; then
  MODEL="-m $2 "
fi

./llama-cli $MODEL --color \
    -f ./prompts/reason-act.txt \
    -i --interactive-first \
    --top_k 10000 --temp 0.2 --repeat_penalty 1 -t 7 -c 2048 \
    -r "Question:" -r "Observation:" --in-prefix " " \
    -n -1
