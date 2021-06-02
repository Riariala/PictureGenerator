import UI
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI.Interface()

    window.show()
    sys.exit(app.exec_())