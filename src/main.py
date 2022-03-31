import sys
import SettingsCom
import UI_main
from ModbusComTask import ModbusComTask
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from easymodbus.modbusClient import ModbusClient


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.settings_com = SettingsCom.SettingsCom(self)
        self.MB_client = None

        # Setup UI
        self.ui = self._setup_ui()

    def _open_settings_com(self):
        self.settings_com.show()

    def _try_connect_client(self):
        self.statusBar().showMessage("Try connecting to " + self.settings_com.ip + " ...")
        print("Try connecting to " + self.settings_com.ip + " ...")
        self.MB_client = ModbusClient(self.settings_com.ip, self.settings_com.port)
        try:
            self.MB_client.connect()
            if self.MB_client.is_connected():
                self.ui.status_bar.showMessage("Successful connection")
            else:
                self.ui.status_bar.showMessage("Connection failed")
        except ConnectionRefusedError:
            self.ui.status_bar.showMessage("Connection Refused")
        finally:
            print("is coi" + str(self.MB_client.is_connected()))
            #print(self.MB_client.__tcpClientSocket)

    def _try_disconnect_client(self):
        print("disconnect")

    def _add_com_task(self):
        task = ModbusComTask(self)
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
