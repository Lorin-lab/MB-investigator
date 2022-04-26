from PyQt5.QtWidgets import *
import UI_settingsCom


class SettingsCom(QMainWindow):
    """This class contains the communication parameters and is the menu for editing them."""
    def __init__(self, parent, call_back_func):
        super(SettingsCom, self).__init__(parent)
        self._call_back_func = call_back_func

        # Settings
        self.ip = "192.168.0.123"
        self.port = 502
        self.timeout = 5.0

        # UI setup
        self._ui = self._setup_ui()

    def _validation(self):
        """save the settings close the menu and call the 'call back' function"""
        self.ip = self._ui.IP_edit.text()
        self.port = int(self._ui.port_edit.text())
        self.close()
        self._call_back_func()

    def _cancel(self):
        """Reset widget with actual settings and close the menu"""
        self._ui.port_edit.setText(str(self.port))
        self._ui.IP_edit.setText(self.ip)
        self.close()

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_settingsCom.UiSettingsCom(self)

        ui.port_edit.setText(str(self.port))
        ui.IP_edit.setText(self.ip)

        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui
