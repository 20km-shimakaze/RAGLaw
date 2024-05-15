from .law_find import LawFind
from openai import OpenAI
import utils
import logging

DEFULT_PROMPT = [
    {"role": "system", "content": "你是一个法律顾问。你总是提供既正确又有用的经过深思熟虑的回答。能够根据提供的法律信息和结合已有的知识，详细且有逻辑的回答他人问题"}
]

class ChatLaw():
    def __init__(self, url: str="http://192.168.1.48:8000/v1", api_key="not-needed"):
        super().__init__()
        self.law_find = LawFind()
        self.client_openai = OpenAI(base_url=url, api_key=api_key)
        #TODO history class    
        self.history = DEFULT_PROMPT

    
    def get_response(self, question, history):
        """ 调用openai接口, 获取回答"""
        # 用户的问题加入到message
        self.clean_history()
        for human, assistant in history:
            self.history.append({"role": "user", "content": human})
            self.history.append({"role": "assistant", "content": assistant})

        law_data = self.law_find.find_law(question, limit=3)
        prompt = "可以参考的的法律条文为\n:"
        for law_str in law_data:
            prompt += law_str + '\n'
        prompt += question

        self.history.append({"role": "user", "content": prompt})
        # 问chatgpt问题的答案
        rsp = self.client_openai.chat.completions.create(
            model="local-model",
            messages=self.history,
            temperature=0.7,
            stream=True,
            )
        # 得到的答案加入message，多轮对话的历史信息
        partial_message = ""
        for chunk in rsp:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message
        self.history.append({"role": "assistant", "content": partial_message})
        logging.info(f"\n----------\n{partial_message}\n----------\n")
        # return partial_message

    def ask(self, msg: str, temperature: float=0.7):
        rsp = self.client_openai.chat.completions.create(
            messages=msg,
            temperature=temperature,
            stream=True,
        )
        return rsp.get("choices")[0]["message"]["content"]
    
    def clean_history(self):
        self.history.clear()
        self.history = DEFULT_PROMPT



        



    