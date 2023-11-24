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

from data_models.remote_device import RemoteDevice


class ConnectionThread(QThread):
    # pyqtSignal should be not in the __init__ !
    success_sig = pyqtSignal()
    fail_sig = pyqtSignal(Exception)

    def __init__(self, remote_device: RemoteDevice):
        super(ConnectionThread, self).__init__()
        self.modbus_client = remote_device

    def run(self):
        try:
            self.modbus_client.open_connection()
        except (Exception) as ex:
            self.fail_sig.emit(ex)
        else:
            self.success_sig.emit()
        finally:
            self.deleteLater()

