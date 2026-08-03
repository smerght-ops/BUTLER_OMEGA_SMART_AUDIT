# -*- coding: utf-8 -*-
MODEL_STACK = {
    "chat": ["qwen35-ru:latest", "qwen35:latest"],
    "code": ["DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest", "sub-coder-32b:latest", "codestral:latest"],
    "review": ["sub-coder-32b:latest", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"],
    "architecture": ["DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest", "butler-router-70b:latest", "sub-coder-32b:latest"],
    "vision": ["qwen2.5-vl:latest", "llama-vision:latest", "llava:latest"],
    "image": ["DeepSeek-GPU:latest", "gemma-4:latest", "ibm-granite_granite-4.1-30b-Q5_K_S:latest"],
    "memory": ["qwen35-ru:latest"],
}