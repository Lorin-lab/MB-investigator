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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import modbus_tk.defines as cst
from register_row import RegisterRow as Row


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

        self._register_values = []

        # Default parameters
        self._starting_address = 0
        self._quantity = 0
        self._read_func = None
        self._write_func = None

    def change_address_set(self, new_starting_address: int, new_quantity: int, read_func: cst, write_func: cst):
        """
        Change of the modbus address set.
        :param new_starting_address: Starting address
        :param new_quantity: Number of addresses used
        :param read_func: Modbus function for read access
        :param write_func: Modbus function for writ access
        """

        # Save old row
        old_row = []
        for i in range(self._quantity):
            old_row.append(self.get_row(i))

        self._register_values.clear()
        self.setRowCount(new_quantity)

        for i in range(new_quantity):
            # Keep the rows that fit into the new range.
            index_of_the_old_list = (new_starting_address - self._starting_address + i)
            if (0 <= index_of_the_old_list < self._quantity) and read_func == self._read_func:
                # Keeps the old row.
                self._register_values.append(old_row[index_of_the_old_list].register_value)
                self.set_row_by_index(i, old_row[index_of_the_old_list])
            else:
                # Create a new row.
                item = QTableWidgetItem(str(new_starting_address + i))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                self.setItem(i, 0, item)  # column 0 : modbus address
                self.setItem(i, 1, QTableWidgetItem(""))  # column 1 : libelle
                self._register_values.append(None)

        # save new parameters
        self._starting_address = new_starting_address
        self._quantity = new_quantity
        self._write_func = write_func
        self._read_func = read_func

        # Update register value
        self.set_register_values(self._register_values)

    def get_row(self, index) -> Row:
        """
        Get the row content
        :param index: index of the row
        :return: the row
        """
        try:
            value = int(self.item(index, 2).text())
        except ValueError:
            value = None

        row = Row(addr=int(self.item(index, 0).text()),
                  label=(self.item(index, 1).text()),
                  value=value)
        return row

    def set_row_by_index(self, index: int, row: Row):
        """
        Set the content of a row
        :param index: index of the row
        :param row: the content of the row
        :return:
        """
        self.setItem(index, 0, QTableWidgetItem(str(row.register_addr)))
        self.setItem(index, 1, QTableWidgetItem(str(row.label)))
        self.setItem(index, 2, QTableWidgetItem(str(row.register_value)))

    def set_row(self, row: Row):
        """
        Set the content of a row
        :param row: the content of the row
        :return:
        """
        index = row.register_addr - self._starting_address
        self.set_row_by_index(index, row)

    def set_register_values(self, values: list):
        self._register_values = values
        self._update_value_display()

    def _update_value_display(self):
        for i in range(self._quantity):
            # column 2 : value
            item = QTableWidgetItem(str(self._register_values[i]))
            item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            self.setItem(i, 2, item)  # column 2 : value

    def get_register_values(self) -> list:
        return self._register_values

    def export_config(self) -> list:
        """
        Export labels

        :return: Return a list of labels.
        """
        labels = []
        for i in range(self.rowCount()):
            item = self.item(i, 1)
            labels.append(item.text())
        return labels

    def import_config(self, labels: list):
        """
        Import labels

        :param labels: A list that contains labels.
        """
        if type(labels) is not list:
            return

        for i in range(min(self._quantity, len(labels))):
            # column 1 : label
            item = QTableWidgetItem(str(labels[i]))
            self.setItem(i, 1, item)
