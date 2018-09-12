import logging
import os
import sys

from .config import Config
from .exceptions import NoAppInIsoError


class HelloConfig(Config):
    """
    Created in Manjaro-Hello
    """

    def load(self):
        """ load data"""
        if os.path.isfile("/run/miso/bootmnt/manjaro"):
            raise NoAppInIsoError()
        else:
            if "--dev" in sys.argv:
                logging.basicConfig(level=logging.DEBUG)
            else:
                logging.basicConfig(level=logging.DEBUG)
        logging.debug("_PREF_FILE is", self._PREF_FILE)
        self.pref = self.read_json_file(self._PREF_FILE)
        # TODO to set ?
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": "{}/{}.json".format(self._DATA_DIR, self.pref["data-set"])}
        logging.debug("self.file is", self.file)
        return self
