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
import json
import collections
from .data import Data
from .base_config import BaseConfig

from application_utility.translation import i18n
_ = i18n.language.gettext


class Config(BaseConfig, Data):
    """Configuration with data"""

    def load(self):
        pass

    def __init__(self, application: str):
        BaseConfig.__init__(self, application)
        Data.__init__(self)
        self.desktop = self.get_desktop()
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
        src = self.file["main"]
        logging.info(f"json to merge : {src}")
        if not src or not os.path.isfile(src):
            raise ImportError(f"ERROR: json file not found: {src}")

        shutil.copyfile(src, self._MERGE_FILE)
        logging.debug(f"json : {self._MERGE_FILE}")
        self.load_from_file(self._MERGE_FILE)

        iso_file = self.get_iso_filename()
        if iso_file:
            # iso to merge found
            #iso_json = json.loads(iso_file)
            with open(iso_file, "rb") as infile:
                iso_json = json.loads(
                    infile.read().decode("utf8"),
                    object_pairs_hook=collections.OrderedDict)
            for group in iso_json:
                print(type(group))
                print(group)
                for app in group['apps']:
                    print(app)
                    print(type(app))
                    self.append_app(group, app)
            # save merged
            self.save_apps_to_json(self._MERGE_FILE)
            # load complete json
            self.load_from_file(self._MERGE_FILE)
            #exit(0)
