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
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCloseEvent
from modbus_tk.exceptions import *
from PyQt5.QtCore import pyqtSignal

import range_ui
import range_settings_win
import write_win
from mb_regesiter_reader import MbRegisterReader


class RangeWin(QDockWidget):
    """Object for reading and writing to a modbus address range according to parameters.
    All presented with a graphic interface.
    """
    range_counter = 0
    closed_event = pyqtSignal(object)

    def __init__(self, parent, modbus_client):
        super(RangeWin, self).__init__("New range", parent)
        self.modbus_client = modbus_client

        self._reading_thread = None

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
        if self.modbus_client is None:
            self._ui.log_print("Client not connected")
            return

        if self._reading_thread is not None:  # not none when running
            return

        self._ui.read_button.setEnabled(False)

        # Creating thread
        self._reading_thread = MbRegisterReader(
            self.modbus_client,
            self._settings.unit_id,
            self._settings.read_func,
            self._settings.starting_address,
            self._settings.quantity,
            5000,
            loop=self._ui.toggle_read_button.isChecked()
        )

        # Connect signal
        self._reading_thread.finished.connect(self._reading_thread.deleteLater)
        self._reading_thread.finished.connect(self._on_reading_finished)
        self._reading_thread.log_progress.connect(self._ui.log_print)
        self._reading_thread.success.connect(self._ui.table_widget.set_register_values)

        self._reading_thread.start()

    def _on_reading_finished(self):
        self._ui.read_button.setEnabled(True)
        self._reading_thread = None

    def _mb_writing_execute(self, register_row):
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
            "labels": self._ui.table_widget.json_serialize()
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
        self._ui.table_widget.json_deserialize(data.get("labels", None))

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._reading_thread is not None:
            self._reading_thread.set_loop(False)
        self.closed_event.emit(self)

    def _on_reading_loop_toggle(self):
        if self._reading_thread is not None:
            self._reading_thread.set_loop(self._ui.toggle_read_button.isChecked())

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = range_ui.RangeUI(self)
        ui.read_button.clicked.connect(self._mb_reading_execute)
        ui.open_settings_btn.clicked.connect(self.open_settings)
        ui.table_widget.cellClicked.connect(self._on_table_cell_clicked)
        ui.toggle_read_button.clicked.connect(self._on_reading_loop_toggle)
        return ui
