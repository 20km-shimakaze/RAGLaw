from law_find import LawFind
from openai import OpenAI



class ChatLaw():
    def __init__(self, url: str="http://192.168.1.48:8000/v1", api_key="not-needed"):
        super().__init__()
        self.law_find = LawFind()
        self.client_openai = OpenAI(base_url=url, api_key=api_key)
        # TODO 此处放一个类，redis存过去数据


    