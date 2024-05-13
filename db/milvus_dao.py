# 数据库操作
from pymilvus import MilvusClient

# vector = utils.get_rand_vector(shape=(768, ))
#     client = utils.get_client()
#     data = [
#         {"vector": vector, "law_type": "law_book", "info": "今天是遇到了一条狗"}
#     ]
#     res = insert_data(client, data, "law_vec")
#     print(res)
def insert_data(client: MilvusClient, data: list, colle_name: str):
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

def upsert_data(client: MilvusClient, data: list, colle_name: str):
    """主键重复更新，否则插入"""
    res = client.upsert(
        collection_name=colle_name,
        data=data
    )
    return res

def search_single_vector(client: MilvusClient, data: list, colle_name:str, output_fields: list=None, limit: int=1, search_params={"metric_type": "COSINE", "params": {}}):
    """查找与给定查询向量最相似的向量"""
    res = client.search(
        collection_name=colle_name,
        data=data,
        limit=limit,
        output_fields=output_fields
    )
    return res

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.split(sys.path[0])[0])
    import utils
    import db.milvus_database as milvus_database
    client = utils.get_client()
    milvus_database.load_colle(client, "law_vec")
    # print(database.check_colle_info(client, "law_vec"))
    data = utils.get_rand_vector((768, ))
    # res = delete_data(client, "id in [449481636260111509, 449481636260111507, 449481636260111505]", "law_vec")
    res = search_single_vector(client, [data], "law_vec", limit=2, output_fields=["info"])[0][0]
    print(res)


    