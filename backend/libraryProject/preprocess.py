from utils import CustomFormatter, size_and_amount_files
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords, wordnet
import logging
import os
import pandas as pd
import tqdm as td
import string
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')


class PreProcess:
    def __init__(self, data_folder='data', dataframe_name='date.csv'):
        self.init_logger()
        self.logger.debug(f"Initializing {__class__.__name__}...")

        self.data_folder = data_folder
        self.dataframe_name = dataframe_name
        self.logger.info(f"Data folder: '{self.data_folder}'")
        self.logger.info(f"Dataframe name: '{self.dataframe_name}'")

        self.dataframe_exists = os.path.exists(dataframe_name)

        self.file_size, self.amount_files = size_and_amount_files(
            folder=data_folder)

        self.logger.info(f"Initialized {__class__.__name__}!")
        self.combine()

    def init_logger(self):
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(CustomFormatter())
        file_handler = logging.FileHandler(
            os.path.join('logs', 'PREPROCESS.log'))
        file_handler.setFormatter(CustomFormatter())

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def combine(self):
        td.tqdm.pandas()
        self.logger.debug(f"Preprocessing raw data from '{self.data_folder}'")
        if (not self.dataframe_exists):
            self.logger.warning(
                f"Dataframe '{self.dataframe_name}' does not exist")
            df = None

            with td.tqdm(total=self.file_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for file_name in os.listdir(self.data_folder):
                    file_path = os.path.join(self.data_folder, file_name)
                    try:
                        new_df = pd.read_csv(file_path)
                        new_df = new_df.progress_applymap(
                            lambda s: s.lower() if type(s) == str else s)

                        self.logger.debug("Removing puctuation...")
                        new_df.abstract = new_df.abstract.progress_apply(
                            remove_punctuation)
                        new_df.title = new_df.title.progress_apply(
                            remove_punctuation)
                        self.logger.info("Removed punction.")

                        self.logger.debug("Removing stopwords...")
                        new_df.abstract = new_df.abstract.progress_apply(
                            remove_stopwords)
                        new_df.title = new_df.title.progress_apply(
                            remove_stopwords)
                        self.logger.info("Removed stopwords.")

                        self.logger.debug("Lemmatizing...")
                        new_df.abstract = new_df.abstract.progress_apply(
                            lemmatization)
                        new_df.title = new_df.title.progress_apply(
                            lemmatization)
                        self.logger.info("Lemmatized.")

                        if (df is None):
                            df = new_df
                        else:
                            df = pd.concat([df, new_df])
                    except Exception as e:
                        self.logger.warning(f"[{file_path}] - {e}")
                    pbar.update(os.path.getsize(file_path))

            self.logger.info(f"Loaded csv: #{len(df)} rows.")
            self.dataframe = df
            self.save_dataframe()
        else:
            self.logger.info(
                f"Dataframe '{self.dataframe_name}' already exists!")

    def save_dataframe(self):
        self.logger.debug(f"Saving dataframe '{self.dataframe_name}'...")
        try:
            self.dataframe.to_csv(self.dataframe_name, index=False)
            self.logger.info(
                f"Saved dataframe '{self.dataframe_name}' successfully")
        except Exception as e:
            self.logger.warning(
                f"Failed to save dataframe '{self.dataframe_name}': {e}")


def remove_punctuation(question):
    for char in string.punctuation:
        question = str(question).replace(char, '')
    return question


def remove_stopwords(question):
    stop_words = stopwords.words("english")
    return ' '.join([word for word in question.split() if word not in stop_words])


def get_pos_tag(word):
    word_tag = nltk.pos_tag([word])
    if word_tag[0][1].startswith('J'):
        return wordnet.ADJ
    elif word_tag[0][1].startswith('V'):
        return wordnet.VERB
    elif word_tag[0][1].startswith('N'):
        return wordnet.NOUN
    elif word_tag[0][1].startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatization(sentence):
    w_tokenizer = WhitespaceTokenizer()
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word, get_pos_tag(word)) for word in w_tokenizer.tokenize(sentence)])


if __name__ == '__main__':
    pp = PreProcess()
