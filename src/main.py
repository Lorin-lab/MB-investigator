import sys
import SettingsCom
import UI_main
from ModbusComTask import ModbusComTask
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from modbus_tk import modbus_tcp, hooks

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.settings_com = SettingsCom.SettingsCom(self)
        self.MB_client = None
        self.task_list = []

        # Setup UI
        self.ui = self._setup_ui()

        self._add_com_task()

    def _open_settings_com(self):
        self.settings_com.show()

    def _try_connect_client(self):
        self.statusBar().showMessage("Try connecting to " + self.settings_com.ip + " ...")
        print("Try connecting to " + self.settings_com.ip + " ...")

        self.MB_client = modbus_tcp.TcpMaster(self.settings_com.ip, self.settings_com.port, self.settings_com.timeout)
        hooks.install_hook("modbus_tcp.TcpMaster.after_connect", self._on_client_connected)
        hooks.install_hook("modbus_tcp.TcpMaster.after_close", self._on_client_disconnected)

        for task in self.task_list:
            task.MB_client = self.MB_client

        try:
            self.MB_client.open()
        except ConnectionRefusedError:
            self.ui.status_bar.showMessage("Connection Refused")
        finally:
            pass

    def _try_disconnect_client(self):
        self.MB_client.close()

    def _on_client_connected(self,master):
        print("connected")
        self.statusBar().showMessage("connected")

    def _on_client_disconnected(self, master):
        print("disconnected")
        self.statusBar().showMessage("disconnected")

    def _add_com_task(self):
        task = ModbusComTask(self, self.MB_client)
        self.task_list.append(task)
        self.addDockWidget(Qt.RightDockWidgetArea, task)

    def _setup_ui(self):
        ui = UI_main.UiMain()
        ui.init_ui(self)
        ui.client_config_toolbutton.clicked.connect(self._open_settings_com)
        ui.connect_toolbutton.clicked.connect(self._try_connect_client)
        ui.diconnect_toolbutton.clicked.connect(self._try_disconnect_client)
        ui.Add_section_toolbuton.clicked.connect(self._add_com_task)
        ui.status_bar.showMessage("Welcome")
        return ui


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
