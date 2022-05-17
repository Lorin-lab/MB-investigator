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
from PyQt5.QtGui import QValidator
import re


class IntValidator(QValidator):
    """validator that ensures that the integer in text is ready for the int() function.
    Also bounds the value of the integer between the values passed in parameter.
    """
    def __init__(self, min_value: int, max_value: int):
        super(QValidator, self).__init__()
        if min_value > max_value:
            raise ValueError("the min value is higher than the max value.")
        self.min_value = min_value
        self.max_value = max_value

    def fixup(self, text: str) -> str:  # real signature unknown; restored from __doc__
        """Override QValidator.fixup
        Args:
            text: The string to fixup.

        Return:
            the corrected text.
            """

        try:
            number = int(text)
            if number < self.min_value:
                text = str(self.min_value)
            elif number > self.max_value:
                text = str(self.max_value)
        except ValueError:
            text = str(self.min_value)

        return text

    def validate(self, text: str, pos: int) -> (int, str, int):
        """Override QValidator.validate

        Args:
            text: The string to validate.
            pos: The current cursor position.

        Return:
            A tuple (status, string, pos) as a QValidator should.
        """

        # Check intermediate stat
        if text == "" or text == "-":
            return QValidator.Intermediate, text, pos

        # check number format
        match = re.fullmatch("-?[0-9]+", text)
        if match is None:
            return QValidator.Invalid, text, pos

        # check number value
        number = int(text)
        if number < self.min_value:
            if number < 0:
                return QValidator.Acceptable, str(self.min_value), pos
            else:
                return QValidator.Intermediate, text, pos
        elif number > self.max_value:
            if number > 0:
                return QValidator.Acceptable, str(self.max_value), pos
            else:
                return QValidator.Intermediate, text, pos
        else:
            return QValidator.Acceptable, text, pos


class FloatValidator(QValidator):
    """validator that ensures that the float in text is ready for the int() function.
    Also bounds the value of the float between the values passed in parameter.
    """
    def __init__(self, min_value: float, max_value: float):
        super(QValidator, self).__init__()
        if min_value > max_value:
            raise ValueError("the min value is higher than the max value.")
        self.min_value = min_value
        self.max_value = max_value

    def fixup(self, text: str) -> str:  # real signature unknown; restored from __doc__
        """Override QValidator.fixup
        Args:
            text: The string to fixup.

        Return:
            the corrected text.
            """

        try:
            number = float(text)
            if number < self.min_value:
                text = str(self.min_value)
            elif number > self.max_value:
                text = str(self.max_value)
        except ValueError:
            text = str(self.min_value)

        return text

    def validate(self, text: str, pos: int) -> (int, str, int):
        """Override QValidator.validate

        Args:
            text: The string to validate.
            pos: The current cursor position.

        Return:
            A tuple (status, string, pos) as a QValidator should.
        """

        # Check intermediate stat
        if text == "" or text == "-":
            return QValidator.Intermediate, text, pos
        match = re.search("\\.$", text)
        if match is not None:
            return QValidator.Intermediate, text, pos
        match = re.search("^(-?\\.)", text)
        if match is not None:
            return QValidator.Intermediate, text, pos

        # check number format
        match = re.fullmatch("-?[0-9]+(\\.[0-9]+)?", text)
        if match is None:
            return QValidator.Invalid, text, pos

        # check number value
        number = float(text)
        if number < self.min_value:
            if number < 0:
                return QValidator.Acceptable, str(self.min_value), pos
            else:
                return QValidator.Intermediate, text, pos
        elif number > self.max_value:
            if number > 0:
                return QValidator.Acceptable, str(self.max_value), pos
            else:
                return QValidator.Intermediate, text, pos
        else:
            return QValidator.Acceptable, text, pos
