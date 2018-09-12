#!/usr/bin/env python

import gi
import requests
from requests.exceptions import ConnectionError
import os
import logging
import sys

from .browser.app_config import AppConfig
from .browser.application_browser import ApplicationBrowser

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf

# print(dir(gi.repository.Gtk))
# cat /usr/lib/python3.7/site-packages/gi/overrides/Gtk.py
# doc api
# https://lazka.github.io/pgi-docs/Gtk-3.0/index.html


class MainApp:

    def __init__(self):
        """main app window"""
        window = Gtk.Window(title='Manjaro Application Utility', border_width=6)
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.connect('delete-event', Gtk.main_quit)
        window.connect('destroy', self.on_main_window_destroy)

        window.set_default_size(800, 650)

        """
        TODO ?
        icon="system-software-install"
        pixbuf24 = Gtk.IconTheme.get_default().load_icon(icon, 24, 0)
        pixbuf32 = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
        pixbuf48 = Gtk.IconTheme.get_default().load_icon(icon, 48, 0)
        pixbuf64 = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
        pixbuf96 = Gtk.IconTheme.get_default().load_icon(icon, 96, 0)
        self.set_icon_list([pixbuf24, pixbuf32, pixbuf48, pixbuf64, pixbuf96])
        """

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

    def run(self):
        logging.basicConfig(level=logging.DEBUG)
        MainApp()
        Gtk.main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    MainApp()
    Gtk.main()
