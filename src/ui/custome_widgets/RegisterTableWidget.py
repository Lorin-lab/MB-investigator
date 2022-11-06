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
            old_row.append(self._get_row(i))

        self._register_values.clear()
        self.setRowCount(new_quantity)

        for i in range(new_quantity):
            # Keep the rows that fit into the new range.
            index_of_the_old_list = (new_starting_address - self._starting_address + i)
            if (0 <= index_of_the_old_list < self._quantity) and read_func == self._read_func:
                # Keeps the old row.
                self._register_values.append(old_row[index_of_the_old_list].register_value)
                self._set_row(i, old_row[index_of_the_old_list])
            else:
                # Create a new row.
                item = QTableWidgetItem(str(new_starting_address + i))
                item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
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

    def _get_row(self, index):
        """
        Get the row content
        :param index: index of the row
        :return: the row
        """
        try:
            value = int(self.item(index, 2).text())
        except ValueError:
            value = None

        row = self._Row(addr=int(self.item(index, 0).text()),
                        label=(self.item(index, 1).text()),
                        value=value)
        return row

    def _set_row(self, index: int, row):
        """
        Set the content of a row
        :param index: index of the row
        :param row: the content of the row
        :return:
        """
        self.setItem(index, 0, QTableWidgetItem(str(row.register_addr)))
        self.setItem(index, 1, QTableWidgetItem(str(row.label)))
        self.setItem(index, 2, QTableWidgetItem(str(row.register_value)))

    def set_register_values(self, values: list):
        self._register_values = values
        self._update_value_display()

    def _update_value_display(self):
        for i in range(self._quantity):
            # column 2 : value
            item = QTableWidgetItem(str(self._register_values[i]))
            if self._write_func is None:
                item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.setItem(i, 2, item)  # column 1 : value

    def get_register_values(self) -> list:
        return self._register_values

    def _on_table_item_changed(self, item: QTableWidgetItem):
        """
        Is called when a data is change in the table.
        :param item: TableItem that has changed
        """
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

    class _Row:
        """
        Wrap that groups the content of a row
        """
        def __init__(self, addr=0, label="", value=0):
            """
            Constructor
            :param addr: register address
            :param label: label of the register
            :param value: value of the register
            """
            self.register_addr = addr
            self.label = label
            self.register_value = value
