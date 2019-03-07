from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, ForeignKey)

from hotel.data.base import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    image = Column(String)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', backref="posts")

    def __repr__(self):
        return '<Post %r>' % (self.title)
