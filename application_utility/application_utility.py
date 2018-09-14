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
# Authors: fhdk
#          papajoke

import gi
import requests
from requests.exceptions import ConnectionError
import os
import logging
import sys

from .browser.app_config import AppConfig
from .browser.application_browser import ApplicationBrowser
from application_utility.__init__ import __version__

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf

# print(dir(gi.repository.Gtk))
# cat /usr/lib/python3.7/site-packages/gi/overrides/Gtk.py
# doc api
# https://lazka.github.io/pgi-docs/Gtk-3.0/index.html


class MainApp:

    def __init__(self):
        """main app window"""
        window = Gtk.Window(title=f"Manjaro Application Utility {__version__}", border_width=6)
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.connect('delete-event', Gtk.main_quit)
        window.connect('destroy', self.on_main_window_destroy)

        window.set_default_size(800, 650)

        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        window.add(self.main_box)

        conf = AppConfig(application="application-utility")
        self.app_box = ApplicationBrowser(conf, window)
        self.main_box.pack_start(self.app_box, True, True, 0)
        self.main_box.show_all()

        window.show_all()

    @staticmethod
    def on_main_window_destroy(widget):
        Gtk.main_quit()

    def main(self):
        logging.basicConfig(level=logging.DEBUG)
        Gtk.main()
