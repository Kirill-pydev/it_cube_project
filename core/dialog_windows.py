from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QMessageBox, QInputDialog, QFileDialog, QColorDialog, QFontDialog, QDialog, QLabel
)
from PyQt6.QtGui import QColor, QFont

class DialogDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Примеры диалоговых окон")
        self.resize(300, 400)

        layout = QVBoxLayout()

        # Кнопка QMessageBox
        btn_msg = QPushButton("QMessageBox")
        btn_msg.clicked.connect(self.show_message_box)
        layout.addWidget(btn_msg)

        # Кнопка QInputDialog
        btn_input = QPushButton("QInputDialog")
        btn_input.clicked.connect(self.show_input_dialog)
        layout.addWidget(btn_input)

        # Кнопка QFileDialog
        btn_file = QPushButton("QFileDialog")
        btn_file.clicked.connect(self.show_file_dialog)
        layout.addWidget(btn_file)

        # Кнопка QColorDialog
        btn_color = QPushButton("QColorDialog")
        btn_color.clicked.connect(self.show_color_dialog)
        layout.addWidget(btn_color)

        # Кнопка QFontDialog
        btn_font = QPushButton("QFontDialog")
        btn_font.clicked.connect(self.show_font_dialog)
        layout.addWidget(btn_font)

        # Кнопка QDialog
        btn_custom = QPushButton("QDialog (кастомное)")
        btn_custom.clicked.connect(self.show_custom_dialog)
        layout.addWidget(btn_custom)

        self.setLayout(layout)

    # ---------------- Методы для показа диалогов ----------------
    def show_message_box(self):
        msg = QMessageBox()
        msg.setWindowTitle("QMessageBox")
        msg.setText("Это информационное окно")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            print("Да")

    def show_input_dialog(self):
        text, ok = QInputDialog.getText(self, "QInputDialog", "Введите текст:")
        if ok:
            QMessageBox.information(self, "Вы ввели", text)

    def show_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "All Files (*)")
        if file_path:
            QMessageBox.information(self, "Вы выбрали файл", file_path)

    def show_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            QMessageBox.information(self, "Вы выбрали цвет", color.name())

    def show_font_dialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            QMessageBox.information(self, "Вы выбрали шрифт", f"{font.family()}, {font.pointSize()}pt")

    def show_custom_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Кастомное диалоговое окно")
        dialog.resize(200, 100)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это произвольное окно"))
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(dialog.close)
        layout.addWidget(btn_close)
        dialog.setLayout(layout)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = DialogDemo()
    window.show()
    app.exec()
