from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke Photo
    photos = db.relationship('Photo', backref='uploader', lazy=True, cascade='all, delete-orphan')
    # Relasi ke Like
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'

class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(255), nullable=False)
    likes_count = db.Column(db.Integer, default=0)  # Ganti nama dari 'likes' ke 'likes_count'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Foreign Key ke User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relasi ke Like
    likes = db.relationship('Like', backref='photo', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Photo {self.title}>'

# ==================== MODEL BARU: LIKE ====================
class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: 1 user hanya bisa like 1 foto 1 kali
    __table_args__ = (db.UniqueConstraint('user_id', 'photo_id', name='unique_user_photo_like'),)
    
    def __repr__(self):
        return f'<Like User {self.user_id} Photo {self.photo_id}>'