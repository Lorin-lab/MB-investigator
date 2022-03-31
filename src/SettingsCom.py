from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import UI_settingsCom


class SettingsCom(QMainWindow):
    def __init__(self, parent):
        super(SettingsCom, self).__init__(parent)

        # Settings
        self.ip = "192.168.0.121"
        self.port = 502
        self.timeout = 5.0

        # UI setup
        self.ui = self._setup_ui()

    def _validation(self):
        self.ip = self.ui.IP_edit.text()
        self.port = int(self.ui.port_edit.text())
        self.close()

    def _cancel(self):
        self.ui.port_edit.setText(str(self.port))
        self.ui.IP_edit.setText(self.ip)
        self.close()

    def _setup_ui(self):
        ui = UI_settingsCom.UiSettingsCom()
        ui.init_ui(self)

        ui.port_edit.setText(str(self.port))
        ui.IP_edit.setText(self.ip)

        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui
