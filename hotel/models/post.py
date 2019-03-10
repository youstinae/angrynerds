from hotel import db


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    image = db.Column(db.String())
    author_id = db.Column(
        db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def __repr__(self):
        return '<Post %r>' % (self.title)
