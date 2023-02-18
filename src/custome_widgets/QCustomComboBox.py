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
from PyQt5.QtWidgets import *


class QCustomComboBox(QComboBox):
    """Extended view of a QComboBox widget that allows the link between the presented text and an internal value."""
    def __init__(self):
        super(QCustomComboBox, self).__init__()
        self._values = []

    def add_option(self, value, text: str, set_as_current=False):
        """Add a option in the in combo box."""
        self._values.append(value)
        self.addItem(text)
        if set_as_current:
            self.set_current_by_value(value)

    def get_current_option_value(self):
        """Get the value of the current selected option."""
        index = self.currentIndex()
        return self._values[index]

    def get_option_value_by_index(self, index: int):
        """Get the value of a option by index in the list."""
        return self._values[index]

    def set_current_by_value(self, option_value):
        """Set a option as current by its value."""
        for i in range(len(self._values)):
            if self._values[i] == option_value:
                self.setCurrentIndex(i)
                break

    def clear_options(self):
        """Delete all options."""
        self._values.clear()
        self.clear()
