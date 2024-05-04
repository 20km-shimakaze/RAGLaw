import sys
import os
sys.path.append(os.path.split(sys.path[0])[0])
import logging

from tqdm import tqdm

import db
import utils
from sentence_transformers import SentenceTransformer


def process_sentence(model: SentenceTransformer, sentences: list)-> list:
    logging.info("processing embedding start")
    sentence_list = []
    for sentence in tqdm(sentences, desc="process sentence"):
        encode_sentence = model.encode(sentence)
        sentence_list.append(encode_sentence)
    logging.info("processing embedding finish")
    return sentence_list


utils.configure_logging()


logging.info("load model start")
model_path = "chestnutlzj/ChatLaw-Text2Vec"
model = SentenceTransformer(model_path, cache_folder="../models").cuda()
logging.info("load model finish")


logging.info("load law_data start")
law_book_path = ""
law_book_dataset = utils.load_datasets(law_book_path)['train']
law_books = []
data_list = len(law_book_dataset)
for i in tqdm(law_book_dataset, desc="processing str"):
    law_books.append(i)
ans = utils.splice_prompt(law_books, "law_book")
logging.info("load law_data finish")


# processing sentence
process_sentence(model, law_books)


