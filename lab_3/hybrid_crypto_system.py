import sys


from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main() -> None:
    """
    Entry point for the application. Initializes and starts the PyQt application.

    This function sets up the QApplication, creates an instance of the MainWindow,
    displays it, and starts the application's event loop.

    Returns:
        None
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
