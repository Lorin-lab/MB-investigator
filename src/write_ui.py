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

import custome_widgets.CustomQValidators as Validators


class WriteUI(object):
    """This class contains all the widgets and configures them for the communications configuration menu."""
    def __init__(self, main_window):
        general_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(general_layout)
        main_window.setCentralWidget(widget)

        # ****************************
        # Value prompt
        # ****************************

        self.value_edit = QLineEdit()
        flo = QFormLayout()
        flo.addRow("New value", self.value_edit)

        general_layout.addLayout(flo)

        # ****************************
        # Writing mode
        # ****************************
        self.mode_button_group = QButtonGroup()

        self.button_mode_TCP = QRadioButton("Write the value immediately", main_window)
        self.button_mode_TCP.setChecked(True)
        general_layout.addWidget(self.button_mode_TCP)
        self.mode_button_group.addButton(self.button_mode_TCP)

        #self.button_mode_RTU = QRadioButton("Write the value periodically", main_window)
        #general_layout.addWidget(self.button_mode_RTU)
        #self.mode_button_group.addButton(self.button_mode_RTU)

        #self.button_mode_RTU = QRadioButton("Write the value later", main_window)
        #general_layout.addWidget(self.button_mode_RTU)
        #self.mode_button_group.addButton(self.button_mode_RTU)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        general_layout.addLayout(h_layout)

        self.valid_button = QPushButton()
        self.valid_button.setText("Write")
        self.valid_button.setShortcut(QKeySequence(Qt.Key.Key_Enter))  # this not work (Key_Enter == 16777221)
        self.valid_button.setShortcut(QKeySequence(16777220))  # this work
        h_layout.addWidget(self.valid_button)

        self.cancel_button = QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.setShortcut(QKeySequence(Qt.Key.Key_Escape))
        self.cancel_button.setStyleSheet("background-color : red")
        h_layout.addWidget(self.cancel_button)
