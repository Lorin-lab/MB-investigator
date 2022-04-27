from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from modbus_tk.exceptions import *
import modbus_tk.defines as cst

import UI_modbusComTask
import SettingsTask


class ModbusComTask(QDockWidget):
    """Object for reading and writing to a modbus address range according to parameters.
    All presented with a graphic interface.
    """
    def __init__(self, parent, mb_client):
        super(ModbusComTask, self).__init__("New task", parent)
        self.mb_client = mb_client

        # Instantiates the modbus parameters and their menu.
        self._settings = SettingsTask.SettingsTask(self, self._on_settings_update)
        self._raw_mb_datas = [None]

        self._ui = self._setup_ui()
        self._on_settings_update()
        self._open_settings()

    def _open_settings(self):
        """Opens the modbus configuration menu."""
        self._settings.show()

    def _on_settings_update(self):
        """Is called when the new modbus configuration is validated. Update widgets"""
        print(self._settings.read_func)
        print(self._settings.write_func)
        print("!")
        # Update dock title
        self.setWindowTitle(self._settings.task_name)

        # disable/enable Writing button
        if self._settings.write_func is None:
            self._ui.write_button.setDisabled(True)
        else:
            self._ui.write_button.setEnabled(True)

        # Reset raw data list
        self._raw_mb_datas = [None]
        for i in range(self._settings.quantity):
            self._raw_mb_datas.append(None)

        # Reset table
        self._ui.table_widget.setRowCount(self._settings.quantity)
        for i in range(self._settings.quantity):
            # column 0 : modbus address
            item = QTableWidgetItem(str(self._settings.starting_address + i))
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self._ui.table_widget.setItem(i, 0, item)
            # column 1 : libelle
            self._ui.table_widget.setItem(i, 1, QTableWidgetItem(""))

        # update data in to table
        self._update_table_value()

    def _update_table_value(self):
        """Update value column of the table"""
        for i in range(self._settings.quantity):
            # column 2 : value
            item = QTableWidgetItem(str(self._raw_mb_datas[i]))
            if self._settings.write_func is None:
                item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self._ui.table_widget.setItem(i, 2, item)

    def _on_table_item_changed(self, item: QTableWidgetItem):
        """Is called when a data is change in the table."""
        if item.column() == 2:  # Column value
            """Checking value prompt by the user"""
            try:
                value = int(item.text())
                if value < 0:
                    value = 0
                elif value > 1 and \
                        (self._settings.write_func == cst.WRITE_MULTIPLE_COILS or
                         self._settings.write_func == cst.WRITE_SINGLE_COIL):
                    value = 1
                elif value > 65535:
                    value = 65535
                self._raw_mb_datas[item.row()] = value
            except ValueError:
                # if int parse fail then undo change
                item.setText(str(self._raw_mb_datas[item.row()]))

    def _mb_reading_execute(self):
        """Execute modbus reading function"""
        # Checking client
        if self.mb_client is None:
            self._ui.log_print("Client not connected")
            return

        self._ui.log_print("Reading...")
        self.repaint()

        try:
            # Reading data
            datas = self.mb_client.execute(
                self._settings.unit_id,
                self._settings.read_func,
                self._settings.starting_address,
                self._settings.quantity)
            print(datas)
            self._raw_mb_datas = list(datas)
            self._update_table_value()
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
        except OSError as ex:
            self._ui.log_print(str(ex))

    def _mb_writing_execute(self):
        """Execute modbus writing function"""

        # Checking client
        if self.mb_client is None:
            self._ui.log_print("Client not connected")
            return
        # Checking available function
        if self._settings.write_func is None:
            return
        # Checking data
        for i in self._raw_mb_datas:
            if i is None:
                self._ui.log_print("Value none in data")
                return

        try:
            # write data in one shot
            if self._settings.write_func == cst.WRITE_MULTIPLE_COILS or \
                    self._settings.write_func == cst.WRITE_MULTIPLE_REGISTERS:
                self._ui.log_print("Writing...")
                self.repaint()
                feedback = self.mb_client.execute(
                    self._settings.unit_id,
                    self._settings.write_func,
                    self._settings.starting_address,
                    output_value=self._raw_mb_datas
                )
                self._ui.log_print("Successful writing")

            # write data one by one
            elif self._settings.write_func == cst.WRITE_SINGLE_COIL or \
                    self._settings.write_func == cst.WRITE_SINGLE_REGISTER:
                for i in range(len(self._raw_mb_datas)):
                    print("The i: " + str(i))
                    self._ui.log_print("Writing at address" + str(self._settings.starting_address + i))
                    self.repaint()
                    feedback = self.mb_client.execute(
                        self._settings.unit_id,
                        self._settings.write_func,
                        (self._settings.starting_address + i),
                        output_value=self._raw_mb_datas[i]
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

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_modbusComTask.UiModbusComTask(self)
        ui.read_button.clicked.connect(self._mb_reading_execute)
        ui.write_button.clicked.connect(self._mb_writing_execute)
        ui.open_settings_btn.clicked.connect(self._open_settings)
        ui.table_widget.itemChanged.connect(self._on_table_item_changed)
        return ui
