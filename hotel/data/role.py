from flask_security import RoleMixin
from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import relationship

from hotel.data.base import Base


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    users = relationship("User")
