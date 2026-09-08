# 中文注释版说明:
# 本示例演示如何通过 llama-server 的 /embedding 接口并发计算多个文本嵌入(embedding),
# 并用余弦相似度衡量它们之间的语义接近程度。
# 使用方法:先启动带 --embedding 功能的 llama-server,再运行本脚本。
# (由 ggml-org/llama.cpp 中文翻译项目添加注释,代码逻辑与原版一致)
import asyncio
import asyncio.threads
import requests
import numpy as np


n = 8  # 并发请求的数量(共生成 8 个 embedding)

result = []  # 保存所有 embedding 向量

async def requests_post_async(*args, **kwargs):
    # 把阻塞的 requests.post 丢进线程池,包装成协程
    return await asyncio.threads.to_thread(requests.post, *args, **kwargs)

async def main():
    model_url = "http://127.0.0.1:6900"  # llama-server 的监听地址
    responses: list[requests.Response] = await asyncio.gather(*[requests_post_async(
        url= f"{model_url}/embedding",          # 嵌入计算接口
        json= {"content": "a "*1022}            # 请求体:长度约 1022 个 token 的重复文本
    ) for i in range(n)])

    for response in responses:
        embedding = response.json()["embedding"]  # 从响应中取出 embedding 向量
        print(embedding[-8:])                     # 只打印向量的最后 8 维作为预览
        result.append(embedding)

asyncio.run(main())

# compute cosine similarity
# 计算两两 embedding 之间的余弦相似度:
# 值越接近 1 说明两段文本语义越相似;相同内容的 embedding 之间应接近 1

for i in range(n-1):
    for j in range(i+1, n):
        embedding1 = np.array(result[i])
        embedding2 = np.array(result[j])
        # 余弦相似度 = 点积 / (模长1 * 模长2)
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        print(f"Similarity between {i} and {j}: {similarity:.2f}")
