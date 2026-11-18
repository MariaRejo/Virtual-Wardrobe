from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    # 255 characters, because a password hash is longer than 100
    password = db.Column(db.String(255), nullable=False)
    clothes = db.relationship('Cloth', backref='owner', lazy=True)

class Cloth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    season = db.Column(db.String(50), default="All")       # Summer, Winter
    occasion = db.Column(db.String(50), default="Casual")  # Casual, Formal, Party
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
