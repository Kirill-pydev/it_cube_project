from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QListWidgetItem, QHeaderView, \
    QMessageBox
from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import QDate
import sys
import os

from db.init_db import create_database
from core.teachers.teachers_controller import *
from core.teachers.teachers_connection_to_group_controller import *
from core.students.students_controller import *
from core.students.students_connection_to_group_controller import *
from core.directions.directions_controller import *
from core.parents.parents_controller import *
from core.parents.parents_connection_to_students_controller import *
from core.groups.group_controller import *
from core.groups.groups_connection_to_direction_controller import *
from core.others import *
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('ui_models/main_window.ui'), self)
        self.setWindowTitle("main")
        self.setFixedSize(self.size())
        self.teachers.clicked.connect(self.open_teachers)
        self.students.clicked.connect(self.open_students)
        self.directions.clicked.connect(self.open_directions)
        self.parents.clicked.connect(self.open_parents)

    def open_teachers(self):
        self.teachers = Teachers()
        self.teachers.show()
        self.hide()

    def open_students(self):
        self.students = Students()
        self.students.show()
        self.hide()

    def open_directions(self):
        self.directions = Directions()
        self.directions.show()
        self.hide()

    def open_parents(self):
        self.parents = Parents()
        self.parents.show()
        self.hide()


class Teachers(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("ui_models/teachers.ui"), self)
        self.setWindowTitle("Учителя")
        self.setFixedWidth(1102)

        # Блокировка стандартных кнопок окна
        disabling_buttons(self)

        # Кнопки окна и строка поиска
        self.close_btn.clicked.connect(lambda: close_user_window(self))
        self.add_teacher.clicked.connect(self.open_add_teacher)
        self.search_field.textChanged.connect(lambda text: self.on_search_text_changed(text))

        # Загрузка данных на странице
        self.load_table()

    # загрузка данных
    def load_table(self):
        self.data = get_all_teachers()
        self.teachers_list.clear()
        self.teachers_list.setColumnCount(8)
        self.teachers_list.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Отчество", "Номер телефона", "Электронная почта", "Действие",
             "Действие"])
        self.teachers_list.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(len(self.data[i]) + 1):
                if j == 6:
                    item = QtWidgets.QPushButton("Редактировать")
                    self.teachers_list.setCellWidget(i, j, item)
                    item.clicked.connect(lambda _, row_idx=i, row_id=self.data[i][0]: self.update_row(row_id))
                elif j == 7:
                    item = QtWidgets.QPushButton("Удалить")
                    self.teachers_list.setCellWidget(i, j, item)
                    item.clicked.connect(lambda _, row_idx=i, row_id=self.data[i][0]: self.delete_row(row_id))
                else:
                    item = QTableWidgetItem(str(self.data[i][j]))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.teachers_list.setItem(i, j, item)
        self.teachers_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # функция удаления учителя
    def delete_row(self, row_id):
        msg = QMessageBox()
        msg.setText("Удалить преподавателя?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            delete_teacher(row_id)
            delete_teacher_to_group_connection(row_id)
            self.load_table()

    # функция открытия окна редактирования данных преподавателя
    def update_row(self, row_id):
        self.update_teacher_window = AddTeacher(previous_window="teachers", teacher_id=row_id)
        self.update_teacher_window.show()
        self.hide()

    # функция открытия окна добавления нового преподавателя
    def open_add_teacher(self):
        self.add_teacher_window = AddTeacher("teachers")
        self.add_teacher_window.show()
        self.hide()

    # функция поиска по таблице
    def on_search_text_changed(self, text):
        search_text = text.lower()
        columns_to_search = [0, 1, 2, 3]
        for row in range(self.teachers_list.rowCount()):
            match = False
            for col in columns_to_search:
                item = self.teachers_list.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.teachers_list.setRowHidden(row, not match)


class AddTeacher(QMainWindow):
    def __init__(self, previous_window, teacher_id=0):
        super().__init__()
        uic.loadUi(resource_path('ui_models/add_teacher.ui'), self)
        self.setWindowTitle("Добавление учителя")
        self.setFixedSize(851, 521)

        self.previous_window = previous_window
        self.teacher_id = teacher_id

        # Кнопки окна
        self.close_btn.clicked.connect(self.close_add_teacher_window)

        # Отключение стандартных кнопок окна
        disabling_buttons(self)

        if self.teacher_id != 0:
            self.load_data()
            self.add_teacher.clicked.connect(self.update_teacher_func)
            self.add_teacher.setText("Сохранить")
        else:
            self.data = [self.teacher_id, self.surname.text(), self.name.text(), self.father_name.text(),
                         self.phone_number.text(),
                         self.email.text(), self.notes.toPlainText()]
            self.add_teacher.clicked.connect(self.add_teacher_func)

    # функция закрытия окна добавления/редактирования данных преподавателя
    def close_add_teacher_window(self):
        data = [self.teacher_id, self.surname.text(), self.name.text(), self.father_name.text(),
                self.phone_number.text(),
                self.email.text(), self.notes.toPlainText()]
        if data != self.data:
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Вы внесли изменения, но не сохранили их.\nСохранить изменения?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = msg.exec()
            if result == QMessageBox.StandardButton.Yes:
                if self.data[0] == 0:
                    self.add_teacher_func()
                else:
                    self.update_teacher_func()
        back_to_user_window(self)

    # функция добавления нового преподавателя в базу данных
    def add_teacher_func(self):
        data = [self.surname.text(), self.name.text(), self.father_name.text(), self.phone_number.text(),
                self.email.text(), self.notes.toPlainText()]
        res = add_teacher(data)
        if res["succes"]:
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Педагог успешно добавлен!")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes)
            msg.exec()
            self.teacher_id = res["new_data"]
        else:
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText(f"Ошибка\n{'\n'.join(res["message"])}")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes)
            msg.exec()
        self.surname.clear()
        self.name.clear()
        self.father_name.clear()
        self.phone_number.clear()
        self.email.clear()
        self.notes.clear()
        back_to_user_window(self)

    # функция обновления данных преподавателя
    def update_teacher_func(self):
        data = [self.teacher_id, self.surname.text(), self.name.text(), self.father_name.text(),
                self.phone_number.text(),
                self.email.text(), self.notes.toPlainText()]
        update_data = update_teacher(data)
        if update_data["succes"]:
            self.data = data.copy()
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Данные преподавателя обновлены")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes)
            msg.exec()
        else:
            self.load_data()
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText(f"Ошибка\n{'\n'.join(update_data["message"])}")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes)
            msg.exec()

    # загрузка данных
    def load_data(self):
        self.data = get_teacher_by_id(self.teacher_id)
        self.surname.setText(self.data[1])
        self.name.setText(self.data[2])
        self.father_name.setText(self.data[3])
        self.phone_number.setText(self.data[4])
        self.email.setText(self.data[5])
        self.notes.setText(self.data[6])


