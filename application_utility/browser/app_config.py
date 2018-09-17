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
import requests
import sys

from .config import Config


class AppConfig(Config):
    """
    for Stand-alone application
    """

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
                        logging.info(f"json to use: f{self.url['main']}")
                        # TODO save in self._MERGE_FILE
                    except ConnectionError:
                        logging.critical('json data not found')
                    # else:
                    # self.file["main"] = file
        return self
