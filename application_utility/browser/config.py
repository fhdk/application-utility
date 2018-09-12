import logging
import os
import shutil
import urllib.request

from .data import Data
from .base_config import BaseConfig


class Config(BaseConfig, Data):
    """Configuration with data"""

    def load(self):
        pass

    def __init__(self, application: str):
        BaseConfig.__init__(self, application)
        Data.__init__(self)
        self.load()
        self.merge_json()

    def merge_json(self):
        """
            TODO
            merge desktop in main in self.json ? and merge url in file ?
            and use only self._JSON_MERGED ?
            Always save .json in self._JSON_MERGED ?
        """
        # write temp
        if self.url["main"]:
            src = "/tmp/{self.application}-download.json"
            urllib.request.urlretrieve(self.url["main"], src)
            logging.info(f"URL: [{self.url['main']} downloaded")
        else:
            src = self.file["main"]
            logging.info(f"json to merge : {src}")
            if not os.path.isfile(src):
                logging.error(f"ERROR: File not found: {src}")
                raise ImportError(src)

        shutil.copyfile(src, self._JSON_MERGED)
        logging.debug(f"json : {self._JSON_MERGED}")
        self.load_from_file(self._JSON_MERGED)
