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
import glob
import json
import logging
import os
from typing import Iterator

import gi

# /usr/share/gir-10.0/Pamac-9.0.gir
gi.require_version("Pamac", "9.0")
from gi.repository import Pamac

from application_utility.translation import i18n

_ = i18n.language.gettext


class Data:
    def __init__(self):
        self.filename = ""
        self._json = []
        self.filter = ""
        self.group = "*"
        self.desktop = [os.environ.get("XDG_SESSION_DESKTOP", "?").lower()]

    def load_from_file(self, filename: str = ''):
        """
        load json file
        :param filename:
        """
        if filename:
            self.filename = filename
        self._json = self._read_json_file(filename, True)
        # self.__dict__.update(self.json) ??
        # ValueError: dictionary update sequence element #0 has length 4; 2 is required
        # self.all()

    # @property
    # def filter(self) -> str:
    #     return self.filter
    #
    # @filter.setter
    # def filter(self, value: str) ->None:
    #     self.filter = value

    @property
    def json(self) -> list:
        """
        return json but with filters:
            - desktop : self.desktop
            - advanced 0/1 : self.filter
        """
        logging.debug("\n--- read data.json with FILTERS ---\n")
        logging.debug(f"my desktop: {self.desktop}")
        logging.debug(f"filter    : {self.filter}")
        logging.debug(f"groups    : {self.group}")
        result = []
        """
        filter apps based on desktop
        what about WM like openbox?
        create a user choice?
        """
        for group in self._json:
            if self.group != "*":
                if group['name'] != self.group:
                    logging.debug(f"filter group : {group['name']} <> {self.group}")
                    continue

            try:
                if self.filter not in group["filter"]:
                    logging.debug(f"filter group : {group['name']} {group['filter']} < {self.filter}")
                    continue

            except KeyError:
                # not in json file
                pass

            result.append({"name": f"{group['name']}",
                           "icon": f"{group['icon']}",
                           "description": f"{group['description']}",
                           "apps": []})

            for app in group["apps"]:
                try:
                    if self.filter not in app["filter"]:
                        logging.debug(f"\tfilter app: {app['name']} {app['filter']} < {self.filter}")
                        continue
                except KeyError:
                    pass

                """
                add desktop filters
                    "desktop": ["kde","gnome"] = only for kde and gnome
                    "desktop": ["!kde","!gnome"] = all except for kde and gnome
                    -
                    this should probably be a user choice
                """
                keys = app.get('desktop', [])

                if keys:
                    if f"!{self.desktop}" in keys:
                        logging.debug(f"\tfilter desktop(not for): {app['name']} {app['desktop']} < {self.desktop}")
                        # continue

                keys = [x for x in keys if not x.startswith("!")]
                if keys:
                    if self.desktop != "?" and self.desktop not in keys:
                        logging.debug(f"\tfilter desktop(for): {app['name']} {app['desktop']} < {self.desktop}")
                        # continue

                result[-1]["apps"].append(app)
        return result

    @classmethod
    def _read_json_file(cls, filename: str, dictionary: bool = True) -> list:
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

            # transform strcture/datas
            db = Pamac.Database(config=Pamac.Config(conf_path="/etc/pamac.conf"))
            db.enable_appstream()
            for group in result:
                for app in group["apps"]:
                    app["group"] = group['name']  # add for self.all()
                    app["installed"] = cls.app_installed(app["pkg"])
                    """
                    TEST
                    use pamac/appstream for locale description
                    """
                    app['appstream'] = False
                    detail = db.get_pkg(app['pkg'])
                    if detail:
                        app['appstream'] = True
                        d = detail.get_desc()
                        if d:
                            if len(d) > 58:
                                d = d[:56] + ".."
                            app['description'] = d
                        # app['icon'] = detail.get_icon() why not ?

        except OSError:
            pass
        return result

    def save_apps_to_json(self, filename):
        with open(filename, "w") as data_file:
            json.dump(self._json, data_file, indent=2)  # sort_keys=True
            data_file.flush()

    @property
    def categories(self) -> Iterator[str]:
        """
        return all groups in .json -> Generator
        usage:
            print('groups: [%s]' % ', '.join(map(str, .config_plugin.categories)))
        """
        # i18 = i18n_categories()
        try:
            return (g['name'] for g in self.json)
        except KeyError as err:
            logging.critical(f"\n::Error: Bad json format ! [{err}] not found")
            raise

    def __contains__(self, category) -> bool:
        """
        usage: if 'Internet' in config:
        """
        return category in self.categories

    def all(self):
        """
        useful for find one application by name or package
        used by __call__ AppData()
        usage:
            s="Calibre"
            a = [x for x in self.config_plugin.all() if x["name"] == s or x["pkg"] == s ]
        """
        for g in self.json:
            for a in g['apps']:
                yield a

    def __call__(self, name: str):
        """
        find one application

        usage:
            conf.apps('pacman')
        """
        founds = [x for x in self.all() if x["name"] == name or x["pkg"] == name]
        if founds:
            return founds[0]

    def append_app(self, group, app):
        """add one application in database"""
        if not group['group'] in self:
            # create group
            print(f" group {group['group']} not exist ")
            self._json.append({
                "name": group['group'],
                "apps": [],
                "icon": "emblem-new",
                "description": "new group by iso json"
            })
            # TODO set default attributes in generator "desktop".json
            print(set(self.categories))

        else:
            print(f" group {group['group']} exist ")
        # exit(1)
        if not app.get('name'):
            app['name'] = app['pkg']
        if not app.get('icon'):
            app['icon'] = "emblem-package"
        for g in self._json:
            if g["name"] == group["group"]:
                logging.debug(f"Add iso app: {app['name']} in group: %s", group["group"])
                g["apps"].append(app)
                # exit(1)

    @staticmethod
    def app_installed(package: str) -> bool:
        if glob.glob(f"/var/lib/pacman/local/{package}-[0-9]*"):
            return True
        return False
