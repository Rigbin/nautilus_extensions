## based on https://gitlab.gnome.org/GNOME/nautilus-python/-/blob/master/examples/open-terminal.py
import os
import subprocess
from urllib.parse import unquote
from gi.repository import Nautilus, GObject
from typing import List


class OpenVSCodeExtension(GObject.GObject, Nautilus.MenuProvider):
    def _open_code(self, file: Nautilus.FileInfo) -> None:
        filename = unquote(file.get_uri()[7:])
        os.chdir(filename)
        subprocess.run("code .".split(" "))

    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_code(file)

    def menu_background_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_code(file)

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
    ) -> List[Nautilus.MenuItem]:
        if len(files) != 1:
            return []

        file = files[0]
        if not file.is_directory() or file.get_uri_scheme() != "file":
            return []

        item = Nautilus.MenuItem(
            name="NautilusPython::openvscode_file_item",
            label="Open in VSCode",
            tip="Open %s with VSCode" % file.get_name(),
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
        self,
        current_folder: Nautilus.FileInfo,
    ) -> List[Nautilus.MenuItem]:
        item = Nautilus.MenuItem(
            name="NautilusPython::openvscode_file_item2",
            label="Open in VSCode",
            tip="Open %s with VSCode" % current_folder.get_name(),
        )
        item.connect("activate", self.menu_background_activate_cb, current_folder)

        return [
            item,
        ]
