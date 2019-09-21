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

"""
Module alpm
Install / remove packages
use pamac-installer
"""
import gi
import glob
import logging
import subprocess

gi.require_version("Pamac", "9.0")
from gi.repository import Pamac

from application_utility.translation import i18n
_ = i18n.language.gettext


class Alpm:
    """system alpm commit"""
    NOTHING = 0
    REMOVE = 1
    ADD = 2
    BOTH = 3

    def __init__(self):
        """constructor"""
        self.pkg_list_install = []
        self.pkg_list_removal = []

    def do_update(self):
        """run pamac"""
        result = Alpm.NOTHING
        if not self.pkg_list_install and not self.pkg_list_removal:
            return result
        if self.pkg_list_removal:
            refresh = self._install_apps(self.pkg_list_removal, False)
            if not refresh:
                logging.warning("warning: packages not uninstalled")
            else:
                result = Alpm.REMOVE
        if self.pkg_list_install:
            refresh = self._install_apps(self.pkg_list_install, True)
            if not refresh:
                logging.warning("warning: packages not installed")
            else:
                if result == Alpm.NOTHING:
                    result = Alpm.ADD
                else:
                    result = Alpm.BOTH
        return result

    def set_package(self, package_name: str, install: bool, installed: bool) -> None:
        """
        Add or Remove package in lists
            install: add or remove
        """
        if self.to_remove(package_name):
            self.pkg_list_removal.remove(package_name)
        else:
            if not install and installed:
                self.pkg_list_removal.append(package_name)

        if self.to_install(package_name):
            self.pkg_list_install.remove(package_name)
        else:
            if install and not installed:
                self.pkg_list_install.append(package_name)

    def clear(self) -> None:
        """clear lists packages"""
        self.pkg_list_install = []
        self.pkg_list_removal = []

    def to_install(self, package_name) -> bool:
        """package is in list ?"""
        return package_name in self.pkg_list_install

    def to_remove(self, package_name) -> bool:
        """package is in list ?"""
        return package_name in self.pkg_list_removal

    @classmethod
    def _install_apps(cls, pkg_list: list, install: bool = True) -> bool:
        """
        install or remove packages list
        test presence first package in pacman DB
        """
        if not pkg_list:
            return False
        if not install:
            install = ['--remove']
        else:
            install = []
        try:
            subprocess.run(['pamac-installer'] + install + pkg_list, capture_output=True, check=True)
        except FileNotFoundError:
            # next with pamac-qt its in all isos
            logging.warning('ERROR: Pamac not installed !')
            raise
        except subprocess.CalledProcessError as e:
            # e.returncode > 0
            logging.warning(f"ERROR in alpm commit: {e.returncode} ?\n{e.stderr}")
        # after test if "cancel" btn
        if not install:
            return cls.app_installed(pkg_list[0])
        return not cls.app_installed(pkg_list[0])

    @property
    def empty(self):
        """2 lists are empty ?"""
        return not self.pkg_list_removal and not self.pkg_list_install

    @staticmethod
    def app_installed(package: str) -> bool:
        """test if package is installed"""
        if glob.glob(f"/var/lib/pacman/local/{package}-[0-9]*"):
            return True
        return False

    def __str__(self):
        return f"pkg list install: {self.pkg_list_install}\n pkg list removal: {self.pkg_list_removal}"

    @staticmethod
    def pkg_exist(pkgname: str) ->bool:
        """check if a package exist"""
        config = Pamac.Config(conf_path="/etc/pamac.conf")
        db = Pamac.Database(config=config)
        return bool(db.search_pkgs(pkgname))
