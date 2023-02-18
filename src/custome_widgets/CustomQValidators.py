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
from PyQt5.QtGui import QValidator
import re


class FloatValidator(QValidator):
    """
    validator that ensures that the float in text is ready for the float() function.
    Also bounds the value of the float between the values passed in parameter.
    """
    def __init__(self, min_value: float, max_value: float):
        """
        Constructor of the class FloatValidator.

        :param min_value: Minimum value that the number can have.
        :param max_value: Maximum value that the number can have.
        :raise ValueError:
        """

        super(QValidator, self).__init__()
        if min_value > max_value:
            raise ValueError("the min value is higher than the max value.")
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, text: str, pos: int) -> (int, str, int):
        """
        Validate the text at each typed character.

        :param text: the string to validate
        :param pos: The current cursor position.
        :return:
            QValidator status (),
            modified text,
            modified cursor position
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

    def fixup(self, text: str) -> str:
        """
        Attempt to fixe the text when his status is Intermediate

        :param text: Current text
        :return: Corrected text
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


class IntegerValidator(QValidator):
    """
    Abstract class for an integer validator.
    """
    pass


class DecValidator(IntegerValidator):
    """
    validator that ensures that the integer in text is ready for the int() function.
    Also bounds the value of the integer between the values passed in parameter.
    """
    def __init__(self, min_value: int, max_value: int):
        """
        Constructor of the class IntValidator.

        :param min_value: Minimum value that the number can have.
        :param max_value: Maximum value that the number can have.
        :raise ValueError:
        """
        super(QValidator, self).__init__()
        if min_value > max_value:
            raise ValueError("the min value is higher than the max value.")
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, text: str, pos: int) -> (int, str, int):
        """
        Validate the text at each typed character.

        :param text: the string to validate
        :param pos: The current cursor position.
        :return:
            QValidator status (),
            modified text,
            modified cursor position
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

    def fixup(self, text: str) -> str:
        """
        Attempt to fixe the text when his status is Intermediate

        :param text: Current text
        :return: Corrected text
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


class HexValidator(IntegerValidator):
    """
    validator that ensures that the text is in hexadecimal format.
    Also bounds the value of the float between the values passed in parameter.
    """
    def __init__(self, min_value: (int, str), max_value: (int, str)):
        """
        Constructor of the class HexValidator.

        :param min_value: Minimum value that the number can have.
        :param max_value: Maximum value that the number can have.
        :raise ValueError:
        """
        if type(min_value) is str:
            min_value = int(min_value, 16)
        if type(max_value) is str:
            max_value = int(max_value, 16)

        super(QValidator, self).__init__()
        if min_value > max_value:
            raise ValueError("the min value is higher than the max value.")
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, text: str, pos: int) -> (int, str, int):
        """
        Validate the text at each typed character.

        :param text: the string to validate
        :param pos: The current cursor position.
        :return:
            QValidator status (),
            modified text,
            modified cursor position
        """

        # Check intermediate stat
        if text == "":
            return QValidator.Intermediate, text, pos

        # check number format
        match = re.fullmatch("[0-9a-fA-F]+", text)
        if match is None:
            return QValidator.Invalid, text, pos

        # check number value
        number = int(text, 16)
        if number < self.min_value:
            return QValidator.Intermediate, text, pos
        elif number > self.max_value:
            return QValidator.Acceptable, hex(self.max_value).replace("0x", ""), pos
        else:
            return QValidator.Acceptable, text, pos

    def fixup(self, text: str) -> str:
        """
        Attempt to fixe the text when his status is Intermediate

        :param text: Current text
        :return: Corrected text
        """

        try:
            number = int(text, 16)
            if number < self.min_value:
                text = hex(self.min_value).replace("0x", "")
            elif number > self.max_value:
                text = hex(self.max_value).replace("0x", "")
        except ValueError:
            text = hex(self.min_value).replace("0x", "")

        return text
