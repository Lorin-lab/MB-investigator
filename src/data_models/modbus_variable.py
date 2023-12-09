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
from __future__ import annotations  # for that the class is recognize as type hint
import serial
from modbus_tk import modbus_tcp, modbus_rtu, modbus
import modbus_tk.defines as cst


class ModbusVariable:
    """
    Information statement read at a specific modbus address
    """

    def __init__(self, address: int):
        """

        :param address:
        """
        self.label = "unknown"
        self.address = address
        self.value = None
        self.unit = ""
        self.register_quantity = 2
        self.interpretation = None
        self.reading_function = cst.READ_HOLDING_REGISTERS

