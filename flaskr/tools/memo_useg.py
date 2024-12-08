import time
import os
import psutil


def memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)


print("memory useg:", memory_usage())
