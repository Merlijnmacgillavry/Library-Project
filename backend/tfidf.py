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
    def __init__(self, data_folder='data', model_name='model.pkl', dataframe_name='dataframe.csv', records_per_page=20):
        self.init_logger()
        self.logger.debug("Initializing TFIDF...")
        self.data_folder = data_folder
        self.model_name = model_name
        self.dataframe_name = dataframe_name
        self.records_per_page = records_per_page
        self.logger.info(f"Data folder: '{self.data_folder}'")
        self.logger.info(f"Model name: '{self.model_name}'")
        self.logger.info(f"Dataframe name: '{self.dataframe_name}'")
        self.logger.info(
            f"Amount of records shown per page: {self.records_per_page}")

        self.file_size, self.amount_files = size_and_amount_files(
            folder=data_folder)
        self.logger.info(
            f"Total data size is { convert_size(self.file_size)} , amount of files is {self.amount_files}")

        self.model_exists = os.path.exists(model_name)
        self.dataframe_exists = os.path.exists(dataframe_name)
        self.model_matrix = None
        self.logger.info("Initialized TFIDF.")
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
        self.logger.debug("Loading TFIDF model...")

        if ((not self.model_exists) or (not self.dataframe_exists)):
            if not self.model_exists:
                self.logger.warning(
                    f"Model '{self.model_name}' does not exist")
            if not self.dataframe_exists:
                self.logger.warning(
                    f"Dataframe '{self.dataframe_name}' does not exist")
            self.create_model()
            self.save_model()
            self.save_dataframe()
        else:
            self.logger.debug(f"Loading model '{self.model_name}'!")
            with open(self.model_name, 'rb') as file:
                self.model = pickle.load(file)
            self.logger.info("Loaded TFIDF model.")

            self.logger.debug(f"Loading dataframe '{self.dataframe_name}'!")

            self.dataframe = pd.read_csv(self.dataframe_name)
            self.logger.info("Loaded TFIDF dataframe.")

    def create_model(self):
        self.logger.debug(f"Creating model...")
        self.logger.debug(f"Loading data...")
        df = None

        with td.tqdm(total=self.file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for file_name in os.listdir(self.data_folder):
                file_path = os.path.join(self.data_folder, file_name)
                try:
                    new_df = pd.read_csv(file_path)
                    if (df is None):
                        df = new_df
                    else:
                        df = pd.concat([df, new_df])
                except Exception as e:
                    self.logger.warning(f"[{file_path}] - {e}")
                pbar.update(os.path.getsize(file_path))

        self.logger.info(f"Loaded csv: #{len(df)} rows.")

        self.logger.debug(f"Saving dataframe as '{self.dataframe_name}'")

        self.logger.debug(f"Initializing TFIDVectorizer...")
        tfidf = TfidfVectorizer(stop_words='english')

        columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                   'abstract', 'subject topic', 'publication type', 'programme']
        self.logger.debug(f"Loading columns:\n{columns}")

        self.dataframe = df
        # Create a sparse matrix of the TF-IDF values
        self.model = tfidf.fit(df[columns].apply(
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

    def save_dataframe(self):
        self.logger.debug(f"Saving dataframe '{self.dataframe_name}'...")
        try:
            self.dataframe.to_csv(self.dataframe_name, index=False)
            self.logger.info(
                f"Saved dataframe '{self.dataframe_name}' successfully")
        except Exception as e:
            self.logger.warning(
                f"Failed to save dataframe '{self.dataframe_name}': {e}")

    def search(self, query, page):
        start = (page - 1) * self.records_per_page
        end = start + self.records_per_page
        if (self.model_matrix == None):
            columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                       'abstract', 'subject topic', 'publication type', 'programme']
            self.model_matrix = self.model.transform(self.dataframe[columns].apply(
                lambda x: ' '.join(x.dropna().astype(str)), axis=1))
        query_tfidf = self.model.transform([query])
        cosine_similarities = cosine_similarity(
            query_tfidf, self.model_matrix).flatten()
        similarity_scores = sorted(
            list(enumerate(cosine_similarities)), key=lambda x: x[1], reverse=True)

        result = pd.DataFrame(columns=self.dataframe.columns)
        for i in range(start, end):
            doc_index = similarity_scores[i][0]
            result.loc[doc_index] = self.dataframe.iloc[doc_index]
            # self.logger.info(
            #     f"Document #{doc_index}: {self.dataframe.iloc[doc_index]['title']} - Similarity Score: {similarity_scores[i][1]}")

        self.logger.info("Search completed!")
        return result.to_json(orient='records')


if __name__ == '__main__':
    tfidf = TFIDF()
    print(tfidf.search("What is information retrieval?"))
