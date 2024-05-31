import sys
import json
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QAction
)
from hash_card_finder import find_card_data, luhn_algorithm

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon('img/img.png'))
        self.setFixedSize(QSize(500, 300))
        self.setWindowTitle("Getting card number by hash")
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.btn_bins = QLineEdit(placeholderText="Enter the list of bins")
        self.btn_hash_card = QLineEdit(placeholderText="Enter hash")
        self.btn_last_number = QLineEdit(placeholderText="Enter 4 last numbers of card")

        self.btn_number_search = QPushButton("Find card number by hash")
        self.btn_number_search.clicked.connect(self.find_number)
        self.btn_luhn = QPushButton("Check card number by Luhn Algorithm")
        self.btn_luhn.clicked.connect(self.luhn_algorithm)

        self.card_number_label = QLabel()
        self.card_number_label.setText("Card number: ")
        self.card_number_label.setFixedSize(500, 15)
        self.card_number_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.card_number_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.btn_bins)
        layout.addWidget(self.btn_hash_card)
        layout.addWidget(self.btn_last_number)
        layout.addWidget(self.btn_number_search)
        layout.addWidget(self.card_number_label)
        layout.addWidget(self.btn_luhn)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.create_menu_bar()

        self.show()

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        
        load_settings_action = QAction('Load Settings from JSON', self)
        load_settings_action.triggered.connect(self.load_json_settings)
        file_menu.addAction(load_settings_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.exit_program)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def show_about_dialog(self):
        QMessageBox.about(self, "About", "This is a simple application for finding card numbers by hash.")

    def load_json_settings(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select JSON Settings File",
            "",
            "JSON File (*.json)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    settings = json.load(file)
                    self.btn_bins.setText(','.join(map(str, settings.get('bins', []))))
                    self.btn_hash_card.setText(settings.get('hash', ''))
                    self.btn_last_number.setText(settings.get('last_numbers', ''))
                    self.card_number_path = settings.get('card_number_path', 'card_number.json')
                    self.graph_path = settings.get('grafic_path', 'grafic.png')
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"An error occurred while loading settings: {e}"
                )

    def find_number(self) -> None:
        bins = self.btn_bins.text().replace(' ', '').split(",")
        hash_card = self.btn_hash_card.text()
        last_number = self.btn_last_number.text()
        file_path = getattr(self, 'card_number_path', 'card_number.json')

        if (not bins) or (hash_card == "") or (last_number == ""):
            QMessageBox.warning(
                self,
                "Warning!",
                "You have not entered some fields",
            )
        else:
            try:
                result = find_card_data(
                    bins,
                    hash_card,
                    last_number,
                    file_path
                )
                if result:
                    self.card_number_label.setText("Card number: " + result)
                    self.card_number = result
                    QMessageBox.information(None, "Successfully", f"Card number found and saved in {file_path}")
                else:
                    self.card_number_label.setText("Card number: ")
                    self.card_number = ""
                    QMessageBox.information(None, "Error", "Card number wasn't found")
            except Exception as e:
                self.card_number_label.setText("Card number: ")
                self.card_number = ""
                QMessageBox.warning(
                    self,
                    "Error",
                    f"An error occurred while finding the card number: {e}"
                )

    def luhn_algorithm(self) -> None:
        if not hasattr(self, 'card_number') or not self.card_number:
            QMessageBox.warning(
                None, "Before check the card number", "Card number wasn't found or checked yet"
            )
            return

        try:
            result = luhn_algorithm(self.card_number)
            if result:
                QMessageBox.information(
                    None, "Luhn Algorithm result", "Card number is valid")
            else:
                QMessageBox.information(
                    None, "Luhn Algorithm result", "Card number is not valid"
                )
        except Exception as e:
            QMessageBox.warning(None, "Error", f"An error occurred while checking card number: {e}")

    def exit_program(self):
        reply = QMessageBox.question(self, 'Exit program', 'Are you sure that you want to exit the program?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
        else:
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
