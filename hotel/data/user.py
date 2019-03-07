from flask_security import UserMixin  # , RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import (Boolean, DateTime, Column,
                        Integer, String, ForeignKey, Table)

from hotel.data.base import Base


roles_users = Table('roles_users', Base.metadata,
                    Column('user_id', Integer(), ForeignKey('user.id')),
                    Column('role_id', Integer(), ForeignKey('role.id')))


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    last_login_at = Column(DateTime)
    current_login_at = Column(DateTime)
    last_login_ip = Column(String)
    current_login_ip = Column(String)
    login_count = Column(Integer)
    active = Column(Boolean)
    confirmed_at = Column(DateTime)
    posts = relationship("Blog")
    roles = relationship('Role', secondary=roles_users,
                         backref=backref('users', lazy='dynamic'))
