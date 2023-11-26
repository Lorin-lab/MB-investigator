"""
Copyright 2022-2023 Lorin Québatte

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
from socket import timeout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json
from datetime import datetime

from serial import SerialException

from win_device_settings import WinDeviceSettings
import main_ui
import about_win
from connection_thread import ConnectionThread
from range_win import RangeWin
import version
from data_models.remote_device import RemoteDevice


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # Setup device settings window
        self._device_settings_win = WinDeviceSettings(self, self._on_settings_update)

        self._remote_device = RemoteDevice()  # device configuration
        self._connection_thread = None
        self._msgbox_connection = None

        self._ui = self._setup_ui()
        self._ui.status_bar.showMessage("Welcome")

    def _open_settings_com(self):
        """Opens the communications configuration menu."""
        self._device_settings_win.open_device(self._remote_device)

    def _on_settings_update(self, auto_connect: bool = False):
        """Is called when the new communications configuration is validated"""
        if auto_connect:
            self._attempt_connect_client()

    def _attempt_connect_client(self):
        """Try to open connection to the remote device"""
        msg = ""
        # TCP MODE
        if self._remote_device.com_mode == RemoteDevice.ComMode.TCP \
                or self._remote_device.com_mode == RemoteDevice.ComMode.RTU_OVER_TCP:
            msg = f"Attempt to connecting to {self._remote_device.ip} ..."
        elif self._remote_device.com_mode == RemoteDevice.ComMode.RTU:
            msg = f"Attempt to opening {self._remote_device.serial_port_name} ..."

        print(msg)
        self._ui.status_bar.showMessage(msg)
        self.repaint()

        # Prepare msgbox
        self._msgbox_connection = QMessageBox()
        self._msgbox_connection.setStandardButtons(QMessageBox.Cancel)
        self._msgbox_connection.setWindowTitle("Connection")
        self._msgbox_connection.setText(msg)
        self._msgbox_connection.setIcon(QMessageBox.Information)
        self._msgbox_connection.finished.connect(self._on_connection_canceled)
        # Prepare thread
        self._connection_thread = ConnectionThread(self._remote_device)
        self._connection_thread.success_sig.connect(self._on_connection_success)
        self._connection_thread.fail_sig.connect(self._on_connection_fail)
        # Execute
        self._connection_thread.start()
        self._msgbox_connection.exec()

    def _on_connection_canceled(self):
        if not self._connection_thread.isFinished():
            self._connection_thread.terminate()
            print("connection cancel")
            self._ui.status_bar.showMessage("connection cancel")

    def _on_connection_success(self):
        print("Connection opened successfully.")
        self._ui.status_bar.showMessage("Connection opened successfully.")
        if self._msgbox_connection is not None:
            self._msgbox_connection.close()

        msg_box = QMessageBox()
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.setWindowTitle("Connection opened successfully.")
        msg_box.setText("Connection opened successfully.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec()

    def _on_connection_fail(self, ex: Exception):
        print("Connection failed")
        self._ui.status_bar.showMessage("Connection failed")
        if self._msgbox_connection is not None:
            self._msgbox_connection.close()

        # Build error message
        msg = f"The connection failed because an unknown exception occurred.\n\nException: {type(ex).__name__}\nDetails: {ex}"
        if type(ex) is ConnectionRefusedError:
            msg = f"The remote device has refused the connection.\n{ex}"
        elif type(ex) is ConnectionResetError:
            msg = f"The remote device has reset the connection.\n{ex}"
        elif type(ex) is timeout:
            msg = f"Timeout Reached."
        elif type(ex) is SerialException:
            msg = f"The serial port cannot be opened.\n{ex}"

        msg_box = QMessageBox()
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.setWindowTitle("Connection failed")
        msg_box.setText(msg)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec()

    def _try_disconnect_client(self):
        """Disconnect the modbus client"""
        self._ui.status_bar.showMessage("Disconnection...")
        if self._remote_device.modbus_client is None:
            self._ui.status_bar.showMessage("Already disconnected.")
            return
        self._remote_device.close_connection()
        self._ui.status_bar.showMessage("Disconnected.")

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
        com_settings_data = self._remote_device.serialize()
        range_data_list = []
        for range_win in self._range_win_list:
            range_data_list.append(range_win.json_serialize())

        data = {
            "export_date": str(datetime.now()),
            "app_version": version.__VERSION__,
            "com_settings": com_settings_data,
            "range_win": range_data_list
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
            self._remote_device.deserialize(data.get("com_settings", None))

            # import new range
            new_range_win = []

            range_data_list = data.get("range_win", None)  # Extract range list
            if range_data_list is None:
                range_data_list = data.get("tasks", None)  # Old JSON key from version 1.3.0 and earlier

            for range_win_data in range_data_list:
                # Create range
                range_win = RangeWin(self, self._modbus_client)
                range_win.closed_event.connect(self._del_range_win)
                new_range_win.append(range_win)
                # import range data
                range_win.import_config(range_win_data)
                # Dock the range as tab
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, range_win)
                if len(new_range_win) > 1:
                    self.tabifyDockWidget(new_range_win[0], range_win)

            # replace old ranges by the new ones
            for range_win in self._range_win_list:
                self.removeDockWidget(range_win)
            self._range_win_list.clear()
            self._range_win_list.extend(new_range_win)

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
        ui = main_ui.MainWindowUI(self)

        # toolbar
        ui.device_config_tool_btn.clicked.connect(self._open_settings_com)
        ui.connect_tool_btn.clicked.connect(self._attempt_connect_client)
        ui.disconnect_tool_btn.clicked.connect(self._try_disconnect_client)

        # action bar
        about = about_win.AboutWin(self)
        ui.action_about.triggered.connect(about.show)
        ui.action_import_config.triggered.connect(self._import_config)
        ui.action_export_config.triggered.connect(self._export_config)
        ui.action_quit.triggered.connect(self.close)
        ui.action_settings_device.triggered.connect(self._open_settings_com)
        ui.action_open_com.triggered.connect(self._attempt_connect_client)
        ui.action_close_com.triggered.connect(self._try_disconnect_client)

        # tables
        ui.table_holding_registers.set_variable_list(self._remote_device.variables_holding_registers)
        ui.table_input_registers.set_variable_list(self._remote_device.variable_input_registers)
        ui.table_coils.set_variable_list(self._remote_device.variables_coils)
        ui.table_discrete_input.set_variable_list(self._remote_device.variables_discrete_input)

        return ui


# Start code of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
