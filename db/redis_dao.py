import redis
from utils import get_redis_client


def upsert(key, value):
    client = get_redis_client()
    return client.set(key, value)

def delete(key):
    client = get_redis_client()
    return client.delete(key)

def search(key):
    client = get_redis_client()
    return client.get(key)
