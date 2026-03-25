from resources.lib.gui.windows.single_item_window import SingleItemWindow
from resources.lib.common import tools
from resources.lib.modules.globals import g


class ResumeLoadingWindow(SingleItemWindow):
    def __init__(self, xml_file, location=None, item_information=None, saved_source=None):
        super().__init__(xml_file, location, item_information=item_information)
        self.saved_source = saved_source or {}

    def onInit(self):
        super().onInit()  # sets all item.art.* and item.info.* properties
        src = self.saved_source
        self.setProperty("debrid_provider", src.get("debrid_provider", "").replace("_", " "))
        self.setProperty("source_provider", src.get("provider", ""))
        self.setProperty("release_title", src.get("release_title", ""))
        self.setProperty("source_resolution", src.get("quality", ""))
        self.setProperty("source_type", src.get("type", "torrent"))
        if src.get("size"):
            self.setProperty("source_size", tools.source_size_display(src["size"]))
        g.show_busy_dialog()  # overlay loading dots on top of this window
