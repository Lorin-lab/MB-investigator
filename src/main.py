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
import json
from datetime import datetime

from ComSettings import ComSettings
from ui import UI_main
import about_win
from ModbusTask import ModbusTask
import version


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # Instantiates the communication parameters and their menu.
        self._settings_com = ComSettings(self, self._on_settings_update)

        self._modbus_client = None  # Modbus client
        self._task_list = []

        self._ui = self._setup_ui()
        self._ui.status_bar.showMessage("Welcome")

    def _open_settings_com(self):
        """Opens the communications configuration menu."""
        self._settings_com.show()

    def _on_settings_update(self):
        """Is called when the new communications configuration is validated"""
        self._modbus_client = None  # New settings -> client not connected
        self._update_task_client_objet()

    def _try_connect_client(self):
        """Try to connect the modbus client. To the server via TCP, or opening the serial port."""

        # TCP MODE
        if self._settings_com.mode == ComSettings.MbMode.TCP:
            # print message
            text = f"Attempt to connecting to {self._settings_com.ip} ..."
            print(text)
            self._ui.status_bar.showMessage(text)
            self.repaint()

            # setup client
            self._modbus_client = modbus_tcp.TcpMaster(
                self._settings_com.ip,
                self._settings_com.port,
                self._settings_com.timeout
            )

        # RTU MODE
        if self._settings_com.mode == ComSettings.MbMode.RTU:

            # Print message
            text = f"Attempt to opening {self._settings_com.serial_port_name} ..."
            print(text)
            self._ui.status_bar.showMessage(text)
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
            self._modbus_client = modbus_rtu.RtuMaster(serial_port)
            self._modbus_client.set_timeout(self._settings_com.timeout, True)

        # Try connection
        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        try:
            self._modbus_client.open()
        except (OSError, serial.SerialException) as ex:
            self._modbus_client = None

            msg_box.setWindowTitle("Fail to connect")
            msg_box.setText(f"Fail to connect.\n\nException : {type(ex).__name__}.\n\n{ex}")
            msg_box.setIcon(QMessageBox.Critical)

            self._ui.status_bar.showMessage("Fail to connect.")
            print("Fail to connect.")
        else:
            self._update_task_client_objet()

            msg_box.setWindowTitle("Success")
            msg_box.setText("Successfully connected.")
            msg_box.setIcon(QMessageBox.Information)

            self._ui.status_bar.showMessage("Connected.")
            print("Connected.")
        finally:
            msg_box.exec()

    def _try_disconnect_client(self):
        """Disconnect the modbus client"""
        if self._modbus_client is None:
            self._ui.status_bar.showMessage("Already disconnected.")
            return

        self._ui.status_bar.showMessage("Disconnection...")
        self._modbus_client.close()
        self._modbus_client = None
        self._update_task_client_objet()
        self._ui.status_bar.showMessage("Disconnected.")

    def _add_com_task(self):
        """Adds modbus task."""
        task = ModbusTask(self, self._modbus_client)
        self._task_list.append(task)

        # Dock the task as tab
        self.addDockWidget(Qt.TopDockWidgetArea, task)
        if len(self._task_list) > 1:
            self.tabifyDockWidget(self._task_list[0], task)
            task.show()
            task.raise_()  # show + raise : move tab to the front

        task.open_settings()

    def _update_task_client_objet(self):
        """Updates the modbus client object for each modbus task."""
        for task in self._task_list:
            task.modbus_client = self._modbus_client

    def _export_config(self):
        """Export configuration"""

        # File selection dialog
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setNameFilter("*.json")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
        else:  # Canceled
            return

        # Prepare data
        com_settings_data = self._settings_com.export_config()
        tasks_data_list = []
        for task in self._task_list:
            tasks_data_list.append(task.export_config())

        data = {
            "export_date": str(datetime.now()),
            "app_version": version.__VERSION__,
            "com_settings": com_settings_data,
            "tasks": tasks_data_list
        }

        # Write file
        file_objet = open(file_path, "w")
        json.dump(data, file_objet, indent=4)
        file_objet.close()

    def _import_config(self):
        """Import configuration"""

        # Warning message box
        msg_box = QMessageBox()
        msg_box.setText("Your current configuration will be lost. Are you sure you want to import?")
        msg_box.setWindowTitle("Import")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        if msg_box.exec() == QMessageBox.Cancel:
            return  # Abort importing

        # File selection dialog
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("*.json")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
        else:  # Canceled
            return

        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        try:
            # get json
            file_objet = open(file_path, "r")
            data = json.load(file_objet)
            file_objet.close()

            # import com settings
            self._settings_com.import_config(data.get("com_settings", None))

            # import new task
            new_tasks = []
            for task_data in data.get("tasks", None):
                # Create task
                task = ModbusTask(self, self._modbus_client)
                new_tasks.append(task)
                # import task data
                task.import_config(task_data)
                # Dock the task as tab
                self.addDockWidget(Qt.RightDockWidgetArea, task)
                if len(self._task_list) > 1:
                    self.tabifyDockWidget(self._task_list[0], task)

            # replace old tasks by the new ones
            for task in self._task_list:
                self.removeDockWidget(task)
            self._task_list.clear()
            self._task_list.append(new_tasks)

            # if the import is successful:
            msg_box.setText("Successful import")
            msg_box.setWindowTitle("Successful import")
            msg_box.setIcon(QMessageBox.Information)

        except (TypeError, KeyError) as ex:
            msg_box.setText(f"Failure to import.\nCause:\n{ex}")
            msg_box.setWindowTitle("Import failure")
            msg_box.setIcon(QMessageBox.Critical)
        except json.decoder.JSONDecodeError as ex:
            msg_box.setText(f"Failure to import. The json format of the file is invalid. \nDetails:\n{ex}")
            msg_box.setWindowTitle("Import failure")
            msg_box.setIcon(QMessageBox.Critical)
        finally:
            msg_box.exec()

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_main.UiMain(self)

        # toolbar
        ui.client_config_tool_btn.clicked.connect(self._open_settings_com)
        ui.connect_tool_btn.clicked.connect(self._try_connect_client)
        ui.disconnect_tool_btn.clicked.connect(self._try_disconnect_client)
        ui.Add_section_tool_btn.clicked.connect(self._add_com_task)

        # action bar
        about = about_win.AboutWin(self)
        ui.action_about.triggered.connect(about.show)
        ui.action_import_config.triggered.connect(self._import_config)
        ui.action_export_config.triggered.connect(self._export_config)
        ui.action_quit.triggered.connect(self.close)
        ui.action_settings_com.triggered.connect(self._open_settings_com)
        ui.action_open_com.triggered.connect(self._try_connect_client)
        ui.action_close_com.triggered.connect(self._try_disconnect_client)
        ui.action_add_task.triggered.connect(self._add_com_task)
        return ui


# Start code of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
