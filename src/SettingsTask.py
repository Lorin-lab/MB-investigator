from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import UI_modbusComTask
import UI_settingsTask
import modbus_tk.defines as cst


class SettingsTask(QMainWindow):
    def __init__(self, parent, call_back_func):
        super(SettingsTask, self).__init__(parent)
        self.call_back_func = call_back_func

        # Settings
        self.task_name = "New task"
        self.starting_address = 0
        self.quantity = 10
        self.read_func = cst.READ_COILS
        self.write_func = cst.WRITE_SINGLE_COIL

        # Combo lists
        self.read_func_list = (
            "(FC01) Coils",
            "(FC02) Discrete input",
            "(FC03) Holding Registers",
            "(FC04) Input Registers",
        )
        self.coil_write_func_list = (
            "(FC05) Single Coil",
            "(FC15) Multiple Coils"
        )
        self.register_write_func_list = (
            "(FC06) Single Register",
            "(FC16) Multiple Registers"
        )

        # UI setup
        self.ui = self._setup_ui()
        self._on_read_func_change(0)

    def _validation(self):
        self.task_name = self.ui.task_name_edit.text()
        self.starting_address = int(self.ui.start_address_edit.text())
        self.quantity = int(self.ui.quantity_edit.text())

        index_r = self.ui.read_func_list.currentIndex()
        index_w = self.ui.write_func_list.currentIndex()
        # Coil
        if index_r == 0:
            self.read_func = cst.READ_COILS
            if index_w == 0:
                self.write_func = cst.WRITE_SINGLE_COIL
            else:
                self.write_func = cst.WRITE_MULTIPLE_COILS
        # Discrete input
        elif index_r == 1:
            self.read_func = cst.READ_DISCRETE_INPUTS
            self.write_func = None
        # holding register
        elif index_r == 2:
            self.read_func = cst.READ_HOLDING_REGISTERS
            if index_w == 0:
                self.write_func = cst.WRITE_SINGLE_REGISTER
            else:
                self.write_func = cst.WRITE_MULTIPLE_REGISTERS
        # Input register
        elif index_r == 3:
            self.read_func = cst.READ_INPUT_REGISTERS
            self.write_func = None

        self.close()
        self.call_back_func()

    def _cancel(self):
        self.ui.task_name_edit.setText(self.task_name)
        self.ui.start_address_edit.setText(str(self.starting_address))
        self.ui.quantity_edit.setText(str(self.quantity))

        current_index = None
        if self.read_func == cst.READ_COILS:
            current_index = 0
        if self.read_func == cst.READ_DISCRETE_INPUTS:
            current_index = 1
        if self.read_func == cst.READ_HOLDING_REGISTERS:
            current_index = 2
        if self.read_func == cst.READ_INPUT_REGISTERS:
            current_index = 4
        self.ui.read_func_list.setCurrentIndex(current_index)
        self._on_read_func_change(current_index)

        self.close()

    def _on_read_func_change(self, current_index):
        if current_index == 1 or current_index == 3:
            self.ui.write_func_list.setEnabled(False)
            self.ui.write_func_list.clear()
        elif current_index == 0:
            self.ui.write_func_list.setEnabled(True)
            self.ui.write_func_list.clear()
            self.ui.write_func_list.addItems(self.coil_write_func_list)
        elif current_index == 2:
            self.ui.write_func_list.setEnabled(True)
            self.ui.write_func_list.clear()
            self.ui.write_func_list.addItems(self.register_write_func_list)

    def _setup_ui(self):
        ui = UI_settingsTask.UiSettingsTask()
        ui.init_ui(self)

        ui.read_func_list.addItems(self.read_func_list)
        ui.read_func_list.currentIndexChanged.connect(self._on_read_func_change)

        ui.task_name_edit.setText(self.task_name)
        ui.start_address_edit.setText(str(self.starting_address))
        ui.quantity_edit.setText(str(self.quantity))

        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui
