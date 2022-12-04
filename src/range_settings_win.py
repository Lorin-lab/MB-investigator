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
from PyQt5.QtCore import *
import modbus_tk.defines as cst

import range_settings_ui
import custome_widgets.CustomQValidators as Validators


class RangeSettingsUI(QMainWindow):
    """
    This class contains the modbus parameters of a task and is the menu for editing them.
    """

    def __init__(self, parent, call_back_func):
        """
        Constructor of the class MbTaskSettings

        :param parent: The parent window.
        :param call_back_func: The function to call back when new settings are set.
        """
        super(RangeSettingsUI, self).__init__(parent)
        self.call_back_func = call_back_func
        self.setWindowModality(Qt.WindowModality.WindowModal)

        # Settings
        self.name = "New task"
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

        self.update_widgets()

    def _validation(self):
        """save the settings close the menu and call the 'call back' function"""
        self.name = self._ui.range_name_edit.text()
        self.unit_id = int(self._ui.unit_id_edit.text())
        self.starting_address = self._ui.start_address_edit.get_value()
        self.quantity = int(self._ui.quantity_edit.text())

        self.read_func = self._ui.read_func_cb.get_current_option_value()
        self.write_func = self._ui.write_func_cb.get_current_option_value()

        self.close()
        self.call_back_func()

    def _cancel(self):
        """Reset widgets with actual settings and close the menu"""
        self.update_widgets()
        self.close()

    def update_widgets(self):
        """Set widgets with the current parameter value"""
        self._ui.range_name_edit.setText(self.name)
        self._ui.unit_id_edit.setText(str(self.unit_id))
        self._ui.start_address_edit.set_value(self.starting_address)
        self._ui.quantity_edit.setText(str(self.quantity))
        self._on_quantity_edited()

        self._ui.read_func_cb.set_current_by_value(self.read_func)
        self._on_read_func_cb_change(self._ui.read_func_cb.currentIndex())

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

    def _on_address_display_change(self):
        """
        Is called when the address display mode has been changed.
        """
        if self._ui.button_DEC.isChecked():
            self._ui.start_address_edit.smart_change_validator(Validators.DecValidator(0, 65535))
            self._ui.end_address_edit.smart_change_validator(Validators.DecValidator(0, 65535))
        elif self._ui.button_HEX.isChecked():
            self._ui.start_address_edit.smart_change_validator(Validators.HexValidator(0, 65535))
            self._ui.end_address_edit.smart_change_validator(Validators.HexValidator(0, 65535))

    def _on_start_address_edited(self):
        """
        Is called when the start address has been changed.
        """
        start_value = self._ui.start_address_edit.get_value()
        end_value = self._ui.end_address_edit.get_value()
        quantity = end_value - start_value + 1
        if start_value >= end_value:
            self._ui.end_address_edit.set_value(start_value)
            quantity = 1
        elif quantity > 2000:
            self._ui.end_address_edit.set_value(start_value + 1999)
        self._ui.quantity_edit.set_value(quantity)

    def _on_end_address_edited(self):
        """
        Is called when the end address has been changed.
        """
        start_value = self._ui.start_address_edit.get_value()
        end_value = self._ui.end_address_edit.get_value()
        quantity = end_value - start_value + 1
        if start_value >= end_value:
            self._ui.start_address_edit.set_value(end_value)
            quantity = 1
        elif quantity > 2000:
            self._ui.start_address_edit.set_value(end_value - 1999)
        self._ui.quantity_edit.set_value(quantity)

    def _on_quantity_edited(self):
        """
        Is called when the quantity of register has been changed.
        """
        start_value = self._ui.start_address_edit.get_value()
        quantity = self._ui.quantity_edit.get_value()
        end_value = start_value + quantity - 1
        if end_value > 65535:
            end_value = 65535
            self._ui.quantity_edit.set_value(end_value - start_value + 1)
        self._ui.end_address_edit.set_value(end_value)

    def export_config(self) -> dict:
        """
        Export configuration

        :return: Return parameters into a dictionary.
        """
        data = {
            "task_name": self.name,
            "unit_id": self.unit_id,
            "starting_address": self.starting_address,
            "quantity": self.quantity,
            "read_func": self.read_func,
            "write_func": self.write_func,
        }
        return data

    def import_config(self, data: dict):
        """
        Import configuration

        :param data: Dict that contains parameters to be imported.
        """
        if data is None:
            return
        # Write data into the widget. Because widget have value check.
        self._ui.range_name_edit.setText(str(data.get("task_name", self.name)))
        self._ui.unit_id_edit.setText(str(data.get("unit_id", self.unit_id)))
        self._ui.start_address_edit.setText(str(data.get("starting_address", self.starting_address)))
        self._ui.quantity_edit.setText(str(data.get("quantity", self.quantity)))

        self._ui.read_func_cb.set_current_by_value(data.get("read_func", self.read_func))
        self._on_read_func_cb_change(self._ui.read_func_cb.currentIndex())
        self._ui.write_func_cb.set_current_by_value(data.get("write_func", self.write_func))

        self._validation()

    def _setup_ui(self):
        """
        Load widgets and connect them to function.
        """
        ui = range_settings_ui.RangeSettingsWin(self)

        ui.read_func_cb.currentIndexChanged.connect(self._on_read_func_cb_change)
        ui.start_address_edit.editingFinished.connect(self._on_start_address_edited)
        ui.end_address_edit.editingFinished.connect(self._on_end_address_edited)
        ui.quantity_edit.editingFinished.connect(self._on_quantity_edited)
        ui.button_group.idClicked.connect(self._on_address_display_change)
        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui
