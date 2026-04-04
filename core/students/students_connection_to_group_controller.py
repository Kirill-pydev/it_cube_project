from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import StudentsConnectionToGroup, Teacher, TeachersConnectionToGroup, Group


def get_students_id_by_group_id(group_id):
    with Session(engine) as session:
        students = session.query(StudentsConnectionToGroup).filter(StudentsConnectionToGroup.group_id.is_(group_id), StudentsConnectionToGroup.date_of_deduction.is_(None)).all()
        students_id = [student.student_id for student in students]
        return students_id

def add_new_student_to_group_connection(data):
    group_id, student_id, enrollment_date = data
    with Session(engine) as session:
        connection = StudentsConnectionToGroup(group_id=group_id, student_id=student_id, enrollment_date=enrollment_date)
        session.add(connection)
        session.commit()
        return True

def update_student_to_group_connection(data):
    group_id, student_id, date_of_deduction = data
    with Session(engine) as session:
        connection = session.query(StudentsConnectionToGroup).filter(StudentsConnectionToGroup.group_id.is_(group_id), StudentsConnectionToGroup.student_id.is_(student_id), StudentsConnectionToGroup.date_of_deduction.is_(None)).first()
        connection.date_of_deduction = date_of_deduction
        session.commit()
        return True

def get_groups_by_student_id(student_id):
    with Session(engine) as session:
        connections = session.query(StudentsConnectionToGroup).filter(StudentsConnectionToGroup.student_id.is_(student_id)).all()
        result = []
        for connection in connections:
            teacher_info = session.query(TeachersConnectionToGroup).filter(TeachersConnectionToGroup.group_id.is_(connection.group_id)).first()
            teacher = session.query(Teacher).filter(Teacher.id.is_(teacher_info.teacher_id)).first()
            teacher = ' '.join([teacher.surname, teacher.name, teacher.father_name])
            group = session.query(Group).filter(Group.id.is_(connection.group_id)).first()
            result.append([connection.id, group.group_name, teacher, group.start_of_the_course, group.end_of_the_course, connection.enrollment_date, connection.date_of_deduction])
        return result

def delete_student_connections_to_groups(student_id):
    with Session(engine) as session:
        session.query(StudentsConnectionToGroup).filter(StudentsConnectionToGroup.student_id.is_(student_id)).delete(
            synchronize_session=False)
        session.commit()
        return True
