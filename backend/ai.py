import os
import backoff
import numpy as np
import openai
import pandas as pd
import logging
from utils import CustomFormatter
from dotenv import load_dotenv, find_dotenv
import tqdm as td


class AI:
    def __init__(self, model_name=f'openai_model.csv', data_name='data.csv', records_per_page=20):
        load_dotenv(find_dotenv())
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

        openai.api_key = os.environ['OPEN_AI_KEY']

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
                self.model = pd.read_csv(file)
            self.logger.info(f"Loaded {__class__.__name__} model.")
            print(self.model["embeddings"].head())
            # self.logger.debug(f"Loading data '{self.data_name}'!")

            # self.data = pd.read_csv(self.data_name)

            # self.logger.info("Loaded TFIDF data.")

    def create_model(self):
        embeddings = []
        amount_slices = 200
        slices = np.array_split(self.data, amount_slices)
        columns = ['title', 'author', 'research group', 'contributor', 'publication year',
                   'abstract', 'subject topic', 'publication type', 'programme']
        with td.tqdm(total=amount_slices) as pbar:
            for i in range(amount_slices):
                slice = slices[i][columns]
                text_slice = slice.apply(lambda x: ''.join(
                    [str(x[col]) if not pd.isna(x[col]) else ' ' for col in slice.columns]), axis=1)
                response = completions_with_backoff(
                    input=text_slice.to_list(), model="text-embedding-ada-002")
                for x in range(len(response.data)):
                    embeddings.append(response['data'][x]['embedding'])
                pbar.update(1/amount_slices * 100)

        self.model = pd.DataFrame({'embedding': embeddings})

    def save_model(self):
        self.model.to_csv(self.model_name)


@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    res = openai.Embedding.create(**kwargs)
    return res


if __name__ == '__main__':
    openai = AI()
