import os

__version__ = "0.3.1"

path = os.path.join(os.path.dirname(__file__), "resources")

ICONPATH = os.path.join(path, "icons")
TRANSLATIONSPATH = os.path.join(path, "translations")
UIPATH = os.path.join(path, "ui")


def get_icon_path(icon_name: str) -> str:
    """Returns the path to the SVG icon."""
    return os.path.join(ICONPATH, icon_name + ".svg")
