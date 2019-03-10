
from hotel import db


class Room(db.Model):
    """
    Create a Room table
    """
    id = db.Column(db.Integer(), primary_key=True)
    open = db.Column(db.Boolean(), unique=False, default=True)
    tenant_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
