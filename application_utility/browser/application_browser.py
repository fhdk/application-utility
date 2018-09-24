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

import gi
import json
import logging
import os
import urllib.request

from .hello_config import HelloConfig
from .config import Config
from .alpm import Alpm
from application_utility import __version__
from application_utility.constants import txt

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gi.require_version('Pamac', '1.0')
from gi.repository import Pamac

# Applications class constants

TITLE = f"{txt.MAU} v.{__version__}"

GROUP, ICON, APPLICATION, DESCRIPTION, ACTIVE, PACKAGE, INSTALLED = list(range(7))


class ApplicationBrowser(Gtk.Box):
    """Class Applications  with viw, title and btns"""

    def __init__(self, config: Config, window: Gtk.Window, orientation=Gtk.Orientation.VERTICAL, spacing=1):
        super().__init__(orientation=orientation, spacing=spacing, expand=True)
        self.config = config
        self.orientation = Gtk.Orientation.VERTICAL
        self.parent = window
        self.app = "application-utility"
        if not isinstance(self.config, HelloConfig):
            icon = "system-software-install"
            pix_buf24 = Gtk.IconTheme.get_default().load_icon(icon, 24, 0)
            pix_buf32 = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
            pix_buf48 = Gtk.IconTheme.get_default().load_icon(icon, 48, 0)
            pix_buf64 = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
            pix_buf96 = Gtk.IconTheme.get_default().load_icon(icon, 96, 0)
            window.set_icon_list([pix_buf24, pix_buf32, pix_buf48, pix_buf64, pix_buf96])

        self.info_bar_appstream = Gtk.InfoBar()

        # initialize data storage
        self.app_store = list()
        self.group_store = list()
        self.tree_view = Gtk.TreeView()
        self.alpm = Alpm()

        self.app_browser_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, expand=True)
        self.add(self.app_browser_box)

        # InfoBar title
        self.info_bar_title = Gtk.InfoBar()
        self.info_bar_title.set_message_type(Gtk.MessageType.OTHER)
        self.info_bar_title.set_show_close_button(True)
        self.info_bar_title.set_revealed(True)
        self.info_bar_title.connect("response", self.on_remove_title_box)
        # title label
        self.title_label = Gtk.Label()
        self.title_label.set_markup(f"<b>{txt.MAM}: </b> "
                                    f"{txt.SELECT_APPS} <b>{txt.BTN_UPDATE_SYSTEM}</b> {txt.WHEN_READY}. ")
        # pack title info
        self.info_bar_title.pack_start(self.title_label, expand=True, fill=True, padding=0)
        # pack title info to app browser box
        self.app_browser_box.pack_start(self.info_bar_title, expand=False, fill=True, padding=0)

        # InfoBar appstream detail
        self.info_bar_appstream = Gtk.InfoBar()
        self.info_bar_appstream.set_message_type(Gtk.MessageType.OTHER)
        self.info_bar_appstream.set_show_close_button(True)
        self.info_bar_appstream.set_revealed(True)
        self.info_bar_appstream.connect("response", self.on_remove_detail_box)
        # app stream data
        self.detail_label = Gtk.Label()
        self.detail_label.set_line_wrap(True)
        self.info_bar_appstream.pack_start(self.detail_label, expand=True, fill=True, padding=0)

        # pack appstream info to app browser box
        self.app_browser_box.pack_start(self.info_bar_appstream, expand=False, fill=True, padding=0)

        # button box
        self.button_box = Gtk.Box(spacing=10)
        # advanced button
        advanced_button = Gtk.ToggleButton(label=f"{txt.BTN_ADVANCED}")
        advanced_button.set_tooltip_text(f"{txt.BTN_ADVANCED_TIP}")
        advanced_button.connect("clicked", self.on_advanced_clicked)
        # download button
        download_button = Gtk.Button(label=f"{txt.BTN_DOWNLOAD}")
        download_button.set_tooltip_text(f"{txt.BTN_DOWNLOAD_TIP}")
        download_button.connect("clicked", self.on_download_clicked)
        # reset button
        reset_button = Gtk.Button(label=f"{txt.BTN_RESET}")
        reset_button.set_tooltip_text(f"{txt.BTN_RESET_TIP}")
        reset_button.connect("clicked", self.on_reload_clicked)

        # update system button
        self.update_system_button = Gtk.Button(label=f"{txt.BTN_UPDATE_SYSTEM}")
        self.update_system_button.set_tooltip_text(f"{txt.BTN_UPDATE_SYSTEM_TIP}")
        self.update_system_button.connect("clicked", self.on_update_system_clicked)
        self.update_system_button.set_sensitive(False)

        # Group filter
        # example: https://gitlab.gnome.org/GNOME/pygobject/blob/master/examples/demo/demos/combobox.py#L90
        self.group_store = self.load_groups_data()
        group_combo = Gtk.ComboBox.new_with_model(self.group_store)
        group_combo.connect("changed", self.on_group_filter_changed)
        renderer_text = Gtk.CellRendererText()
        group_combo.pack_start(renderer_text, True)
        group_combo.add_attribute(renderer_text, "text", 0)
        group_combo.set_active(0)

        # Packing button box
        # advanced button
        self.button_box.pack_start(advanced_button, expand=False, fill=False, padding=10)

        # group combo combo
        self.button_box.pack_start(group_combo, False, False, 10)

        # update system button
        self.button_box.pack_end(self.update_system_button, expand=False, fill=False, padding=10)

        # with Hello, we have btn "HOME" so check if we are Manjaro Hello
        if not isinstance(self.config, HelloConfig):
            # create close button if stand alone
            close_button = Gtk.Button(label=f"{txt.BTN_CLOSE}")
            close_button.set_tooltip_text(f"{txt.BTN_CLOSE_TIP}")
            close_button.connect("clicked", self.on_close_clicked)
            # pack close button
            self.button_box.pack_end(close_button, expand=False, fill=False, padding=10)

        # reload button
        self.button_box.pack_end(reset_button, expand=False, fill=False, padding=10)

        # download button
        # self.button_box.pack_end(download_button, expand=False, fill=False, padding=10)

        # pack button box to app browser
        self.app_browser_box.pack_start(self.button_box, expand=False, fill=False, padding=10)

        # create view and app store
        self.tree_view, self.app_store = self.create_view_tree()

        # create a scrollable window
        app_window = Gtk.ScrolledWindow()
        app_window.set_vexpand(True)
        app_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        # add window to tree view
        app_window.add(self.tree_view)

        # setup grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        # add grid to app browser
        self.app_browser_box.add(grid)
        grid.attach(app_window, 0, 0, 5, len(self.app_store))

        # show time
        self.show_all()
        if self.info_bar_appstream:
            self.info_bar_appstream.hide()

    def create_view_tree(self):
        """create gtk view and model"""
        # setup list store model
        app_store = self.load_app_data()

        # create a tree view with the model store
        tree_view = Gtk.TreeView.new_with_model(app_store)
        tree_view.set_activate_on_single_click(True)
        tree_view.props.has_tooltip = True
        tree_view.connect("query-tooltip", self.on_query_tooltip_tree_view)
        tree_view.connect("button-press-event", self.on_tree_dblclick)

        # column model: icon
        icon = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("", icon, icon_name=ICON)
        tree_view.append_column(column)

        # column model: group name column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(f"{txt.COL_GROUP}", renderer, text=GROUP)
        tree_view.append_column(column)

        # column model: app name column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(f"{txt.COL_APPLICATION}", renderer, text=APPLICATION)
        # column.set_resizable(False)
        column.set_cell_data_func(renderer, self.treeview_cell_app_data_function, None)
        tree_view.append_column(column)

        # column model: description column
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(f"{txt.COL_DESCRIPTION}", renderer, text=DESCRIPTION)
        column.set_resizable(True)  # for test
        tree_view.append_column(column)

        # column model: install column
        toggle = Gtk.CellRendererToggle()
        toggle.connect("toggled", self.on_app_toggle)
        column = Gtk.TreeViewColumn(f"{txt.COL_ACTION}", toggle, active=ACTIVE)
        column.set_cell_data_func(toggle, self.treeview_cell_check_data_function, None)

        # column.set_sizing(Gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_resizable(False)  # not possible with last :(
        column.set_max_width(40)
        column.set_fixed_width(40)
        tree_view.append_column(column)

        return tree_view, app_store

    def load_app_data(self):
        # not use data set for the moment
        store = Gtk.TreeStore(str, str, str, str, bool, str, bool)
        for group in self.config.json:
            if group["apps"]:  # if group is empty after filters
                g_desc = group["description"]
                while len(g_desc) < 72:
                    g_desc = g_desc + " "
                index = store.append(None,
                                     [group["name"],
                                      group["icon"],
                                      None, g_desc, None, None, None])
                for app in group["apps"]:
                    status = app["installed"]
                    installed = " "
                    if status:
                        installed = "*"

                    # restore user checks
                    if not status and self.alpm.to_install(app["pkg"]):
                        status = True

                    if installed == "*" and self.alpm.to_remove(app["pkg"]):
                        status = False

                    tree_item = (None,
                                 app["icon"],
                                 app["name"],
                                 app["description"],
                                 status,
                                 app["pkg"],
                                 status)
                    store.append(index, tree_item)
        return store

    def load_groups_data(self):
        """create gtk store and set data"""
        store = Gtk.ListStore(str)
        store.append(["*"])
        for g in self.config.categories:
            store.append([g])
        return store

    def reload_app_data(self, refresh: bool = False):
        """
        Reload application data
        :param refresh: Refresh only if source json changed
        """
        self.alpm.clear()
        self.app_store.clear()
        if refresh:
            self.config.load().merge_json()
            if isinstance(self.config, HelloConfig):
                self.group_store = self.load_groups_data()
        self.app_store = self.load_app_data()
        self.tree_view.set_model(self.app_store)
        if self.config.group != "*":
            self.tree_view.expand_all()
        self.update_system_button.set_sensitive(not self.alpm.empty)

    def treeview_cell_check_data_function(self, column: Gtk.TreeViewColumn, renderer_cell: Gtk.CellRenderer, model: Gtk.TreeModel, iter_a: Gtk.TreeIter, user_data):
        """hide checkbox for groups"""
        value = model.get(iter_a, GROUP)
        renderer_cell.set_visible(not value[0])

    def treeview_cell_app_data_function(self, column: Gtk.TreeViewColumn, renderer_cell: Gtk.CellRenderer, model: Gtk.TreeModel, iter_a: Gtk.TreeIter, user_data):
        """change font if installed"""
        value = model.get(iter_a, INSTALLED)
        if value[0]:
            renderer_cell.props.weight = 600
        else:
            renderer_cell.props.weight = 400

    def on_remove_title_box(self, panel: Gtk.InfoBar, id: str):
        if self.info_bar_title:
            self.info_bar_title.hide()
            # Or not destroy ? for use set_title_box
            # self.title_box.destroy()
            # self.title_box = None

    def set_title_box(self, html: str, color: Gtk.MessageType = Gtk.MessageType.INFO):
        while len(html) < 200:
            html = html + " "
        if isinstance(self.config, HelloConfig):
            self.info_bar_title.set_message_type(color)
            self.title_label.set_markup(f"<big>{txt.MAM}</big> " + html)
            self.title_label.set_markup(html)
            self.info_bar_title.show()
        else:
            dialog = Gtk.MessageDialog(self, parent=self.parent,
                                       message_type=color,
                                       buttons=Gtk.ButtonsType.OK,
                                       text=html)
            dialog.run()
            dialog.destroy()

    def on_remove_detail_box(self, panel: Gtk.InfoBar, id: str):
        if self.info_bar_appstream:
            self.info_bar_appstream.hide()

    def set_detail_box(self, pkg: str):
        """
        show appstream detals Application
        for Hello, show in new page self.builder.get_object("stack") and show in webbrowser ?
        """

        """
        TODO
        for picture import and show ...
        https://developer.gnome.org/gnome-devel-demos/stable/image.py.html.en
            "To load an image over a network use set_from_pixbuf(pixbuf),"
        as ?
        https://stackoverflow.com/questions/11549480/load-and-show-an-image-from-the-web-in-python-with-gtk-3
        """
        if not self.info_bar_title:
            return

        pkg = self.config(pkg)
        if not pkg or not pkg["appstream"]:
            return

        db = Pamac.Database(config=Pamac.Config(conf_path="/etc/pamac.conf"))
        db.enable_appstream()

        detail = db.get_pkg_details(pkg['pkg'], pkg['name'])
        if detail:
            if self.info_bar_title:
                self.info_bar_title.hide()
            if not detail.get_long_desc() and not detail.get_url():  # ? not detail.get_screenshot() ?
                return
            # logging.info(dir(detail))
            long_desc = detail.get_long_desc()
            while len(long_desc) < 250:
                long_desc = long_desc + " "
            html = f"<b>{detail.get_app_name()}</b> {detail.get_version()}\n"
            html += f"<b>{detail.get_desc()}</b>\n"
            html += f"{long_desc}\n"
            html += f"<a href=\"{detail.get_url()}\">{detail.get_url()}</a>"

            # if detail.get_screenshot():
            #     # TODO if have &amp in original -> BUG
            #     # for speed fix pkg:evolution ->get_screenshot ??
            #     html += f"<a href=\"{detail.get_screenshot().replace('&','&amp;')}\">picture</a>\n"
            #
            # logging.info(detail.get_screenshot())

            self.detail_label.set_markup(html)
            self.info_bar_appstream.show()

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    def on_tree_dblclick(self, treeview: Gtk.TreeView, event):
        """show detail application"""
        # TODO how to import constant ?
        if event.button == 1 and int(event.type == 5):  # Gdk.EventType.GDK_2BUTTON_PRESS:
            path_info = treeview.get_path_at_pos(event.x, event.y)
            if path_info is None:
                return
            path, col, cellx, celly = path_info
            if self.app_store[path][PACKAGE] is not None:
                pkg = self.config(self.app_store[path][PACKAGE])
                if pkg:
                    self.set_detail_box(pkg["name"])
            else:
                if treeview.row_expanded(path):
                    treeview.collapse_row(path)
                else:
                    treeview.expand_to_path(path)

    def on_reload_clicked(self, widget):
        self.reload_app_data()
        self.set_title_box(f"{txt.SELECTION_RESET}")

    def on_group_filter_changed(self, combo):
        """filter grid by one group"""
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            group = model[tree_iter][0]
            self.config.group = group
            self.app_store.clear()
            self.app_store = self.load_app_data()
            self.tree_view.set_model(self.app_store)
            if self.config.group != "*":
                self.tree_view.expand_all()

    def on_advanced_clicked(self, widget):
        """set one filter on/off on view"""
        if widget.get_active():
            self.config.filter = "advanced"
        else:
            self.config.filter = "default"
        self.reload_app_data(False)

    def on_download_clicked(self, widget):
        # TODO to rewrite with config ...
        #    with self.reload_app_data(True)
        if self.net_check():
            # noinspection PyBroadException
            try:
                for download in self.config.pref["data-sets"]:
                    url = "{}/{}.json".format(self.config.pref["url"], download)
                    file = self.fix_path("{}/{}.json".format(self.config.pref["user_path"], download))
                    req = urllib.request.Request(url=url)
                    with urllib.request.urlopen(req, timeout=2) as response:
                        data = json.loads(response.read().decode("utf8"))
                        self.write_json_file(data, file)
                self.reload_app_data(True)
                self.set_title_box(txt.DOWLOAD_COMPLETE)
            except Exception as e:
                logging.error(e)

        else:
            # or re-use panal-title for dialogs info ? it's more gtk3 ?
            self.set_title_box(f"{txt.DOWNLOAD_NA}\n{txt.GITLAB} {txt.SERVER_NA}",
                               Gtk.MessageType.ERROR)

    def on_query_tooltip_tree_view(self, widget: Gtk.TreeView, x, y, keyboard_tip: bool, tooltip):
        """Show tooltip only if installed"""
        is_found, x, y, model, path, iter_a = widget.get_tooltip_context(x, y, keyboard_tip)
        if is_found:
            value = model.get(iter_a, INSTALLED)
            if value[0]:
                msg = f"{txt.PKG_INSTALLED_TIP}"
                active = model.get(iter_a, ACTIVE)
                if not active[0]:
                    msg = msg + f" , {txt.PKG_REMOVE_TIP}"
                tooltip.set_markup(msg)
                widget.set_tooltip_row(tooltip, path)
                return True
        return False

    def on_app_toggle(self, cell, path):
        """Event selector Install/unInstall application"""
        # a group has no package attached and we don't install groups
        if self.app_store[path][PACKAGE] is not None:
            self.app_store[path][ACTIVE] = not self.app_store[path][ACTIVE]
            on_off = self.app_store[path][ACTIVE]
            pkg = self.config(self.app_store[path][PACKAGE])
            installed = pkg['installed']
            pkg = pkg['pkg']
            # update lists
            self.alpm.set_package(pkg, on_off, installed)
            self.update_system_button.set_sensitive(not self.alpm.empty)
            if self.config.dev:
                logging.debug(self.alpm)

    def on_update_system_clicked(self, widget):
        if self.alpm.do_update() != self.alpm.NOTHING:
            self.set_title_box(f"{txt.SYSTEM_UPDATED}", Gtk.MessageType.INFO)
            # reload json for view new apps installed
            self.reload_app_data(True)

    @staticmethod
    def fix_path(path):
        """Make good paths.
        :param path: path to fix
        :type path: str
        :return: fixed path
        :rtype: str
        """
        if "~" in path:
            path = path.replace("~", os.path.expanduser("~"))
        return path

    @staticmethod
    def net_check():
        """Check for internet connection"""
        resp = None
        host = f"https://{txt.GITLAB}"
        # noinspection PyBroadException
        try:
            resp = urllib.request.urlopen(host, timeout=2)
        except Exception:
            pass
        return bool(resp)

    @staticmethod
    def write_json_file(data, filename, dictionary=False):
        """Writes data to file as json
        :param data
        :param filename:
        :param dictionary:
        """
        try:
            if dictionary:
                with open(filename, "wb") as outfile:
                    json.dump(data, outfile)
            else:
                with open(filename, "w") as outfile:
                    json.dump(data, outfile, indent=2)
            return True
        except OSError:
            return False