class Students(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path("ui_models/students.ui"), self)
        self.setFixedWidth(1453)

        # Кнопки
        self.add_student_button.clicked.connect(self.open_add_student)
        self.close_btn.clicked.connect(lambda: close_user_window(self))

        # Поле поиска
        self.search_field.textChanged.connect(lambda text: self.on_search_text_changed(text))

        # Отключение базовых кнопок окна
        disabling_buttons(self)

        self.load_table()

    # загрузка данных
    def load_table(self):
        self.data = get_all_students()
        self.students_list.setColumnCount(15)
        self.students_list.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Отчество", "Школа", "Пол", "Дата рождения", "Класс", "Номер ПФДО",
             "Номер телефона", "Электронная почта", "ОПД", "ФС", "Действие",
             "Действие"])
        self.students_list.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(len(self.data[i]) + 1):
                if j == 13:
                    item = QtWidgets.QPushButton("Редактировать")
                    self.students_list.setCellWidget(i, j, item)
                    item.clicked.connect(lambda _, row_idx=i, row_id=self.data[i][0]: self.update_row(row_id))
                elif j == 14:
                    item = QtWidgets.QPushButton("Удалить")
                    self.students_list.setCellWidget(i, j, item)
                    item.clicked.connect(lambda _, row_idx=i, row_id=self.data[i][0]: self.delete_row(row_id))
                elif j == 11 or j == 12:
                    if self.data[i][j + 1] == 1:
                        item = QTableWidgetItem("Да")
                    else:
                        item = QTableWidgetItem("Нет")
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.students_list.setItem(i, j, item)
                else:
                    item = QTableWidgetItem(str(self.data[i][j]))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.students_list.setItem(i, j, item)
        self.students_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # функция удаления ученика
    def delete_row(self, row_id):
        msg = QMessageBox()
        msg.setText("Удалить ученика?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            delete_student(row_id)
            parents_id = delete_connection_to_parent_by_student_id(row_id)
            delete_parent(parents_id)
            delete_student_connections_to_groups(row_id)
            self.load_table()

    # функция открытия окна для редактирования даанных ученика
    def update_row(self, row_id):
        self.update_student_window = AddStudent(previous_window="students", student_id=row_id)
        self.update_student_window.show()
        self.hide()

    # функция поиска по таблице
    def on_search_text_changed(self, text):
        search_text = text.lower()
        # Индексы столбцов, где будет поиск
        columns_to_search = [0, 1, 2, 3]
        for row in range(self.students_list.rowCount()):
            match = False
            for col in columns_to_search:
                item = self.students_list.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.students_list.setRowHidden(row, not match)

    # функция открытия окна для добавления нового ученика
    def open_add_student(self):
        self.add_student_window = AddStudent()
        self.add_student_window.show()
        self.hide()


class AddStudent(QMainWindow):
    def __init__(self, previous_window, student_id=0):
        super().__init__()
        uic.loadUi(resource_path('ui_models/add_student.ui'), self)
        self.setFixedSize(800, 793)
        disabling_buttons(self)

        # необходимые переменные
        self.student_id = student_id
        self.previous_window = previous_window
        self.parents = []
        self.data = []

        self.close_btn.clicked.connect(self.close_current_window) # закрытие окна
        self.open_history.clicked.connect(self.open_student_learning_history) # просмотр истории обучения

        # функционал добавления/удаления/редактирования данных родителей ученика
        self.add_parent_1.clicked.connect(self.add_parent_func)
        self.add_parent_2.clicked.connect(self.add_parent_func)
        self.add_parent_1.setEnabled(False)
        self.add_parent_2.setEnabled(False)
        self.open_history.setEnabled(False)
        self.delete_parent_1.clicked.connect(lambda: self.delete_parent(0))
        self.update_parent_1.clicked.connect(lambda: self.update_parent(0))
        self.delete_parent_2.clicked.connect(lambda: self.delete_parent(1))
        self.update_parent_2.clicked.connect(lambda: self.update_parent(1))
        self.delete_parent_1.hide()
        self.update_parent_1.hide()
        self.delete_parent_2.hide()
        self.update_parent_2.hide()

        if self.student_id != 0:
            self.load_data()
            self.add_parent_1.setEnabled(True)
            self.add_parent_2.setEnabled(True)
            self.open_history.setEnabled(True)
            self.add_student_button.clicked.connect(self.update_student_func)
            self.add_student_button.setText("Сохранить")
        else:
            self.data = [self.student_id, self.surname.text(), self.name.text(), self.father_name.text(),
                         self.school.text(),
                         self.gender.currentText(), self.birth_date.date().toString("dd.MM.yyyy"),
                         self.class_number.text(),
                         self.certificate_pfdo.text(),
                         self.phone_number.text(), self.email.text(), self.notes.toPlainText(),
                         self.agreement_for_processing.isChecked(), self.agreement_for_shooting.isChecked()]
            self.add_student_button.clicked.connect(self.add_student_func)

    # функция добавлния нового ученика в базу данных
    def add_student_func(self):
        surname = self.surname.text()
        name = self.name.text()
        father_name = self.father_name.text()
        school = self.school.text()
        gender = self.gender.currentText()
        birth_date = self.birth_date.date().toString("dd.MM.yyyy")
        class_number = self.class_number.text()
        certificate_pfdo = self.certificate_pfdo.text()
        phone_number = self.phone_number.text()
        email = self.email.text()
        notes = self.notes.toPlainText()
        sp = [surname, name, father_name, school, gender, birth_date, class_number, certificate_pfdo, phone_number,
              email, notes]
        sp.append(self.agreement_for_processing.isChecked())
        sp.append(self.agreement_for_shooting.isChecked())
        self.student_data = add_student(sp)
        if self.student_data["succes"]:
            self.student_id = self.student_data["new_data"][0]
            self.data = [self.student_data["new_data"][0]] + sp.copy()
            self.add_parent_1.setEnabled(True)
            self.add_parent_2.setEnabled(True)
            self.open_history.setEnabled(True)
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Ученик успешно добавлен!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            messages = '\n'.join(self.student_data["message"])
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText(f"Ошибка\n{messages}")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    # функция обновления данных существующего ученика
    def update_student_func(self):
        sp = [self.student_id, self.surname.text(), self.name.text(), self.father_name.text(), self.school.text(),
              self.gender.currentText(), self.birth_date.date().toString("dd.MM.yyyy"), self.class_number.text(),
              self.certificate_pfdo.text(),
              self.phone_number.text(), self.email.text(), self.notes.toPlainText(),
              self.agreement_for_processing.isChecked(), self.agreement_for_shooting.isChecked()]
        if sp != self.data:
            student_data = update_student(sp)
            if student_data["succes"]:
                self.data = sp.copy()
                msg = QMessageBox()
                msg.setWindowTitle("QMessageBox")
                msg.setText("Данные об ученике успешно обновлены!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("QMessageBox")
                msg.setText(f"Ошибка\n{'\n'.join(student_data["message"])}")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
                button = False

    # загрузка данных
    def load_data(self):
        self.data = get_student_by_id(self.student_id)
        self.surname.setText(self.data[1])
        self.name.setText(self.data[2])
        self.father_name.setText(self.data[3])
        self.school.setText(self.data[4])
        self.gender.setCurrentText(self.data[5])
        self.birth_date.setDate(QDate.fromString(self.data[6], "dd.MM.yyyy"))
        self.class_number.setText(self.data[7])
        self.certificate_pfdo.setText(self.data[8])
        self.phone_number.setText(self.data[9])
        self.email.setText(self.data[10])
        self.notes.setText(self.data[11])
        self.agreement_for_processing.setChecked(self.data[12] in ["Yes", 1])
        self.agreement_for_shooting.setChecked(self.data[13] in ["Yes", 1])
        self.parents = get_parents_by_id(get_parents_by_student_id(self.student_id))
        if self.parents:
            if len(self.parents) > 0:
                self.add_parent_1.hide()
                self.parent_1.setText(" ".join(self.parents[0][1:4]))
                self.delete_parent_1.show()
                self.update_parent_1.show()
            if len(self.parents) > 1:
                self.add_parent_2.hide()
                self.parent_2.setText(" ".join(self.parents[1][1:4]))
                self.delete_parent_2.show()
                self.update_parent_2.show()

    # функция для добавления родителя ученика (1)
    def add_parent_func(self):
        self.parents_w = AddParent(previous_window=self.previous_window, student_id=self.student_id)
        # self.parents_w.text_submitted.connect(self.parent_1_label)
        self.parents_w.show()
        self.hide()

    # функция открытия истории обучения ученика
    def open_student_learning_history(self):
        self.history = GroupsHistory(self.student_id)
        self.history.show()
        self.hide()

    # удаление родителя
    def delete_parent(self, parent_position):
        msg = QMessageBox()
        msg.setText("Удалить данные о родителе?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            pravda_1 = delete_parent([self.parents[parent_position][0]])
            pravda_2 = delete_connection_by_student_and_parent_id([self.parents[parent_position][0], self.student_id])
            if pravda_1 and pravda_2:
                if parent_position == 0:
                    self.parent_1.clear()
                    self.parent_1.hide()
                    self.add_parent_1.show()
                    self.delete_parent_1.hide()
                    self.update_parent_1.hide()
                else:
                    self.parent_2.clear()
                    self.parent_2.hide()
                    self.add_parent_2.show()
                    self.delete_parent_2.hide()
                    self.update_parent_2.hide()

    # обновления данных родителя
    def update_parent(self, parent_position):
        self.update_parent_window = AddParent(previous_window=self.previous_window, student_id=self.student_id,
                                              parent_id=self.parents[parent_position][0])
        self.update_parent_window.show()
        self.hide()

    # открытие списка всех родителей
    def open_parents(self):
        self.parents_window = Parents()
        self.parents_window.show()
        self.hide()

    # функционал корректного закрытия окна редактирования данных ученика, для соблюдения правильной последовательности закрытия
    def close_current_window(self):
        sp = [self.student_id, self.surname.text(), self.name.text(), self.father_name.text(), self.school.text(),
              self.gender.currentText(), self.birth_date.date().toString("dd.MM.yyyy"), self.class_number.text(),
              self.certificate_pfdo.text(),
              self.phone_number.text(), self.email.text(), self.notes.toPlainText(),
              self.agreement_for_processing.isChecked(), self.agreement_for_shooting.isChecked()]
        if sp != self.data:
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Вы внесли изменения, но не сохранили их.\nСохранить изменения?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = msg.exec()
            if result == QMessageBox.StandardButton.Yes:
                if self.data[0] == 0:
                    self.add_student_func()
                else:
                    self.update_student_func()
        if self.previous_window == "parents":
            self.open_parents()
        else:
            back_to_user_window(self)


class Directions(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('ui_models/directions.ui'), self)
        self.setFixedWidth(800)
        disabling_buttons(self)
        self.close_btn.clicked.connect(lambda: close_user_window(self))
        self.add_direction.clicked.connect(self.open_add_direction)

        # необходимые переменные
        directions = get_all_directions()

        # заполнение данных
        for i in range(len(directions)):
            name = directions[i][1]
            code = directions[i][0]
            button_text = f"{name}"
            button = QPushButton(button_text)
            btn = QListWidgetItem(self.directions_list)
            btn.setSizeHint(button.sizeHint())
            self.directions_list.addItem(btn)
            self.directions_list.setItemWidget(btn, button)
            button.clicked.connect(lambda _, x=code: self.show_message(x))

    # функция открытия окна для добавления нового направления
    def open_add_direction(self):
        self.add_direction = AddDirection()
        self.add_direction.show()
        self.hide()

    # функцияя открытия окна направления
    def show_message(self, direction_id):
        self.add = Groups(direction_id=direction_id, previous_window="directions")
        self.add.show()
        self.hide()


class AddDirection(QMainWindow):
    def __init__(self, previous_window):
        super().__init__()
        uic.loadUi(resource_path('ui_models/add_update_direction.ui'), self)
        self.setFixedSize(521, 209)
        disabling_buttons(self)
        self.close_btn.clicked.connect(lambda: back_to_user_window(self))
        self.save.clicked.connect(self.save_direction)

        # переменные
        self.previous_window = previous_window

    # создание нового направления
    def save_direction(self):
        data = [self.direction_name.text()]
        if add_direction(data):
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Направление успешно добавлено!")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes)
            msg.exec()
        back_to_user_window(self)


class Groups(QMainWindow):
    def __init__(self, direction_id, previous_window):
        super().__init__()
        uic.loadUi(resource_path('ui_models/groups.ui'), self)
        self.setFixedWidth(800)
        disabling_buttons(self)
        self.close_btn.clicked.connect(lambda: back_to_user_window(self))
        self.add_group.clicked.connect(self.add_new_group)
        self.delete_direction.clicked.connect(self.func_delete_direction)

        # переменные
        self.previous_window = previous_window
        self.direction_id = direction_id

        self.load_data()

    # функция открытия окна для добавления новой группы
    def add_new_group(self):
        self.add_group_window = AddGroup(direction_id=self.direction_id)
        self.add_group_window.show()
        self.hide()

    # загрузка данных
    def load_data(self):
        self.groups = get_all_groups_by_id_list(get_groups_id_by_direction_id(self.direction_id))
        for i in range(len(self.groups)):
            name = self.groups[i][1]
            code = self.groups[i][0]
            button_text = f"{name}"
            button = QPushButton(button_text)
            btn = QListWidgetItem(self.groups_list)
            btn.setSizeHint(button.sizeHint())
            self.groups_list.addItem(btn)
            self.groups_list.setItemWidget(btn, button)
            button.clicked.connect(lambda _, x=code: self.show_message(x))

    # взаимодействие с данными уже созданной группы
    def show_message(self, group_id):
        self.open_group = AddGroup(direction_id=self.direction_id, group_id=group_id, previous_window=self.previous_window)
        self.open_group.show()
        self.hide()

    # функция удаления направления (если в направлении ещё не созданны группы)
    def func_delete_direction(self):
        if len(get_groups_id_by_direction_id(self.direction_id)) != 0:
            msg = QMessageBox()
            msg.setText("Вы не можете удалить направление, т.к. у него есть группы")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setText("Удалить направление?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = msg.exec()
            if result == QMessageBox.StandardButton.Yes:
                delete_direction(self.direction_id)
            back_to_user_window(self)


class AddGroup(QMainWindow):
    def __init__(self, previous_window, direction_id, group_id=None):
        super().__init__()
        uic.loadUi(resource_path('ui_models/add_update_group.ui'), self)
        # всё, что связанно с окном
        self.setFixedSize(800, 827)
        disabling_buttons(self)
        self.close_btn.clicked.connect(self.back_to_group)
        self.enroll_student.clicked.connect(self.add_student_to_course)
        self.enroll_student.setEnabled(False)

        # переменные
        self.previous_window = previous_window
        self.group_id = group_id
        self.direction_id = direction_id
        self.direction = get_direction_by_id(self.direction_id)
        self.direction_name.setText(self.direction[1])

        # заполнение выпадающего списка учителями
        teachers = get_all_teachers()
        self.teacher.addItem("Не выбран")
        for el in teachers:
            self.teacher.addItem(' '.join([el[1], el[2], el[3]]), userData=el[0])

        # заполнение информации, если открывается окно уже существующей группы
        if self.group_id:
            self.save.clicked.connect(self.update_group)
            self.group_info = get_all_groups_by_id_list([self.group_id])[0]
            self.group_name.setText(self.group_info[1])
            self.teacher_info = get_teacher_by_id(get_connection_by_group_id(self.group_id))
            self.set_teacher(self.teacher_info[0])
            self.start_of_the_course.setDate(QDate.fromString(self.group_info[2], "dd.MM.yyyy"))
            self.end_of_the_course.setDate(QDate.fromString(self.group_info[3], "dd.MM.yyyy"))
            self.enroll_student.setEnabled(True)
            self.load_table()
        else:
            self.save.clicked.connect(self.save_new_group)

    # функция открытия окна для зачисления учащихся в группу
    def add_student_to_course(self):
        self.enroll_window = EnrollStudent(group_id=self.group_id, direction_id=self.direction_id)
        self.enroll_window.show()
        self.hide()

    # функция создания новой группы в базе данных
    def save_new_group(self):
        group_name = self.group_name.text()
        teacher_id = self.teacher.currentData()
        start_of_the_course = self.start_of_the_course.date().toString("dd.MM.yyyy")
        end_of_the_course = self.end_of_the_course.date().toString("dd.MM.yyyy")
        self.group_id = add_new_group(group_name, start_of_the_course, end_of_the_course)
        if self.group_id and teacher_id:
            add_new_teacher_to_group_connection(self.group_id, teacher_id)
            add_new_connection_group_to_direction(self.direction_id, self.group_id)
            self.enroll_student.setEnabled(True)

    # возврат к списку групп раннее выбранного направления
    def back_to_group(self):
        self.groups = Groups(direction_id=self.direction_id, previous_window=self.previous_window)
        self.groups.show()
        self.hide()

    # установка учителя (для уже существующей группы)
    def set_teacher(self, teacher_id):
        if teacher_id:
            for i in range(self.teacher.count()):
                if self.teacher.itemData(i) == teacher_id:
                    self.teacher.setCurrentIndex(i)
                    break
        else:
            self.teacher.setCurrentIndex(0)

    # функция обновления данныых уже существющей группы
    def update_group(self):
        group_name = self.group_name.text()
        teacher_id = self.teacher.currentData()
        start_of_the_course = self.start_of_the_course.date().toString("dd.MM.yyyy")
        end_of_the_course = self.end_of_the_course.date().toString("dd.MM.yyyy")
        update_group([self.group_id, group_name, start_of_the_course, end_of_the_course])
        update_teacher_to_group_connection([self.group_id, teacher_id])

    # загрузка данных таблицы учеников группы
    def load_table(self):
        students = get_students_by_id(get_students_id_by_group_id(self.group_id), 0)
        self.students_list.setColumnCount(9)
        self.students_list.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Отчество", "Номер ПФДО",
             "Номер телефона", "Электронная почта", "Дополнительно", "Действие"])
        self.students_list.setRowCount(len(students))
        for i in range(len(students)):
            id_column = 0
            for j in range(len(students[i]) + 1):
                if j == 12:
                    item = QtWidgets.QPushButton("Отчислить")
                    self.students_list.setCellWidget(i, id_column, item)
                    item.clicked.connect(lambda _, row_idx=i, student_id=students[i][0]: self.deduct(student_id))
                elif j in [0, 1, 2, 3, 8, 9, 10, 11]:
                    item = QTableWidgetItem(str(students[i][j]))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.students_list.setItem(i, id_column, item)
                    id_column += 1

    # функция отчисления учащегося из группы
    def deduct(self, student_id):
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        update_student_to_group_connection([self.group_id, student_id, time_now])
        for row in range(self.students_list.rowCount()):
            item = self.students_list.item(row, 0)  # столбец с ID
            if item and item.text() == str(student_id):
                self.students_list.removeRow(row)


class EnrollStudent(QMainWindow):
    def __init__(self, group_id, direction_id):
        super().__init__()
        uic.loadUi(resource_path('ui_models/enroll_student.ui'), self)
        self.setFixedWidth(1103)
        self.close_btn.clicked.connect(self.close_enroll_students_window)
        disabling_buttons(self)

        # переменные
        self.group_id = group_id
        self.direction_id = direction_id

        self.load_table()

    # загрузка данных
    def load_table(self):
        students = get_students_by_id(get_students_id_by_group_id(self.group_id), 1)
        self.students_list.setColumnCount(9)
        self.students_list.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Отчество", "Номер ПФДО",
             "Номер телефона", "Электронная почта", "Дополнительно", "Действие"])
        self.students_list.setRowCount(len(students))
        self.search_field.textChanged.connect(lambda text: self.on_search_text_changed(text))

        for i in range(len(students)):
            id_column = 0
            for j in range(len(students[i]) + 1):
                if j == 12:
                    item = QtWidgets.QPushButton("Зачислить")
                    self.students_list.setCellWidget(i, id_column, item)
                    item.clicked.connect(lambda _, row_idx=i, student_id=students[i][0]: self.enroll(student_id))
                elif j in [0, 1, 2, 3, 8, 9, 10, 11]:
                    item = QTableWidgetItem(str(students[i][j]))
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.students_list.setItem(i, id_column, item)
                    id_column += 1

        self.students_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # зачисление в группу
    def enroll(self, student_id):
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        add_new_student_to_group_connection([self.group_id, student_id, time_now])
        for row in range(self.students_list.rowCount()):
            item = self.students_list.item(row, 0)
            if item and item.text() == str(student_id):
                self.students_list.removeRow(row)

    # механизм строки поиска
    def on_search_text_changed(self, text):
        search_text = text.lower()
        # Индексы столбцов, где будет поиск
        columns_to_search = [0, 1, 2, 3]
        for row in range(self.students_list.rowCount()):
            match = False
            for col in columns_to_search:
                item = self.students_list.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.students_list.setRowHidden(row, not match)

    # закрытие окна выбора учеников для зачисления, возврат к окну группы
    def close_enroll_students_window(self):
        self.hide()
        self.direction_window = AddGroup(direction_id=self.direction_id, group_id=self.group_id)
        self.direction_window.show()


