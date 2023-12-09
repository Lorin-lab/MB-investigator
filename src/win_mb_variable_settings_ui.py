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
from custome_widgets.IntegerLineEdit import QIntegerLineEdit
import custome_widgets.CustomQValidators as Validators


class RangeSettingsWin(object):
    """This class contains all the widgets and configures them for the range configuration menu."""
    def __init__(self, main_window):
        main_window.setWindowTitle('Modbus variable settings')
        main_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(main_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # other settings
        # ****************************
        # range name edit
        self.range_label_edit = QLineEdit()
        self.range_label_edit.setMaxLength(25)

        form_layout = QFormLayout()
        form_layout.addRow("Label", self.range_label_edit)
        main_layout.addLayout(form_layout)

        # ****************************
        # Registers address group
        # ****************************
        addr_group_box = QGroupBox("Register address")
        main_layout.addWidget(addr_group_box)

        # buttons
        self.button_group = QButtonGroup()
        buttons_layout = QHBoxLayout()

        self.button_DEC = QRadioButton("DEC", main_window)
        self.button_DEC.setChecked(True)
        buttons_layout.addWidget(self.button_DEC)
        self.button_group.addButton(self.button_DEC)

        self.button_HEX = QRadioButton("HEX", main_window)
        buttons_layout.addWidget(self.button_HEX)
        self.button_group.addButton(self.button_HEX)

        # Starting address edit
        self.start_address_edit = QIntegerLineEdit()
        self.start_address_edit.setValidator(Validators.DecValidator(0, 65535))

        # End address
        self.end_address_label = QLabel("0")

        # Quantity edit
        self.quantity_edit = QIntegerLineEdit()
        self.quantity_edit.setValidator(Validators.DecValidator(1, 2000))

        # form Layout
        form_layout = QFormLayout()
        form_layout.addRow("Address display", buttons_layout)
        form_layout.addRow("Address", self.start_address_edit)
        form_layout.addRow("Quantity", self.quantity_edit)
        form_layout.addRow("End address", self.end_address_label)
        addr_group_box.setLayout(form_layout)

        # ****************************
        # Modbus function group
        # ****************************
        md_fn_group_box = QGroupBox("Interpretation")
        main_layout.addWidget(md_fn_group_box)

        # Interpretation list
        self.interpretaton_cb = QCustomComboBox()

        # unit
        self.unit_label_edit = QLineEdit()
        self.unit_label_edit.setMaxLength(10)

        # form Layout
        form_layout = QFormLayout()
        form_layout.addRow("Interpretation", self.interpretaton_cb)
        form_layout.addRow("Unit", self.unit_label_edit)
        md_fn_group_box.setLayout(form_layout)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)

        self.valid_button = QPushButton()
        self.valid_button.setText("Validation")
        h_layout.addWidget(self.valid_button)

        self.cancel_button = QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.setStyleSheet("background-color : red")
        h_layout.addWidget(self.cancel_button)
