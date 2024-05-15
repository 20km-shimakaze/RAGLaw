import sys
import os
sys.path.append(os.path.split(sys.path[0])[0])
from utils import get_redis_client

def test_redis_client():
    client = get_redis_client()
    assert client.set('yuzino', 'akazuki') != 0
    assert client.get('yuzino') == b'akazuki'




