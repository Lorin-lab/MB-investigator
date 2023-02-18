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


class RegisterRow:
    """
    Wrap that groups the content of a row
    """
    def __init__(self, addr=0, label="", value=0):
        """
        Constructor
        :param addr: register address
        :param label: label of the register
        :param value: value of the register
        """
        self.register_addr = addr
        self.label = label
        self.register_value = value
