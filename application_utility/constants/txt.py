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
#

"""application-utility Text Module"""

from application_utility.translation import i18n

_ = i18n.language.gettext
# gitlab
URL_GITLAB = "gitlab.manjaro.org"
ISO_URL_OFFICIAL = "https://gitlab.manjaro.org/profiles-and-settings/iso-profiles/raw/manjaro-architect/manjaro"
ISO_URL_COMMUNITY = "https://gitlab.manjaro.org/profiles-and-settings/iso-profiles/raw/manjaro-architect/community"
# header
MAM = _("Manjaro Application Maintenance")
MAU = _("Manjaro Application Utility")
SELECT_APPS = _("Select/Deselect apps you want to install/remove")
WHEN_READY = _("when ready")
# buttons
BTN_ADVANCED = _("advanced")
BTN_ADVANCED_TIP = _("Toggle an extended selection of packages")
BTN_DOWNLOAD = _("download")
BTN_DOWNLOAD_TIP = _("Download the most recent selection of packages")
BTN_RESET = _("reset")
BTN_RESET_TIP = _("Reset your current selections...")
BTN_UPDATE_SYSTEM = _("UPDATE SYSTEM")
BTN_UPDATE_SYSTEM_TIP = _("Apply your current selections to the system")
BTN_CLOSE = _("close")
BTN_CLOSE_TIP = _("Discard selections and close app")
# tree view columns
COL_GROUP = _("Group")
COL_APPLICATION = _("Application")
COL_DESCRIPTION = _("Description")
COL_ACTION = _("Install/Remove")
PKG_INSTALLED_TIP = _("Installed")
PKG_REMOVE_TIP = _("to remove")
# message
SELECTION_RESET = _("Your selections has been reset")
DOWNLOAD_COMPLETE = _("App data has been downloaded and list is reset")
SYSTEM_UPDATED = _("Your system has been updated")
DOWNLOAD_NA = _("Download not available")
SERVER_NA = _("server could not be reached")





