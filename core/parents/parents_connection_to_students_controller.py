from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import ParentsConnectionToStudents


def add_new_p_connection(data):
    parent_id, student_id = data
    new_connection = ParentsConnectionToStudents(parent_id=parent_id, student_id=student_id)
    with Session(engine) as session:
        session.add(new_connection)
        session.commit()
        return True

def delete_connection_to_parent_by_student_id(student_id):
    with Session(engine) as session:
        res = session.query(ParentsConnectionToStudents).filter(ParentsConnectionToStudents.student_id == student_id).all()
        parents_id = [parent.parent_id for parent in res]
        session.query(ParentsConnectionToStudents).filter(ParentsConnectionToStudents.student_id == student_id).delete(synchronize_session=False)
        session.commit()
        return parents_id

def delete_connection_by_student_and_parent_id(data):
    student_id, parent_id = data
    with Session(engine) as session:
        session.query(ParentsConnectionToStudents).filter(ParentsConnectionToStudents.student_id == student_id, ParentsConnectionToStudents.parent_id == parent_id).delete(synchronize_session=False)
        session.commit()
        return True


def get_parents_by_student_id(student_id):
    with Session(engine) as session:
        res = session.query(ParentsConnectionToStudents).filter(ParentsConnectionToStudents.student_id == student_id).all()
        parents_id = []
        for i in range(len(res)):
            parents_id.append(res[i].parent_id)
        return parents_id