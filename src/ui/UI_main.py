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
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from utils import *


class UiMain(object):
    """This class contains all the widgets and configures them for the main window."""
    def __init__(self, main_window):
        main_window.setWindowTitle('MB-Investigator')
        main_window.resize(400, 500)

        # ****************************
        # menu action bar
        # ****************************
        menu_bar = QMenuBar(main_window)
        main_window.setMenuBar(menu_bar)

        # file menu
        self.action_import_config = QAction("Import config", main_window)
        self.action_export_config = QAction("Export config", main_window)
        self.action_about = QAction("About", main_window)
        self.action_quit = QAction("Quit", main_window)

        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(self.action_import_config)
        file_menu.addAction(self.action_export_config)
        file_menu.addAction(self.action_about)
        file_menu.addAction(self.action_quit)

        # Communication settings
        self.action_settings_com = QAction("Settings", main_window)
        self.action_open_com = QAction("Open/Connect", main_window)
        self.action_close_com = QAction("Close/Disconnect", main_window)

        com_menu = menu_bar.addMenu('Communication')
        com_menu.addAction(self.action_settings_com)
        com_menu.addAction(self.action_open_com)
        com_menu.addAction(self.action_close_com)

        # Tasks
        self.action_add_task = QAction("Add Range", main_window)

        task_menu = menu_bar.addMenu('Range')
        task_menu.addAction(self.action_add_task)

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
        self.client_config_tool_btn = QToolButton()
        self.client_config_tool_btn.setAutoRaise(True)
        self.client_config_tool_btn.setIcon(QIcon(resource_path("icons/outline_settings_black_24dp.png")))
        self.client_config_tool_btn.setToolTip("Communication settings")
        self.toolbar.addWidget(self.client_config_tool_btn)

        # connect button
        self.connect_tool_btn = QToolButton()
        self.connect_tool_btn.setAutoRaise(True)
        self.connect_tool_btn.setIcon(QIcon(resource_path("icons/outline_link_black_24dp.png")))
        self.connect_tool_btn.setToolTip("Open/Connect")
        self.toolbar.addWidget(self.connect_tool_btn)

        # disconnect button
        self.disconnect_tool_btn = QToolButton()
        self.disconnect_tool_btn.setAutoRaise(True)
        self.disconnect_tool_btn.setIcon(QIcon(resource_path("icons/outline_link_off_black_24dp.png")))
        self.disconnect_tool_btn.setToolTip("Close/Disconnect")
        self.toolbar.addWidget(self.disconnect_tool_btn)

        # Add com task button
        self.Add_section_tool_btn = QToolButton()
        self.Add_section_tool_btn.setAutoRaise(True)
        self.Add_section_tool_btn.setIcon(QIcon(resource_path("icons/outline_add_box_black_24dp.png")))
        self.Add_section_tool_btn.setToolTip("Add range")
        self.toolbar.addWidget(self.Add_section_tool_btn)
