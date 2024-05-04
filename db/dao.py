# 数据库操作
from pymilvus import MilvusClient
import utils

# vector = utils.get_rand_vector(shape=(768, ))
#     client = utils.get_client()
#     data = [
#         {"vector": vector, "law_type": "law_book", "info": "今天是遇到了一条狗"}
#     ]
#     res = insert_data(client, data, "law_vec")
#     print(res)
def insert_data(client: MilvusClient, data: dict, colle_name: str):
    res = client.insert(
        collection_name=colle_name,
        data=data
    )
    return res

def delete_data(client: MilvusClient, filter: str, colle_name: str):
    res = client.delete(
        collection_name=colle_name,
        filter=filter
    )
    return res

if __name__ == "__main__":
    pass
    