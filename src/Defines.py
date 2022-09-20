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

from enum import Enum


class NumberDisplay(Enum):
    """
    Enumeration of number representation
    """
    BIN = 1  # Binary (Base-2)
    OCT = 2  # Octal (Base-8)
    DEC = 3  # Decimal  (Base-10)
    HEX = 4  # Hexadecimal (Base-16)
