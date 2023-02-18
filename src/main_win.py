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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from modbus_tk import modbus_tcp, modbus_rtu
import serial
import json
from datetime import datetime

from com_settings_win import ComSettingsWin
import main_ui
import about_win
from range_win import RangeWin
import version


class MainWindow(QMainWindow):
    """Main window of the application."""

    def __init__(self):
        super(MainWindow, self).__init__()

        # Instantiates the communication parameters and their menu.
        self._com_settings_win = ComSettingsWin(self, self._on_settings_update)

        self._modbus_client = None  # Modbus client
        self._range_win_list = []

        self._ui = self._setup_ui()
        self._ui.status_bar.showMessage("Welcome")

    def _open_settings_com(self):
        """Opens the communications configuration menu."""
        self._com_settings_win.show()

    def _on_settings_update(self):
        """Is called when the new communications configuration is validated"""
        self._modbus_client = None  # New settings -> client not connected
        self._update_range_client_objet()

    def _try_connect_client(self):
        """Try to connect the modbus client. To the server via TCP, or opening the serial port."""

        # TCP MODE
        if self._com_settings_win.mode == ComSettingsWin.MbMode.TCP:
            # print message
            text = f"Attempt to connecting to {self._com_settings_win.ip} ..."
            print(text)
            self._ui.status_bar.showMessage(text)
            self.repaint()

            # setup client
            self._modbus_client = modbus_tcp.TcpMaster(
                self._com_settings_win.ip,
                self._com_settings_win.port,
                self._com_settings_win.timeout
            )

        # RTU MODE
        if self._com_settings_win.mode == ComSettingsWin.MbMode.RTU:

            # Print message
            text = f"Attempt to opening {self._com_settings_win.serial_port_name} ..."
            print(text)
            self._ui.status_bar.showMessage(text)
            self.repaint()

            # setup client
            serial_port = serial.Serial(
                port=None,  # Set null to avoid automatic opening
                baudrate=self._com_settings_win.baud_rate,
                bytesize=self._com_settings_win.data_bits,
                parity=self._com_settings_win.parity,
                stopbits=self._com_settings_win.stop_bits,
                xonxoff=(self._com_settings_win.flow_control == ComSettingsWin.FlowControl.XON_XOFF),
                rtscts=(self._com_settings_win.flow_control == ComSettingsWin.FlowControl.RTS_CTS),
                dsrdtr=(self._com_settings_win.flow_control == ComSettingsWin.FlowControl.DSR_DTR)
            )
            serial_port.port = self._com_settings_win.serial_port_name
            self._modbus_client = modbus_rtu.RtuMaster(serial_port)
            self._modbus_client.set_timeout(self._com_settings_win.timeout, True)

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
            self._update_range_client_objet()

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
        self._update_range_client_objet()
        self._ui.status_bar.showMessage("Disconnected.")

    def _add_range_win(self):
        """Adds modbus range."""
        range_win = RangeWin(self, self._modbus_client)
        range_win.set_close_callback(self._del_range_win)
        self._range_win_list.append(range_win)

        # Dock the range as tab
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, range_win)
        if len(self._range_win_list) > 1:
            self.tabifyDockWidget(self._range_win_list[0], range_win)
            range_win.show()
            range_win.raise_()  # show + raise : move tab to the front

        # open settings
        range_win.open_settings()

    def _del_range_win(self, range_win: RangeWin):
        """
        Delete range window. Use for range window self delete
        :param range_win: range to delete
        """
        try:
            self._range_win_list.remove(range_win)
        except ValueError:
            pass

    def _update_range_client_objet(self):
        """Updates the modbus client object for each modbus range."""
        for addr_range in self._range_win_list:
            addr_range.modbus_client = self._modbus_client

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
        com_settings_data = self._com_settings_win.export_config()
        range_data_list = []
        for range_win in self._range_win_list:
            range_data_list.append(range_win.export_config())

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
            self._com_settings_win.import_config(data.get("com_settings", None))

            # import new range
            new_range_win = []

            range_data_list = data.get("range_win", None)  # Extract range list
            if range_data_list is None:
                range_data_list = data.get("tasks", None)  # Old JSON key from version 1.3.0 and earlier

            for range_win_data in range_data_list:
                # Create range
                range_win = RangeWin(self, self._modbus_client)
                range_win.set_close_callback(self._del_range_win)
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
        ui.client_config_tool_btn.clicked.connect(self._open_settings_com)
        ui.connect_tool_btn.clicked.connect(self._try_connect_client)
        ui.disconnect_tool_btn.clicked.connect(self._try_disconnect_client)
        ui.Add_section_tool_btn.clicked.connect(self._add_range_win)

        # action bar
        about = about_win.AboutWin(self)
        ui.action_about.triggered.connect(about.show)
        ui.action_import_config.triggered.connect(self._import_config)
        ui.action_export_config.triggered.connect(self._export_config)
        ui.action_quit.triggered.connect(self.close)
        ui.action_settings_com.triggered.connect(self._open_settings_com)
        ui.action_open_com.triggered.connect(self._try_connect_client)
        ui.action_close_com.triggered.connect(self._try_disconnect_client)
        ui.action_add_range.triggered.connect(self._add_range_win)
        return ui


# Start code of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
