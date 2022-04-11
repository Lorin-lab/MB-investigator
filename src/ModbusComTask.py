import socket

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import UI_modbusComTask
import SettingsTask
from modbus_tk.exceptions import *
import modbus_tk.defines as cst


class ModbusComTask(QDockWidget):
    def __init__(self, parent, MB_client):
        super(ModbusComTask, self).__init__("New task", parent)
        self.MB_client = MB_client
        self.settings = SettingsTask.SettingsTask(self, self._on_settings_update)

        self.raw_mb_datas = [None]

        self.ui = self._setup_ui()
        self._on_settings_update()
        self._open_settings()

    def _open_settings(self):
        self.settings.show()

    def _on_settings_update(self):
        self.setWindowTitle(self.settings.task_name)

        # disable/enable Write button
        if self.settings.write_func is None:
            self.ui.write_button.setDisabled(True)
        else:
            self.ui.write_button.setEnabled(True)

        # update raw datas
        self.raw_mb_datas = [None]
        for i in range(self.settings.quantity):
            self.raw_mb_datas.append(None)

        # update table
        self.ui.table_widget.setRowCount(self.settings.quantity)
        for i in range(self.settings.quantity):
            # column 0 : modbus address
            item = QTableWidgetItem(str(self.settings.starting_address + i))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.ui.table_widget.setItem(i, 0, item)
            # column 1 : libelle
            self.ui.table_widget.setItem(i, 1, QTableWidgetItem(""))

        self._update_table_value()

    def _update_table_value(self):
        for i in range(self.settings.quantity):
            # column 2 : value
            item = QTableWidgetItem(str(self.raw_mb_datas[i]))
            if self.settings.write_func is None:
                item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.ui.table_widget.setItem(i, 2, item)

    def _on_table_item_changed(self, item: QTableWidgetItem):
        if item.column() == 2:
            try:
                value = int(item.text())
                if value < 0:
                    value = 0
                elif value > 1 and (self.settings.write_func == cst.WRITE_MULTIPLE_COILS or self.settings.write_func == cst.WRITE_SINGLE_COIL):
                    value = 1
                elif value > 65535:
                    value = 65535
                self.raw_mb_datas[item.row()] = value
            except ValueError:
                pass
            item.setText(str(self.raw_mb_datas[item.row()]))

    def _read_execute(self):
        if self.MB_client is None:
            self.ui.status_print("Client not connected")
            return

        self.ui.status_print("Reading...")
        self.repaint()

        try:
            datas = self.MB_client.execute(
                1, self.settings.read_func, self.settings.starting_address, self.settings.quantity)
            print(datas)
            self.raw_mb_datas = list(datas)
            self._update_table_value()
            self.ui.status_print("Successful reading")
        except ModbusError as ex:
            error = ex.get_exception_code()
            if error == 1:
                self.ui.status_print("MB exception " + str(error) + ": Illegal Function")
            if error == 2:
                self.ui.status_print("MB exception " + str(error) + ": Illegal data address")
            if error == 3:
                self.ui.status_print("MB exception " + str(error) + ": Illegal data value")
            if error == 4:
                self.ui.status_print("MB exception " + str(error) + ": Slave device failure")
        except OSError as ex:
            self.ui.status_print(str(ex))

    def _write_execute(self):

        # Checking client
        if self.MB_client is None:
            self.ui.status_print("Client not connected")
            return
        # Checking available function
        if self.settings.write_func is None:
            return
        # Checking data
        for i in self.raw_mb_datas:
            if i is None:
                self.ui.status_print("Value none in data")
                return

        try:
            # write data in one shot
            if self.settings.write_func == cst.WRITE_MULTIPLE_COILS or self.settings.write_func == cst.WRITE_MULTIPLE_REGISTERS:
                self.ui.status_print("Writing...")
                self.repaint()
                feedback = self.MB_client.execute(
                    1,
                    self.settings.write_func,
                    self.settings.starting_address,
                    output_value=self.raw_mb_datas
                )
                self.ui.status_print("Successful writing")
            # write data one by one
            elif self.settings.write_func == cst.WRITE_SINGLE_COIL or self.settings.write_func == cst.WRITE_SINGLE_REGISTER:
                for i in range(len(self.raw_mb_datas)):
                    print("The i: " + str(i))
                    self.ui.status_print("Writing at address" + str(self.settings.starting_address + i))
                    self.repaint()
                    feedback = self.MB_client.execute(
                        1,
                        self.settings.write_func,
                        (self.settings.starting_address + i),
                        output_value=self.raw_mb_datas[i]
                    )
                    self.ui.status_print("Successful writing")

        except ModbusError as ex:
            error = ex.get_exception_code()
            if error == 1:
                self.ui.status_print("MB exception " + str(error) + ": Illegal Function")
            if error == 2:
                self.ui.status_print("MB exception " + str(error) + ": Illegal data address")
            if error == 3:
                self.ui.status_print("MB exception " + str(error) + ": Illegal data value")
            if error == 4:
                self.ui.status_print("MB exception " + str(error) + ": Slave device failure")
        except OSError as ex:
            self.ui.status_print(str(ex))

    def _setup_ui(self):
        ui = UI_modbusComTask.UiModbusComTask()
        ui.init_ui(self)
        ui.read_button.clicked.connect(self._read_execute)
        ui.write_button.clicked.connect(self._write_execute)
        ui.open_settings_btn.clicked.connect(self._open_settings)
        ui.table_widget.itemChanged.connect(self._on_table_item_changed)
        return ui
