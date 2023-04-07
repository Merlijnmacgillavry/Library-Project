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
from transformers import AutoTokenizer, TFAutoModel


class SBERT:
    def __init__(self, model_name=f'SBERT_model.pkl', data_name='data.csv', records_per_page=20):
        self.init_logger()
        self.logger.debug(f"Initializing {__class__.__name__}...")

        self.model_name = model_name
        self.data_name = data_name
        self.records_per_page = records_per_page

        self.logger.info(f"Model name: '{self.model_name}'")
        self.logger.info(f"Data name: '{self.data_name}'")
        self.logger.info(
            f"Amount of records shown per page: {self.records_per_page}")

        self.model_exists = os.path.exists(model_name)
        self.data_exists = os.path.exists(data_name)

        self.sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

        self.logger.info(f"Initialized {__class__.__name__}.")
        self.load_model()

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
            self.model = self.model.numpy()
            self.logger.info(f"Loaded {__class__.__name__} model.")
            self.logger.debug(f"Loading data '{self.data_name}'!")
            self.data = pd.read_csv(self.data_name)
            self.logger.info(f"Loaded {__class__.__name__} data.")

    def create_model(self):
        td.pandas()
        data = self.data
        self.logger.debug("Combining texts...")
        text = data.progress_apply(
            lambda row: self.combine_text(row), axis=1)
        self.logger.info("Combined texts..")

        self.logger.debug("encoding corpus")

        embeddings = self.sbert_model.encode(text, show_progress_bar=True)
        print(embeddings)
        self.logger.info("encoded documents")
        self.model = embeddings

    def search(self, query, page):
        td.pandas()

        self.logger.debug(f"Searching for '{query}' on page {page}...")

        start = (page - 1) * self.records_per_page

        query_embedding = self.sbert_model.encode(query)
        query_embedding = query_embedding.numpy()
        print(query_embedding.shape)

        self.data['embedding'] = self.model['embedding']
        self.data['similarity'] = self.data['embedding']
        print(self.data.head())

    def find_similarity(self, doc_embedding, query_embedding):
        doc_embedding = np.fromstring(doc_embedding).reshape((1, -1))
        query_embedding = np.array(query_embedding).reshape((1, -1))
        try:
            return np.dot(doc_embedding.T, query_embedding)

        except Exception as e:
            self.logger.error(f"Exception thrown: {e}")
            return 0

    def combine_text(self, row):
        columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                   'abstract', 'subject topic', 'publication type', 'programme']
        text = ''.join([str(row[col]) if not pd.isna(
            row[col]) else ' ' for col in columns])
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
    sbert = SBERT()
    sbert.search("what is info retrieval", 1)
