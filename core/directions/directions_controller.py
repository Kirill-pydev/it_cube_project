from sqlalchemy.orm import Session
from db.init_db import engine
from db.models import Direction


def get_all_directions():
    with Session(engine) as session:
        directions = session.query(Direction).all()
        result = [
            [direction.id,
             direction.direction_name]
            for direction in directions
        ]
    return result


def add_direction(data):
    direction_name = data[0]
    direction = Direction(
        direction_name=direction_name
    )
    with Session(engine) as session:
        session.add(direction)
        session.commit()
        return direction.id


def get_direction_by_id(direction_id):
    with Session(engine) as session:
        direction = session.get(Direction, direction_id)
        return [direction.id, direction.direction_name]


def delete_direction(direction_id):
    with Session(engine) as session:
        direction = session.get(Direction, direction_id)
        if not direction:
            return False
        session.delete(direction)
        session.commit()
        return True
