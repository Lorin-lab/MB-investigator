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
from PyQt5.QtWidgets import *
import modbus_tk.defines as cst

from ui import UI_mbTaskSettings


class MbTaskSettings(QMainWindow):
    """This class contains the modbus parameters of a task and is the menu for editing them."""
    def __init__(self, parent, call_back_func):
        super(MbTaskSettings, self).__init__(parent)
        self.call_back_func = call_back_func

        # Settings
        self.task_name = "New task"
        self.unit_id = 1
        self.starting_address = 0
        self.quantity = 10
        self.read_func = cst.READ_COILS
        self.write_func = cst.WRITE_SINGLE_COIL

        # UI setup
        self._ui = self._setup_ui()

        # setup read func combo box
        self._ui.read_func_cb.add_option(cst.READ_COILS, "(FC01) Coils", set_as_current=True)
        self._ui.read_func_cb.add_option(cst.READ_DISCRETE_INPUTS, "(FC02) Discrete input")
        self._ui.read_func_cb.add_option(cst.READ_HOLDING_REGISTERS, "(FC03) Holding Registers")
        self._ui.read_func_cb.add_option(cst.READ_INPUT_REGISTERS, "(FC04) Input Registers")
        self._on_read_func_cb_change(0)

    def _validation(self):
        """save the settings close the menu and call the 'call back' function"""
        self.task_name = self._ui.task_name_edit.text()
        self.unit_id = int(self._ui.unit_id_edit.text())
        self.starting_address = int(self._ui.start_address_edit.text())
        self.quantity = int(self._ui.quantity_edit.text())

        self.read_func = self._ui.read_func_cb.get_current_option_value()
        self.write_func = self._ui.write_func_cb.get_current_option_value()

        self.close()
        self.call_back_func()

    def _cancel(self):
        """Reset widget with actual settings and close the menu"""
        self._ui.task_name_edit.setText(self.task_name)
        self._ui.unit_id_edit.setText(str(self.unit_id))
        self._ui.start_address_edit.setText(str(self.starting_address))
        self._ui.quantity_edit.setText(str(self.quantity))

        self._ui.read_func_cb.set_current_by_value(self.read_func)
        self._on_read_func_cb_change(self._ui.read_func_cb.currentIndex())

        self.close()

    def _on_read_func_cb_change(self, current_index):
        """Setup options of the writing func combo box, according to the modbus reading function."""
        self._ui.write_func_cb.clear_options()

        read_func = self._ui.read_func_cb.get_option_value_by_index(current_index)
        if read_func == cst.READ_COILS:
            self._ui.write_func_cb.setEnabled(True)
            self._ui.write_func_cb.add_option(cst.WRITE_SINGLE_COIL, "(FC05) Single Coil")
            self._ui.write_func_cb.add_option(cst.WRITE_MULTIPLE_COILS, "(FC15) Multiple Coils")
        elif read_func == cst.READ_HOLDING_REGISTERS:
            self._ui.write_func_cb.setEnabled(True)
            self._ui.write_func_cb.add_option(cst.WRITE_SINGLE_REGISTER, "(FC06) Single Register")
            self._ui.write_func_cb.add_option(cst.WRITE_MULTIPLE_REGISTERS, "(FC16) Multiple Register")
        else:
            self._ui.write_func_cb.setEnabled(False)
            self._ui.write_func_cb.add_option(None, "Not available")

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_mbTaskSettings.UiMbTaskSettings(self)

        ui.task_name_edit.setText(self.task_name)
        ui.unit_id_edit.setText(str(self.unit_id))

        ui.read_func_cb.currentIndexChanged.connect(self._on_read_func_cb_change)

        ui.start_address_edit.setText(str(self.starting_address))
        ui.quantity_edit.setText(str(self.quantity))

        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui

    class ComboBoxOption:
        """Packaging to group a value with a string to display for the combo boxes."""
        def __init__(self, value, text, associated_options=None):
            self.value = value
            self.text = text
            self.associated_options = associated_options