class Parents(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('ui_models/parents.ui'), self)
        self.setFixedWidth(1103)
        self.close_btn.clicked.connect(lambda: close_user_window(self))
        self.search_field.textChanged.connect(lambda text: self.on_search_text_changed(text))
        disabling_buttons(self)

        self.load_table()

    # загрузка данных
    def load_table(self):
        self.data = get_all_parents()
        self.parents_list.setColumnCount(9)
        self.parents_list.setHorizontalHeaderLabels(
            ["ID", "Фамилия", "Имя", "Отчество", "Номер телефона", "Электронная почта", "Дополнительно", "Ребенок",
             "Действие"])
        self.parents_list.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(len(self.data[i]) + 1):
                if j == 8:
                    item = QtWidgets.QPushButton("Редактировать")
                    self.parents_list.setCellWidget(i, j, item)
                    item.clicked.connect(lambda _, row_idx=i, row_id=self.data[i][0]: self.update_row(row_id))
                else:
                    if j == 7:
                        item = QtWidgets.QPushButton("Ссылка")
                        self.parents_list.setCellWidget(i, j, item)
                        item.clicked.connect(lambda _, row_idx=i, row_id=self.data[i][7]: self.open_student(row_id))
                    else:
                        item = QTableWidgetItem(str(self.data[i][j]))
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.parents_list.setItem(i, j, item)
        self.parents_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # редактирование данных родителя
    def update_row(self, row_id):
        self.hide()
        self.update_parent_window = AddParent(previous_window="parents", parent_id=row_id)
        self.update_parent_window.show()

    # функция поиска в таблице
    def on_search_text_changed(self, text):
        search_text = text.lower()
        # Индексы столбцов, где будет поиск
        columns_to_search = [0, 1, 2, 3]
        for row in range(self.parents_list.rowCount()):
            match = False
            for col in columns_to_search:
                item = self.parents_list.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.parents_list.setRowHidden(row, not match)

    # функция открытия ученика через родителя
    def open_student(self, student_id):
        self.student_window = AddStudent(previous_window="parents", student_id=student_id)
        self.student_window.show()
        self.hide()


