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

import collections
import json
import sys


class BaseConfig:
    """
    set config from env or plugin or standalone App
    pass this class to object ApplicationBrowser constructor())
    """
    _PREF_FILE = r"/usr/share/application-utility/preferences.json"
    _DATA_DIR = r"/usr/share/application-utility"
    _MERGE_FILE = r"/tmp/application-preferences.json"

    def __init__(self, application: str):
        self.application = application
        self.pref = {}
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": ""}
        self.dev = "--dev" in sys.argv

    def load(self):
        """to override live iso ? desktop ?"""
        raise NotImplementedError

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
