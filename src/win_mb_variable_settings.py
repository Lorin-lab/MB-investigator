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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import modbus_tk.defines as cst

import win_mb_variable_settings_ui
import custome_widgets.CustomQValidators as Validators
from data_models.modbus_variable import ModbusVariable


class WinMbVariableSettings(QMainWindow):
    """
    This class contains the modbus parameters of a task and is the menu for editing them.
    """

    def __init__(self, parent, call_back_func):
        """
        Constructor of the class MbTaskSettings

        :param parent: The parent window.
        :param call_back_func: The function to call back when new settings are set.
        """
        super(WinMbVariableSettings, self).__init__(parent)
        self.call_back_func = call_back_func
        self.setWindowModality(Qt.WindowModality.WindowModal)

        self.mb_variable = ModbusVariable(0)

        # UI setup
        self._ui = self._setup_ui()

        # setup interpretation combo box
        self._ui.interpretaton_cb.add_option(None, "ROW - Binary")
        self._ui.interpretaton_cb.add_option(None, "ROW - Octal")
        self._ui.interpretaton_cb.add_option(None, "ROW - Decimal", set_as_current=True)
        self._ui.interpretaton_cb.add_option(None, "ROW - Hexadecimal")
        self._ui.interpretaton_cb.add_option(None, "Unsigned integer")
        self._ui.interpretaton_cb.add_option(None, "Signed integer")
        self._ui.interpretaton_cb.add_option(None, "Float simple")
        self._ui.interpretaton_cb.add_option(None, "Float double")
        self._ui.interpretaton_cb.add_option(None, "TEXT - ASCII")
        self._ui.interpretaton_cb.add_option(None, "TEXT - UTF-8")

        self.update_widgets()

    def open_mb_variable(self, mb_variable: ModbusVariable):
        self.show()
        self.mb_variable = mb_variable
        self.update_widgets()

    def update_widgets(self):
        """Set widgets with the current parameter value"""
        self._ui.range_label_edit.setText(self.mb_variable.label)
        self._ui.start_address_edit.set_value(self.mb_variable.address)
        self._ui.quantity_edit.setText(str(self.mb_variable.register_quantity))
        self._on_quantity_edited()

        self._ui.interpretaton_cb.set_current_by_value(self.mb_variable.interpretation)
        self._ui.unit_label_edit.setText(self.mb_variable.unit)

    def _save_settings(self):
        """save the settings close the menu and call the 'call back' function"""
        self.mb_variable.label = self._ui.range_label_edit.text()
        self.mb_variable.address = self._ui.start_address_edit.get_value()
        self.mb_variable.register_quantity = int(self._ui.quantity_edit.get_value())

        self.mb_variable.interpretation = self._ui.interpretaton_cb.get_current_option_value()
        self.mb_variable.unit = self._ui.unit_label_edit.text()

        self.close()
        self.call_back_func()

    def _on_cancel_button(self):
        """Reset widgets with actual settings and close the menu"""
        self.close()

    def _on_apply_button(self):
        self._save_settings()
        self.close()
        self._call_back_func(False)

    def _on_address_display_change(self):
        """
        Is called when the address display mode has been changed.
        """
        if self._ui.button_DEC.isChecked():
            self._ui.start_address_edit.smart_change_validator(Validators.DecValidator(0, 65535))
        elif self._ui.button_HEX.isChecked():
            self._ui.start_address_edit.smart_change_validator(Validators.HexValidator(0, 65535))

    def _on_start_address_edited(self):
        """
        Is called when the start address has been changed.
        """
        start_value = self._ui.start_address_edit.get_value()
        end_value = int(self._ui.end_address_label.text())
        quantity = end_value - start_value + 1
        if start_value >= end_value:
            self._ui.end_address_label.setText(str(start_value))
            quantity = 1
        elif quantity > 2000:
            self._ui.end_address_label.setText(str(end_value + 1999))
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
        self._ui.end_address_label.setText(str(end_value))

    def _setup_ui(self):
        """
        Load widgets and connect them to function.
        """
        ui = win_mb_variable_settings_ui.RangeSettingsWin(self)

        ui.start_address_edit.editingFinished.connect(self._on_start_address_edited)
        ui.quantity_edit.editingFinished.connect(self._on_quantity_edited)

        ui.button_group.idClicked.connect(self._on_address_display_change)
        ui.valid_button.clicked.connect(self._save_settings)
        ui.cancel_button.clicked.connect(self._on_cancel_button)

        return ui
