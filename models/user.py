from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_token = db.Column(db.String(256), nullable=True)
    reset_token_expiry = db.Column( db.DateTime(timezone=True), nullable=True)
    token_version = db.Column(db.Integer, nullable=False, default=0)
    role = db.Column(db.String(20), nullable=False, default="student")


