#!/usr/bin/env python3
#
# This file is part of application-utility.
#
# application-utility is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# application-utility is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with application-utility.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: papajoke
#          fhdk


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
        self.application = application
        self.load()
        self.merge_json()

    def merge_json(self):
        """
            TODO
            merge desktop in main in self.json ? and merge url in file ?
            and use only self._MERGE_FILE ?
            Always save .json in self._MERGE_FILE ?
        """
        # write temp
        if self.url["main"]:
            src = f"/tmp/{self.application}-download.json"
            urllib.request.urlretrieve(self.url["main"], src)
            logging.info(f"URL: [{self.url['main']} downloaded")
        else:
            src = self.file["main"]
            logging.info(f"json to merge : {src}")
            if not os.path.isfile(src):
                logging.error(f"ERROR: File not found: {src}")
                raise ImportError(src)

        shutil.copyfile(src, self._MERGE_FILE)
        logging.debug(f"json : {self._MERGE_FILE}")
        self.load_from_file(self._MERGE_FILE)
