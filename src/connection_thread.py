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

import time

import modbus_tk.modbus
from PyQt5.QtCore import QThread, pyqtSignal
from modbus_tk.exceptions import *
import modbus_tk.defines as cst


class ConnectionThread(QThread):
    # pyqtSignal should be not in the __init__ !
    success = pyqtSignal()
    fail = pyqtSignal(Exception)

    def __init__(self, modbus_client: modbus_tk.modbus.Master):
        super(ConnectionThread, self).__init__()
        self.modbus_client = modbus_client

    def run(self):
        try:
            self.modbus_client.open()
        except (Exception) as ex:
            self.fail.emit(ex)
        else:
            self.success.emit()
        finally:
            self.deleteLater()

