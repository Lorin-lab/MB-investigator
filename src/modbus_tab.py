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
import random

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import modbus_tk.defines as cst

from custome_widgets.recognizablePushButton import RecognizablePushButton
from data_models.modbus_variable import ModbusVariable
from utils import resource_path
from win_mb_variable_settings import WinMbVariableSettings


class ModbusTab(QWidget):
    def __init__(self):
        super(ModbusTab, self).__init__()

        self._variable_list = []
        self._mb_variable_win = WinMbVariableSettings(self, self.redraw)

        # ui
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.add_button = QPushButton("+")
        self.add_button.clicked.connect(self.add_mb_variable)
        self._table = QTableWidget()
        column_list = ["Address", "Label", "Value", "Status", "", ""]
        self._table.setColumnCount(len(column_list))
        self._table.setColumnWidth(4, 5)
        self._table.setColumnWidth(5, 5)
        self._table.setHorizontalHeaderLabels(column_list)
        self._table.verticalHeader().hide()
        layout.addWidget(self.add_button)
        layout.addWidget(self._table)

    def set_variable_list(self, variable_list: list):
        self._variable_list = variable_list
        self.redraw()

    def redraw(self):
        length = len(self._variable_list)
        self._table.setRowCount(length)
        for i in range(length):
            self._draw_row(i, self._variable_list[i])

    def _draw_row(self, index, mb_variable: ModbusVariable):
        # Address
        if mb_variable.register_quantity > 1:
            text = f"{mb_variable.address} - {mb_variable.address + mb_variable.register_quantity - 1}"
            self._table.setItem(index, 0, QTableWidgetItem(text))
        else:
            self._table.setItem(index, 0, QTableWidgetItem(str(mb_variable.address)))
        # Label
        self._table.setItem(index, 1, QTableWidgetItem(mb_variable.label))
        # value
        self._table.setItem(index, 2, QTableWidgetItem(str(mb_variable.value)))
        # status
        self._table.setItem(index, 2, QTableWidgetItem("..."))
        # edit button
        button = RecognizablePushButton(mb_variable,
                                        QIcon(resource_path("icons/tune_FILL0_wght400_GRAD0_opsz48.svg")),
                                        "")
        button.RecognizableClicked.connect(self.edit_mb_variable)
        self._table.setCellWidget(index, 4, button)
        # remove button
        button_remove = RecognizablePushButton(mb_variable,
                                               QIcon(resource_path("icons/delete_FILL0_wght400_GRAD0_opsz24.svg")),
                                               "")
        button_remove.RecognizableClicked.connect(self.remove_mb_variable)
        self._table.setCellWidget(index, 5, button_remove)

    def add_mb_variable(self):
        new = ModbusVariable(0)
        self.edit_mb_variable(new)
        self._variable_list.append(new)
        self.redraw()

    def remove_mb_variable(self, mb_variable: ModbusVariable):
        print(f"u:{mb_variable.address}")
        self._variable_list.remove(mb_variable)
        self.redraw()

    def edit_mb_variable(self, mb_variable: ModbusVariable):
        self._mb_variable_win.open_mb_variable(mb_variable)