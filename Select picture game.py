import random
import os
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class GuessThePicture(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Угадай слово по картинке")
        self.resize(500, 400)

        # Список картинок
        self.pictures = [
            "cat.jpg",
            "dog.jpg",
            "bird.jpg",
            "tree.jpg",
            "flower.jpg",
            "house.jpg"
        ]
        # Список слов с вариациями
        self.words = [
            ["Cat", "Кошка", "Кот", "Кошечка"],
            ["Dog", "Собака", "Пес", "Щенок"],
            ["Bird", "Птица", "Птаха", "Птичка"],
            ["Tree", "Дерево", "Древо"],
            ["Flower", "Цветок", "Роза", "Лилия", "Тюльпан"],
            ["House", "Дом", "Домик", "Жилье"]
        ]

        self.used_pictures = []  # Список использованных картинок

        self.current_picture = None
        self.current_word = None

        self.lives = 3  # Начальное количество жизней

        # Создание элементов интерфейса
        self.picture_label = QLabel()
        self.picture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.picture_label.hide()  # Скрываем картинку по умолчанию

        self.word_label = QLabel("Угадайте слово:")
        self.word_label.setFont(QFont("Arial", 16))
        self.word_label.hide()  # Скрываем подсказку по умолчанию

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите слово")
        self.input_field.hide()  # Скрываем поле ввода по умолчанию

        self.check_button = QPushButton("Проверить")
        self.check_button.clicked.connect(self.check_answer)
        self.check_button.hide()  # Скрываем кнопку "Проверить" по умолчанию

        self.back_button = QPushButton("Вернуться в главное меню")
        self.back_button.clicked.connect(self.back_to_main_menu)
        self.back_button.hide()  # Скрываем кнопку "Вернуться" по умолчанию

        self.exit_button = QPushButton("Выход")
        self.exit_button.clicked.connect(self.close)

        self.rules_button = QPushButton("Правила")
        self.rules_button.clicked.connect(self.show_rules)

        self.start_button = QPushButton("Начать игру")
        self.start_button.clicked.connect(self.start_game)

        self.lives_label = QLabel(f"Жизни: {self.lives}")
        self.lives_label.setFont(QFont("Arial", 14))

        # Размещение элементов в окне
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.rules_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.lives_label)  # Добавляем метку с жизнями
        layout.addWidget(self.picture_label)
        layout.addWidget(self.word_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.check_button)
        layout.addWidget(self.back_button)  # Добавляем кнопку "Вернуться"
        self.setLayout(layout)

    def start_game(self):
        self.start_button.hide()
        self.rules_button.hide()
        self.exit_button.hide()

        self.picture_label.show()
        self.word_label.show()
        self.input_field.show()
        self.check_button.show()
        self.back_button.show()  # Отображаем кнопку "Вернуться" при начале игры

        self.lives = 3  # Сбрасываем количество жизней
        self.lives_label.setText(f"Жизни: {self.lives}")

        self.load_new_picture()

    def load_new_picture(self):
        # Выбираем случайную картинку, которая еще не была показана
        while True:
            index = random.randint(0, len(self.pictures) - 1)
            if self.pictures[index] not in self.used_pictures:
                self.current_picture = self.pictures[index]
                self.used_pictures.append(self.current_picture)  # Добавляем использованную картинку в список
                break

        self.current_word = random.choice(self.words[index])  # Случайный выбор варианта слова из списка

        # Загрузка и отображение картинки
        picture_path = os.path.join("pictures", self.current_picture)  # Используем относительный путь
        if os.path.exists(picture_path):
            pixmap = QPixmap(picture_path)
            self.picture_label.setPixmap(pixmap.scaledToWidth(300))
        else:
            QMessageBox.warning(self, "Ошибка", "Картинка не найдена!")

        # Очистка поля ввода
        self.input_field.clear()

    def check_answer(self):
        user_answer = self.input_field.text().strip()

        # Проверяем, есть ли введенное слово в списке вариантов
        if user_answer.lower() in [word.lower() for word in self.words[self.pictures.index(self.current_picture)]]:
            QMessageBox.information(self, "Правильно!", "Вы угадали!")
            self.load_new_picture()
        else:
            QMessageBox.warning(self, "Неверно!", "Попробуйте еще раз!")
            self.lives -= 1
            self.lives_label.setText(f"Жизни: {self.lives}")
            if self.lives == 0:
                self.back_to_main_menu()
    
    def show_rules(self):
        QMessageBox.information(self, "Правила игры", "Правила игры:\n\n1. Перед вами будет показана картинка.\n2. Вам нужно ввести в поле ввода слово, которое соответствует изображению.\n3. Нажмите кнопку \"Проверить\", чтобы проверить свой ответ.")

    def back_to_main_menu(self):
        self.start_button.show()
        self.rules_button.show()
        self.exit_button.show()

        self.picture_label.hide()
        self.word_label.hide()
        self.input_field.hide()
        self.check_button.hide()
        self.back_button.hide()  # Скрываем кнопку "Вернуться" при возврате в главное меню
        self.used_pictures.clear()  # Очищаем список использованных картинок

if __name__ == "__main__":
    app = QApplication([])
    window = GuessThePicture()
    window.show()
    app.exec()