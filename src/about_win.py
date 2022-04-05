from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import UI_about_win


class AboutWin(QMainWindow):
    def __init__(self, parent):
        super(AboutWin, self).__init__(parent)
        self.ui = self._setup_ui()

    def _setup_ui(self):
        ui = UI_about_win.UiAboutWin()
        ui.init_ui(self)
        return ui
