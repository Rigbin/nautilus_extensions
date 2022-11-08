## based on https://gitlab.gnome.org/GNOME/nautilus-python/-/blob/master/examples/open-terminal.py
import os
import subprocess
from urllib.parse import unquote
from gi.repository import Nautilus, GObject
from typing import List


class OpenAlacrittyExtension(GObject.GObject, Nautilus.MenuProvider):
    def _open_alacritty(self, file: Nautilus.FileInfo) -> None:
        filename = unquote(file.get_uri()[7:])
        os.chdir(filename)
        os.environ["WAYLAND_DISPLAY"] = ""
        subprocess.Popen(["alacritty", "--working-directory", "."], close_fds=True)


    def menu_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_alacritty(file)

    def menu_background_activate_cb(
        self,
        menu: Nautilus.MenuItem,
        file: Nautilus.FileInfo,
    ) -> None:
        self._open_alacritty(file)

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
            name="NautilusPython::openalacritty_file_item",
            label="Open in Alacritty",
            tip="Open Alacritty In %s" % file.get_name(),
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
            name="NautilusPython::openalacritty_file_item2",
            label="Open in Alacritty",
            tip="Open Alacritty In %s" % current_folder.get_name(),
        )
        item.connect("activate", self.menu_background_activate_cb, current_folder)

        return [
            item,
        ]
