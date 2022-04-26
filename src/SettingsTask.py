from PyQt5.QtWidgets import *
import modbus_tk.defines as cst

import UI_settingsTask


class SettingsTask(QMainWindow):
    """This class contains the modbus parameters of a task and is the menu for editing them."""
    def __init__(self, parent, call_back_func):
        super(SettingsTask, self).__init__(parent)
        self.call_back_func = call_back_func

        # Settings
        self.task_name = "New task"
        self.starting_address = 0
        self.quantity = 10
        self.read_func = cst.READ_COILS
        self.write_func = cst.WRITE_SINGLE_COIL

        # Combo options
        self._coil_write_funcs = [
            self.ComboBoxOption(cst.WRITE_SINGLE_COIL, "(FC05) Single Coil"),
            self.ComboBoxOption(cst.WRITE_MULTIPLE_COILS, "(FC15) Multiple Coils")
        ]
        self._register_write_funcs = [
            self.ComboBoxOption(cst.WRITE_SINGLE_REGISTER, "(FC06) Single Register"),
            self.ComboBoxOption(cst.WRITE_MULTIPLE_REGISTERS, "(FC16) Multiple Register")
        ]
        self._read_funcs = [
            self.ComboBoxOption(cst.READ_COILS, "(FC01) Coils", self._coil_write_funcs),
            self.ComboBoxOption(cst.READ_DISCRETE_INPUTS, "(FC02) Discrete input"),
            self.ComboBoxOption(cst.READ_HOLDING_REGISTERS, "(FC03) Holding Registers", self._register_write_funcs),
            self.ComboBoxOption(cst.READ_INPUT_REGISTERS, "(FC04) Input Registers")
        ]

        # UI setup
        self._ui = self._setup_ui()
        self._on_read_func_change(0)

    def _validation(self):
        """save the settings close the menu and call the 'call back' function"""
        self.task_name = self._ui.task_name_edit.text()
        self.starting_address = int(self._ui.start_address_edit.text())
        self.quantity = int(self._ui.quantity_edit.text())

        # Saving modbus function
        index_r = self._ui.read_func_list.currentIndex()
        index_w = self._ui.write_func_list.currentIndex()
        read_func_option = self._read_funcs[index_r]
        self.read_func = read_func_option.value
        if read_func_option.associated_options is None:
            self.write_func = None
        else:
            self.write_func = read_func_option.associated_options[index_w].value

        self.close()
        self.call_back_func()

    def _cancel(self):
        """Reset widget with actual settings and close the menu"""
        self._ui.task_name_edit.setText(self.task_name)
        self._ui.start_address_edit.setText(str(self.starting_address))
        self._ui.quantity_edit.setText(str(self.quantity))

        # Reading modbus function combo box
        for i in range(len(self._read_funcs)):
            if self._read_funcs[i].value == self.read_func:
                self._ui.read_func_list.setCurrentIndex(i)
                self._on_read_func_change(i)
                break

        self.close()

    def _on_read_func_change(self, current_index):
        """Updates the writing combo box according to the modbus reading function."""
        self._ui.write_func_list.clear()
        func_wrap = self._read_funcs[current_index]
        if func_wrap.associated_options is None:
            self._ui.write_func_list.setEnabled(False)
        else:
            self._ui.write_func_list.setEnabled(True)
            for obj in func_wrap.associated_options:
                self._ui.write_func_list.addItem(obj.text)

    def _setup_ui(self):
        """Load widgets and connect them to function."""
        ui = UI_settingsTask.UiSettingsTask(self)

        for obj in self._read_funcs:
            ui.read_func_list.addItem(obj.text)
        ui.read_func_list.currentIndexChanged.connect(self._on_read_func_change)

        ui.task_name_edit.setText(self.task_name)
        ui.start_address_edit.setText(str(self.starting_address))
        ui.quantity_edit.setText(str(self.quantity))

        ui.valid_button.clicked.connect(self._validation)
        ui.cancel_button.clicked.connect(self._cancel)

        return ui

    class ComboBoxOption:
        """Packaging to group a value with a string to display for the combo boxes."""
        def __init__(self, value, text, associated_options=None):
            self.value = value
            self.text = text
            self.associated_options = associated_options
