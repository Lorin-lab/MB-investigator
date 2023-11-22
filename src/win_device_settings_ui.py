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
from PyQt5.QtWidgets import *

from custome_widgets.QCustomComboBox import QCustomComboBox
import custome_widgets.CustomQValidators as Validators


class WinDeviceSettingsUI(object):
    """This class contains all the widgets and configures them for the communications configuration menu."""
    def __init__(self, main_window):
        general_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(general_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # General settings
        # ****************************
        other_group_box = QGroupBox("General")
        general_layout.addWidget(other_group_box)
        other_group_layout = QVBoxLayout()
        other_group_box.setLayout(other_group_layout)

        self.device_name = QLineEdit()
        self.device_name.setMaxLength(25)

        # write function list
        self.write_func_cb = QCustomComboBox()

        flo = QFormLayout()
        flo.addRow("Device name", self.device_name)
        other_group_layout.addLayout(flo)

        # ****************************
        # Modbus settings
        # ****************************
        other_group_box = QGroupBox("Modbus")
        general_layout.addWidget(other_group_box)
        other_group_layout = QVBoxLayout()
        other_group_box.setLayout(other_group_layout)

        self.unit_id = QLineEdit()
        self.unit_id.setValidator(Validators.FloatValidator(0, 255))

        self.reading_period = QLineEdit()
        self.reading_period.setValidator(Validators.DecValidator(10, 60000))

        self.read_timeout = QLineEdit()
        self.read_timeout.setValidator(Validators.FloatValidator(0.0, 60.0))

        # write function list
        self.write_func_cb = QCustomComboBox()

        flo = QFormLayout()
        flo.addRow("Unit ID (0?)", self.unit_id)
        flo.addRow("Reading period (ms)", self.reading_period)
        flo.addRow("Read timeout (s)", self.read_timeout)
        flo.addRow("Writing function", self.write_func_cb)
        other_group_layout.addLayout(flo)

        # ****************************
        # communication settings
        # ****************************
        other_group_box = QGroupBox("Communication")
        general_layout.addWidget(other_group_box)
        other_group_layout = QVBoxLayout()
        other_group_box.setLayout(other_group_layout)

        self.mode_button_group = QButtonGroup()

        self.button_mode_TCP = QRadioButton("TCP", main_window)
        self.button_mode_TCP.setChecked(True)
        other_group_layout.addWidget(self.button_mode_TCP)
        self.mode_button_group.addButton(self.button_mode_TCP)

        self.button_mode_tcp_over_RTU = QRadioButton("RTU over TCP", main_window)
        other_group_layout.addWidget(self.button_mode_tcp_over_RTU)
        self.mode_button_group.addButton(self.button_mode_tcp_over_RTU)

        self.button_mode_RTU = QRadioButton("RTU", main_window)
        other_group_layout.addWidget(self.button_mode_RTU)
        self.mode_button_group.addButton(self.button_mode_RTU)

        communication_settings_layout = QHBoxLayout()
        other_group_layout.addLayout(communication_settings_layout)

        # ****************************
        # TCP settings
        # ****************************
        self.tcp_group_box = QGroupBox("TCP")
        communication_settings_layout.addWidget(self.tcp_group_box)
        tcp_group_layout = QVBoxLayout()
        self.tcp_group_box.setLayout(tcp_group_layout)

        # IP Line edit
        self.IP_edit = QLineEdit()
        self.IP_edit.setMaxLength(15)

        # Port Line edit
        self.port_edit = QLineEdit()
        self.port_edit.setValidator(Validators.DecValidator(0, 65535))

        # connection timeout
        self.tcp_connection_timeout = QLineEdit()
        self.tcp_connection_timeout.setValidator(Validators.DecValidator(1, 60))

        flo = QFormLayout()
        flo.addRow("IPv4 (ipv6?) or Hostname", self.IP_edit)
        flo.addRow("Port", self.port_edit)
        flo.addRow("Connection timeout (s)", self.tcp_connection_timeout)
        tcp_group_layout.addLayout(flo)

        # ****************************
        # RTU settings
        # ****************************
        self.rtu_group_box = QGroupBox("RTU")
        communication_settings_layout.addWidget(self.rtu_group_box)
        rtu_group_layout = QVBoxLayout()
        self.rtu_group_box.setLayout(rtu_group_layout)

        self.serial_port_name_cb = QCustomComboBox()
        self.baud_rate_cb = QCustomComboBox()
        self.data_bits_cb = QCustomComboBox()
        self.parity_cb = QCustomComboBox()
        self.stop_bits_cb = QCustomComboBox()
        self.flow_control_cb = QCustomComboBox()

        flo = QFormLayout()
        flo.addRow("Port name", self.serial_port_name_cb)
        flo.addRow("Bits per second", self.baud_rate_cb)
        flo.addRow("Data bits", self.data_bits_cb)
        flo.addRow("Parity", self.parity_cb)
        flo.addRow("Stop bits", self.stop_bits_cb)
        flo.addRow("Flow control", self.flow_control_cb)
        rtu_group_layout.addLayout(flo)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        general_layout.addLayout(h_layout)

        self.cancel_button = QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("background-color : red")
        h_layout.addWidget(self.cancel_button)

        self.apply_button = QPushButton()
        self.apply_button.setText("Apply")
        h_layout.addWidget(self.apply_button)

        self.apply_connect_button = QPushButton()
        self.apply_connect_button.setText("Apply and open connection")
        self.apply_connect_button.setDefault(True)
        h_layout.addWidget(self.apply_connect_button)
