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
import os
import logging
import tempfile
import requests
#from requests.exceptions import ConnectionError

from application_utility.constants import txt


class BaseConfig:
    """
    set config from env or plugin or standalone App
    pass this class to object ApplicationBrowser constructor())
    """
    _PREF_FILE = r"/usr/share/application-utility/preferences.json"
    _DATA_DIR = r"/usr/share/application-utility"
    _MERGE_FILE = r"/tmp/{}-preferences.json"

    def __init__(self, application: str):
        self.application = application
        self._MERGE_FILE = self._MERGE_FILE.format(application)
        self.pref = {}
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": ""}
        self.dev = "--dev" in sys.argv
        if self.dev:
            self._DATA_DIR = "./share"
            self._PREF_FILE = "./share/preferences.json"
            logging.basicConfig(stream=sys.stderr,
                                level=logging.DEBUG,
                                format='::(%(levelname)s): %(message)s')

    def load(self):
        """to override live iso ? desktop ?"""
        raise NotImplementedError

    @staticmethod
    def read_json_file(filename: str, dictionary: bool = True) ->list:
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

    def get_iso_filename(self):
        """get filename from env, if url create temp file"""
        # TODO
        # to rewrite by a maintener
        desktop = os.environ.get("XDG_SESSION_DESKTOP", "none").lower()
        # convert for some desktop parameter : exemples
        switcher = {
            "e": "enlightenment",
            "i3": "i3",
            #"openbox" : self.get_make_a_new_test_env()
        }
        desktop = switcher.get(desktop, desktop)
        # test if exist
        src = f"{self._DATA_DIR}/{desktop}.json"
        if not os.path.isfile(src):
            logging.warning("iso not found: %s", src)

            # TODO rewrite with self.preferences ... ?
            # TODO use txt.OFFICIAL_ISO_URL
            if desktop in ("xfce", "kde", "gnome"):
                src = f"https://gitlab.manjaro.org/profiles-and-settings/iso-profiles/tree/master/manjaro/{desktop}.json"
            else:
                src = f"https://gitlab.manjaro.org/profiles-and-settings/iso-profiles/tree/master/community/{desktop}.json"
            logging.debug("find iso url: %s", src)
            try:
                ret = requests.head(src, allow_redirects=True)
                if ret.status_code < 300:
                    logging.info("iso json to use: %s", src)
                    request = requests.get(src, allow_redirects=True)
                    tmp_file = tempfile.NamedTemporaryFile(delete=False)
                    tmp_file.write(request.content)
                    tmp_file.close()
                    return tmp_file.name
                else:
                    logging.debug("url %s bad access", src)
            except requests.exceptions.ConnectionError:
                logging.debug("url %s not found", src)
            except requests.exceptions.MissingSchema:
                logging.debug("bad url %s", src)
            return None
        else:
            return src
