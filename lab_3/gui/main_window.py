import json
import os
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel, QLineEdit, QFormLayout, QSpinBox
)
from PyQt5.QtCore import pyqtSlot
from crypto.key_generation import generate_keys
from crypto.encryption import encrypt_data
from crypto.decryption import decrypt_data

class MainWindow(QWidget):
    def __init__(self):
        """
        Initializes the main window of the hybrid cryptosystem application.
        """
        super().__init__()

        self.initUI()

    def initUI(self) -> None:
        """
        Sets up the user interface components and layout for the main window.
        """
        self.setWindowTitle('Гибридная криптосистема')

        layout = QVBoxLayout()

        self.settings_label = QLabel('Путь к файлу настроек:')
        self.settings_path = QLineEdit()
        self.settings_path.setText('settings.json')

        self.key_length_label = QLabel('Длина ключа:')
        self.key_length = QSpinBox()
        self.key_length.setRange(32, 448)
        self.key_length.setSingleStep(8)
        self.key_length.setValue(128)

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

    def load_settings(self) -> Optional[Dict[str, Any]]:
        """
        Loads the settings from the specified JSON file.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the settings if successful, None otherwise.
        """
        settings_file = self.settings_path.text()
        if not os.path.exists(settings_file):
            QMessageBox.critical(self, "Ошибка", f"Файл настроек {settings_file} не найден.")
            return None
        try:
            with open(settings_file, 'r') as file:
                settings = json.load(file)
            settings['key_length'] = self.key_length.value()
            return settings
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при чтении файла настроек: {e}")
            return None

    def ensure_directory_exists(self, path: str) -> None:
        """
        Ensures that the directory for the given path exists. Creates the directory if it does not exist.

        Args:
            path (str): The file path for which to ensure the directory exists.
        """
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    @pyqtSlot()
    def on_generate_keys(self) -> None:
        """
        Slot to handle the key generation process when the 'Generate Keys' button is clicked.
        """
        settings = self.load_settings()
        if settings:
            try:
                key_path = settings.get('symmetric_key', '')
                if not key_path:
                    raise ValueError("Путь для симметричного ключа не указан в файле настроек.")
                
                self.ensure_directory_exists(key_path)
                generate_keys(settings)
                QMessageBox.information(self, "Успех", "Ключи успешно сгенерированы.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при генерации ключей: {e}")

    @pyqtSlot()
    def on_encrypt_data(self) -> None:
        """
        Slot to handle the data encryption process when the 'Encrypt Data' button is clicked.
        """
        settings = self.load_settings()
        if settings:
            try:
                encrypt_data(settings)
                QMessageBox.information(self, "Успех", "Данные успешно зашифрованы.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при шифровании данных: {e}")

    @pyqtSlot()
    def on_decrypt_data(self) -> None:
        """
        Slot to handle the data decryption process when the 'Decrypt Data' button is clicked.
        """
        settings = self.load_settings()
        if settings:
            try:
                decrypt_data(settings)
                QMessageBox.information(self, "Успех", "Данные успешно дешифрованы.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при дешифровании данных: {e}")
