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

    def load(self):
        """ load file or url by parameter console"""
        self.preferences = self.read_json_file(self._PREFERENCES.format(self.application))
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": "/usr/share/{}/{}.json".format(self.application,
                                                                           self.preferences['data_set'])}
        if self.dev:
            self.file = {"desktop": "", "main": "share/{}.json".format(self.preferences['data_set'])}
        if len(sys.argv) > 1:
            file = sys.argv[1]
            if os.path.isfile(file):
                self.file["main"] = file
            else:
                try:
                    requests.get(file)
                    # TODO save in self._JSON_MERGED
                except ConnectionError:
                    logging.critical('json data not found')
                else:
                    self.url["main"] = file
        return self
