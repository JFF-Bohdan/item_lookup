import os

import psutil


def get_current_memory_usage() -> int:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss
