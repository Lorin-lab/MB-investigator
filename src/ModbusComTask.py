from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import UI_modbusComTask

class ModbusComTask(QDockWidget):
    def __init__(self, parent):
        super(ModbusComTask, self).__init__("New task", parent)
        self.MB_function_code_list = (
           "(FC01) Read Colls",
           "(FC02) Read Discrete",
           "(FC03) Read Holding Registers",
           "(FC04) Read Input Registers",
           "(FC05) Write Single Coll",
           "(FC06) Write Single Register",
           "(FC15) Write Multiple Colls",
           "(FC16) Write Multiple Registers"
        )
        self.raw_values = [None]

        self.ui = self._setup_ui()
        self.resetTable()

    def resetTable(self):
        print("reset table")
        start_address = int(self.ui.start_address_edit.text())
        num_registre = int(self.ui.num_registre_edit.text())

        if start_address + num_registre > 65535:
            delta = 65535 - start_address
            num_registre = delta
            self.ui.num_registre_edit.setText(str(delta))

        for i in range(start_address, start_address + num_registre):
            self.raw_values.append(None)

        self.updateTable()

    def updateTable(self):
        start_address = int(self.ui.start_address_edit.text())
        num_registre = int(self.ui.num_registre_edit.text())

        self.ui.table_widget.setRowCount(num_registre)

        for i in range(num_registre):
            # column 0 : modbus address
            item = QTableWidgetItem(str(start_address + i))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.ui.table_widget.setItem(i, 0, item)
            # column 1 : libelle
            self.ui.table_widget.setItem(i, 1, QTableWidgetItem(""))
            # column 2 : value
            item = QTableWidgetItem(str(self.raw_values[i]))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.ui.table_widget.setItem(i, 2, item)

    def _setup_ui(self):
        ui = UI_modbusComTask.UiModbusComTask()
        ui.init_ui(self)
        ui.cb.addItems(self.MB_function_code_list)
        ui.start_address_edit.returnPressed.connect(self.resetTable)
        ui.num_registre_edit.returnPressed.connect(self.resetTable)
        return ui
