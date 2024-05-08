import utils
from sentence_transformers import SentenceTransformer
import db

class LawFind():
    def __init__(self, model_path: str="chestnutlzj/ChatLaw-Text2Vec", colle_name: str="law_vec"):
        self.client = utils.get_client()
        self.colle_name = colle_name
        db.load_colle(self.client, self.colle_name)
        self.embadding_model = SentenceTransformer(model_path, cache_folder="./models").cuda()

    def find_law(self, text: str, limit: int=3):
        """查找对应句子中数据库最接近的limit条数据"""
        encoded_sentence = self.embadding_model.encode(text)
        res = db.search_single_vector(self.client, [encoded_sentence], self.colle_name, output_fields=['info'], limit=limit)[0]
        return [data['entity']['info'] for data in res]


