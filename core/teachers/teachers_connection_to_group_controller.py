from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import TeachersConnectionToGroup


def add_new_teacher_to_group_connection(group_id, teacher_id):
    with Session(engine) as session:
        connection = TeachersConnectionToGroup(group_id=group_id, teacher_id=teacher_id)
        session.add(connection)
        session.commit()
        return True

def get_connection_by_group_id(group_id):
    with Session(engine) as session:
        connection = session.query(TeachersConnectionToGroup).filter(TeachersConnectionToGroup.group_id.is_(group_id)).one_or_none()
        return connection.teacher_id

def update_teacher_to_group_connection(data):
    group_id, teacher_id = data
    with Session(engine) as session:
        connection = session.query(TeachersConnectionToGroup).filter(TeachersConnectionToGroup.group_id.is_(group_id)).one_or_none()
        if connection:
            connection.teacher_id = teacher_id
        session.commit()
        return True

def delete_teacher_to_group_connection(teacher_id):
    with Session(engine) as session:
        session.query(TeachersConnectionToGroup).filter(TeachersConnectionToGroup.teacher_id.is_(teacher_id)).delete(synchronize_session=False)
        session.commit()
        return True