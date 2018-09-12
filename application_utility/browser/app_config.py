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
        self.pref = self.read_json_file(self._PREF_FILE)
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": "/usr/share/{}/{}.json".format(
            self.application, self.pref["data-set"])}

        if self.dev:
            self.file = {"desktop": "", "main": "share/{}.json".format(self.pref["data-set"])}
        if len(sys.argv) > 1 and "--dev" not in sys.argv:
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
