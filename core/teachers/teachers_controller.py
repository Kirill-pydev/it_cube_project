from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import Teacher
from core.others import *


def get_all_teachers():
    with Session(engine) as session:
        teachers = session.query(Teacher).all()
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
    surname, name, father_name, phone, email, notes = data
    valid_number, valid_email = False, False
    res = {"new_data": [], "succes": False, "message": []}
    if (phone != "" and is_valid_phone_number(phone)) or phone == "":
        valid_number = True
    if (email != "" and is_valid_email(email)) or email == "":
        valid_email = True
    if valid_email and valid_email and [surname, name, father_name].count("") <= 2:
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
            res["new_data"].append(teacher.id)
            res["succes"] = True
            res["message"].append("Ok")
    else:
        if not valid_email:
            res["message"].append("Неверный формат электронной почты")
        if not valid_number:
            res["message"].append("Неверный формат номера телефона")
        if [surname, name, father_name].count("") == 3:
            res["message"].append("Заполните хотя бы одно поле с инициалами")
    return res


def delete_teacher(teacher_id):
    with Session(engine) as session:
        teacher = session.get(Teacher, teacher_id)
        if not teacher:
            return False

        session.delete(teacher)
        session.commit()
        return True


def update_teacher(data):
    teacher_id, surname, name, father_name, phone, email, notes = data
    res = {"succes": False, "message": []}
    valid_number, valid_email = False, False
    if (phone != "" and is_valid_phone_number(phone)) or phone == "":
        valid_number = True
    if (email != "" and is_valid_email(email)) or email == "":
        valid_email = True
    if valid_number and valid_email and [surname, name, father_name].count("") <= 2:
        with Session(engine) as session:
            teacher = session.get(Teacher, teacher_id)
            if not teacher:
                res['message'].append("Учитель не найден")
                return res
            teacher.surname = surname
            teacher.name = name
            teacher.father_name = father_name
            teacher.phone = phone
            teacher.email = email
            teacher.notes = notes
            session.commit()
            res['succes'] = True
            res['message'].append("Ok")
    else:
        if not valid_email:
            res["message"].append("Неверный формат электронной почты")
        if not valid_number:
            res["message"].append("Неверный формат номера телефона")
        if [surname, name, father_name].count("") == 3:
            res["message"].append("Заполните хотя бы одно поле с инициалами")
    return res


def get_teacher_by_id(teacher_id):
    if teacher_id:
        with Session(engine) as session:
            teacher = session.query(Teacher).filter(Teacher.id == teacher_id).one_or_none()
            return [teacher.id, teacher.surname, teacher.name, teacher.father_name, teacher.phone, teacher.email,
                    teacher.notes]
    else:
        return False
