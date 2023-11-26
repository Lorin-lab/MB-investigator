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
import modbus_tk.defines as cst

import write_ui
import custome_widgets.CustomQValidators as Validators


class WriteWin(QMainWindow):
    """This class is the dialog box to write in a register"""

    def __init__(self, register_row, write_func: cst, callback_method):
        super().__init__()
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._register_row = register_row
        self._callback_method = callback_method

        # UI setup
        self._ui = self._setup_ui()

        if write_func == cst.WRITE_MULTIPLE_COILS or write_func == cst.WRITE_SINGLE_COIL:
            self._ui.value_edit.setValidator(Validators.DecValidator(0, 1))
        else:
            self._ui.value_edit.setValidator(Validators.DecValidator(0, 65535))

        self._ui.value_edit.setText(str(register_row.register_value))
        self._ui.value_edit.selectAll()

    def _write(self):
        try:
            self._register_row.register_value = int(self._ui.value_edit.text())
        except ValueError:
            self._register_row.register_value = None
        self.close()
        self._callback_method(self._register_row)

    def _cancel(self):
        self.close()

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = write_ui.WriteUI(self)
        ui.valid_button.clicked.connect(self._write)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui
