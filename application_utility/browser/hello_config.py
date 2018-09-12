import logging
import os
import sys

from .config import Config
from .exceptions import NoAppInIsoError


class HelloConfig(Config):
    """
    in manjaro-Hello only
    """

    def load(self):
        """ load data"""
        if os.path.isfile("/run/miso/bootmnt/manjaro"):
            raise NoAppInIsoError()
        else:
            if "--dev" in sys.argv:
                logging.basicConfig(level=logging.DEBUG)
            else:
                pass
            self.preferences = self.read_json_file(self._PREFERENCES)
        # TODO to set ?
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": "./data/{}.json".format(self.preferences["data-set"])}
        return self
