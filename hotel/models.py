from hotel.database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
    String, ForeignKey


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    image = Column(String)
    author_id = Column(Integer, ForeignKey(
        'user.id'), nullable=False, index=True)
    author = relationship('User', backref="user_posts",
                          foreign_keys=[author_id])
                          
    def __repr__(self):
        return '<Post %r>' % (self.title)


class Room(Base):
    # class Rooom(Base, RoleMixin): **(if it requires security)**
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    open = Column(Boolean, unique=False, default=True)
    tenant_id = Column(Integer, ForeignKey('user.id'))
    # Everything else about the room can go here
    # capacity = ...
    # beds = ...
    # just practicing with this, still new to it.
