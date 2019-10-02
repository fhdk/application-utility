import json
import os
import urllib.request

from application_utility.constants import txt
from application_utility.translation import i18n

_ = i18n.language.gettext


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


def net_check():
    """Check for internet connection"""
    resp = None
    host = f"{txt.GITLAB}"
    # noinspection PyBroadException
    try:
        resp = urllib.request.urlopen(host, timeout=2)
    except Exception:
        pass
    return bool(resp)


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
