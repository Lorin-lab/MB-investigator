"""
Copyright 2022 Lorin Québatte

This file is part of MB-investigator.

MB-investigator is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MB-investigator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with MB-investigator. If not,
see <https://www.gnu.org/licenses/>.
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from modbus_tk import modbus_tcp, modbus_rtu, hooks
import serial

from ComSettings import ComSettings
from ui import UI_main
import about_win
from ModbusTask import ModbusTask


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # Instantiates the communication parameters and their menu.
        self._settings_com = ComSettings(self, self._on_settings_update)

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
        """Try to connect the modbus client. To the server via TCP, or opening the serial port."""

        # TCP MODE
        if self._settings_com.mode == ComSettings.MbMode.TCP:
            print("Try connecting to " + self._settings_com.ip + " ...")
            self._ui.status_bar.showMessage("Try connecting to " + self._settings_com.ip + " ...")
            self.repaint()

            # setup client
            self._mb_client = modbus_tcp.TcpMaster(
                self._settings_com.ip,
                self._settings_com.port,
                self._settings_com.timeout
            )

        # RTU MODE
        if self._settings_com.mode == ComSettings.MbMode.RTU:
            # Check serial port
            if self._settings_com.serial_port_name is None:
                self._ui.status_bar.showMessage("No serial port selected")
                return

            # Print message
            print("Try opening " + str(self._settings_com.serial_port_name) + " ...")
            self._ui.status_bar.showMessage("Try opening " + str(self._settings_com.serial_port_name) + " ...")
            self.repaint()

            # setup client
            serial_port = serial.Serial(
                port=None,  # Set null to avoid automatic opening
                baudrate=self._settings_com.baud_rate,
                bytesize=self._settings_com.data_bits,
                parity=self._settings_com.parity,
                stopbits=self._settings_com.stop_bits,
                xonxoff=(self._settings_com.flow_control == ComSettings.FlowControl.XON_XOFF),
                rtscts=(self._settings_com.flow_control == ComSettings.FlowControl.RTS_CTS),
                dsrdtr=(self._settings_com.flow_control == ComSettings.FlowControl.DSR_DTR)
            )
            serial_port.port = self._settings_com.serial_port_name
            self._mb_client = modbus_rtu.RtuMaster(serial_port)
            self._mb_client.set_timeout(self._settings_com.timeout, True)

        # Try connection
        try:
            # Try connection
            self._mb_client.open()

            # Successful connection
            self._ui.status_bar.showMessage("Connected.")
            print("Connected")
            self._update_task_client_objet()
        except ConnectionRefusedError:
            self._ui.status_bar.showMessage("Connection Refused.")
            self._mb_client = None
        except serial.SerialException as ex:
            self._ui.status_bar.showMessage(str(ex))
            self._mb_client = None
        except OSError as ex:
            print(ex)
            self._ui.status_bar.showMessage(str(ex))
            self._mb_client = None

    def _try_disconnect_client(self):
        """Disconnect the modbus client"""
        if self._mb_client is None:
            self._ui.status_bar.showMessage("Already disconnected.")
            return

        self._ui.status_bar.showMessage("Disconnection...")
        self._mb_client.close()
        self._mb_client = None
        self._update_task_client_objet()
        self._ui.status_bar.showMessage("Disconnected.")

    def _add_com_task(self):
        """Adds modbus task."""
        task = ModbusTask(self, self._mb_client)
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
