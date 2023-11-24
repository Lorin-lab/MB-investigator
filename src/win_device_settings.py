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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import serial
import serial.tools.list_ports

import win_device_settings_ui
from data_models.remote_device import RemoteDevice


class WinDeviceSettings(QMainWindow):
    """This window is for set remote device parameters."""

    def __init__(self, parent, call_back_func):
        super(WinDeviceSettings, self).__init__(parent)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setWindowTitle("Device settings")
        self._call_back_func = call_back_func

        self.device = RemoteDevice()

        # UI setup
        self._ui = self._setup_ui()
        self._on_mode_changed()

    def open_device(self, device: RemoteDevice):
        self.device = device
        self.update_widgets()
        self.show()

    def update_widgets(self):
        """Set widgets with the current parameter value"""
        # General settings
        self._ui.device_name.setText(self.device.name)

        # Modbus Settings
        self._ui.unit_id.setText(str(self.device.unit_id))
        self._ui.reading_period.setText(str(self.device.reading_period))
        self._ui.read_timeout.setText(str(self.device.reading_timeout))
        self._ui.write_func_cb.set_current_by_value(self.device.mb_writing_preference)

        # Communication Settings
        self._ui.button_mode_TCP.setChecked(self.device.com_mode == RemoteDevice.ComMode.TCP)
        self._ui.button_mode_tcp_over_RTU.setChecked(self.device.com_mode == RemoteDevice.ComMode.RTU_OVER_TCP)
        self._ui.button_mode_RTU.setChecked(self.device.com_mode == RemoteDevice.ComMode.RTU)
        self._on_mode_changed()

        # TCP settings
        self._ui.port_edit.setText(str(self.device.port))
        self._ui.IP_edit.setText(self.device.ip)
        self._ui.tcp_connection_timeout.setText(str(self.device.tcp_timeout))

        # RTU settings
        self._ui.serial_port_name_cb.set_current_by_value(self.device.serial_port_name)
        self._ui.baud_rate_cb.set_current_by_value(self.device.baud_rate)
        self._ui.data_bits_cb.set_current_by_value(self.device.data_bits)
        self._ui.parity_cb.set_current_by_value(self.device.parity)
        self._ui.stop_bits_cb.set_current_by_value(self.device.stop_bits)
        self._ui.flow_control_cb.set_current_by_value(self.device.flow_control)

    def showEvent(self, event: QShowEvent) -> None:
        """Called when the settings menu is open"""
        self._refresh_serial_port()

    def _refresh_serial_port(self):
        """List available serial port and refresh combo box"""
        serial_list = serial.tools.list_ports.comports()
        self._ui.serial_port_name_cb.clear_options()

        if len(serial_list) > 0:
            print("__Ports__")
            for port, desc, hwid in sorted(serial_list):
                print("{}: {} [{}]".format(port, desc, hwid))
                self._ui.serial_port_name_cb.add_option(port, "({0}) {1}".format(port, desc))
        else:
            self._ui.serial_port_name_cb.add_option(None, "None found")

    def _on_mode_changed(self):
        """Is called when communication mode is changed"""
        is_rtu = self._ui.button_mode_RTU.isChecked()
        self._ui.tcp_group_box.setDisabled(is_rtu)
        self._ui.rtu_group_box.setDisabled(not is_rtu)

    def _on_cancel_button(self):
        """Reset widget with actual settings and close the menu"""
        self.close()

    def _on_apply_button(self):
        self._save_settings()
        self.close()
        self._call_back_func(False)

    def _on_apply_and_connect_button(self):
        self._save_settings()
        self.close()
        self._call_back_func(True)

    def _save_settings(self):
        """save the settings close the menu and call the 'call back' function"""
        self.device.close_connection()

        # General settings
        self.device.name = self._ui.device_name.text()

        # Modbus
        self.device.unit_id = self._ui.unit_id.text()
        self.device.reading_period = int(self._ui.reading_period.text())
        self.device.reading_timeout = int(self._ui.read_timeout.text())
        self.device.mb_writing_preference = self._ui.write_func_cb.get_current_option_value()

        # Communication settings
        if self._ui.button_mode_TCP.isChecked():
            self.device.com_mode = RemoteDevice.ComMode.TCP
        elif self._ui.button_mode_RTU.isChecked():
            self.device.com_mode = RemoteDevice.ComMode.RTU
        else:
            self.device.com_mode = RemoteDevice.ComMode.RTU_OVER_TCP

        # TCP settings
        self.device.ip = self._ui.IP_edit.text()
        self.device.port = int(self._ui.port_edit.text())
        self.device.tcp_timeout = int(self._ui.tcp_connection_timeout.text())

        # RTU settings
        self.serial_port_name = self._ui.serial_port_name_cb.get_current_option_value()
        self.baud_rate = self._ui.baud_rate_cb.get_current_option_value()
        self.data_bits = self._ui.data_bits_cb.get_current_option_value()
        self.parity = self._ui.parity_cb.get_current_option_value()
        self.stop_bits = self._ui.stop_bits_cb.get_current_option_value()
        self.flow_control = self._ui.flow_control_cb.get_current_option_value()

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = win_device_settings_ui.WinDeviceSettingsUI(self)

        # connect event
        ui.mode_button_group.idClicked.connect(self._on_mode_changed)
        ui.apply_button.clicked.connect(self._on_apply_button)
        ui.apply_connect_button.clicked.connect(self._on_apply_and_connect_button)
        ui.cancel_button.clicked.connect(self._on_cancel_button)

        # Setup Combo options
        ui.write_func_cb.add_option(RemoteDevice.WritingPreference.SINGLE, "Single (FC05/FC06)")
        ui.write_func_cb.add_option(RemoteDevice.WritingPreference.MULTIPLE, "Multiple (FC15/FC16)")

        baud_rate_list = [50, 75, 110, 134, 150, 200, 300, 600, 1200,
                          1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
        for i in baud_rate_list:
            ui.baud_rate_cb.add_option(i, str(i))
        ui.baud_rate_cb.set_current_by_value(9600)

        ui.serial_port_name_cb.add_option(None, "None found")

        ui.data_bits_cb.add_option(serial.FIVEBITS, "5"),
        ui.data_bits_cb.add_option(serial.SIXBITS, "6"),
        ui.data_bits_cb.add_option(serial.SEVENBITS, "7"),
        ui.data_bits_cb.add_option(serial.EIGHTBITS, "8", set_as_current=True)

        ui.parity_cb.add_option(serial.PARITY_NONE, "None", set_as_current=True),
        ui.parity_cb.add_option(serial.PARITY_EVEN, "Even"),
        ui.parity_cb.add_option(serial.PARITY_ODD, "Odd"),
        ui.parity_cb.add_option(serial.PARITY_MARK, "Mark"),
        ui.parity_cb.add_option(serial.PARITY_SPACE, "Space")

        ui.stop_bits_cb.add_option(serial.STOPBITS_ONE, "1", set_as_current=True),
        ui.stop_bits_cb.add_option(serial.STOPBITS_ONE_POINT_FIVE, "1.5"),
        ui.stop_bits_cb.add_option(serial.STOPBITS_TWO, "2")

        ui.flow_control_cb.add_option(RemoteDevice.FlowControl.NONE, "None", set_as_current=True),
        ui.flow_control_cb.add_option(RemoteDevice.FlowControl.XON_XOFF, "xON/xOFF (software)"),
        ui.flow_control_cb.add_option(RemoteDevice.FlowControl.RTS_CTS, "RTS/CTS (hardware)"),
        ui.flow_control_cb.add_option(RemoteDevice.FlowControl.DSR_DTR, "DSR/DTR (hardware)")

        return ui
