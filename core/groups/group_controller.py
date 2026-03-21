from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import Group


def add_new_group(group_name, start_of_the_course, end_of_the_course):
    with Session(engine) as session:
        group = Group(group_name=group_name, start_of_the_course=start_of_the_course, end_of_the_course=end_of_the_course)
        session.add(group)
        session.commit()
        return group.id

def get_all_groups_by_id_list(data):
    with Session(engine) as session:
        groups = session.query(Group).filter(Group.id.in_(data)).all()
        result = [
            [group.id,
             group.group_name,
             group.start_of_the_course,
             group.end_of_the_course]
            for group in groups
        ]
        return result

def update_group(data):
    group_id, group_name, start_of_the_course, end_of_the_course = data
    with Session(engine) as session:
        group = session.get(Group, group_id)
        group.group_name = group_name
        group.start_of_the_course = start_of_the_course
        group.end_of_the_course = end_of_the_course
        session.commit()
        return True