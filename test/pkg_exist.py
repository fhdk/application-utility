import gi

gi.require_version("Pamac", "9.0")
from gi.repository import Pamac


def pkg_exist(pkgname: str) -> []:
    """check if a package exist"""
    config = Pamac.Config(conf_path="/etc/pamac.conf")
    db = Pamac.Database(config=config)

    return db.search_pkgs(pkgname)

    # return bool(db.search_pkgs(pkgname))


for pkg in pkg_exist("chromium"):
    print(pkg.get_name())
