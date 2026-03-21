from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import Teacher
from core.others import *


def get_all_teachers():
    # data = [[1, "Старцев", "Кирилл", "Денисович", "+79827968538", "kirillgame912@gmail.com", "Пропуск"], [2, "Баталов", "Вадим", "Алексеевич", "+79124561768", "vdm.izh@gmail.com", "Гений"], [3, "Фефилова", "Полина", "Дмитриевна", "+79127669176", "poli.fefa@gmail.com", "Самая умная"]]
    with Session(engine) as session:
        teachers = session.query(Teacher).all()

        # Преобразуем объекты Teacher в список списков
        result = [
            [
                teacher.id,
                teacher.surname,
                teacher.name,
                teacher.father_name,
                teacher.phone,
                teacher.email,
                teacher.notes
            ]
            for teacher in teachers
        ]

    return result



def add_teacher(data):
    if is_valid_phone_number(data[3]) and is_valid_email(data[4]):
        surname, name, father_name, phone, email, notes = data
        teacher = Teacher(
            surname=surname,
            name=name,
            father_name=father_name,
            phone=phone,
            email=email,
            notes=notes
        )

        with Session(engine) as session:
            session.add(teacher)
            session.commit()
        return True
    return False


def delete_teacher(teacher_id):
    with Session(engine) as session:
        teacher = session.get(Teacher, teacher_id)
        if not teacher:
            return False

        session.delete(teacher)
        session.commit()
        return True


def update_teacher(data):
    if is_valid_phone_number(data[4]) and is_valid_email(data[5]):
        teacher_id, surname, name, father_name, phone, email, notes = data
        with Session(engine) as session:
            teacher = session.get(Teacher, teacher_id)
            if not teacher:
                return False  # учитель не найден

            # Обновляем поля
            teacher.surname = surname
            teacher.name = name
            teacher.father_name = father_name
            teacher.phone = phone
            teacher.email = email
            teacher.notes = notes

            session.commit()
            return True
    else:
        return False


def get_teacher_by_id(teacher_id):
    with Session(engine) as session:
        teacher = session.query(Teacher).filter(Teacher.id == teacher_id).one_or_none()
        return [teacher.id, teacher.surname, teacher.name, teacher.father_name, teacher.phone, teacher.email, teacher.notes]
