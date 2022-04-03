from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import UI_modbusComTask
import SettingsTask
import modbus_tk.defines as cst


class ModbusComTask(QDockWidget):
    def __init__(self, parent, MB_client):
        super(ModbusComTask, self).__init__("New task", parent)
        self.MB_client = MB_client
        self.settings = SettingsTask.SettingsTask(self, self._on_settings_update)

        self.raw_mb_datas = [None]

        self.ui = self._setup_ui()
        self._on_settings_update()

    def _open_settings(self):
        self.settings.show()

    def _on_settings_update(self):
        self.setWindowTitle(self.settings.task_name)

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
            item.setFlags(Qt.ItemFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled))
            self.ui.table_widget.setItem(i, 2, item)

    def _read_execute(self):
        if self.MB_client is None:
            print("pas connecté")
            return

        datas = self.MB_client.execute(
            1, self.settings.read_func, self.settings.starting_address, self.settings.quantity)
        print(datas)
        self.raw_mb_datas = datas
        self._update_table_value()

    def _setup_ui(self):
        ui = UI_modbusComTask.UiModbusComTask()
        ui.init_ui(self)
        ui.read_write_button.clicked.connect(self._read_execute)
        ui.open_settings_btn.clicked.connect(self._open_settings)
        return ui
