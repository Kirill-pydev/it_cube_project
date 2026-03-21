from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import GroupsConnectionToDirection

def get_groups_id_by_direction_id(direction_id):
    with Session(engine) as session:
        res = session.query(GroupsConnectionToDirection).filter(GroupsConnectionToDirection.direction_id == direction_id).all()
        result = [el.group_id for el in res]
        return result

def get_direction_id_by_group_id(group_id):
    with Session(engine) as session:
        connection = session.query(GroupsConnectionToDirection).filter(GroupsConnectionToDirection.group_id == group_id).one_or_none()
        return connection.direction_id

def add_new_connection_group_to_direction(direction_id, group_id):
    with Session(engine) as session:
        connection = GroupsConnectionToDirection(direction_id=direction_id, group_id=group_id)
        session.add(connection)
        session.commit()
        return True


def delete_groups_by_direction_id(direction_id):
    with Session(engine) as session:
        groups_ids = get_groups_id_by_direction_id(direction_id)
        session.query(GroupsConnectionToDirection).filter(GroupsConnectionToDirection.group_id.in_(groups_ids), GroupsConnectionToDirection.direction_id == direction_id).delete(synchronize_session=False)
        session.commit()
        return True