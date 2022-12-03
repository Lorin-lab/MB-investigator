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
import custome_widgets.CustomQValidators as Validators


class QIntegerLineEdit(QLineEdit):
    """
    LineEdit widget that can change integer validator without losing its value.
    """
    def __init__(self):
        """ Constructor of the class QIntegerLineEdit. """
        super(QIntegerLineEdit, self).__init__()

    def smart_change_validator(self, new_validator: Validators.IntegerValidator):
        """
        Replace the current validator by a new integer validator without losing its value.

        :param new_validator:
        """
        value = self.get_value()
        self.setValidator(new_validator)
        self.set_value(value)

    def get_value(self) -> int:
        """
        Get the current value of the typed integer.

        :return: The value. Return 0 if the text can't be parsed into an integer.
        """
        try:
            if type(self.validator()) is Validators.HexValidator:
                return int(self.text(), 16)
            elif type(self.validator()) is Validators.DecValidator:
                return int(self.text(), 10)
            else:
                return 0
        except ValueError:
            return 0

    def set_value(self, value: int):
        """
        Set the integer value and format it according to the validator.

        :param value: The value to set.
        """
        if type(self.validator()) is Validators.HexValidator:
            new_text = hex(value).replace("0x", "")
        elif type(self.validator()) is Validators.DecValidator:
            new_text = str(value)
        else:
            new_text = ""
        self.setText(new_text)
