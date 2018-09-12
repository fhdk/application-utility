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
