import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from utils import *
import logging
import scipy.sparse
import tqdm as td
import pickle


class TFIDF:
    def __init__(self, model_name='TFIDFmodel.pkl', data_name='data.csv', records_per_page=20):
        self.init_logger()
        self.logger.debug("Initializing TFIDF...")

        self.model_name = model_name
        self.data_name = data_name
        self.records_per_page = records_per_page

        self.logger.info(f"Model name: '{self.model_name}'")
        self.logger.info(f"Data name: '{self.data_name}'")
        self.logger.info(
            f"Amount of records shown per page: {self.records_per_page}")

        self.model_exists = os.path.exists(model_name)
        self.data_exists = os.path.exists(data_name)
        self.model_matrix = None
        self.logger.info(f"Initialized {__class__.__name__}.")
        self.load_model()

    def init_logger(self):
        self.logger = logging.getLogger('TFIDF')
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CustomFormatter())
        file_handler = logging.FileHandler(os.path.join('logs', 'TFIDF.log'))
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
        self.logger.info("Loaded TFIDF data.")

        if ((not self.model_exists)):
            if not self.model_exists:
                self.logger.warning(
                    f"Model '{self.model_name}' does not exist")
            if not self.data_exists:
                self.logger.warning(
                    f"Data'{self.data_name}' does not exist")
            self.create_model()
            self.save_model()
        else:
            self.logger.debug(f"Loading model '{self.model_name}'!")
            with open(self.model_name, 'rb') as file:
                self.model = pickle.load(file)
            self.logger.info("Loaded TFIDF model.")

        self.logger.debug(f"Loading model matrix...")
        columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                   'abstract', 'subject topic', 'publication type', 'programme']
        self.model_matrix = self.model.transform(self.data[columns].apply(
            lambda x: ' '.join(x.dropna().astype(str)), axis=1))
        self.logger.info(f"Model matrix loaded!")

    def create_model(self):
        self.logger.debug(f"Creating model...")

        self.logger.debug(f"Initializing TFIDVectorizer...")
        tfidf = TfidfVectorizer(stop_words='english')

        columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                   'abstract', 'subject topic', 'publication type', 'programme']

        self.logger.debug(f"Loading columns:\n{columns}")

        # Create a sparse matrix of the TF-IDF values
        self.model = tfidf.fit(self.data[columns].apply(
            lambda x: ' '.join(x.fillna("").astype(str)), axis=1))

        self.logger.info(f"Created model.")

    def save_model(self):
        self.logger.debug(f"Saving model {self.model_name}...")
        try:
            with open(self.model_name, 'wb') as file:
                pickle.dump(self.model, file)
            self.logger.info(f"Saved model '{self.model_name}' successfully")
        except Exception as e:
            self.logger.error(
                f"Failed to save model '{self.model_name}': {e}")

    def search(self, query, page):
        self.logger.debug(f"Searching for '{query}' on page {page}...")
        start = (page - 1) * self.records_per_page
        end = start + self.records_per_page

        query = query.lower()

        query_tfidf = self.model.transform([query])

        cosine_similarities = cosine_similarity(
            query_tfidf, self.model_matrix).flatten()

        similarity_scores = sorted(
            list(enumerate(cosine_similarities)), key=lambda x: x[1], reverse=True)

        result = pd.DataFrame(columns=self.data.columns)

        for i in range(start, end):
            doc_index = similarity_scores[i][0]
            result.loc[doc_index] = self.data.iloc[doc_index]
            # self.logger.info(
            #     f"Document #{doc_index}: {self.dataframe.iloc[doc_index]['title']} - Similarity Score: {similarity_scores[i][1]}")

        self.logger.info("Search completed!")
        return result.to_json(orient='records')


if __name__ == '__main__':
    tfidf = TFIDF()
    # print(tfidf.search("What is information retrieval?", 12))
