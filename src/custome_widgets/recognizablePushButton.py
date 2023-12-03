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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class RecognizablePushButton(QPushButton):
    RecognizableClicked = pyqtSignal(object)

    def __init__(self, reference: object, text: str, parent=None):
        super().__init__(text, parent)
        self.reference = reference
        self.clicked.connect(self._recognizable_clicked)

    def __init__(self, reference: object, icon: QIcon, text: str, parent=None):
        super().__init__(icon, text, parent)
        self.reference = reference
        self.clicked.connect(self._recognizable_clicked)

    def _recognizable_clicked(self):
        self.RecognizableClicked.emit(self.reference)


