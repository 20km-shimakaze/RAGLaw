from pymilvus import MilvusClient, DataType, db, connections
from utils import get_client

# 数据库操作

def create_coll():
    """创建数据库"""
    schema = MilvusClient.create_schema(
        auto_id=True,
        enable_dynamic_field=True,
    )
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="law_type", datatype=DataType.VARCHAR, max_length=32)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)
    schema.add_field(field_name="info", datatype=DataType.VARCHAR, max_length=51200)
    
    index_params = client.prepare_index_params()

    index_params.add_index(
        field_name="id"
    )
    index_params.add_index(
        field_name="vector",
        index_type="AUTOINDEX",
        metric_type="COSINE"
    )
    # index_params.add_index(
    #     field_name="law_type",
    #     index_type="STL_SORT"
    # )
    # index_params.add_index(
    #     field_name="info",
    #     index_type="STL_SORT"
    # )

    # 创建数据库
    client.create_collection(
        collection_name="law_vec",
        schema=schema,
        index_params=index_params
    )

def drop_colle(client: MilvusClient, colle_name: str):
    client.drop_collection(
        collection_name=colle_name
    )


def check_colle_info(client: MilvusClient, name: str):
    res = client.describe_collection(
        collection_name="law_vec"
    )
    return res

def check_colle_state(client: MilvusClient, name: str):
    res = client.get_load_state(
        collection_name=name
    )
    return res

def release_colle(client: MilvusClient, name: str):
    client.release_collection(
        collection_name=name
    )

def load_colle(client: MilvusClient, name: str):
    # Milvus Standalone replica_number must 1
    client.load_collection(
        collection_name=name,
        replica_number=1
    )

# def check

if __name__ == '__main__':
    client = get_client()

