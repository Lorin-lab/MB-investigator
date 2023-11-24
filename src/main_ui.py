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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from utils import *
import version


class MainWindowUI(object):
    """This class contains all the widgets and configures them for the main window."""
    def __init__(self, main_window: QMainWindow):
        main_window.setWindowTitle(f'MB-Investigator {version.__VERSION__}')
        main_window.resize(750, 600)
        self.tabs_widget = QTabWidget()
        main_window.setCentralWidget(self.tabs_widget)

        # ****************************
        # Tabs
        # ****************************

        tabs_name = ["Holding Registers", "Input Registers", "Coils", "Discrete input"]
        for name in tabs_name:
            widget = QWidget()
            layout = QVBoxLayout()
            widget.setLayout(layout)
            table = QTableWidget()
            layout.addWidget(table)

            table.setColumnCount(5)
            table.setRowCount(10)
            table.setHorizontalHeaderLabels(["Address", "Label", "Value", "Status", "Action"])

            self.tabs_widget.addTab(widget, name)


        # ****************************
        # menu action bar
        # ****************************
        menu_bar = QMenuBar(main_window)
        main_window.setMenuBar(menu_bar)

        # file menu
        self.action_import_config = QAction("Import config", main_window)
        self.action_export_config = QAction("Export config", main_window)
        self.action_quit = QAction("Quit", main_window)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.action_import_config)
        file_menu.addAction(self.action_export_config)
        file_menu.addAction(self.action_quit)

        # Communication settings
        self.action_settings_device = QAction("Communication settings", main_window)
        self.action_settings_device.setIcon(QIcon(resource_path("icons/outline_settings_black_24dp.png")))
        self.action_open_com = QAction("Open connection", main_window)
        self.action_open_com.setIcon(QIcon(resource_path("icons/outline_link_black_24dp.png")))
        self.action_close_com = QAction("Close connection", main_window)
        self.action_close_com.setIcon(QIcon(resource_path("icons/outline_link_off_black_24dp.png")))

        com_menu = menu_bar.addMenu('Remote device')
        com_menu.addAction(self.action_settings_device)
        com_menu.addAction(self.action_open_com)
        com_menu.addAction(self.action_close_com)

        # Help
        self.action_about = QAction("About", main_window)
        self.action_open_manual = QAction("Online manual", main_window)

        help_menu = menu_bar.addMenu('Help')
        help_menu.addAction(self.action_about)
        help_menu.addAction(self.action_open_manual)

        # ****************************
        # Status bar
        # ****************************
        self.status_bar = QStatusBar(main_window)
        main_window.setStatusBar(self.status_bar)

        # ****************************
        # Tool bar
        # ****************************
        self.toolbar = QToolBar(main_window)
        main_window.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.toolbar)
        # config button
        self.device_config_tool_btn = QToolButton()
        self.device_config_tool_btn.setAutoRaise(True)
        self.device_config_tool_btn.setIcon(QIcon(resource_path("icons/outline_settings_black_24dp.png")))
        self.device_config_tool_btn.setToolTip("Communication settings")
        self.toolbar.addWidget(self.device_config_tool_btn)

        # connect button
        self.connect_tool_btn = QToolButton()
        self.connect_tool_btn.setAutoRaise(True)
        self.connect_tool_btn.setIcon(QIcon(resource_path("icons/outline_link_black_24dp.png")))
        self.connect_tool_btn.setToolTip("Open connection")
        self.toolbar.addWidget(self.connect_tool_btn)

        # disconnect button
        self.disconnect_tool_btn = QToolButton()
        self.disconnect_tool_btn.setAutoRaise(True)
        self.disconnect_tool_btn.setIcon(QIcon(resource_path("icons/outline_link_off_black_24dp.png")))
        self.disconnect_tool_btn.setToolTip("Close connection")
        self.toolbar.addWidget(self.disconnect_tool_btn)

