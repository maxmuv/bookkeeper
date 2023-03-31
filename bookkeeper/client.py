import presenter
from PySide6 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    presenter = presenter.Presenter()
    presenter.view.window.show()
    sys.exit(app.exec())
