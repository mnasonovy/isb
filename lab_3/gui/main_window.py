import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QFormLayout, QSpinBox
)
from PyQt5.QtCore import pyqtSlot
from crypto.key_generation import generate_keys
from crypto.encryption import encrypt_data
from crypto.decryption import decrypt_data

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Гибридная криптосистема')

        layout = QVBoxLayout()

        self.settings_label = QLabel('Путь к файлу настроек:')
        self.settings_path = QLineEdit()
        self.settings_path.setText('settings.json')

        self.key_length_label = QLabel('Длина ключа:')
        self.key_length = QSpinBox()
        self.key_length.setRange(32, 448)
        self.key_length.setSingleStep(8)
        self.key_length.setValue(128)  # Default value

        form_layout = QFormLayout()
        form_layout.addRow(self.settings_label, self.settings_path)
        form_layout.addRow(self.key_length_label, self.key_length)

        self.generate_button = QPushButton('Генерация ключей')
        self.generate_button.clicked.connect(self.on_generate_keys)

        self.encrypt_button = QPushButton('Шифрование данных')
        self.encrypt_button.clicked.connect(self.on_encrypt_data)

        self.decrypt_button = QPushButton('Дешифрование данных')
        self.decrypt_button.clicked.connect(self.on_decrypt_data)

        layout.addLayout(form_layout)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def load_settings(self):
        settings_file = self.settings_path.text()
        if not os.path.exists(settings_file):
            QMessageBox.critical(self, "Ошибка", f"Файл настроек {settings_file} не найден.")
            return None
        with open(settings_file, 'r') as file:
            settings = json.load(file)
        settings['key_length'] = self.key_length.value()
        return settings

    @pyqtSlot()
    def on_generate_keys(self):
        settings = self.load_settings()
        if settings:
            generate_keys(settings)
            QMessageBox.information(self, "Успех", "Ключи успешно сгенерированы.")

    @pyqtSlot()
    def on_encrypt_data(self):
        settings = self.load_settings()
        if settings:
            encrypt_data(settings)
            QMessageBox.information(self, "Успех", "Данные успешно зашифрованы.")

    @pyqtSlot()
    def on_decrypt_data(self):
        settings = self.load_settings()
        if settings:
            decrypt_data(settings)
            QMessageBox.information(self, "Успех", "Данные успешно дешифрованы.")
