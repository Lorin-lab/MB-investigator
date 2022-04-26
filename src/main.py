import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from modbus_tk import modbus_tcp, hooks

import SettingsCom
import UI_main
import about_win
from ModbusComTask import ModbusComTask


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # Instantiates the communication parameters and their menu.
        self._settings_com = SettingsCom.SettingsCom(self, self._on_settings_update)

        self._mb_client = None  # Modbus client
        self._task_list = []

        self._ui = self._setup_ui()
        self._ui.status_bar.showMessage("Welcome")

    def _open_settings_com(self):
        """Opens the communications configuration menu."""
        self._settings_com.show()

    def _on_settings_update(self):
        """Is called when the new communications configuration is validated"""
        self._mb_client = None  # New settings -> client not connected
        self._update_task_client_objet()

    def _try_connect_client(self):
        """Try to connect the app to a modbus server"""
        self._ui.status_bar.showMessage("Try connecting to " + self._settings_com.ip + " ...")
        self.repaint()
        print("Try connecting to " + self._settings_com.ip + " ...")

        # setup client
        self._mb_client = modbus_tcp.TcpMaster(self._settings_com.ip, self._settings_com.port, self._settings_com.timeout)
        hooks.install_hook("modbus_tcp.TcpMaster.after_connect", self._on_client_connected)
        hooks.install_hook("modbus_tcp.TcpMaster.after_close", self._on_client_disconnected)
        self._update_task_client_objet()

        # try connection
        try:
            self._mb_client.open()
        except ConnectionRefusedError:
            self._ui.status_bar.showMessage("Connection Refused")
            self._mb_client = None
        except OSError as ex:
            print(ex)
            self._ui.status_bar.showMessage(str(ex))
            self._mb_client = None
        # Finally if the connection succeeds then _on_client_connected is called.

    def _try_disconnect_client(self):
        """Disconnect the modbus client"""
        if self._mb_client is not None:
            self._mb_client.close()

    def _on_client_connected(self, master):
        """Is called when the application is connected to a modbus server."""
        print("connected")
        self._ui.status_bar.showMessage("Connected")

    def _on_client_disconnected(self, master):
        """Is called when the application is disconnected from a modbus server."""
        print("disconnected")
        self._ui.status_bar.showMessage("Disconnected")
        self._mb_client = None
        self._update_task_client_objet()

    def _add_com_task(self):
        """Adds modbus task."""
        task = ModbusComTask(self, self._mb_client)
        self._task_list.append(task)

        # Dock the task as tab
        self.addDockWidget(Qt.RightDockWidgetArea, task)
        if len(self._task_list) > 1:
            self.tabifyDockWidget(self._task_list[0], task)

    def _update_task_client_objet(self):
        """Updates the modbus client object for each modbus task."""
        for task in self._task_list:
            task.mb_client = self._mb_client

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_main.UiMain(self)

        ui.client_config_tool_btn.clicked.connect(self._open_settings_com)
        ui.connect_tool_btn.clicked.connect(self._try_connect_client)
        ui.disconnect_tool_btn.clicked.connect(self._try_disconnect_client)
        ui.Add_section_tool_btn.clicked.connect(self._add_com_task)

        about = about_win.AboutWin(self)
        ui.action_about.triggered.connect(about.show)
        ui.action_quit.triggered.connect(self.close)
        return ui


# Start code of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
