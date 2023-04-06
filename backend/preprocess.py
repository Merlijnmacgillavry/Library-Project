import logging
import os

from utils import CustomFormatter


class PreProcess:
    def __init__(self, data_folder='data', dataframe_name='data.csv'):
        self.init_logger()
        self.logger.debug(f"Initializing {__class__.__name__}...")
        self.data_folder = data_folder
        self.dataframe_name = dataframe_name
        self.logger.info(f"Data folder: '{self.data_folder}'")
        self.logger.info(f"Dataframe name: '{self.dataframe_name}'")
        self.dataframe_exists = os.path.exists(dataframe_name)
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
        self.logger.debug(f"Preprocessing raw data from '{self.data_folder}'")
        if (not self.dataframe_exists):
            self.logger.warning(
                f"Dataframe '{self.dataframe_name}' does not exist")
            # TODO:
            # Do actual combining like in tfidf
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


if __name__ == '__main__':
    pp = PreProcess()
