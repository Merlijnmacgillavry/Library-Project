import json
import os
import pickle
import backoff
import numpy as np
import openai
import pandas as pd
import logging
from utils import CustomFormatter
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm as td
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi, BM25L, BM25Plus


class BM25:
    def __init__(self, model_name=f'model.pkl', data_name='data.csv', bm_type="Plus", records_per_page=20):
        self.bm_type = bm_type
        self.model_name = f"BM25{bm_type}{model_name}"
        self.init_logger()
        self.logger.debug(f"Initializing {__class__.__name__}...")

        self.data_name = data_name
        self.records_per_page = records_per_page

        self.logger.info(f"Model name: '{self.model_name}'")
        self.logger.info(f"Data name: '{self.data_name}'")
        self.logger.info(
            f"Amount of records shown per page: {self.records_per_page}")

        self.model_exists = os.path.exists(self.model_name)
        self.data_exists = os.path.exists(data_name)

        self.logger.info(f"Initialized {__class__.__name__}.")
        self.load_model()

    def create_BM25(self, tokenized_corpus):
        match self.bm_type:
            case "Okapi":
                self.model = BM25Okapi(tokenized_corpus)
            case "L":
                self.model = BM25L(tokenized_corpus)
            case "Plus":
                self.model = BM25Plus(tokenized_corpus)
            case _:
                self.logger.error(
                    f"Bad input! - Wrong BM-model provided: `{self.bm_type}` can only use ['Okapi', 'L', 'Plus' ]")
        self.logger.info(f"Created `BM{self.bm_type}` model!")

    def init_logger(self):
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CustomFormatter())
        file_handler = logging.FileHandler(
            os.path.join('logs', f"{__class__.__name__}.log"))
        file_handler.setFormatter(CustomFormatter())

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def load_model(self):
        self.logger.debug(f"Loading {__class__.__name__} model...")
        if (not self.data_exists):
            self.logger.error(
                f"Failed to load data! - File '{self.data_name}' does not exist!")
            return

        self.logger.debug(f"Loading data '{self.data_name}'!")
        self.data = pd.read_csv(self.data_name)
        self.logger.info(f"Loaded {__class__.__name__} data.")

        if ((not self.model_exists)):
            if not self.model_exists:
                self.logger.warning(
                    f"Model '{self.model_name}' does not exist")
            self.create_model()
            self.save_model()
        else:
            self.logger.debug(f"Loading model '{self.model_name}'!")
            with open(self.model_name, 'rb') as file:
                self.model = pickle.load(file)
            self.logger.info(f"Loaded {__class__.__name__} model.")
            self.logger.debug(f"Loading data '{self.data_name}'!")
            self.data = pd.read_csv(self.data_name)
            self.logger.info(f"Loaded {__class__.__name__} data.")

    def create_model(self):
        self.logger.debug(f"Creating model...")
        td.pandas()
        data = self.data
        tokenized_corpus = data.progress_apply(
            lambda row: self.embed_text(row), axis=1)
        self.create_BM25(tokenized_corpus)
        self.logger.info(f"Created model.")

    def search(self, query, page):
        self.logger.debug(f"Searching for '{query}' on page {page}...")

        query = query.lower()
        start = (page - 1) * self.records_per_page

        tokenized_query = query.split(" ")
        doc_scores = self.model.get_scores(tokenized_query)
        df = pd.DataFrame({'scores': doc_scores})

        sorted_scores = df.sort_values(['scores'], ascending=[False])
        indexes = sorted_scores[start:start+20]
        print(indexes.index.values.tolist())
        res = []
        for doc_index in indexes.index.values:
            res.append(self.data.loc[doc_index])
        dataframe = pd.DataFrame(res)
        self.logger.info("Search completed!")
        return dataframe.to_json(orient='records')

    def embed_text(self, row):
        columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                   'abstract', 'subject topic', 'publication type', 'programme']
        text = ''.join([str(row[col]) if not pd.isna(
            row[col]) else ' ' for col in columns])
        text = text.split(" ")
        return text

    def save_model(self):
        self.logger.debug(f"Saving model {self.model_name}...")
        try:
            with open(self.model_name, 'wb') as file:
                pickle.dump(self.model, file)
            self.logger.info(f"Saved model '{self.model_name}' successfully")
        except Exception as e:
            self.logger.error(
                f"Failed to save model '{self.model_name}': {e}")


if __name__ == '__main__':
    bm25 = BM25()
    print(bm25.search("what is info retrieva", 1))
