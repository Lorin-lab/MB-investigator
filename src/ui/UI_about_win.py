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
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class UiAboutWin(object):
    """This class contains all the widgets and configures them for the about window."""
    def __init__(self, main_window):
        main_window.setWindowTitle('About')
        v_layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(v_layout)
        main_window.setCentralWidget(widget)

        # title
        title = QLabel("MB-investigator")
        title.setStyleSheet("QLabel {font-size: 20px;}")
        v_layout.addWidget(title)

        # Version
        v_layout.addWidget(QLabel("Version: v1.1.0"))

        # Licence
        v_layout.addWidget(QLabel("Licence: GNU General Public License Version 3"))

        # Source code link
        source_code_link = QLabel()
        source_code_link.setText(
            "Source code: "
            "<a href=\"https://github.com/Lorin-lab/MB-investigator\">https://github.com/Lorin-lab/MB-investigator</a>"
        )
        source_code_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        source_code_link.setOpenExternalLinks(True)
        v_layout.addWidget(source_code_link)
