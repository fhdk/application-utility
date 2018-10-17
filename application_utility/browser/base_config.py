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
# from requests.exceptions import ConnectionError

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
            if os.environ.get("PLUGIN_HELLO"):
                # running as plugin - env set in launch.sh
                self._DATA_DIR = os.environ.get("PYTHONPATH") + "/share"
                self._PREF_FILE = f"{self._DATA_DIR}/preferences.json"
            else:
                # running as standalone
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

    @staticmethod
    def get_arg_value(key: str, default: str = "") ->str:
        """read param value"""
        for arg in sys.argv:
            if arg.lower().startswith(f"--{key}="):
                value = arg[len(key)+3:]
                if value.startswith('"'):
                    value = value[1:-1]
                return value
        return default

    def get_datafile(self, filedefault: str, key: str = "file") ->str:
        """read param,
        if value is url then download file
        return empty if not exists
        """
        arg_file = self.get_arg_value(key, filedefault)
        if arg_file.startswith("http"):
            arg_file = self.download_file(arg_file)
        if os.path.isfile(arg_file):
            return arg_file
        else:
            logging.warning("File not exist ? %s", arg_file)

    @staticmethod
    def download_file(src: str) ->str:
        """download file in tmp file
            return file name
        """
        try:
            ret = requests.head(src, allow_redirects=True)
            if ret.status_code < 300:
                logging.info("iso json to use: %s", src)
                request = requests.get(src, allow_redirects=True)
                # TODO create /tmp/m-apps ?
                tmp_file = tempfile.NamedTemporaryFile(delete=False) # dir="m-apps"
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

    @staticmethod
    def get_desktop() ->str:
        """ get local desktop"""
        desktop = BaseConfig.get_arg_value("desktop")
        if not desktop:
            desktop = os.environ.get("DESKTOP_SESSION", "?").lower()
            switcher = {
                "budgie-desktop": "budgie",
                "/usr/share/xsessions/plasma": "kde",
                "/usr/share/xsessions/lxqt": "lxqt",
                "jade": "webdad",
                "/usr/share/xsessions/jwm": "jwm",
                "awesome": "awesome",
                "bspwm": "bspwm",
                "cinnamon": "cinnamon",
                "deepin": "deepin",
                "i3": "i3",
                "lxde": "lxde",
                "mate": "mate",
                "openbox": "openbox",
                "gnome": "gnome",
                "xfce": "xfce",
            }
            desktop = switcher.get(desktop, "?")
        return desktop.lower()

    @staticmethod
    def get_manjaro_desktop(find_desktop: str, prefix: bool = True) ->str:
        """return generator on all manjaro desktop available"""
        desks = ["xfce", "kde", "gnome"]
        if find_desktop in desks:
            if prefix:
                find_desktop = "manjaro/"+find_desktop
            return find_desktop
        desks = ["openbox", "mate", "deepin", "bspwm", "cinnamon", "lxqt", "awesome", "budgie", "lxde", "i3", "webdad"]
        if find_desktop in desks:
            if prefix:
                find_desktop = "community/"+find_desktop
            return find_desktop
        return ""

    #TODO to remove or move to tests
    @staticmethod
    def get_desktop_tests():
        for test in ["LXDE", "lxde", 'MATE', 'mate', "budgie-desktop", "/usr/share/xsessions/plasma"]:
            os.environ["DESKTOP_SESSION"] = test
            desktop = BaseConfig.get_desktop()
            print("desktop", desktop, "for env:"+test)
            desktop = BaseConfig.get_manjaro_desktop(desktop)
            print("\t", desktop)

    def get_iso_filename(self) ->str:
        """get filename from env, if url create temp file
        can use parameter: 
            app.py --iso="https://gitlab.manjaro.org/papajoke/application-utility/raw/dev/share/kde.json"
            app.py --iso="/home/****.json"
            app.py --desktop=gnome
        """
        # TODO
        # to rewrite by a maintener

        desktop = self.get_desktop()
        # test if exist
        src = f"{self._DATA_DIR}/{desktop}.json"
        src = self.get_datafile(src, "iso")
        if src and not os.path.isfile(src):
            logging.warning("iso not found: %s", src)

            # TODO use txt.OFFICIAL_ISO_URL
            desktop = self.get_manjaro_desktop(desktop)
            if desktop:
                src = f"https://gitlab.manjaro.org/profiles-and-settings/iso-profiles/raw/manjaro-architect/{desktop}/apps.json"
                logging.debug("find iso url: %s", src)
                return self.download_file(src)
        else:
            return src

#test desktops
#BaseConfig.get_desktop_tests()
#exit(0)
