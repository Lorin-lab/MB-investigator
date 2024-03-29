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


class ComSettingsUI(object):
    """This class contains all the widgets and configures them for the communications configuration menu."""
    def __init__(self, main_window):
        general_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(general_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # Selection mode
        # ****************************
        self.mode_button_group = QButtonGroup()

        self.button_mode_TCP = QRadioButton("TCP, RTU over TCP", main_window)
        self.button_mode_TCP.setChecked(True)
        general_layout.addWidget(self.button_mode_TCP)
        self.mode_button_group.addButton(self.button_mode_TCP)

        self.button_mode_RTU = QRadioButton("RTU", main_window)
        general_layout.addWidget(self.button_mode_RTU)
        self.mode_button_group.addButton(self.button_mode_RTU)

        # ****************************
        # TCP settings
        # ****************************
        self.tcp_group_box = QGroupBox("TCP")
        general_layout.addWidget(self.tcp_group_box)
        tcp_group_layout = QVBoxLayout()
        self.tcp_group_box.setLayout(tcp_group_layout)

        # IP Line edit
        self.IP_edit = QLineEdit()
        self.IP_edit.setMaxLength(15)

        # Port Line edit
        self.port_edit = QLineEdit()
        self.port_edit.setValidator(Validators.DecValidator(0, 65535))

        flo = QFormLayout()
        flo.addRow("IP or Hostname", self.IP_edit)
        flo.addRow("Port", self.port_edit)
        tcp_group_layout.addLayout(flo)

        # ****************************
        # RTU settings
        # ****************************
        self.rtu_group_box = QGroupBox("RTU")
        general_layout.addWidget(self.rtu_group_box)
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
        # Other settings
        # ****************************
        other_group_box = QGroupBox("General settings")
        general_layout.addWidget(other_group_box)
        other_group_layout = QVBoxLayout()
        other_group_box.setLayout(other_group_layout)

        self.timeout = QLineEdit()
        self.timeout.setValidator(Validators.FloatValidator(0.0, 60.0))

        flo = QFormLayout()
        flo.addRow("Timeout (sec)", self.timeout)
        other_group_layout.addLayout(flo)

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
        self.apply_connect_button.setText("Apply and connect")
        self.apply_connect_button.setDefault(True)
        h_layout.addWidget(self.apply_connect_button)
