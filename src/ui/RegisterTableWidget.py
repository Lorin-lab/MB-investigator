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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import modbus_tk.defines as cst


class RegisterTableWidget(QTableWidget):
    def __init__(self):
        super(RegisterTableWidget, self).__init__()

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Address", "Label", "Value"])
        self.verticalHeader().hide()
        self.setStyleSheet("QTableWidget { "
                           "background-color : #CFCFCF;"
                           "border: 2px solid black;"
                           "}")
        self.itemChanged.connect(self._on_table_item_changed)

        self._register_values = []

        # Default parameters
        self._starting_address = 0
        self._quantity = 10
        self._write_func = None

    def change_registers_set(self, starting_address: int, quantity: int, write_func: cst):
        self._register_values.clear()

        self.setRowCount(quantity)
        for i in range(quantity):
            self._register_values.append(None)

            # column 0 : modbus address
            item = QTableWidgetItem(str(starting_address + i))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.setItem(i, 0, item)
            # column 1 : libelle
            self.setItem(i, 1, QTableWidgetItem(""))

        # save new parameters
        self._starting_address = starting_address
        self._quantity = quantity
        self._write_func = write_func

        self.set_register_values(self._register_values)

    def set_register_values(self, values: list):
        self._register_values = values
        self._update_value_display()

    def _update_value_display(self):
        for i in range(self._quantity):
            # column 2 : value
            item = QTableWidgetItem(str(self._register_values[i]))
            if self._write_func is None:
                item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.setItem(i, 2, item)

    def get_register_values(self) -> list:
        return self._register_values

    def _on_table_item_changed(self, item: QTableWidgetItem):
        """Is called when a data is change in the table."""
        if item.column() == 2:  # Column value
            """Checking value prompt by the user"""
            try:
                value = int(item.text())
                if value < 0:
                    value = 0
                elif value > 1 and \
                        (self._write_func == cst.WRITE_MULTIPLE_COILS or
                         self._write_func == cst.WRITE_SINGLE_COIL):
                    value = 1
                elif value > 65535:
                    value = 65535
                self._register_values[item.row()] = value
                item.setText(str(value))
            except ValueError:
                # if int parse fail then undo change
                item.setText(str(self._register_values[item.row()]))

    def export_config(self):
        labels = []
        for i in range(self.rowCount()):
            item = self.item(i, 1)
            labels.append(item.text())
        return labels

    def import_config(self, data):
        # import label
        labels = data
        for i in range(min(self._quantity, len(labels))):
            # column 1 : label
            item = QTableWidgetItem(str(labels[i]))
            self.setItem(i, 1, item)
