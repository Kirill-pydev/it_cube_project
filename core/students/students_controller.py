from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import Student
from core.others import *


def get_all_students():
    with Session(engine) as session:
        students = session.query(Student).all()
        result = [
            [
                student.id,
                student.surname,
                student.name,
                student.father_name,
                student.school,
                student.gender,
                student.birth_date,
                student.class_number,
                student.certificate_pfdo,
                student.phone,
                student.email,
                student.notes,
                student.agreement_for_processing,
                student.agreement_for_shooting
            ]
            for student in students
        ]

        return result


def add_student(data):
    surname, name, father_name, school, gender, birth_date, class_number, certificate_pfdo, phone, email, notes, agreement_for_processing, agreement_for_shooting = data
    valid_email, valid_number, valid_pfdo = False, False, False
    res = {"new_data": [], "succes": False, "message": []}
    if (phone != "" and is_valid_phone_number(phone)) or phone == "":
        valid_number = True
    if (email != "" and is_valid_email(email)) or email == "":
        valid_email = True
    if (str(certificate_pfdo) != "" and len(str(certificate_pfdo)) == 10) or str(certificate_pfdo) == "":
        valid_pfdo = True
    if valid_email and valid_number and valid_pfdo:
        student = Student(
            surname=surname,
            name=name,
            father_name=father_name,
            school=school,
            gender=gender,
            birth_date=birth_date,
            class_number=class_number,
            certificate_pfdo=certificate_pfdo,
            phone=phone,
            email=email,
            notes=notes,
            agreement_for_processing=agreement_for_processing,
            agreement_for_shooting=agreement_for_shooting
        )
        with Session(engine) as session:
            session.add(student)
            session.commit()
            res["new_data"].append(student.id)
            res["succes"] = True
            res["message"].append("Ok")
    else:
        if not valid_email:
            res["message"].append("Неверный формат электронной почты")
        if not valid_number:
            res["message"].append("Неверный формат номера телефона")
        if not valid_pfdo:
            res["message"].append("Неверный формат номера сертификата ПФДО")
    return res


def delete_student(student_id):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            return False
        session.delete(student)
        session.commit()
        return True


def update_student(data):
    student_id, surname, name, father_name, school, gender, birth_date, class_number, certificate_pfdo, phone, email, notes, agreement_for_processing, agreement_for_shooting = data
    valid_email, valid_number, valid_pfdo = False, False, False
    res = {"succes": False, "message": []}
    if (phone != "" and is_valid_phone_number(phone)) or phone == "":
        valid_number = True
    if (email != "" and is_valid_email(email)) or email == "":
        valid_email = True
    if (str(certificate_pfdo) != "" and len(str(certificate_pfdo)) == 10) or str(certificate_pfdo) == "":
        valid_pfdo = True
    if valid_email and valid_number and valid_pfdo:
        with Session(engine) as session:
                student = session.get(Student, student_id)
                if not student:
                    res["message"].append("Такого ученика не существует")
                student.surname = surname
                student.name = name
                student.father_name = father_name
                student.school = school
                student.gender = gender
                student.birth_date = birth_date
                student.class_number = class_number
                student.certificate_pfdo = certificate_pfdo
                student.phone = phone
                student.email = email
                student.notes = notes
                student.agreement_for_processing = agreement_for_processing
                student.agreement_for_shooting = agreement_for_shooting
                session.commit()
                res["succes"] = True
    else:
        if not valid_email:
            res["message"].append("Неверный формат электронной почты")
        if not valid_number:
            res["message"].append("Неверный формат номера телефона")
        if not valid_pfdo:
            res["message"].append("Неверный формат номера сертификата ПФДО")
    return res



def get_students_by_id(data, mode):
    fil = Student.id.in_(data)
    if mode == 1:
        fil = ~Student.id.in_(data)
    with Session(engine) as session:
        students = session.query(Student).filter(fil).all()
    result = [
        [
            student.id,
            student.surname,
            student.name,
            student.father_name,
            student.school,
            student.gender,
            student.birth_date,
            student.class_number,
            student.certificate_pfdo,
            student.phone,
            student.email,
            student.notes
        ]
        for student in students
    ]
    return result

def get_student_by_id(student_id):
    with Session(engine) as session:
        student = session.query(Student).filter(Student.id == student_id).one_or_none()
        result = [
                student.id,
                student.surname,
                student.name,
                student.father_name,
                student.school,
                student.gender,
                student.birth_date,
                student.class_number,
                student.certificate_pfdo,
                student.phone,
                student.email,
                student.notes,
                student.agreement_for_processing,
                student.agreement_for_shooting
            ]
        return result

