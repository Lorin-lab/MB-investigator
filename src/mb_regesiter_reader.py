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


class MbRegisterReader(QThread):
    # pyqtSignal should be not in the __init__ !
    log_progress = pyqtSignal(str)
    success = pyqtSignal(list)
    fail = pyqtSignal()

    def __init__(self,
                 modbus_client: modbus_tk.modbus.Master,
                 unit_id: int,
                 read_func: modbus_tk.defines,
                 starting_address: int,
                 quantity: int,
                 delay: int,
                 loop=False):
        super(MbRegisterReader, self).__init__()

        self.modbus_client = modbus_client
        self.unit_id = unit_id
        self.read_func = read_func
        self.starting_address = starting_address
        self.quantity = quantity
        self.delay = delay
        self.loop = loop

    def run(self):
        while True:
            self.log_progress.emit("Reading...")

            try:
                # Reading data
                datas = self.modbus_client.execute(
                    self.unit_id,
                    self.read_func,
                    self.starting_address,
                    self.quantity)
                self.success.emit(list(datas))
                self.log_progress.emit("Successful reading")
            except ModbusError as ex:
                error = ex.get_exception_code()
                if error == 1:
                    self.log_progress.emit("MB exception " + str(error) + ": Illegal Function")
                if error == 2:
                    self.log_progress.emit("MB exception " + str(error) + ": Illegal data address")
                if error == 3:
                    self.log_progress.emit("MB exception " + str(error) + ": Illegal data value")
                if error == 4:
                    self.log_progress.emit("MB exception " + str(error) + ": Slave device failure")
                self.fail.emit()
            except ModbusInvalidResponseError as ex:
                self.log_progress.emit("Modbus invalid response exception: " + str(ex))
                self.fail.emit()
            except OSError as ex:
                self.log_progress.emit(str(ex))
                self.fail.emit()

            if not self.loop:
                print("stop")
                return #  Exit loop
            else:
                print("continue")
            time.sleep(self.delay / 1000)  # millisecond to second
            print("end loop")

    def set_loop(self, loop):
        print(f"loop: {loop}")
        self.loop = loop
