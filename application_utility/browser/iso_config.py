#!/usr/bin/env python
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


import os

from .config import Config


class IsoConfig(Config):
    """
    for iso only ?
    usefull ? not sure ...
    "live_path": "/run/miso/bootmnt/manjaro",
    """

    def __init__(self, application):
        # raise NoAppInIsoError()
        if not os.path.isfile(self.pref["live_path"]):
            raise ImportError(path=self.pref["live_path"])
        super().__init__(application)

    def load(self):
        """to override live iso ? desktop ?"""
        # TODO to set
        self.url = {"desktop": "", "main": ""}
        self.file = {"desktop": "", "main": ""}
        return self
