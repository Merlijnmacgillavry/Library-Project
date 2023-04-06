import logging
import os
import pandas as pd
import tqdm as td
from utils import CustomFormatter, size_and_amount_files


class PreProcess:
    def __init__(self, data_folder='data', dataframe_name='data.csv'):
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


if __name__ == '__main__':
    pp = PreProcess()
