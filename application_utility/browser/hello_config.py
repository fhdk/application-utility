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
        logging.debug("_DATA_DIR is %s", self._DATA_DIR)
        logging.debug("_PREF_FILE is %s", self._PREF_FILE)
        self.pref = self.read_json_file(self._PREF_FILE)
        # TODO to set ?
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": f"{self._DATA_DIR}/{self.pref['data-set']}.json"}
        self.file["main"] = self.get_datafile(self.file["main"], "file")
        logging.debug("self.file is %s", self.file)
        return self
