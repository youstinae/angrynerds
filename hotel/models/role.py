from flask_login import RoleMixin
from app import db


class Role(db.Model, RoleMixin):
    """
    Create a Role table
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    description = db.Column(db.String())

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
