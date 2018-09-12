#!/usr/bin/env python3

import logging
import os
import requests
import sys

from .config import Config


class AppConfig(Config):
    """
    for Stand-alone application
    """

    def __init__(self):
        super().__init__(application="application-utility")

    def load(self):
        """ load file or url by parameter console"""
        self.pref = {"data-set": "default"}
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": f"{self._DATA_DIR}/default.json"}
        if len(sys.argv) > 1:  # and not "--dev" in sys.argv:
            file = sys.argv[1]
            if os.path.isfile(file):
                self.file["main"] = file
            else:
                if file.startswith("http"):
                    try:
                        # TODO make only head() ?
                        requests.get(file)
                        self.url["main"] = file
                        logging.info(f"json to use: [{self.url['main']}")
                        # TODO save in self._JSONMERGED
                    except ConnectionError:
                        logging.critical('json data not found')
                    # else:
                    # self.file["main"] = file
        return self
