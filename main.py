from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from hotel import app, db
import hotel.models


Base = declarative_base()
session = scoped_session(sessionmaker())

engine = create_engine('sqlite:///db/hotel.db')
session.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all()

if __name__ == "__main__":
    app.create_app()
    app.app_context().push()
    db.create_all()
    app.run()
