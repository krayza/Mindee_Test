from app import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    image_name = db.Column(db.String(80), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    api_return = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title
