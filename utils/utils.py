import numpy as np

from pymilvus import MilvusClient
from redis import Redis

client_milvus_one = None
client_redis_one = None

def get_milvus_client(uri="http://localhost:19530"):
    global client_milvus_one
    if client_milvus_one is None:
        client_milvus_one = MilvusClient(
            uri=uri
        )
    return client_milvus_one

def get_redis_client(host="localhost", port=6379, db=0):
    global client_redis_one
    if client_redis_one is None:
        client_redis_one = Redis(
            host=host,
            port=port,
            db=db
        )
    return client_redis_one

def get_rand_vector(shape: tuple)->list:
    return np.random.rand(*shape)

def configure_logging(level=None):
    import logging
    import os
    import colorlog
    if level is None:
        level = getattr(logging, os.environ.get("LOG_LEVEL", "INFO"))
    logger = logging.getLogger()
    color_handler = colorlog.StreamHandler()
    formatter  = colorlog.ColoredFormatter(
        "%(log_color)s %(levelname)s [%(asctime)s] [%(filename)s:%(lineno)d] - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'purple',
            'INFO': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
        secondary_log_colors={},
        style='%'
    )
    color_handler.setFormatter(formatter)  # 将格式器设置给 ColorHandler
    logger.setLevel(level)  # 设置日志级别
    logger.addHandler(color_handler)  # 添加 ColorHandler 到日志记录器


if __name__ == "__main__":
    print(get_rand_vector((4, )))