class AddParent(QMainWindow):
    def __init__(self, previous_window, student_id=0, parent_id=0):
        super().__init__()
        uic.loadUi(resource_path('ui_models/add_parent.ui'), self)
        self.setFixedSize(800, 437)
        disabling_buttons(self)
        self.close_btn.clicked.connect(self.close_current_window)

        self.previous_window = previous_window
        self.student_id = student_id
        self.parent_id = parent_id

        if self.parent_id != 0:
            self.load_data()
            self.add_parent.setText("Сохранить")
            self.add_parent.clicked.connect(self.update_parent)
        else:
            surname = self.surname.text()
            name = self.name.text()
            father_name = self.father_name.text()
            phone_number = self.phone_number.text()
            email = self.email.text()
            notes = self.notes.toPlainText()
            self.data = [self.parent_id, surname, name, father_name, phone_number, email, notes]
            self.add_parent.clicked.connect(self.save_parent)

    # добавить нового родителя в базу данных
    def save_parent(self):
        surname = self.surname.text()
        name = self.name.text()
        father_name = self.father_name.text()
        phone_number = self.phone_number.text()
        email = self.email.text()
        notes = self.notes.toPlainText()
        sp = [surname, name, father_name, phone_number, email, notes]
        parent_data = add_parent(sp)
        if parent_data["succes"]:
            add_new_p_connection([parent_data["parent_id"], self.student_id])
            self.back_to_student()
            self.hide()
        else:
            msg = QMessageBox()
            msg.setText(f"Ошибка\n{'\n'.join(parent_data["message"])}")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    # обнвление данных родителя
    def update_parent(self):
        surname = self.surname.text()
        name = self.name.text()
        father_name = self.father_name.text()
        phone_number = self.phone_number.text()
        email = self.email.text()
        notes = self.notes.toPlainText()
        sp = [self.parent_id, surname, name, father_name, phone_number, email, notes]
        if sp != self.data:
            update_parent_data = update_parent(sp)
            if update_parent_data["succes"]:
                self.data = sp.copy()
                msg = QMessageBox()
                msg.setWindowTitle("QMessageBox")
                msg.setText("Данные родителя успешно обновлены!")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("QMessageBox")
                msg.setText(f"Ошибка\n{'\n'.join(update_parent_data["message"])}")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()

    # загрузка данных
    def load_data(self):
        self.data = get_parents_by_id([self.parent_id])[0]
        self.surname.setText(self.data[1])
        self.name.setText(self.data[2])
        self.father_name.setText(self.data[3])
        self.phone_number.setText(self.data[4])
        self.email.setText(self.data[5])
        self.notes.setText(self.data[6])

    # возвращение к окну с учениками
    def back_to_student(self):
        self.student_window = AddStudent(previous_window=self.previous_window, student_id=self.student_id)
        self.student_window.show()
        self.hide()

    # закрытие окна
    def close_current_window(self):
        surname = self.surname.text()
        name = self.name.text()
        father_name = self.father_name.text()
        phone_number = self.phone_number.text()
        email = self.email.text()
        notes = self.notes.toPlainText()
        sp = [self.parent_id, surname, name, father_name, phone_number, email, notes]
        if sp != self.data:
            msg = QMessageBox()
            msg.setWindowTitle("QMessageBox")
            msg.setText("Вы внесли изменения, но не сохранили их.\nСохранить изменения?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            result = msg.exec()
            if result == QMessageBox.StandardButton.Yes:
                if self.data[0] == 0:
                    self.save_parent()
                else:
                    self.update_parent()
        if self.previous_window == "parents" and self.student_id == 0:
            back_to_user_window(self)
        elif (self.previous_window == "parents" and self.student_id != 0) or (
                self.previous_window == "students" and self.student_id != 0):
            self.back_to_student()


class GroupsHistory(QMainWindow):
    def __init__(self, student_id):
        super().__init__()
        uic.loadUi(resource_path("ui_models/history_of_directions.ui"), self)
        self.setFixedSize(1040, 600)
        disabling_buttons(self)
        self.close_btn.clicked.connect(self.close_history_window)

        # переменные
        self.student_id = student_id
        self.load_table()

    # загрузка данных
    def load_table(self):
        groups = get_groups_by_student_id(self.student_id)
        self.history_list.setColumnCount(7)
        self.history_list.setHorizontalHeaderLabels(
            ["id курса", "Название курса", "Преподаватель", "Дата начала курса", "Дата окончания курса",
             "Дата начала обучения", "Дата окончания обучения"])
        self.history_list.setRowCount(len(groups))

        for i in range(len(groups)):
            for j in range(len(groups[i])):
                item = QTableWidgetItem(str(groups[i][j]))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_list.setItem(i, j, item)

        self.history_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    # закрыть окно
    def close_history_window(self):
        self.student_info = AddStudent(student_id=self.student_id)
        self.student_info.show()
        self.hide()

# закрытие пользовательских окон, возврат в главное меню
def close_user_window(window):
    window.hide()
    window.main_w = MainWindow()
    window.main_w.show()

# универсальная функция для возврата к пользовательским окнам (педагоги, ученики, родители, напрвления)
def back_to_user_window(window):
    sl = {"teachers": Teachers(), "students": Students(), "directions": Directions(), "parents": Parents()}
    window.hide()
    window.user_window = sl[window.previous_window]
    window.user_window.show()

# функция корректной загрузки ui файлов
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)


if __name__ == '__main__':
    create_database()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
