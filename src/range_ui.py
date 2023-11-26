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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import datetime

from utils import *


class RangeUI(object):
    """This class contains all the widgets and configures them for the addr range window."""
    def __init__(self, main_window):
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setObjectName("mainWidget")
        widget.setStyleSheet("QWidget#mainWidget { "
                             "background-color : #CFCFCF;"
                             "border-radius: 5px; "
                             "margin: 2px;"
                             "border: 2px solid black;"
                             "}")
        widget.setLayout(v_layout)
        main_window.setWidget(widget)

        # ****************************
        # Main buttons
        # ****************************
        h_layout = QHBoxLayout()
        v_layout.addLayout(h_layout)

        self.read_button = QPushButton()
        self.read_button.setText("Read all")
        h_layout.addWidget(self.read_button)

        self.toggle_read_button = QCheckBox()
        self.toggle_read_button.setText("Periodic reading")
        self.toggle_read_button.setCheckable(True)
        h_layout.addWidget(self.toggle_read_button)

        self.open_settings_btn = QToolButton()
        self.open_settings_btn.setIcon(QIcon(resource_path("icons/tune_FILL0_wght400_GRAD0_opsz48.svg")))
        self.open_settings_btn.setToolTip("Range parameters")
        h_layout.addWidget(self.open_settings_btn)

        # ****************************
        # plain text
        # ****************************
        self.plain_text_log = QPlainTextEdit()
        self.plain_text_log.setFixedHeight(70)
        self.plain_text_log.setTextInteractionFlags(
            Qt.TextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse |
                                    Qt.TextInteractionFlag.TextSelectableByKeyboard))
        self.log_print("Ready")
        v_layout.addWidget(self.plain_text_log)

        # ****************************
        # table
        # ****************************
        #self.table_widget = ModbusVariableTable()
        v_layout.addWidget(self.table_widget)

    def log_print(self, text):
        """insert log into the plain text widget"""
        now = datetime.now()
        current_time = now.strftime("[%H:%M:%S] ")
        self.plain_text_log.insertPlainText("\n" + current_time + text)
        self.plain_text_log.ensureCursorVisible()
