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
