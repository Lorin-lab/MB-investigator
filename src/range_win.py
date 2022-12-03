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
from modbus_tk.exceptions import *
import modbus_tk.defines as cst

import range_ui
import range_settings_win


class RangeWin(QDockWidget):
    """Object for reading and writing to a modbus address range according to parameters.
    All presented with a graphic interface.
    """
    range_counter = 0

    def __init__(self, parent, modbus_client):
        super(RangeWin, self).__init__("New range", parent)
        self.modbus_client = modbus_client

        # Instantiates the modbus parameters and their menu.
        self._settings = range_settings_win.RangeSettingsUI(self, self._on_settings_update)

        RangeWin.range_counter += 1
        self._settings.name = "Range {0}".format(RangeWin.range_counter)
        self._settings.update_widgets()

        self._ui = self._setup_ui()
        self._on_settings_update()

    def open_settings(self):
        """Opens the modbus configuration menu."""
        self._settings.show()

    def _on_settings_update(self):
        """Is called when the new modbus configuration is validated. Update widgets"""
        # Update dock title
        self.setWindowTitle(self._settings.name)

        # disable/enable Writing button
        if self._settings.write_func is None:
            self._ui.write_button.setDisabled(True)
        else:
            self._ui.write_button.setEnabled(True)

        # update table
        self._ui.table_widget.change_address_set(self._settings.starting_address,
                                                 self._settings.quantity,
                                                 self._settings.read_func,
                                                 self._settings.write_func)

    def _mb_reading_execute(self):
        """Execute modbus reading function"""
        # Checking client
        if self.modbus_client is None:
            self._ui.log_print("Client not connected")
            return

        self._ui.log_print("Reading...")
        self.repaint()

        try:
            # Reading data
            datas = self.modbus_client.execute(
                self._settings.unit_id,
                self._settings.read_func,
                self._settings.starting_address,
                self._settings.quantity)
            self._ui.table_widget.set_register_values(list(datas))
            self._ui.log_print("Successful reading")
        except ModbusError as ex:
            error = ex.get_exception_code()
            if error == 1:
                self._ui.log_print("MB exception " + str(error) + ": Illegal Function")
            if error == 2:
                self._ui.log_print("MB exception " + str(error) + ": Illegal data address")
            if error == 3:
                self._ui.log_print("MB exception " + str(error) + ": Illegal data value")
            if error == 4:
                self._ui.log_print("MB exception " + str(error) + ": Slave device failure")
        except ModbusInvalidResponseError as ex:
            self._ui.log_print("Modbus invalid response exception: " + str(ex))
        except OSError as ex:
            self._ui.log_print(str(ex))

    def _mb_writing_execute(self):
        """Execute modbus writing function"""

        # Checking client
        if self.modbus_client is None:
            self._ui.log_print("Client not connected")
            return
        # Checking available function
        if self._settings.write_func is None:
            return
        # Checking data
        for i in self._ui.table_widget.get_register_values():
            if i is None:
                self._ui.log_print("Value none in data")
                return

        try:
            data = self._ui.table_widget.get_register_values()
            # write data in one shot
            if self._settings.write_func == cst.WRITE_MULTIPLE_COILS or \
                    self._settings.write_func == cst.WRITE_MULTIPLE_REGISTERS:
                self._ui.log_print("Writing...")
                self.repaint()
                feedback = self.modbus_client.execute(
                    self._settings.unit_id,
                    self._settings.write_func,
                    self._settings.starting_address,
                    output_value=data
                )
                self._ui.log_print("Successful writing")

            # write data one by one
            elif self._settings.write_func == cst.WRITE_SINGLE_COIL or \
                    self._settings.write_func == cst.WRITE_SINGLE_REGISTER:
                for i in range(len(data)):
                    self._ui.log_print("Writing at address" + str(self._settings.starting_address + i))
                    self.repaint()
                    feedback = self.modbus_client.execute(
                        self._settings.unit_id,
                        self._settings.write_func,
                        (self._settings.starting_address + i),
                        output_value=data[i]
                    )
                    self._ui.log_print("Successful writing")

        except ModbusError as ex:
            error = ex.get_exception_code()
            if error == 1:
                self._ui.log_print("MB exception " + str(error) + ": Illegal Function")
            if error == 2:
                self._ui.log_print("MB exception " + str(error) + ": Illegal data address")
            if error == 3:
                self._ui.log_print("MB exception " + str(error) + ": Illegal data value")
            if error == 4:
                self._ui.log_print("MB exception " + str(error) + ": Slave device failure")
        except OSError as ex:
            self._ui.log_print(str(ex))

    def export_config(self) -> dict:
        """
        Export configuration

        :return: Return parameters into a dictionary.
        """
        config = {
            "settings": self._settings.export_config(),
            "labels": self._ui.table_widget.export_config()
        }
        return config

    def import_config(self, data: dict):
        """
        Import configuration

        :param data: Dict that contains parameters to be imported.
        """
        if data is None:
            return
        # import modbus settings
        self._settings.import_config(data.get("settings", None))

        # import label
        self._ui.table_widget.import_config(data.get("labels", None))

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = range_ui.RangeUI(self)
        ui.read_button.clicked.connect(self._mb_reading_execute)
        ui.write_button.clicked.connect(self._mb_writing_execute)
        ui.open_settings_btn.clicked.connect(self.open_settings)
        return ui
