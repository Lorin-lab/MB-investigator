from PyQt5.QtWidgets import *
from ui import UI_about_win


class AboutWin(QMainWindow):
    def __init__(self, parent):
        super(AboutWin, self).__init__(parent)
        self._ui = self._setup_ui()

    def _setup_ui(self):
        ui = UI_about_win.UiAboutWin(self)
        return ui
