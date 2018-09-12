import logging
import os
import sys

from .config import Config


class HelloConfig(Config):
    """
    in manjaro-Hello only
    """

    def load(self):
        """ load datas"""
        if os.path.isfile("/run/miso/bootmnt/manjaro"):
            # raise NoAppInIsoError()
            self.preferences = self.read_json_file(f"/usr/share/manjaro-hello/data/preferences.json")
        else:
            if "--dev" in sys.argv:
                logging.basicConfig(level=logging.DEBUG)
                self.preferences = self.read_json_file("data/preferences.json")
            else:
                self.preferences = self.read_json_file(f"/usr/share/manjaro-hello/data/preferences.json")
        # TODO to set ?
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": "./data/{}.json".format(self.preferences["data_set"])}
        return self
