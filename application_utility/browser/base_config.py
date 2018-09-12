import collections
import json
import sys


class BaseConfig:
    """
    set config from env or plugin or standalone App
    pass this class to object ApplicationBrowser constructor())
    """
    _PREF_FILE = r"/usr/share/application-utility/preferences.json"
    _DATA_DIR = r"/usr/share/applications-utility"
    _JSON_MERGED = r"/tmp/application-preferences.json"

    def __init__(self, application: str):
        self.application = application
        self.pref = {}
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": ""}
        self.dev = "--dev" in sys.argv

    def load(self):
        """to override live iso ? desktop ?"""
        raise NotImplementedError

    # @property
    # def filter(self) ->str:
    #     return self.apps.filter
    #
    # @filter.setter
    # def filter(self, value: str) ->None:
    #     self.apps.filter = value

    @staticmethod
    def read_json_file(filename, dictionary=True):
        """
        Read json data from file
        """
        result = list()
        try:
            if dictionary:
                with open(filename, "rb") as infile:
                    result = json.loads(
                        infile.read().decode("utf8"),
                        object_pairs_hook=collections.OrderedDict)
            else:
                with open(filename, "r") as infile:
                    result = json.load(infile)
        except OSError:
            pass
        return result
