from datetime import datetime

from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey, Integer,
                        MetaData, Numeric, PrimaryKeyConstraint, String, Table,
                        UniqueConstraint, create_engine)

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer(), primary_key=True),
              Column('username', String(15), nullable=False, unique=True),
              Column('email_address', String(255), nullable=False),
              Column('password', String(25), nullable=False),
              Column('created_on', DateTime(), default=datetime.now),
              Column('updated_on', DateTime(),
                     default=datetime.now, onupdate=datetime.now))

profiles = Table('profiles', metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('first_name', String(60), nullable=False),
                 Column('last_name', String(120), nullable=False),
                 Column('phone', String(20), nullable=False),
                 Column('user_id', ForeignKey('users.id')))


engine = create_engine('sqlite:///data/hotel.db')
metadata.create_all(engine)