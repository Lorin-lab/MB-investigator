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
from PyQt5.QtGui import QCloseEvent
from modbus_tk.exceptions import *
import modbus_tk.defines as cst

import range_ui
import range_settings_win
import write_win
from register_row import RegisterRow as Row


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

    def _mb_writing_execute(self, register_row: Row):
        """Execute modbus writing function"""

        # Checking client
        if self.modbus_client is None:
            self._ui.log_print("Client not connected")
            return
        # Checking available function
        if self._settings.write_func is None:
            self._ui.log_print("No writing function available")
            return
        # Checking data
        if register_row.register_value is None:
            self._ui.log_print("Value none in data")
            return

        try:
            data = self._ui.table_widget.get_register_values()
            # write data in one shot
            self._ui.log_print("Writing...")
            self.repaint()
            feedback = self.modbus_client.execute(
                self._settings.unit_id,
                self._settings.write_func,
                register_row.register_addr,
                output_value=register_row.register_value
            )
            self._ui.log_print("Successful writing")
            self._ui.table_widget.set_row(register_row)

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

    def _on_table_cell_clicked(self, row: int, column: int):
        if column == 2 and self._settings.write_func is not None:
            self._write_dialog = write_win.WriteWin(self._ui.table_widget.get_row(row),
                                                    self._settings.write_func,
                                                    self._mb_writing_execute)
            self._write_dialog.show()

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

    def set_close_callback(self, func):
        self._close_event_callback_func = func

    def closeEvent(self, event: QCloseEvent) -> None:
        self._close_event_callback_func(self)

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = range_ui.RangeUI(self)
        ui.read_button.clicked.connect(self._mb_reading_execute)
        ui.open_settings_btn.clicked.connect(self.open_settings)
        ui.table_widget.cellClicked.connect(self._on_table_cell_clicked)
        return ui
