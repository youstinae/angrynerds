from sqlalchemy import (Column, Integer, ForeignKey, Boolean)
# from flask_security import RoleMixin **(if it requires security)**
from hotel.data.base import Base


class Room(Base):
    # class Rooom(Base, RoleMixin): **(if it requires security)**
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    open = Column(Boolean, unique=False, default=True)
    tenantID = Column(Integer, ForeignKey('user.id'))
    # Everything else about the room can go here
    # capacity = ...
    # beds = ...
    # just practicing with this, still new to it.
