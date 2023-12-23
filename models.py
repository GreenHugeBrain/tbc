from werkzeug.security import generate_password_hash
from ext import db, app, login_manager
from flask_login import UserMixin

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()

class Comment(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(200), nullable=False)


class Product(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    img = db.Column(db.String)

class User(db.Model, UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(50))  

    def __init__(self, username, password, role='guest'):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role


User('user', 'mypassword')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        new_user = User(username='adminuser', password='adminuser15129', role='admin')
        new_user.create()

        normal_user = User(username='normaluser', password='normaldefaultuser', role='guest')
        normal_user.create()
