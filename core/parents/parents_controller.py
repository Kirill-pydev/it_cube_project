from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import Parent, ParentsConnectionToStudents
from core.others import *


def add_parent(data):
    surname, name, father_name, phone, email, notes = data
    valid_email, valid_number = False, False
    res = {"parent_id": 0, "succes": False, "message": []}
    if (phone != "" and is_valid_phone_number(phone)) or phone == "":
        valid_number = True
    if (email != "" and is_valid_email(email)) or email == "":
        valid_email = True
    if valid_email and valid_number and surname != '' and name != '':
        parent = Parent(
            surname=surname,
            name=name,
            father_name=father_name,
            phone=phone,
            email=email,
            notes=notes
        )
        with Session(engine) as session:
            session.add(parent)
            session.commit()
            res["parent_id"] = parent.id
            res["succes"] = True
    else:
        if not valid_email:
            res["message"].append("Неверный формат электронной почты")
        if not valid_number:
            res["message"].append("Неверный формат номера телефона")
        else:
            res["message"].append("Заполните имя и фамилию")
    return res


def delete_parent(data):
    with Session(engine) as session:
        session.query(Parent).filter(Parent.id.in_(data)).delete(synchronize_session=False)
        session.commit()
        return True


def get_all_parents():
    with Session(engine) as session:
        parents = session.query(Parent).all()
        result = []
        for parent in parents:
            student_id = session.query(ParentsConnectionToStudents).filter(ParentsConnectionToStudents.parent_id.is_(parent.id)).first()
            result.append([parent.id,
             parent.surname,
             parent.name,
             parent.father_name,
             parent.phone,
             parent.email,
             parent.notes, student_id.student_id])
        return result


def get_parents_by_id(data):
    with Session(engine) as session:
        parents = session.query(Parent).filter(Parent.id.in_(data))
        parents_list = [
            [parent.id,
             parent.surname,
             parent.name,
             parent.father_name,
             parent.phone,
             parent.email,
             parent.notes]
            for parent in parents
        ]
        return parents_list


def update_parent(data):
    parent_id, surname, name, father_name, phone, email, notes = data
    valid_email, valid_number = False, False
    res = {"succes": False, "message": []}
    if (phone != "" and is_valid_phone_number(phone)) or phone == "":
        valid_number = True
    if (email != "" and is_valid_email(email)) or email == "":
        valid_email = True
    if valid_email and valid_number:
        with Session(engine) as session:
            parent = session.get(Parent, parent_id)
            if not parent:
                res["succes"] = False
            else:
                parent.surname = surname
                parent.name = name
                parent.father_name = father_name
                parent.phone = phone
                parent.email = email
                parent.notes = notes
                session.commit()
                res["succes"] = True
    else:
        if not valid_email:
            res["message"].append("Неверный формат электронной почты")
        if not valid_number:
            res["message"].append("Неверный формат номера телефона")
    return res
