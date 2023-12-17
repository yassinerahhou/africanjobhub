from datetime import datetime
from app import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer # first thing we import to addd rst password funtion in our site
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# we l l ccreat 2 methods to geenerate tokens : reset & verify the token :
    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY']) # s = serialaser object ! 
        return s.dumps({'user_id': self.id}) # dumps ?
    
    @staticmethod
    # s = take the token as an argument and creat serialazer , if we hav exeption (not the same)  return non if not retur user whi that user id
    
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    category = db.Column(db.String(10), nullable=False)  # Added category field

  

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"