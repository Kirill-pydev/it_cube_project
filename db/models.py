from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    father_name = Column(String, nullable=True)
    school = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    class_number = Column(String, nullable=True)
    certificate_pfdo = Column(String, nullable=True, unique=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    agreement_for_shooting = Column(Integer, nullable=True)
    agreement_for_processing = Column(Integer, nullable=True)


class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    father_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    father_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)


class Direction(Base):
    __tablename__ = "directions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    direction_name = Column(String, nullable=True)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=True)
    start_of_the_course = Column(String, nullable=True)
    end_of_the_course = Column(String, nullable=True)


class TeachersConnectionToGroup(Base):
    __tablename__ = "teachers_connection_to_group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)


class ParentsConnectionToStudents(Base):
    __tablename__ = "parents_connection_to_students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)


class GroupsConnectionToDirection(Base):
    __tablename__ = "groups_connection_to_direction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    direction_id = Column(Integer, ForeignKey("directions.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)


class StudentsConnectionToGroup(Base):
    __tablename__ = "students_connection_to_group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    enrollment_date = Column(String, nullable=True)
    date_of_deduction = Column(String, nullable=True)
